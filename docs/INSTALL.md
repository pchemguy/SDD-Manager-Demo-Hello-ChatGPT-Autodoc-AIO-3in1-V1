# Install Hello World 0.1.0

Extract hello-world-0.1.0-browser.zip and open index.html in a desktop Chromium or Firefox browser. You can also copy the extracted files together to any static website directory. No Node.js installation, development server or backend is required to use the app.

The message starts red. Select red, blue or green with the radio buttons, labels or standard keyboard controls. Reloading starts red; separate pages have independent selections. Nothing is saved.

SHA256SUMS identifies the exact release archives. For example, on Windows CMD use certutil -hashfile ARCHIVE.zip SHA256 and compare its value. Linux users can use sha256sum -c SHA256SUMS.

Tested on Linux with Playwright-managed Chromium 156 headless shell and Firefox 157. Full Chromium native-browser checks were unavailable because this execution host denies a required Unix socket. This release does not claim native sidebar behavior or Windows delivery; those platforms are delivered in later releases.
