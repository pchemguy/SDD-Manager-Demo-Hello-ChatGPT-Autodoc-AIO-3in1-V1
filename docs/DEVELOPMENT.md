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
