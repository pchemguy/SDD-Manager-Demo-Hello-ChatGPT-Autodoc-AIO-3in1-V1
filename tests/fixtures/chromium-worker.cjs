const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function event(){const handlers=[];return {addListener:f=>handlers.push(f),emit:(...a)=>handlers.forEach(f=>f(...a))};}
function worker(){
  const chrome={runtime:{id:'own',getURL:p=>'chrome-extension://own/'+p,onConnect:event()},
    sidePanel:{onOpened:event(),onClosed:event(),setPanelBehavior:async v=>{assert.equal(v.openPanelOnActionClick,true)}},
    windows:{onRemoved:event()}};
  vm.runInNewContext(fs.readFileSync('platforms/chromium/background.js','utf8'),{chrome,crypto:require('node:crypto').webcrypto,console});
  function connect(id,token=null,sender={id:'own',url:'chrome-extension://own/index.html'}){
    const p={name:'hello-panel',sender,onMessage:event(),onDisconnect:event(),sent:[],postMessage(m){this.sent.push(m)},disconnect(){this.disconnected=true;this.onDisconnect.emit()}};
    chrome.runtime.onConnect.emit(p);p.onMessage.emit({type:'panel-ready',windowId:id,token});return p;
  }
  return {chrome,connect};
}
const w=worker(),a=w.connect(10);
assert(a.sent.length>0,'Panel readiness requires a session reply');
let msg=a.sent.at(-1);assert.equal(msg.windowId,10);assert.equal(msg.reset,true);
a.onMessage.emit({type:'applied',windowId:10,token:msg.token});
w.chrome.sidePanel.onOpened.emit({windowId:10});assert.equal(a.sent.at(-1).token,msg.token,'Ready-before-open must not create another reset session');
const b=w.connect(20);w.chrome.sidePanel.onOpened.emit({windowId:20});const bCount=b.sent.length;
w.chrome.sidePanel.onClosed.emit({windowId:10});w.chrome.sidePanel.onOpened.emit({windowId:10});
assert.notEqual(a.sent.at(-1).token,msg.token);assert.equal(b.sent.length,bCount,'Window B must remain unchanged');
const latest=a.sent.at(-1);a.onDisconnect.emit();const resumed=w.connect(10,latest.token);assert.equal(resumed.sent.at(-1).reset,false,'Applied token on reconnection must preserve selection');
const count=resumed.sent.length;w.chrome.sidePanel.onOpened.emit({windowId:10});assert.equal(resumed.sent.length,count,'Duplicate opening is harmless');
const restarted=worker(),live=restarted.connect(10,latest.token);assert.equal(live.sent.at(-1).reset,false,'Worker restart alone must not reset an open panel');
restarted.chrome.sidePanel.onClosed.emit({windowId:10});restarted.chrome.sidePanel.onOpened.emit({windowId:10});assert.equal(live.sent.at(-1).reset,true);
const hostile=w.connect(30,null,{id:'foreign',url:'chrome-extension://own/index.html'});assert(hostile.disconnected);assert.equal(hostile.sent.length,0);
const malformed=w.connect(1.5);assert.equal(malformed.sent.length,0);
console.log('Modeled Chromium lifecycle ordering, reconnection, isolation and sender validation passed');
