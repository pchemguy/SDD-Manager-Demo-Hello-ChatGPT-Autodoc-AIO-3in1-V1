# Install Hello World 0.2.0

## Browser

Extract hello-world-0.2.0-browser.zip and open index.html, or deploy the extracted files together to a static website directory. No Node.js, development server or backend is required.

## Windows x64 portable app

Extract the entire hello-world-0.2.0-windows-x64.zip into a writable folder, including its resources, locales and DLLs. Run HelloWorld.exe from that folder. Keep the distribution together; copying only the executable is insufficient. No separate Node.js, npm, development server or backend is needed. Remove the folder to uninstall.

This is an unsigned portable application package, not an installer or Microsoft Store distribution. Windows may show a security prompt for an unrecognized downloaded application. Bundled upstream Electron runtime files and license notices are retained. Native Windows execution was not tested on the Linux build host; the package is cross-built and inspected, not certified for a particular Windows installation.

## Interaction and checksums

Hello World starts red. Select red, blue or green by radio, label or standard keyboard controls. Reloading or restarting starts red; instances remain independent and nothing is saved.

SHA256SUMS identifies the exact archive bytes. Windows CMD: certutil -hashfile ARCHIVE.zip SHA256. Linux: sha256sum -c SHA256SUMS.

Shared renderer checks passed in managed Chromium 156 headless shell and Firefox 157 on Linux. Firefox needed the process-local content-sandbox override for the diagnosed host uid_map restriction, only during trusted local testing. Full Chromium native execution was unavailable because a host-denied Unix socket remains denied with its internal sandbox disabled. Sidebar packages are not part of this release.
