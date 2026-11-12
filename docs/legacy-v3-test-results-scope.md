# Legacy V3 test-ledger scope warning

The existing `reports/test-results.json` was created for the V3-era package and includes V3/Remotion adapter and FFmpeg smoke checks. Its PASS records are historical evidence for the specific V3 code, environment and artifacts named in those records only.

They do **not** validate V4.1.2 or V4.1.3, the GitHub V4-CTL candidate, current private package content, live ChatGPT invocation, Remotion runtime/render, current MP4 output or production release. Do not aggregate the historical AT-001…AT-033 statuses into the V4.1.3 test count.

For V4.1.3:
- private-package full validator/pytest after overlay: `NOT_RUN` until actually executed;
- GitHub CI: applies only to the exact commit SHA recorded in GitHub Actions;
- external host/provider/renderer/media/rights/human checks remain separate.
