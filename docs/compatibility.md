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
