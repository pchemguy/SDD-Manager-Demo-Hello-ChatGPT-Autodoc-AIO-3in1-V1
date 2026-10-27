'use strict';
const { app, BrowserWindow, protocol, session } = require('electron');
const fs = require('node:fs/promises');
const path = require('node:path');
const root = path.join(__dirname, 'renderer');
const types = { 'index.html':'text/html', 'app.js':'text/javascript', 'bootstrap.js':'text/javascript',
  'styles.css':'text/css', 'version.json':'application/json' };
let window;
protocol.registerSchemesAsPrivileged([{ scheme:'hello', privileges:{ standard:true, secure:true, supportFetchAPI:true } }]);
async function resource(request) {
  if (!['GET','HEAD'].includes(request.method)) return new Response('Method not allowed', {status:405});
  let raw;
  try { raw=decodeURIComponent(request.url.split(/[?#]/)[0]); }
  catch { return new Response('Invalid path', {status:400}); }
  if (!raw.startsWith('hello://app/') || raw.includes('\\')) return new Response('Forbidden', {status:403});
  const name=raw.slice('hello://app/'.length) || 'index.html';
  if (!Object.hasOwn(types,name)) return new Response('Not found', {status:404});
  try {
    const file=path.join(root,name);
    if ((await fs.lstat(file)).isSymbolicLink()) return new Response('Forbidden', {status:403});
    const bytes=await fs.readFile(file);
    return new Response(request.method==='HEAD'?null:bytes, {headers:{'Content-Type':types[name]+'; charset=utf-8'}});
  } catch { return new Response('Not found', {status:404}); }
}
app.whenReady().then(async () => {
  await Promise.all(Object.keys(types).map(name => fs.access(path.join(root,name))));
  protocol.handle('hello',resource);
  session.defaultSession.setPermissionRequestHandler((_webContents,_permission,callback) => callback(false));
  window=new BrowserWindow({width:400,height:440,minWidth:220,minHeight:180,title:'Hello World',autoHideMenuBar:true,
    webPreferences:{nodeIntegration:false,contextIsolation:true,sandbox:true,devTools:false}});
  window.removeMenu();
  window.webContents.setWindowOpenHandler(() => ({action:'deny'}));
  for (const event of ['will-navigate','will-redirect']) {
    window.webContents.on(event,(e,url) => { if (url!=='hello://app/index.html') e.preventDefault(); });
  }
  window.on('closed',() => { window=null; });
  await window.loadURL('hello://app/index.html');
}).catch(error => { console.error('Hello World startup failed:',error.message);app.exit(1); });
app.on('window-all-closed',() => app.quit());
