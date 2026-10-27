# Development

Use Node.js 22+ and Python 3.11+. Dependencies and browser binaries are project-local; no global installation or virtual environment is required.

```text
python -m pip install --target .tools/python -r requirements-dev.txt
```

Set PYTHONPATH to the absolute .tools/python directory and PLAYWRIGHT_BROWSERS_PATH to the absolute .tools/browsers directory for installation and execution. On Windows use CMD set commands; PowerShell is not used.

```text
python -m playwright install --only-shell chromium firefox
python -m pytest tests/environment -q
```

Each pytest case has a 45-second timeout, with shorter browser launch/navigation/action bounds. A job supervisor should additionally bound the whole test process and terminate only its owned tree. Environment probes do not certify application acceptance. Application build commands are documented as their implementations become available.

## This execution host

Normal CDN downloads returned HTML. The matching official Playwright 1.64.1 noble image supplied managed browsers via the bundled Playwright policy fallback; exact manifest/layer identities and extraction checks are recorded in [environment evidence](dev/reports/phases/1/ENVIRONMENT.md). No global browser or dependencies were installed.

On this constrained Linux host only, set HELLO_FIREFOX_UNSANDBOXED=1 for trusted local test pages after diagnosing uid_map EPERM. This opts Firefox into its documented process-local content-sandbox override. Re-evaluate on another host. Full Chromium fails on a host-denied Unix socket even with --no-sandbox; shell and Firefox checks work.

## Browser build

```text
node scripts/build.mjs browser
python -m pytest tests/ui tests/build -q
```

Open build/browser/index.html directly or copy that directory to a static host. HELLO_UI_ROOT selects an extracted static build for the shared UI suite. Actual UI checks passed in Chromium shell and Firefox; two zoom overflow failures were corrected by reducing fluid control spacing.

## Package browser release

```text
python scripts/package.py release --phase 1
python scripts/package.py verify --phase 1
python -m pytest tests/build tests/packaging tests/ui -q
```

Artifacts are allowlisted, checksummed deterministic ZIPs under dist. Never package the repository or credential file. Rebuild after choosing the final release commit so version.json identifies its exact source.

## Desktop host

```text
node scripts/build.mjs desktop
python -m pytest tests/desktop tests/build tests/ui -q
```

The generated build/desktop/app contains a minimal Electron entry and the identical renderer assets. Host security/resource tests execute the real entry using a modeled Electron API and real filesystem resources in a path containing spaces. They are not native Windows launch evidence. Windows runtime packaging is a separate delivery task.

## Windows runtime packaging

```text
python scripts/package.py release --phase 2
python scripts/package.py verify --phase 2
python -m pytest tests/desktop tests/packaging -q
```

Electron 45.0.0 win32-x64 and its official archive SHA-256 are pinned in toolchain.json. The packaging script checks integrity before safe extraction, preserves the complete runtime/notices, adds resources/app, removes the stock demo and renames the launcher HelloWorld.exe. No Wine, native executable editing, global Electron install or separate user Node.js is required. Native Windows execution remains untested on this Linux host.

## Chromium side panel

```text
node scripts/build.mjs chromium
python -m pytest tests/extensions -q -k chromium
```

Use built output, not source manifest templates; version comes from package.json. The worker uses Chrome 142 open/closed events and authenticated window-scoped ports. Session tokens, per-port sequence validation and readiness acknowledgments preserve a live selection during reconnection and reject obsolete/wrong-window messages. Tests cover the real worker in a modeled API harness and the real panel bridge/DOM in both working browsers. They do not claim native sidePanel events. Full Chromium launch was already diagnosed as host socket EPERM with --no-sandbox; native panel checks remain excluded on this host.
