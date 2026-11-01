# Proposed fixes for Hikvision-Addons

These are independent, reviewable contributions against upstream commit
`fb6abc177f62c480e39a6dbc9dbee997875c76a9` (main, reviewed 2026-11-01).
They are **not an upstream release** and have **not been installed on our live intercom**.
The three changes are proposed as separate commits in [draft PR #390](https://github.com/pergolafabio/Hikvision-Addons/pull/390).

| Patch | Result | Verification |
| --- | --- | --- |
| 0001 | Bind the interval separately for each device's call, scene and alarm polling task | Nine regression tests fail on the original source and pass with this patch; distinct intervals, reverse order, existing zero-to-15-second fallback |
| 0002 | Use the same opt-in snapshot path for SDK `ringing` and polled `ring`; suppress repeated states and overlapping captures; prevent an old SDK timer resetting a later call | Ten isolated transition/publication tests, plus the nine interval tests |
| 0003 | Update the ringing blueprint to a `sensor` selector and both current state values | Parsed YAML and manual review; no physical visitor test |

## Apply and check

Use a separate checkout of the upstream repository at the exact commit above.
Inspect all three patches before applying. The base file SHA-256 values are in
`manifest.json`. The patches are sequential: 0002 is based on 0001. Patch 0003
is independent of the Python changes.

```sh
git switch --detach fb6abc177f62c480e39a6dbc9dbee997875c76a9
git apply --check /path/to/0001-per-device-poll-intervals.patch
git apply /path/to/0001-per-device-poll-intervals.patch
git apply --check /path/to/0002-snapshots-on-polled-ring.patch
git apply /path/to/0002-snapshots-on-polled-ring.patch
git apply --check /path/to/0003-current-call-state-blueprint.patch
git apply /path/to/0003-current-call-state-blueprint.patch
python3 -m unittest discover -s hikvision-doorbell/tests -p 'test_poll_intervals.py' -v
python3 -m unittest discover -s hikvision-doorbell/tests -p 'test_ring_snapshots.py' -v
```

The additional tests use the actual source functions extracted with Python AST,
with fake devices and sensors. They do not need a broker or native SDK. They do
not replace upstream's full test suite, an add-on build, or a real call test.
Snapshot capture still uses the existing synchronous SDK implementation.
The overlap guard deliberately skips a new capture while a previous capture is
pending; it does not promise one completed image for every rapid call.

The blueprint suppresses initial unknown/unavailable states and a transition
between `ring` and `ringing`. It cannot identify every historical SDK event:
an old event delivered as a new idle-to-ring transition needs additional live
verification in the receiving automation. Do not use the blueprint to unlock a
gate automatically.

## Existing behavior to keep in mind

- `call_state_poll: 0` means a 15-second fallback, not disabled polling. Omit the
  value/use null to leave call polling disabled; choose a positive interval when
  the model supports the ISAPI call-status query.
- `snapshot` defaults to false. Without 0002, the SDK ring branch captures a
  snapshot, but the call-status polling branch does not.
- Relay/unlock events confirm a relay action or access event, not a gate's
  physical position. Use an independent contact sensor for position.
- Firmware and features must be checked per model and hardware revision. A
  KD8003(B) firmware report is not evidence for a KV6113(C).
- A browser video stream, a working SIP answer and a browser microphone are
  three separate capabilities. Keep a proven local SIP/DECT path available.

## Rollback

In the isolated upstream checkout, reverse the patches in order 0003, 0002,
0001 using `git apply -R`. If you built an add-on from these changes, retain its
previous image and configuration before installation. This repository does
not silently install a custom add-on or change a working SIP registration.

See [our verified compatibility notes](../../docs/compatibility.md).
