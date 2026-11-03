# Publication validation —2026-11-03

Scope: portable indoor-notice module plus an independent MQTT command for
Hikvision-Addons. This is an adaptation of our measured native sender, not a new
claim of universal Hikvision support.

Baselines:

- Companion repository: `c7556a76c8b6cb9aba76927da62054c66549f4fe`.
- Upstream add-on: `eb5be4f95e66d2abdc575bb637a25b8511f7d05d`.
- Existing household gateway/source remains separate; no deployment, sound test,
  relay action, SIP change, new service or home package installation is part of publication.

## Offline verification

-23 companion tests: strict JSON/UTF-8, native levels3/4, exact struct offsets,
  backing-picture memory, fixed32-bit function signature, crash/timeout dedup,
  cross-connection duplicate protection, capacity/rate limits, private journal,
  symlink/FIFO rejection, JPEG normalisation and metadata removal.
- Compiled local C transport stub exercises the actual private ctypes function
  wrapper and verifies that pre-existing SDK function signatures remain unchanged.
- Native add-on suite:98 passed,8 skipped with CI=1 (physical-device tests skipped).
  The35 new tests include the19 shared sender tests and16 adapter tests. Baseline
  SDK load/setup tests use the upstream's existing Linux library, without a device login.
- Targeted tests cover exact-device routing, busy/unavailable failure, retained
  replay, bad JSON, MQTT reconnect, and ambiguous normalised station names.
- Fatal flake8 selection and canonical path-scope checks pass. Diff reviewed for
  auth, dependencies, callbacks and existing control paths. No production SDK-wide
  typedef/signature/callback changes and no new add-on dependencies.
- HA YAML parsed and Jinja serialization checked with synthetic inputs, including
  Cyrillic, quotes, newlines, event-ID length and optional picture. These checks
  do not establish installation of the examples in a live HA instance.
- Synthetic status card640x360/22524 bytes inspected visually: seven readable
  lines, Cyrillic and explicit demonstration label. Full Pillow decode passes.

Local suite environment: Python3.12, pinned upstream requirements with the old
optional `ruamel.yaml.clib==0.2.7` omitted (it cannot build here); pure-Python
ruamel.yaml remains at the upstream version. Repository requirements are unchanged.
The upstream suite emits existing destructor/deprecation warnings under this
environment. No Docker-image build, ARM execution, real broker-reconnect test or
hardware run of this new adapter was performed.

## Evidence limits and operator contract

The source installation's owner observed native text/JPEG and the native alarm
sound on VDP-H3212W/V2.2.22 build230720 before this extraction. That evidence does
not establish physical acceptance of the newly packaged adapter. SDK accepted
does not mean physically displayed, heard or read.

Fresh idle checking cannot make the device read/send atomic. The module does
not change sound volume or quiet-hour state. JPEG structure validation is bounded
and is not a full entropy decoder: files must come from a trusted normaliser.
This contribution deliberately has no unknown retry, mass old-event replay,
automatic journal pruning, receipt listener or second SDK connection.

Rollback: revert the contribution's code/docs, preserve notice-journal and
media, and retain the current image before any separately authorised deployment.
The home production release does not need rollback for a source-only publication.
