(function () {
  'use strict';
  const sessions=new Map(), panels=new Map();
  const validId=id=>Number.isInteger(id)&&id>=0;
  const validToken=t=>typeof t==='string'&&t.length>0&&t.length<=128;
  const fresh=()=>({token:crypto.randomUUID(),needsReset:true,open:null,fresh:false});
  function send(id) {
    const route=panels.get(id),state=sessions.get(id);
    if (!route||!state) return;
    try { route.port.postMessage({type:'session',windowId:id,token:state.token,reset:state.needsReset,sequence:++route.sequence}); }
    catch { if (panels.get(id)===route) panels.delete(id); }
  }
  chrome.runtime.onConnect.addListener(port=>{
    if (port.name!=='hello-panel'||port.sender?.id!==chrome.runtime.id||port.sender?.url!==chrome.runtime.getURL('index.html')||port.sender?.tab) {
      port.disconnect();return;
    }
    const route={port,windowId:null,sequence:0};
    port.onMessage.addListener(message=>{
      if (!message||!validId(message.windowId)) return;
      const id=message.windowId;
      if (route.windowId!==null&&route.windowId!==id) return;
      if (message.type==='panel-ready'&&(message.token===null||validToken(message.token))) {
        let state=sessions.get(id);
        if (!state) {
          state=fresh();state.fresh=message.token===null;
          if (message.token!==null) {state.token=message.token;state.needsReset=false;}
          sessions.set(id,state);
        } else {
          if (message.token===state.token) state.needsReset=false;
          if (message.token===null) state.fresh=true;
        }
        route.windowId=id;panels.set(id,route);send(id);
      } else if (message.type==='applied'&&panels.get(id)===route) {
        const state=sessions.get(id);
        if (state&&message.token===state.token) state.needsReset=false;
      }
    });
    port.onDisconnect.addListener(()=>{
      if (panels.get(route.windowId)===route) panels.delete(route.windowId);
    });
  });
  chrome.sidePanel.onOpened.addListener(({windowId:id})=>{
    if (!validId(id)) return;
    let state=sessions.get(id);
    if (state?.open===true) return;
    if (!state?.fresh) state=fresh();
    state.open=true;state.fresh=false;sessions.set(id,state);send(id);
  });
  chrome.sidePanel.onClosed.addListener(({windowId:id})=>{
    if (!validId(id)||sessions.get(id)?.open===false) return;
    const state=fresh();state.open=false;sessions.set(id,state);send(id);
  });
  chrome.windows.onRemoved.addListener(id=>{sessions.delete(id);panels.delete(id);});
  chrome.sidePanel.setPanelBehavior({openPanelOnActionClick:true}).catch(error=>console.error('Panel configuration failed:',error.message));
}());
