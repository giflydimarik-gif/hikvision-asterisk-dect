# Credits

The Hikvision indoor-registration approach and the `hikvision_register.py` helper are based on
the public Hikvision-Addons work by `pergolafabio`:

https://github.com/pergolafabio/Hikvision-Addons

Reference documentation:

https://github.com/pergolafabio/Hikvision-Addons/blob/main/asterisk/asterisk.as.indoor.md

The Asterisk/DECT configuration in this repository documents the tested local installation
and the changes needed for the Hikvision + DECT call path.

Indoor notice references:

- Hikvision, [How to Send Notices to Indoor Station from iVMS-4200](https://www.hikvisioneurope.com/eu/portal/portal/Technical%20Materials/07%20%20Video%20Intercom/03%20%20How%20to%20Guidance/1st%20Gen/How%20to%20Send%20Notices%20to%20Indoor%20Station%20from%20iVMS-4200.pdf).
- Public [HCNetSDK C++ notice demonstration](https://github.com/yyj8209/HikSyn/blob/master/DlgVideoIntercomNoticeDataCfg.cpp),
  showing the manufacturer's native command and picture structures.

The new portable notice implementation and its offline fixtures are original
code, derived from our own measured integration. No proprietary SDK binary or
private camera image is redistributed by the indoor-notifications module.
