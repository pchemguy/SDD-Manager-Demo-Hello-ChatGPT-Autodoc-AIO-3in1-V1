# Install Hello World 0.3.0

All platforms display Hello World with vertically stacked red, blue and green radios. Selecting by pointer, label or standard keyboard controls changes the text immediately. Fresh pages, desktop launches and sidebar reopenings start red. A live open sidebar retains its selection when resized, unfocused or used alongside tab navigation. Color is not persisted or synchronized between windows.

## Browser

Extract hello-world-0.3.0-browser.zip and open index.html, or deploy the extracted files together to a static website directory. No Node.js, development server or backend is required.

## Windows x64 portable app

Extract the entire hello-world-0.3.0-windows-x64.zip into a writable folder, including DLLs, resources and locales. Run HelloWorld.exe from that folder. Keep the distribution together; copying only the executable is insufficient. No separate Node.js, npm, development server or backend is needed. Removing the folder removes the application files; Electron may retain its normal profile/cache outside that folder.

This is an unsigned portable application package, not an installer or Microsoft Store distribution. Windows may show a security prompt for an unrecognized downloaded application. Upstream Electron runtime files and license notices are retained. Native Windows launch was not tested on this Linux build host; the package is cross-built and inspected, without a native OS compatibility claim.

## Chromium development extension

Requires desktop Chromium/Chrome 142+ with the sidePanel opening and closing APIs. Other Chromium vendors are not automatically certified by their engine version.

1. Extract hello-world-0.3.0-chromium-dev.zip into a permanent folder.
2. Open chrome://extensions, enable Developer mode, choose Load unpacked and select the extracted folder containing manifest.json.
3. Use the extension menu to pin Hello World if desired, then click its Open Hello World toolbar action to open the side panel.
4. Close the panel with its native close control; reopening starts red. Keep the extracted folder in place while installed.

This is an unpacked development package, not a signed or Chrome Web Store distribution. No separate Node.js, local server or backend is required.

## Firefox development extension

Requires desktop Firefox 140+ with MV3 sidebar_action support.

1. Extract hello-world-0.3.0-firefox-dev.zip or retain the ZIP for temporary loading.
2. Open about:debugging, choose This Firefox and Load Temporary Add-on, then select the extracted manifest.json or the ZIP.
3. Select Hello World from Firefox's native sidebar chooser or View/Sidebar menu.
4. Closing the sidebar discards its selection; reopening starts red. Temporary add-ons are removed when Firefox restarts and must be loaded again for another development session.

This package is unsigned and intended for temporary development loading, not permanent signed or Add-ons Store installation. It bundles all app assets and needs no separate Node.js, local server or backend.

## Checksums and verification limits

SHA256SUMS identifies the exact archive bytes. Windows CMD: certutil -hashfile ARCHIVE.zip SHA256. Linux: sha256sum -c SHA256SUMS.

Shared UI checks passed in managed Chromium 156 headless shell and Firefox 157 on Linux. Firefox needed a process-local content-sandbox override only for trusted local testing after diagnosed uid_map EPERM. Full Chromium could not run because the host denies a required Unix socket even with its internal sandbox disabled. Chromium lifecycle routing was tested with modeled APIs plus the real DOM bridge; native sidePanel events were not tested. A bounded native Firefox temporary-install probe could not access its internal debugging facility; native Firefox installation/sidebar events remain unverified. Manifest, complete package contents, shared UI, adapter and extracted-artifact checks are distinct from those unavailable native checks.
