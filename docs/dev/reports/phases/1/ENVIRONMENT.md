# Browser environment evidence

T-001, phase/1-browser-baseline from main at 1c47661ed5b8a1593638f07b6dd64cfba499a8c5. Linux x64; Node 24.22.1, Python 3.12.14. Exact Python dependencies pinned in requirements-dev.txt: pytest 9.1.1, Playwright 1.64.1 and transitive requirements.

Normal managed Chromium download returned HTTP 200 text/html (195 bytes), Site Unavailable, rather than ZIP. Independent Firefox installation ended with an owned directory-lock heartbeat failure. Both installer processes exited; no active owner remained. Version-matched official Microsoft image fallback used: mcr.microsoft.com/playwright:v1.64.1-noble, linux/amd64 manifest sha256:d65108d1a8095d8b0c4a5e32bf1807a40a5ce90ff0c78473e1116b1c243235e8. Config and needed layers were verified by SHA-256 and declared sizes before selective extraction.

Browser layers: sha256:eb005fbb9cada4cd1b9476577a1eef0e000a2a0e9e319f84ecf4bfff1a4f28bb, sha256:7a46c6fa11d20264f19eb470179e005df7330ab62c0edbcf979e39634ee9b039. Only Chromium, Chromium headless shell, Firefox and FFmpeg managed directories copied into .tools/browsers. Archive paths, internal links and entry types validated; no relevant whiteouts occurred. No global browser installed or personal profile used.

Managed Chromium 156.0.8078.4 revision 1248 and Firefox 157.0 revision 1555. Initial environment suite: Chromium passed; Firefox failed at new_page with Target crashed. DEBUG=pw:browser exposed /proc/self/uid_map: EPERM in Firefox content processes. Process-local HELLO_FIREFOX_UNSANDBOXED=1 maps to MOZ_DISABLE_CONTENT_SANDBOX=1 only for trusted local test pages on this constrained host.

Final command: HELLO_FIREFOX_UNSANDBOXED=1 python /tmp/hello-run.py python -m pytest tests/environment -q. Result: 2 passed in 3.50s; each test creates two isolated contexts/pages, inputs, computed blue text, PNG screenshot and teardown. Both first-cycle screenshots inspected: visible blue glyphs and button, correct rendering. Default launch/navigation/action deadlines and 45-second pytest case timeout; outer owned subprocess tree bounded to 180 seconds.

Full Chromium probe: headless, channel chromium, chromium_sandbox=False, effective --no-sandbox. Aborted with process_singleton_posix.cc socket() failed: Operation not permitted (1). This is a host-denied socket, not an internal sandbox setting that another flag can repair. Native full-Chromium/sidePanel execution is excluded under BROWSER_DEV_POLICY for this host. Shell checks remain available and do not establish native sidePanel behavior. Windows native execution unavailable.

These are provisioning and representative execution results, not application acceptance. No behavioral RED/GREEN claim applies to dependency provisioning.
