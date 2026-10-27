# Delivery plan

## Delivery strategy

Deliver the [SPEC](SPEC.md) through three bounded platform increments. The first provides the complete usable browser interaction; the second adds a standalone Windows package; the third adds both sidebar extensions together. Preserve all delivered versions at each increment, using the same canonical UI assets and testing relevant regressions before integration. The [design](ARCHITECTURE.md) separates platform hosting from shared selection behavior.

| Phase | Version | User-visible outcome | Included contracts | Deferred platform scope |
| --- | --- | --- | --- | --- |
| 1 Browser baseline | 0.1.0 | Open the browser build and change Hello World between three colors | R1-R5, browser portion of R9-R10 | Electron and extension hosts/packages |
| 2 Windows desktop | 0.2.0 | Extract and launch the same application as a Windows desktop app; browser remains available | R1-R6, browser/Windows portions of R9-R10 | Chromium and Firefox extensions |
| 3 Browser sidebars | 0.3.0 | Open the same application in Chromium and Firefox sidebars; browser and desktop remain available | R1-R10, all applicable platform cases | Signing and store publication are outside project scope |

One delivery milestone per phase is appropriate to this application's narrow functionality. Splitting a three-color interaction into separate technical milestones would add handoff overhead without another useful product boundary. Each delivery milestone includes integrated behavior, artifact production and whole-capability review; a separate final review milestone checks the complete phase. The extension phase includes two adapters because both browsers must ship together, not because the adapters are interchangeable.

## Phase 1 — Browser baseline

Dependency: accepted project preparation integrated and published to the actual default branch; implementation range and preparation/phase tracking readiness established.

### Milestone 1.1 — Usable browser package

Produce the smallest complete browser product: canonical native controls, immediate color changes, keyboard use, initial/reset behavior and a fluid layout. Establish the actual pinned development/test environment alongside the first slice, including dedicated managed Chromium and Firefox, finite execution bounds and representative interaction/render/teardown checks. Environment provisioning evidence is separate from application acceptance.

Assemble a static build with relative local assets and no runtime service or external dependency. Verify it from a local file and from a static path using the built or extracted archive, not only source files. Include archive integrity, local references, installation guidance and initial version metadata. Do not install or implement Electron or extension hosts in this phase merely to prepare their eventual delivery.

Exit: R1-R5 and applicable R9-R10 pass feasible checks; screenshots confirm rendered message/controls and narrow layout. Repeated sessions and restoration preserve the intended default behavior. Browser archive, INSTALL.md and checksums are release-ready. Whole-milestone code review, applicable tests, blocker repair, milestone report and HANDOFF are included in the final delivery task. Demonstrate initial red and keyboard/pointer color changes at narrow width; this supports the human decision to continue, amend or simplify without adding an unsolicited approval gate to an authorized range.

### Milestone 1.2 — Phase review

Exactly one phase code-review/testing/report task follows milestone 1.1 completion and closure. Review integrated browser behavior, package/source/version identities and outstanding findings. Run applicable regressions, repair blockers and record the phase report. Then integrate the verified complete phase into default, verify the merged result and publish release 0.1.0 under the release procedure below.

## Phase 2 — Windows desktop

Dependency: phase 1 complete, integrated and published with verified release 0.1.0; authorization and phase tracking permit advancement.

### Milestone 2.1 — Portable desktop package

Add the Electron host and its local-resource boundary without changing the common UI/controller. Establish the exact supported Electron runtime version and trusted download/checksum evidence. Exercise host lifecycle and denied path/navigation/permission behavior with feasible host-side checks. Build the Windows x64 portable distribution from the official runtime and local application resources; user installation must not depend on developer tooling.

Regenerate the browser build at version 0.2.0 and assemble the cumulative browser/Windows release set. Verify the actual Windows ZIP's executable architecture, entry point, renderer assets, runtime resources and notices, plus archive safety and dependency completeness. Check paths containing spaces. Run native Windows launch/close/relaunch checks if a suitable facility exists; otherwise record them as untested, without turning unavailable target-native execution into a gate. Re-run shared browser regressions against the browser archive and the desktop renderer asset identity.

Exit: applicable R1-R6 and R9-R10 pass feasible checks; both archives and installation instructions agree on version and distribution type. Whole-milestone code review, regressions, blocker repair, report and HANDOFF are folded into the final delivery task. The demonstration is the actual portable-package launch when available, otherwise the extracted package/resource evidence together with the browser-rendered common UI, explicitly labeled as non-native evidence. The human may continue, amend or simplify at this boundary.

### Milestone 2.2 — Phase review

Exactly one phase review/testing/report task follows milestone 2.1 completion and closure. Review desktop isolation, Windows package completeness and preservation of browser behavior. Resolve blockers and retain verification limits. Integrate and verify the complete phase before publishing cumulative release 0.2.0.

## Phase 3 — Browser sidebars

Dependency: phase 2 complete, integrated and published with verified release 0.2.0; authorization and tracking permit advancement.

### Milestone 3.1 — Dual sidebar packages

Add the Chromium MV3 side panel adapter and Firefox MV3 sidebar entry around the common assets. Verify Chromium 142 lifecycle routing, readiness/reconnect ordering and window isolation separately from the simple color behavior. Firefox uses document recreation and its native sidebar chooser. Validate the declared API/version floors and development-loading procedures against actual selected browser builds.

Produce separate extension ZIPs and regenerate browser/Windows packages at version 0.3.0. Exercise shared UI from extracted extension assets and feasible adapter tests. Use capable native extension hosts to load the actual packages and check open/change/close/reopen and independent windows where available. In Chromium, full-browser extension execution is distinct from headless-shell shared-UI checks. In Firefox, a browser page or mocked sidebar event is not native add-on evidence. Diagnose unavailable facilities under repository policy; document exclusions and continue feasible package/adapter checks.

Exit: R1-R10 applicable coverage and all four archive checks pass within the available verification scope. Required entry files, permission sets, local resources, metadata and lifecycle contracts are checked. Installation instructions distinguish unpacked Chromium development loading and Firefox temporary add-on loading from signed/store distribution. Whole-milestone review, regressions, blocker repair, milestone report and HANDOFF belong to the final delivery task. Demonstrate both sidebars when native hosts are available; otherwise retain the exact package, shared-rendering and adapter evidence with excluded native cases stated. This boundary supports the human decision on completion or further work.

### Milestone 3.2 — Phase review

Exactly one phase review/testing/report task follows milestone 3.1 completion and closure. Review the full cumulative application, adapter isolation, package correctness and relevant regressions; aggregate remaining TODOs in the final implementation report. Integrate and verify the complete phase before publishing release 0.3.0 with every platform archive.

## Verification, integration and releases

| Concern | Evidence and ordering |
| --- | --- |
| Environment | Pin the selected test/runtime versions; record dedicated binaries and effective modes. Follow repository browser and Playwright guidance proactively, including bounded recovery before dependent work. |
| Application | Use pytest for test execution and Python Playwright for available Chromium/Firefox UI. Keep rendering, input, restoration and actual artifact execution in scope. Narrow layout/zoom and correct rendered colors require visual evidence. |
| Platform coverage | Host-side checks, package contents and modeled adapter events are feasible evidence, not native compatibility claims. Unavailable Windows/native full-browser execution is excluded under repository policy; actual feasible build/test failures remain blockers. |
| Milestone exits | Final delivery task owns whole-capability code review, tests, fixes, report and HANDOFF; its completion includes all earlier milestone tasks. No standalone delivery-milestone review task is needed because each phase has one delivery milestone. |
| Phase exits | Dedicated phase review requires the delivery milestone complete/closed, verifies interactions and retains the report and unresolved TODOs. Phase review milestone contains exactly one task. |
| Integration | Audit task completion persistence, inspect complete phase differences, explicitly merge into the recorded default parent, verify merged state, publish and read back before dependent phase work. |
| Release | After verified integration, finalize release notes/version on the actual default branch release commit, publish/read back it and the version tag, then upload/publish only the verified cumulative asset set. Download/read back asset bytes and compare SHA-256. Source-only tags do not satisfy delivery. |

Release notes identify delivered features, exact archive installation, unsigned/development status, tested environments, excluded native checks and checksums. The release contains INSTALL.md and SHA256SUMS alongside applicable platform archives. Pin the source commit used for packaging; if release preparation changes runtime source or version metadata, rebuild/recheck affected packages before publication. Release publication is a post-integration operation; phase review must not claim that an upload already succeeded.

## Risks and control

The main risks are runtime/browser provisioning, retained-panel lifecycle ordering and mistaking source verification for packaged or native behavior. Resolve setup before dependent execution, check adapter race/isolation cases, and inspect actual final artifacts. Preserve required artifact delivery when a target-native facility is absent. No unrequested backend, persistence, installer, signing or store process is needed. Exact physical owners and commands are defined in layout and TASKS; this plan supplies the delivery boundaries.
