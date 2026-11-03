# PR #394: custom text and optional JPEG

The unchanged SDK structs, `Doorbell.send_notice`, `_notice_input_callback` and `_send_notice_callback` from [25c48281aebd](https://github.com/giflydimarik-gif/Hikvision-Addons/commit/25c48281aebd5199ea64d179606fb9b7a35c7d45) were run against **VDP-H3212W / V2.2.22 build 230720**, using its existing authenticated SDK. Source Git blob hashes were verified before AST extraction; method bodies were not rewritten. The harness populated the two drafts through the actual input callback, checked that editing sent nothing, then invoked one fresh `PRESS`.

At **2026-11-03 08:53:42–43 UTC (11:53:42–43 Moscow)**, exactly one real native command **16008**, structure size **1552**, normal level **4**, with **one 22,524-byte JPEG**, was accepted (`sdk_error=null`). [Sanitized SDK result and exact source hashes](sdk-result.json).

| Field | Value |
| --- | --- |
| Title | Home Assistant |
| Text | Проверка PR394: свой текст и JPEG. Картинка содержит демонстрационные данные. |
| Native notice ID | ha-20261103115342100613 |
| Image | [Existing demonstration card](../../examples/card-preview.jpg), baseline RGB JPEG, 640 × 360 |
| Image SHA-256 | `8657cf8b591616ad0f5186ea9a131fb7bfb897192a1e19c39b09fcfd3d1fb86f` |

The existing send lock and durable no-retry claim protected the attempt. Existing journals and protected configuration files were preserved; device settings were equal before and after. The temporary JPEG was removed. No full fork deployment, live HA entity click or household mode change was performed. Local validation: **98 tests passed, 8 hardware-only tests skipped**, fatal flake8 and scope/diff checks passed. [CI checks for this revision](https://github.com/pergolafabio/Hikvision-Addons/actions/runs/41606265254).

**SDK acceptance is not physical screen confirmation.** The JPEG and this new custom body still require a photograph/visual confirmation on the station; sound, automatic wake and reading receipts are unverified. The [older photographs](../pr394-2026-11-03/README.md) show the fixed text-only message from d17398, and are not evidence for this JPEG test. No new device screenshot or photo is claimed here.
