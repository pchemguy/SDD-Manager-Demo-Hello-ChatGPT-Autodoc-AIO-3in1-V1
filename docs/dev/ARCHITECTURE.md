# ARCHITECTURE

The [project brief](PROJECT.md) defines a single color-selection application delivered through browser, Windows desktop and browser sidebars. The system uses shared local web assets and thin platform hosts.

## Major blocks and dependency direction

| Block | Owns | Depends on |
| --- | --- | --- |
| Shared application | Message, native radio group, current color and reset behavior | DOM and standard JavaScript only |
| Browser entry | Loading the shared application as a static page | Shared application |
| Electron host | Application/window lifecycle, restricted renderer and packaged resource loading | Electron runtime and shared application assets |
| Chromium extension adapter | Side panel declaration, toolbar opening, window-scoped lifecycle reset delivery | Chromium extension APIs and shared reset interface |
| Firefox extension adapter | Sidebar declaration and local entry page | Firefox extension APIs and shared application |
| Build and release tools | Allowlisted assembly, version metadata, archive/checksum generation and artifact checks | Source assets and pinned development/runtime tools |

Platform hosts depend inward on the shared application. Shared color selection imports no Electron, extension API, filesystem, network or storage facility. Build dependencies do not become user runtime requirements. No backend or cross-instance coordinator exists.

## Shared application design

Use plain HTML, CSS and JavaScript. A single DOM controller owns each mounted instance, with a finite color set and one reset operation. Native inputs provide exclusive selection and keyboard behavior. Initialization sets both checked state and message color to red, overriding browser form restoration. Reset updates them together. The group and message derive from one current selection; no persistent copy exists.

Use external local scripts and styles without inline executable code or remotely hosted assets. A fluid layout wraps the message as necessary, preserves vertically stacked controls and allows vertical scrolling. Keep color selection independent of viewport geometry.

This scope does not justify a UI framework, state library, dependency injection container or storage abstraction. Thin platform entry scripts may supply reset events, but all color and rendering behavior stays shared. Exact contracts belong to [SPEC](SPEC.md) when available.

## Platform boundaries

The browser entry is a static document with relative asset paths. It needs no application server logic. A deployment may use an ordinary static host; the distributable is also designed to open locally without a development server by using non-module local script loading.

Electron uses a small main-process entry to create one window per application launch and loads only bundled resources. A registered local application protocol serves the allowlisted renderer assets with fixed MIME types and rejects paths outside that asset root. Node integration is disabled, context isolation and renderer sandboxing are enabled, and new windows, external navigation and permission requests are denied. No preload or IPC bridge is required because the UI has no privileged capability.

The Windows portable ZIP is assembled from a pinned official Electron win32-x64 distribution plus resources/app. Retain its runtime resources and license notices, add the small application entry and shared assets, and remove only the stock demo entry. The pinned archive and official checksum are verified before extraction. This follows Electron's documented manual distribution path and avoids making Windows-specific executable editing a cross-build prerequisite. Branding may use the application title and launch filename without claiming Authenticode signing or customized executable metadata.

Chromium uses Manifest V3, a global side panel and the sidePanel permission, without content scripts, host permissions or persistent storage. Minimum Chromium API level is 142 because explicit opening and closing events support reset on reopening. A background service worker routes reset events only to the panel in the matching browser window. A newly created panel starts red independently of message delivery. A retained panel must receive the open-session reset, including after service-worker suspension/reconnection; tab navigation and focus changes do not reset an open session. The adapter must not broadcast resets across windows.

Firefox uses Manifest V3 with sidebar_action and a local panel document. Closing the sidebar unloads that document; reopening initializes the shared application at red. Firefox needs no background color store or Chromium API compatibility shim. Use a stable extension ID and record the tested Firefox version. A Firefox 140+ desktop target is selected for the development package; Chromium-vendor support beyond the required APIs is not implied.

## Build, verification and distribution

Node.js development scripts assemble static assets without a bundler or symlinked workspace. Python packaging utilities can assemble ZIPs and verify the Electron download using standard libraries. Test execution uses pytest; Python Playwright exercises shared UI in managed Chromium and Firefox. Exact versions are pinned during environment setup rather than fetched as moving latest dependencies. Native extension checks use a capable full browser where available; shared-page or mocked adapter checks do not establish native panel lifecycle behavior.

Build each platform from an explicit allowlist. Exclude credentials, repository metadata, development tooling, tests and unrelated project files. Version metadata originates from the root application manifest, then feeds desktop metadata, extension manifests, archive names and release notes. Checksums identify the exact uploaded artifacts. Retain cumulative platform artifacts in each applicable release.

Platform-native Windows execution and unavailable full-browser checks are scoped under the repository policies. Record excluded checks distinctly; failed feasible checks remain blockers. A package is delivered only after its feasible artifact checks pass; source tests alone do not establish package validity.

## Architectural review

The boundaries have cohesive ownership and one-way dependencies: shared behavior is reused without importing a platform; each adapter owns only its actual lifecycle variation; packaging is separate from runtime behavior. There is no persistence or backend to synchronize. Principal risk is Chromium's retained panel lifecycle, which requires window-scoped real-event and reconnect checks. Firefox native installation and Windows cross-build evidence are separate from shared renderer verification.

## Platform references

Sources inspected on 2026-10-27; version-specific API and packaging assumptions must be rechecked if the selected runtime changes.

- [Chromium sidePanel API and lifecycle events](https://developer.chrome.com/docs/extensions/reference/api/sidePanel).
- [Firefox sidebar document lifecycle](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/user_interface/Sidebars).
- [Firefox sidebar manifest](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/sidebar_action).
- [Electron security guidance](https://www.electronjs.org/docs/latest/tutorial/security).
- [Electron manual application packaging](https://www.electronjs.org/docs/latest/tutorial/application-distribution).
- [Playwright Python extension testing](https://playwright.dev/python/docs/chrome-extensions).
