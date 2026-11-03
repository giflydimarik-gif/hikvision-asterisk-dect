# Verified scope and compatibility

Reviewed 2026-11-01. No account IDs, serial numbers, passwords, addresses or
private images are needed to reproduce the public examples.

| Component / feature | Evidence | Limit |
| --- | --- | --- |
| DS-KV6113-PE1(C), V3.7.0 build 250929 | Read-only device-info query on our installed panel | Other revisions/firmware are unverified |
| Hikvision-Addons stable 3.0.34 | Installed add-on running; one outdoor device configured; call-state polling interval 2 seconds | Proposed patches target newer upstream main and are not installed |
| Current call status | Authenticated ISAPI GET returns `CallStatus.status = idle` | No real ring was generated during this review |
| HA to MQTT to panel | Read-only call-status command returned status attributes in HA | HA button press time alone is insufficient proof of a fresh device response; repeated-value correlation still needs an explicit response timestamp or MQTT evidence |
| Snapshot | Existing camera transport and the public examples are available | Add-on snapshot option is off; new polled-ring patch has isolated tests only |
| Local SIP registration | Existing Asterisk and Hikvision registration services running | Does not establish that every current DECT handset rang, audio worked, or DTMF unlocked a gate during this review |
| Original Netcraze NC1812 + DECT101 example | README records the previously tested setup | Do not present it as an independently tested Gigaset N510 configuration |
| VDP-H3212W, V2.2.22 build 230720 | Read-only SDK login; current scene `atHome` and AudioOut GET succeeded | Setting a scene, restoring volume and broadcast are not physically tested; the listed call commands are capabilities, not proof of successful answer |
| Wall-panel video / microphone | Video and two-way audio need separate checks | One-way audio support does not establish microphone support; an insecure browser context may restrict a microphone |
| Gate state | Independent existing position sensor | Relay state and an HTTP success response do not prove gate movement |

The deployment plan and private infrastructure details live in our private
operations repository. Public examples retain placeholders; never copy local
credential files, launch data, private camera frames or raw SIP authentication
logs into issues.

For quiet hours, preserve the actual indoor volume across restarts. The current
add-on keeps the previous volume in memory; repeated mute and restart behavior
must be considered before treating an unmute to the default 7 as restoration.
Notifications should remain independent of indoor sound.

## Indoor notifications — publication review,2026-11-03

The earlier table is the2026-11-01 baseline. Later work established the following
additional, scoped observations on VDP-H3212W/V2.2.22 build230720:

| Feature | Evidence | Limit |
|---|---|---|
| Russian text, native notice16008 | User observed banner and full message in the source installation | Other models/firmware are unverified |
| JPEG attachment | User observed thumbnail/full image of one synthetic640x360 image | The new portable module caps images at24KiB and one attachment |
| Native alarm-notice type3 | User reported a short siren in the source installation | No programmable duration, TTS or guaranteed sound while muted |
| Home quiet-volume preservation | Existing private integration confirmed a temporary0→9→0 cycle and kept talk volume/settings | This is a separate integration, not included in the portable MQTT command |
| Portable SDK/MQTT adaptation | Offline regression tests, C transport stub, JPEG decode and synthetic card inspection | No new physical-device acceptance or Docker-image test for this adaptation |
| Reading receipt | Bounded earlier observation received no matching event | Neither confirmed reading nor confirmed absence of reading |

See [the module contract](../indoor-notifications/README.md) and
[publication validation](../indoor-notifications/VALIDATION.md). The public package
contains no house-specific rule configuration, private screenshots, serials,
addresses or credentials. Existing home production was not redeployed for this contribution.

## Current add-on notice review — 2026-11-03

[PR #394](https://github.com/pergolafabio/Hikvision-Addons/pull/394), head `fb45f64265bb`,
uses `Title | Body`, one optional local/HTTP(S) JPEG, one button and STDIN
`sendNotice indoor`. It passed 117 tests and all five CI jobs. The exact-source
STDIN/SDK harness accepted one custom-title level-4 notice on VDP-H3212W without
deploying the full fork. Earlier HTTPS tests used the same image loader and a
22,524-byte JPEG. Physical image rendering, a live HA click and Supervisor STDIN
remain separate acceptance boundaries.

The current add-on path bounds a JPEG to512KiB; our device advertises512KB.
The portable package's24KiB limit, alarm type, six entities and durable journal
describe the separate archived PR #393 adapter. That PR was closed without merge.
See [the current workflow](../indoor-notifications/README.md#актуальный-вклад-в-add-on-pr-394).
