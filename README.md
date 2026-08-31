# Hikvision + Asterisk + DECT

Рабочая схема для связки вызывной панели Hikvision с обычной DECT-трубкой через Asterisk.

Проект вырос из реальной домашней установки: вызов с Hikvision приходит в Asterisk, затем звонит обычная DECT-трубка. После ответа работает двусторонний звук, а DTMF `#` проходит через SIP-мост и открывает калитку.

## Схема

```text
Hikvision door station
        |
        | SIP/RTP
        v
Hikvision indoor SIP side
        |
        | extension 10000000005
        v
     Asterisk
        |
        | PJSIP
        v
 DECT base / handset 101
```

В моей установке Asterisk работает отдельно, а DECT-база регистрируется на нём как обычный SIP-клиент.

## Что оказалось важным

### 1. Аудио Hikvision и RTP

Главная проблема была не в SIP-сигнализации, а в RTP. Для Hikvision indoor endpoint рабочими оказались:

```ini
direct_media=no
rtp_symmetric=no
rtp_port_start=9654
rtp_port_end=9656
```

В конкретной установке Hikvision отправлял аудио на UDP 9654. Включение `rtp_symmetric=yes` для этого endpoint ломало обратный звук: Asterisk начинал отправлять RTP не туда.

Для обычной DECT-трубки, наоборот, используется обычный endpoint с `rtp_symmetric=yes`.

### 2. Кодеки

Рабочие аудиокодеки:

```ini
allow=alaw
allow=ulaw
```

Для видеочасти можно оставить:

```ini
allow=h264
```

Сам DECT-вызов, конечно, остаётся аудио.

### 3. Как вызывается Python-скрипт

Python здесь **не запускается из dialplan при нажатии `#`**.

`hikvision_register.py` нужен для другой задачи: он регистрирует Asterisk как дополнительный indoor extension Hikvision.

Запуск постоянный через systemd:

```text
hikvision-indoor-register.service
        |
        v
run-hikvision-register.sh
        |
        v
python3 hikvision_register.py
```

Пароль не хранится в Python-файле. Launcher читает его из отдельного файла:

```text
/etc/asterisk/hikvision-indoor-secret.conf
```

Пример есть в репозитории.

### 4. Как работает `#` и открытие калитки

Вызов уже находится в двустороннем SIP/RTP-мосте:

```text
Hikvision <-> Asterisk <-> DECT
```

DECT-трубка передаёт `#` как DTMF (RFC2833 / `telephone-event`). Asterisk пропускает DTMF через активный bridge в сторону Hikvision. Hikvision обрабатывает команду и открывает замок.

То есть отдельный `System(python3 ...)` в `extensions.conf` для открытия двери в этой конфигурации не нужен.

## Файлы

```text
asterisk/
  pjsip_hikvision_bridge.conf
  pjsip_dect_example.conf
  extensions_hikvision_indoor.conf
  hikvision-indoor-secret.conf.example

scripts/
  hikvision_register.py
  run-hikvision-register.sh

systemd/
  hikvision-indoor-register.service

docs/
  troubleshooting.md
```

## Подключение файлов к Asterisk

В конце `/etc/asterisk/pjsip.conf`:

```ini
#include pjsip_hikvision_bridge.conf
```

В `/etc/asterisk/extensions.conf`:

```ini
#include extensions_hikvision_indoor.conf
```

После изменения конфигурации:

```bash
asterisk -rx "pjsip reload"
asterisk -rx "dialplan reload"
```

## Dialplan

Рабочая логика максимально простая:

```ini
[hikvision-indoor-in]
exten => 10000000005,1,NoOp(Hikvision indoor call)
 same => n,Progress()
 same => n,Set(CALLERID(num)=105)
 same => n,Set(CALLERID(name)=Gate)
 same => n,Dial(PJSIP/101,40)
 same => n,Hangup()
```

## Безопасность

В репозитории намеренно нет реальных:

- SIP-паролей;
- пароля Hikvision;
- внешних адресов;
- токенов;
- приватных ключей.

IP-адреса в примерах заменены на placeholders. Перед использованием подставьте адреса своей сети.

## Оборудование исходной установки

- Hikvision DS-KV6113-PE1(C)
- видеодомофон VDP-H3212W
- Asterisk 22
- DECT/SIP-база Netcraze Ultra (NC-1812)
- обычная DECT-трубка

## Статус

Конфигурация собрана на основе реально работающей установки: вызов, двусторонний звук и открытие калитки с DECT-трубки проверены на практике.
