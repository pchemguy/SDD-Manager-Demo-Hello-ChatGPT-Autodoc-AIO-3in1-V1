# Main documentation preparation record

## Current control

- Mode: autodoc/onepass, explicitly selected in the project request on 2026-10-27.
- Scope: complete Hello World application across browser, Windows Electron and Chromium/Firefox sidebar extensions, delivered in that order.
- Approval basis: PROJECT approved by the user response "OK." on 2026-10-27 to proposal commit d1c86e888029abdfb6038a76ab6e54c17a229110. ARCHITECTURE through TASKS checkpoints are preapproved by autodoc selection. No implementation range or whole-package QC advance has been selected.
- Tracking: enabled for preparation and implementation by root AGENTS.md. The sdd-docs-main milestone and all nine exact bundled issue definitions were created and read back before repository writes.
- Next boundary: complete remaining documents through DOCS-008 and stop before DOCS-009, package integration and implementation.
- Reporting: concise Standard; preserve material choices, blockers and checkpoints.

## Scope and decisions

The user request is the complete target scope. The baseline displays Hello World and three vertically stacked radio buttons labeled red, blue and green; red is initially selected and the message is red. Exactly one selection controls the message color immediately. Share logic and UI across browser, Windows Electron and both sidebar extensions; keep platform-specific code separate. Runtime packages require no separate Node.js, development server or backend. Each completed, verified, integrated platform phase receives a release including packages for all platforms delivered so far and installation/distribution limitations.

Material proposals for PROJECT review: session-only color selection; every fresh UI and sidebar reopening starts red; native radio keyboard behavior; narrow resizable layout; portable Windows x64 ZIP; development extension packages with signing/store status stated explicitly; versions 0.1.0, 0.2.0 and 0.3.0. These choices were accepted with PROJECT by the user response "OK." on 2026-10-27. No persistence, cookie/URL configuration or file operations are introduced.

## Decisions and document evidence

| Task | Evidence / decision basis |
| --- | --- |
| DOCS-001 | All four root files existed and were preserved byte for byte, checked against baseline SHA-256 identities. Task list copied from the same repository-pinned SDD Manager 0.15.4 package. Default provenance setup completed as described below. Initialization completion is in this commit; publication and issue closure must be read back before dependent work. |
| DOCS-002 | PROJECT proposal SHA-256 fb2ef7fdcd6cd88e96b8ba652c592ab9211172cbbefe1cab848d9f6e6951fbcb; human approval received in the user response "OK." on 2026-10-27; approved bytes retained unchanged. Reviewed against the complete user scope, document role and root instructions; all three platforms and cumulative artifact releases covered. Lifecycle and distribution choices accepted with the brief. DOCS-002 completion accompanies this approval record. |
| DOCS-003 | Define shared UI and isolated platform hosts Autodoc scoped preapproval applies. Reviewed approved PROJECT coverage, ownership and dependency direction, lifecycle reset design, source-backed platform constraints, package isolation and product-document content boundaries. No unresolved architecture blocker; runtime/API evidence remains to be collected during implementation. Content identities: docs/dev/ARCHITECTURE.md SHA-256 a7d383106368f0a75a857189f687e1cb2bd26dc6c09672b0cfc3d3d095c262d7. |
| DOCS-004 | Define component ownership and lifecycle seams Autodoc scoped preapproval applies. Reviewed architecture-to-component allocation, current-state ownership, reset/reconnect races, resource teardown and error boundaries. No framework, storage or speculative privileged bridge introduced. Preparation evidence rows normalized into one table; no product design change. Content identities: docs/dev/DECOMPOSITION.md SHA-256 f5b6c4c7ca13e31f4bda6ef17646cfe8a35a76ad4f2426637e81952c0db57e8f. |
| DOCS-009 | Not authorized by autodoc stop; remains pending. |

## Initialization

- Retained: AI_DISCLOSURE.md, SDD-MANAGER.md, AGENTS.md and SKILL_DISCOVERY_PROTOCOL.md. Copied root files: none. SHA-256 preservation checks passed.
- All four root files were present, so no mixed-initialization continuation checkpoint applies.
- Default manual provenance setup: base main at 6b6ed864477d4678c30cb45207dd5d04e4b52a5b; seed design-docs/ai-logs at 1608fb36cf08349139d96c41983cadcefff67b9a; verified explicit merge into main at dbbe994263b938ccf48bbad91d13be22f7f8994f. Seed and merge were published with exact remote readback. Both scaffold assets match package bytes. No conversation was recorded.
- Execution host: Linux; Node 24.22.1, Python 3.12.14 and Git 2.51.1 available. Windows shell policy applies only to Windows hosts. Target-native Windows execution has not been established; cross-build and package checks remain in scope, with native execution limits reported honestly.
- Repository eligible and initially clean at 6b6ed864477d4678c30cb45207dd5d04e4b52a5b; no existing project documents, application, pending work or alternate workflow branches found. Repository discovery was read-only.
- Credential exclusion verified with Git before protected conventional token storage. Credential remains untracked and excluded.
- Current reset: none; onepass.

## Pending transitions

Publish/read back the DOCS-004 completion commit, then close/read back its preparation issue before dependent progression. Continue only through DOCS-008; package QC and implementation remain outside the current range.
