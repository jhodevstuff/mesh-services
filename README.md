# mesh-services

Meshtastic web services, for the moment only e-mail support. More to come (maybe).

---
## Setup and usage
Disclaimer: This was developed and tested on a Raspberry Pi 4 running Debian, using a Heltec V3 LoRa Node.

1. Connect your Meshtastic Node to your computer/server (use a data cable!)
2. Rename the `config-sample.json` to `config.json`
3. Set the baud rate in the config file `config.json` correctly (can be changed in the Meshtastic app)
4. Setup SMTP server login data in the `config.json`
5. Run the mesh-services script(s) with python3

Using the Meshtastic app you can send a direct message to the server-node (connected to the computer running the script).
The computer will get the infos via the serial output and will process it.

---

### meshmail
`python3 meshmail.py`
Send mails from a device without internet connection.

Prompt:
```
@mail
to: person@example.com
from (optional): YourName
subject: Test Mail
content: This is your mail content!
```

Known bugs:
- Only a few words will work, so keep your messages short
- Single line (Meshtastic web interface) not supported by now
- Should use the sender's node name as default recipient but it won't
- Unexpected promt format will cause errors



###### Developed by Joshua Hoffmann / 2024-10-20 / v1.0