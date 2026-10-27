# Phase 3 final review

T-012. Reviewed the complete supported application and R1-R10 routes: shared native-radio state/rendering and lifecycle, Electron host/resource/security boundary, both extension entries/permissions, Chromium sender/window/token/order/reconnect behavior, cumulative build/package/provenance/integrity and install guidance. No unresolved product contract defect remains in the verified scope.

Finding P3-001: default pytest collection omitted tests/build because build is in pytest standard recursion exclusions. Explicit prior product suites included it. Updated norecursedirs in pytest.ini and verified default collection/execution now includes both environment probes and builder tests. Resolved. Expanded modeled open-before-ready/stale-ack/sender checks and real bridge rejection of an unknown no-reset session without changing production behavior.

Fresh final default suite: 34 passed in 26.63s. Four-platform artifact verification passed. Prior extracted-artifact UI result: 8 checks per platform, 32 total; current changes affect test discovery/coverage only, so artifact UI evidence remains applicable. Retained screenshots inspected.

T-009 through T-011 each have one initial task-owned closing commit containing result, evidence and checkbox. This task closes with final phase/implementation reports and HANDOFF. Milestone 3.1 closed/read back before review.

TODO: None. Native Windows launch, native Chromium sidePanel and Firefox installation/sidebar events are explicit unavailable-facility exclusions, not passes or deferred code TODOs. Details and bounded probes are retained in task/development evidence.

Next: publish/close T-012 and review milestone, integrate/verify/publish complete phase, then publish byte-verified release 0.3.0 from the actual default-branch release commit. No release success is asserted here.

## T-012 forward verification repair

P3-002: tracked-file audit found broad build/ ignore also excluded tests/build/test_build.py. Earlier checks executed this local test file, but it was not present in prior published task trees. Narrowed root generated-output rules to /build/ and /dist/ and included the previously omitted builder tests in the tracked source. This is a current reproducibility/acceptance repair; it does not rewrite earlier commits or claim those trees contained the omitted file. Hold integration until repaired tracked source is verified and T-012 closure read back. No second initial task closure is created.

## Fresh tracked-checkout recheck

P3-002 resolved. Published repair source 97e866f269f6fe80d7a9bab319bb3b4c272f300a was checked out into a new detached Git worktree. Builder tests were present in its tracked files. Rebuilt/verified all four artifacts from that tree and ran the default suite: 34 passed in 26.97s. No tracked changes remained in the verification checkout. Exact matching project-job dependencies/browser binaries and the checksum-verified Electron cache were reused; no untracked source test was copied into it. Earlier published trees remain unchanged and are not retrospectively claimed to contain the omitted tests. T-012 completion reassessment is cleared; publish this evidence and reclose/read back issue 21 before milestone/phase integration. No second initial task closure.
