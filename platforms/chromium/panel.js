(function () {
  'use strict';
  const controller=window.HelloColorApp.mount(document);
  window.addEventListener('pageshow',()=>controller.reset());
  // Standalone renderer checks exercise common UI only, without an extension API claim.
  if (typeof chrome!=='object'||!chrome.runtime?.id) return;
  const group=document.querySelector('#colors'), retired=new Set();
  let current=null,token=null,lastSequence=0,timer=null,disposed=false,windowId=null;
  group.disabled=true;
  async function connect() {
    if (disposed) return;
    try {
      const info=await chrome.windows.getCurrent();
      if (disposed) return;
      windowId=info.id;
      const port=chrome.runtime.connect({name:'hello-panel'});current=port;lastSequence=0;
      port.onMessage.addListener(message=>{
        if (current!==port||!message||message.type!=='session'||message.windowId!==windowId||
            !Number.isInteger(message.sequence)||message.sequence<=lastSequence||
            typeof message.token!=='string'||!message.token.length||message.token.length>128||
            typeof message.reset!=='boolean'||retired.has(message.token)) return;
        if (token&&message.token!==token&&!message.reset) return;
        if (message.token!==token) {
          if (token) retired.add(token);
          token=message.token;
          if (message.reset) controller.reset();
        }
        lastSequence=message.sequence;group.disabled=false;
        port.postMessage({type:'applied',windowId,token});
      });
      port.onDisconnect.addListener(()=>{
        void chrome.runtime.lastError;
        if (current===port) {current=null;if(!disposed)timer=setTimeout(connect,250);}
      });
      port.postMessage({type:'panel-ready',windowId,token});
    } catch {
      if (!disposed&&chrome.runtime.id) timer=setTimeout(connect,1000);
    }
  }
  window.addEventListener('pagehide',event=>{
    if (event.persisted) return;
    disposed=true;clearTimeout(timer);current?.disconnect();controller.dispose();
  });
  connect();
}());
