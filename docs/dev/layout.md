# Repository layout

## Ownership map

This is the intended physical allocation for [DECOMPOSITION](DECOMPOSITION.md) and [PLAN](PLAN.md). The repository currently contains guidance, the pinned SDD Manager plugin and development documents. Paths below describe ownership, not a claim that application files already exist.

| Path | Owner and purpose | Checks / consumers |
| --- | --- | --- |
| app/index.html | C1 canonical message and native radio markup; local CSP and relative resources | UI and static-reference tests; all build variants |
| app/styles.css | C1 fluid layout, exact message colors and visible focus | Layout, color and screenshot tests |
| app/app.js | C2 shared controller, window.HelloColorApp mount/reset/dispose boundary; no platform imports | Real interaction tests and focused controller checks where useful |
| app/bootstrap.js | C3 browser/document initialization and restoration reset | Browser entry and Electron/Firefox shared entry |
| platforms/electron/main.cjs | C4 Electron application/window/resource handler; no preload | Desktop host/path tests and generated desktop app |
| platforms/chromium/manifest.json | C5-C6 MV3 side panel, local entries and minimum API level; version supplied by assembler | Extension manifest/package checks |
| platforms/chromium/panel.js | C5 panel bootstrap and window-scoped ready/reset connection | Chromium adapter tests; becomes bootstrap.js in Chromium output |
| platforms/chromium/background.js | C6 lifecycle event registration, routing and reconnection | Chromium adapter and native extension checks |
| platforms/firefox/manifest.json | C7 MV3 sidebar declaration and Gecko identity; version supplied by assembler | Firefox manifest, loading and package tests |
| scripts/build.mjs | C8 allowlisted platform assembly and generated metadata; no production UI behavior | Build tests and every package path |
| scripts/package.py | C9 safe ZIPs, runtime checksum/download/extraction, cumulative release asset assembly and archive verification CLI | Packaging fixture tests and actual-artifact checks |
| package.json | Canonical application version and development command navigation; no required production npm dependencies | Build/package/manifest version checks |
| toolchain.json | Exact Electron runtime version and distribution/checksum source identity selected for desktop delivery | Runtime download and package provenance checks |
| requirements-dev.txt | Exact pytest, Playwright and related selected Python test dependencies | Isolated development/test setup |
| tests/conftest.py | Shared fixtures, finite browser bounds, isolated profiles and built-artifact selection | pytest suites |
| tests/environment/ | Representative managed-browser session/input/rendering/teardown checks | Setup evidence; does not establish app correctness |
| tests/ui/ | R1-R5 shared behavior, lifecycle, keyboard and responsive rendering checks | Built/extracted variants in available managed browsers |
| tests/build/ | Static references, allowlisted copy/source identity and version checks | C8 outputs and browser delivery |
| tests/desktop/ | Local-resource denial, host lifecycle/configuration and Windows distribution checks | C4/C9; optional native checks explicitly reported |
| tests/extensions/ | Manifest/API boundaries, routing/race/isolation fixtures and capable-host native checks | C5-C7, extracted extension packages |
| tests/packaging/ | Download/checksum and unsafe-archive fixtures; actual package inventory/asset-set/checksum checks | C9 and cumulative release verification |
| tests/fixtures/ | Small synthetic archives, mocked extension/host API fixtures and invalid-input data | No credentials, bundled browsers or Electron runtime |
| docs/INSTALL.md | Canonical user installation and unsigned/development limitations | Included in platform archives and release assets |
| docs/DEVELOPMENT.md | Verified setup/build/check commands and evidence-limit explanations | Contributors; link from README and root AGENTS |
| docs/dev/reports/phases/PHASE/MILESTONE.md | Milestone review and verification evidence, using numeric IDs such as 1/1.1.md | Final delivery task in each milestone |
| docs/dev/reports/phases/PHASE/PHASE-REPORT.md | Dedicated phase code-review/testing/exit report | Final phase review task |
| docs/dev/reports/IMPLEMENTATION-REPORT.md | Final cumulative result and unresolved TODO aggregation | Final phase review task |
| RELEASE-NOTES.md | Finalized complete release message for the selected version | Default-branch release commit/tag and GitHub release body |

## Generated outputs and exclusion

| Path | Contents and ownership |
| --- | --- |
| build/browser/ | C8 static index.html, app.js, styles.css and browser bootstrap.js |
| build/desktop/app/ | C8 generated Electron package.json, main.cjs and renderer/ common assets |
| build/windows-x64/ | C9 complete extracted runtime plus resources/app; temporary distribution before ZIP |
| build/chromium/ | C8 root manifest.json, background.js, common index/app/style assets and Chromium bootstrap.js |
| build/firefox/ | C8 root manifest.json and common index/app/style/bootstrap assets |
| dist/ | C9 versioned platform ZIPs, INSTALL.md and SHA256SUMS for the current cumulative release |
| .tools/browsers/ | Dedicated Playwright managed binaries; isolated per-run profiles under an owned temporary directory |
| .tools/electron/ | Pinned trusted runtime archive/checksum cache |
| .tools/python/ | Optional project-local Python dependency target when needed; no global install or required virtual environment |
| .test-results/ | Screenshots and transient test output; selected durable evidence belongs in existing phase reports |

Generated output, downloaded dependencies, caches and credentials are ignored by Git. Build tools use explicit allowlists; ignoring a file does not itself make it safe for packaging. Root gh.tkn is the protected existing credential input and must never enter any archive. Preserve the existing *.tkn exclusion and repository guidance/plugin source.

## Placement and reuse rules

Canonical index.html, app.js and styles.css are copied unchanged into each platform. The common HTML references bootstrap.js; the assembler selects app/bootstrap.js for browser/Electron/Firefox and platforms/chromium/panel.js for Chromium. This is an entry adaptation, not a second color implementation. Desktop renderer files live under its generated renderer directory, with relative references intact. Only the Electron main process imports Electron. Only Chromium adapter files reference chrome APIs; Firefox declares its native sidebar without a compatibility library.

Python pytest is the single test runner. A Python test may run a bounded Node subprocess for a JavaScript adapter/host harness; it does not introduce Node's test runner or a second independently managed suite. Native-only scenarios must be distinctly selectable and reported as excluded if facilities are unavailable, while ordinary app and package checks continue.

The planned command interface is node scripts/build.mjs browser|desktop|chromium|firefox and python scripts/package.py release --phase 1|2|3. The release command assembles the cumulative platform set for the current root version and invokes required builders. python scripts/package.py verify --phase N inspects existing final artifacts without declaring native compatibility. These commands are implementation targets; validate them before publishing them as working setup instructions. Tests use python -m pytest with the owning test directory or selected scenarios.

No application tree is symlinked or served through Vite. Documentation roots remain under docs/dev, with adjacent SPEC/PLAN/TASKS review reports. No copies of executable TASKS live in reports. Root README and AGENTS gain validated project commands as implementation establishes them; planned commands are not represented as already working.
