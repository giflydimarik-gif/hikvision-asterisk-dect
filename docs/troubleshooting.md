# Troubleshooting

## Есть звук только в одну сторону

Для протестированной связки Hikvision критическим оказался RTP-порт 9654.

Проверьте endpoint indoor-устройства:

```ini
direct_media=no
rtp_symmetric=no
rtp_port_start=9654
rtp_port_end=9656
```

На обычном DECT endpoint `rtp_symmetric=yes` оставляѵтся включённым.

## Вызов сбрасывается

Проверьте, что Asterisk зарегистрирован как indoor extension и работает сервис:

```bash
systemctl status hikvision-indoor-register.service
journalctl -u hikvision-indoor-register.service
```

## Python-скрипт не запускается из dialplan

Это нормально. В этой схеме `hikvision_register.py` запускается через systemd, а не через `extensions.conf`.

Цепочка:

```text
systemd -> run-hikvision-register.sh -> python3 hikvision_register.py
```

## Нажатие # не открывает дверь

Проверьте DTMF negotiation. В SDP ожидается:

```text
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
```

`#` должен проходить через уже установленный bridge между DECT и Hikvision.
