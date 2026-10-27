# DECOMPOSITION

This model refines [ARCHITECTURE](ARCHITECTURE.md) into logical units. [SPEC](SPEC.md) owns their exact behavioral and message contracts. No focused child documents are needed for this small application.

## Components and collaboration

| Component | Responsibility and provided boundary | Required collaborators | Verification seam |
| --- | --- | --- | --- |
| C1 Shared document and style | Semantic message and labeled native radio group; responsive presentation, initial checked/color state and focus visibility | Standard browser HTML/CSS | Actual DOM, computed color, radio accessibility names, screenshots and viewport geometry |
| C2 Color controller | Mount one document instance; handle valid selections; reset to red; dispose listeners | C1 and DOM events | Public mount/reset/dispose behavior and event-driven DOM integration |
| C3 Browser bootstrap | Mount once on page readiness; reinitialize on browser restoration of a page session | C2 and document lifecycle | Initial/reload/back-forward restored pages and independent tabs |
| C4 Electron main host | App readiness, one startup window, app shutdown, safe local protocol and renderer restrictions | Electron main APIs, packaged C1/C2/C3 assets | Host entry and packaged-resource checks; native launch when available |
| C5 Chromium panel bridge | Mount shared UI and connect its window identity; apply only current-session reset events; reconnect without losing a still-open selection | C2 and extension runtime messaging | Real extension entry; window-scoped reset, reconnection and lifecycle-race scenarios |
| C6 Chromium lifecycle worker | Configure toolbar side panel opening; route open/close reset by browser window; expire disconnected recipients; register handlers at worker startup | Chromium sidePanel/runtime APIs and C5 ports | API adapter harness and actual full-browser panel events when available |
| C7 Firefox sidebar entry | Load local shared UI for each sidebar document | C1/C2; Firefox sidebar manifest | Document recreation and actual Firefox sidebar lifecycle when available |
| C8 Build assembler | Select platform entry and copy canonical shared assets from an allowlist; validate local references | Version metadata and C1-C7 source | Built output compared with shared source identities |
| C9 Package verifier and release assembler | Verify runtime download, construct platform ZIPs and cumulative release asset set, checksum archives and validate package structure | C8 outputs, official Electron distribution and metadata | Malformed archive fixtures, extracted output, checksum/download equality |

## State and interfaces

C2 owns the selected color in one live document; no platform host owns a competing color value. Mount returns the small reset/dispose boundary consumed by C3, C5 and C7. It accepts only the three canonical color values from its own radio group. Its listeners are installed once and removed on disposal. A rejected invalid event cannot corrupt the current checked/color pair.

C1 declares red in markup and stylesheet, so initial rendering is consistent before script initialization. C2 reasserts initial state after mounting or restoration. Standard native controls own keyboard navigation and mutual exclusion; the controller reacts to their change events rather than reimplementing focus movement.

C5 and C6 exchange lifecycle information only. A panel identifies its browser window and document connection; an open-session reset is routed to that recipient. Duplicate resets are harmless. Old connections are removed, events for other windows are ignored, and reconnecting a live panel is distinct from opening a new session. The worker stores only transient routing/session data and never persists color. Fresh documents start red even if no worker message has arrived; retained documents must consume pending resets after readiness. Exact message types, validation and race acceptance belong to SPEC.

C4 has no renderer bridge. It resolves only allowlisted local renderer resources under a registered application scheme, with an explicit root, canonical path validation, fixed MIME handling and no directory listing. Invalid resource requests fail closed. Closing its last window quits the application; app readiness creates the startup window once. A later process launch is a fresh color session.

C8 copies the common UI/controller for every platform and adds only the appropriate entry and platform manifest. Platform files do not maintain forked copies of the color-selection behavior. Browser output remains independent of both extension globals and Electron.

## Resource and failure boundaries

The UI owns its listeners and current DOM, the Chromium worker owns transient ports, Electron owns the window and resource handler, and build tools own temporary output and downloads. Teardown releases those resources. None needs a database, cookies, extension storage, filesystem dialog or backend.

Source/build/package failures are reported with nonzero tool results; incomplete output cannot be selected as a verified release asset. Download errors, checksum mismatch, unsafe archive paths, missing runtime files and inconsistent version metadata stop the affected packaging operation. Regenerating one platform cannot silently delete another platform from an applicable release set.

## Review outcome

Each component has one behavioral, hosting or build responsibility and an observable seam. C5/C6 form the only lifecycle messaging collaboration; they do not share application state. Build and package verification are distinct from UI correctness. There are no dependency cycles or unresolved ownership decisions; exact contracts remain with SPEC and physical file allocation with layout.
