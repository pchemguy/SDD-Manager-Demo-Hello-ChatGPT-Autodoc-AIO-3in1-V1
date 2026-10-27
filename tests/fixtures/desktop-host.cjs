const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const file = path.resolve(process.argv[2]);
const state = { windows: [], appEvents: {}, protocol: null, permission: null, quit: 0 };
class BrowserWindow {
  constructor(options) {
    this.options = options; this.events = {};
    this.webContents = { on: (name, fn) => this.events[name] = fn,
      setWindowOpenHandler: fn => this.open = fn };
    state.windows.push(this);
  }
  removeMenu() { this.menuRemoved = true; }
  async loadURL(url) { this.url = url; }
  on(name, fn) { this.events[name] = fn; }
}
const electron = {
  app: { whenReady: () => Promise.resolve(), on: (n,f) => state.appEvents[n] = f,
    quit: () => state.quit++, exit: n => { throw Error('Exit ' + n); } },
  BrowserWindow,
  protocol: { registerSchemesAsPrivileged: v => state.schemes = v,
    handle: (scheme, handler) => { state.protocol = handler; } },
  session: { defaultSession: { setPermissionRequestHandler: f => state.permission = f } }
};
vm.runInNewContext(fs.readFileSync(file, 'utf8'), {
  require: name => name === 'electron' ? electron : require(name),
  __dirname: path.dirname(file), console, Response, URL, Buffer
}, { filename: file });
(async () => {
  await new Promise(r => setTimeout(r, 50));
  assert.equal(state.windows.length, 1, 'Startup must create one window');
  const w = state.windows[0];
  assert.equal(w.options.webPreferences.nodeIntegration, false);
  assert.equal(w.options.webPreferences.contextIsolation, true);
  assert.equal(w.options.webPreferences.sandbox, true);
  assert.equal(w.menuRemoved,true);
  assert.equal(w.url, 'hello://app/index.html');
  assert.equal(w.open().action, 'deny');
  let denied = false;w.events['will-navigate']({preventDefault(){denied=true;}}, 'https://example.invalid/');assert(denied);
  state.permission(null, 'camera', result => assert.equal(result, false));
  for (const url of ['hello://app/../index.html','hello://app/%2e%2e/index.html','hello://app/%2fsecret','hello://evil/index.html','hello://app/main.cjs','hello://app/%','https://app/index.html']) {
    const response = await state.protocol({url, method:'GET'});assert(response.status >= 400, url);
  }
  assert.equal((await state.protocol({url:w.url,method:'POST'})).status,405);
  const response=await state.protocol({url:w.url,method:'GET'});
  assert.equal(response.status,200);assert((await response.text()).includes('Hello World'));
  assert(response.headers.get('content-type').includes('text/html'));
  state.appEvents['window-all-closed']();assert.equal(state.quit,1);
  console.log('Host lifecycle, security and local resources verified (modeled Electron API)');
})().catch(e => { console.error(e); process.exitCode=1; });
