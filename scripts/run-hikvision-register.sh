#!/bin/sh
PASS=$(sed -n "s/^password=//p" /etc/asterisk/hikvision-indoor-secret.conf | head -n1)
[ -n "$PASS" ] || exit 2

export HIKVISION_PASSWORD="$PASS"
unset PASS

exec /usr/bin/python3 /usr/local/sbin/hikvision_register.py \
  --ip <ASTERISK_IP> \
  --domain <HIKVISION_INDOOR_IP> \
  --username 10000000005 \
  --extension 10000000005 \
  --name Asterisk
