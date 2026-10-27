import { copyFile, mkdir, rm, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
const root = fileURLToPath(new URL('../', import.meta.url));
const platform = process.argv[2];
if (!['browser','desktop','chromium'].includes(platform)) throw new Error('Unsupported build platform: ' + platform);
const base = path.join(root, 'build', platform);
const out = platform === 'desktop' ? path.join(base, 'app', 'renderer') : base;
const metadata = JSON.parse(await readFile(path.join(root, 'package.json'), 'utf8'));
await rm(base, { recursive: true, force: true });
await mkdir(out, { recursive: true });
for (const name of ['index.html', 'app.js', 'styles.css', 'bootstrap.js']) {
  const source=platform==='chromium'&&name==='bootstrap.js' ? path.join(root,'platforms/chromium/panel.js') : path.join(root,'app',name);
  await copyFile(source, path.join(out, name));
}
await writeFile(path.join(out, 'version.json'), JSON.stringify({ version: metadata.version, platform,
  sourceRevision: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim() }, null, 2) + '\n');
console.log('Built ' + platform + ' ' + metadata.version);

if (platform === 'desktop') {
  await copyFile(path.join(root,'platforms/electron/main.cjs'),path.join(base,'app/main.cjs'));
  await writeFile(path.join(base,'app/package.json'),JSON.stringify({name:'hello-world',version:metadata.version,main:'main.cjs'},null,2)+'\n');
  await copyFile(path.join(root,'LICENSE'),path.join(base,'app/LICENSE'));
}

if (platform === 'chromium') {
  const manifest=JSON.parse(await readFile(path.join(root,'platforms/chromium/manifest.json'),'utf8'));
  manifest.version=metadata.version;
  await writeFile(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
  await copyFile(path.join(root,'platforms/chromium/background.js'),path.join(out,'background.js'));
}
