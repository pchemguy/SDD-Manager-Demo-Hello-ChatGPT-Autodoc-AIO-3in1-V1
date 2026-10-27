# Hello World across browser, desktop and sidebars

## Purpose and scope

Provide a small application with the same immediate color-selection interaction in a browser, a packaged Windows Electron application, and desktop Chromium and Firefox sidebars. Users can run the delivered packages without installing Node.js, starting a development server or configuring a backend.

Display the exact message "Hello World" and a group of three vertically stacked radio buttons labeled "red", "blue" and "green". Exactly one is selected. Initially select red and display the message in red. Selecting another option immediately changes the message text to that color, without an Apply action. Keep the radio labels readable independently of the selected message color.

Share application logic and UI across all platforms while separating platform entry points, packaging and lifecycle handling. Keep the browser and desktop versions available as extensions are added. Support a narrow, resizable sidebar without losing the message or any control.

## Interaction and lifecycle proposals

Use native radio controls with clickable labels, visible keyboard focus and standard keyboard selection. Pointer and keyboard selection have the same immediate effect. Re-selecting the active option leaves the current selection unchanged.

Keep selection session-only and local to each open application instance. Fresh pages, reloads, new desktop windows and newly opened sidebars start red. Closing and reopening a sidebar starts red; merely resizing, moving focus or switching tabs while it remains open preserves the selection. Closing the desktop application and relaunching starts red. Multiple instances do not synchronize their selections. These lifecycle choices are proposed for approval.

The layout remains usable in narrow panels and with ordinary text zoom; controls stay vertically stacked. Small viewports may scroll vertically, and no capability is hidden behind a separate settings screen.

## Delivery and releases

Deliver three bounded platform increments, in order:

1. Browser baseline: reusable UI and interaction, distributed as a deployable static build.
2. Windows Electron: the same UI in a packaged desktop application bundling its runtime assets; retain the browser build.
3. Extensions: Chromium and Firefox sidebar packages delivered together; retain browser and Windows packages.

Proposed versions are 0.1.0, 0.2.0 and 0.3.0 respectively. After each platform increment is implemented, verified and integrated, publish its version tag and GitHub release. Each release contains deployable or installable packages for every platform delivered by that point, installation instructions and verification limitations.

Proposed desktop distribution is an unsigned portable Windows x64 ZIP that launches after extraction. Proposed extension distribution consists of separate development packages for Chromium and Firefox with explicit loading instructions; signing and store publication are outside the proposed delivery. Instructions must identify restrictions on temporary/development loading and must not imply signed or store-distributed installation.

## Quality and verification

Verify initial state, exclusive selection, immediate color changes, label and keyboard input, narrow/resized layout and lifecycle behavior. Cover Chromium and Firefox browser behavior and platform-specific extension entry points. Verify packaged assets, entry points, runtime dependencies and the actual artifacts supplied with releases. A source build alone does not establish a delivered package.

The current execution host is Linux. Windows artifacts may be cross-built and inspected with feasible host-side checks; native Windows execution is excluded unless a suitable execution facility is available. Reports and release notes must distinguish those checks from native launch or installation evidence. An inability to produce a required package remains a delivery blocker.

## Scope boundaries and decisions

The application has no required persistent data, cookie or URL configuration, file import/export, backend, accounts, settings panel or selection synchronization. Conditional platform-adaptation instructions do not add these capabilities.

The lifecycle and distribution choices above are proposals. Shared plain HTML, CSS and JavaScript is the recommended implementation direction because this scope needs only native controls and a small amount of state; framework choice and detailed component/package boundaries remain with ARCHITECTURE. Browser support floors, exact package tooling and reproducible verification commands will be established against platform documentation during detailed preparation.
