# Tesla Custom Integration

[![GitHub Release][releases-shield]][releases]
![GitHub all releases][download-all]
![GitHub release (latest by SemVer)][download-latest]
[![GitHub Activity][commits-shield]][commits]

[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

A fork of the [official Tesla integration](https://www.home-assistant.io/integrations/tesla/) in Home Assistant.

This is the successor to the core app which was removed due to Tesla login issues. Do not report issues to Home Assistant.

To use the component, you will need an application to generate a Tesla refresh token:
-  Android: [Tesla Tokens](https://play.google.com/store/apps/details?id=net.leveugle.teslatokens)
-  iOS: [Auth App for Tesla](https://apps.apple.com/us/app/auth-app-for-tesla/id1552058613)
-  TeslaFi: [Tesla v3 API Tokens](https://support.teslafi.com/en/communities/1/topics/16979-tesla-v3-api-tokens)
## Installation

1. Use [HACS](https://hacs.xyz/docs/setup/download), in `HACS > Integrations > Explore & Add Repositories` search for "Tesla".  After adding this `https://github.com/alandtse/tesla` as a custom repository. Skip to 7.
2. If no HACS, use the tool of choice to open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
3. If you do not have a `custom_components` directory (folder) there, you need to create it.
4. In the `custom_components` directory (folder) create a new folder called `tesla_custom`.
5. Download _all_ the files from the `custom_components/tesla_custom/` directory (folder) in this repository.
6. Place the files you downloaded in the new directory (folder) you created.
7. Restart Home Assistant.
8. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Tesla Custom Integration".

<!---->
## Usage
The `Tesla` integration offers integration with the [Tesla](https://auth.tesla.com/login) cloud service and provides presence detection as well as sensors such as charger state and temperature.


This integration provides the following platforms:

- Binary sensors - such as update available, parking, and charger connection.
- Sensors - such as Battery level, Inside/Outside temperature, odometer, estimated range, and charging rate.
- Device tracker - to track location of your car
- Locks - Door lock, rear trunk lock, front trunk (frunk) lock and charger door lock. Enables you to control Tesla's door, trunks and charger door lock.
- Climate - HVAC control. Allow you to control (turn on/off, set target temperature) your Tesla's HVAC system. Also enables preset modes to enable or disable max defrost mode `defrost` or `normal` operation mode.
- Switches - Charger and max range switch allow you to start/stop charging and set max range charging. Polling switch allows you to disable polling of vehicles to conserve battery. Sentry mode switch enables or disable Sentry mode.

## Options

Tesla options are set via **Configuration** -> **Integrations** -> **Tesla** -> **Options**.

* Seconds between polling - referred to below as the `polling_interval`.

* Wake cars on start - Whether to wake sleeping cars on Home Assistant startup. This allows a user to choose whether cars should continue to sleep (and not update information) or to wake up the cars potentially interrupting long term hibernation and increasing vampire drain.

## Potential Battery impacts

Here are some things to consider and understand when implementing the Tesla component and its potential effect on your car's battery.

- The `polling_interval` determines when to check if the car is awake and new information is available, but the Tesla integration will not wake up a sleeping car during this polling.  By default, the polling will occur every 660 seconds. Polling a car too frequently can keep the car awake and drain the battery. Different firmware versions and measurements of Tesla cars can take from 11 to 15 minutes for sleep mode to occur. There is no official information on sleep mode timings so your mileage may vary and you should experiment with different polling times for an optimal experience.
- The car will, however, be woken up when a command is actively sent to the car, such as door unlock or turning on the HVAC. It will then also fetch updated information while the car is awake based on the `polling_interval`.
- The car can intentionally be woken up to fetch recent information by sending a harmless command, for example, a lock command. This can be used in an automation to, for example, ensure that updated information is available every morning. (Note that the command must be valid for that specific car model. So locking the frunk of a Model 3 will not wake up that car).
- You can also toggle the `polling switch` on/off to  disable polling of the vehicle completely via automations or the Lovelace UI.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

_Component built with [integration_blueprint][integration_blueprint]._

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[buymecoffee]: https://www.buymeacoffee.com/alandtse
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/w/alandtse/tesla?style=for-the-badge
[commits]: https://github.com/alandtse/tesla/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: LICENSE
[license-shield]: https://img.shields.io/github/license/alandtse/tesla.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Alan%20Tse%20%40alandtse-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/alandtse/tesla.svg?style=for-the-badge
[releases]: https://github.com/alandtse/tesla/releases
[download-all]: https://img.shields.io/github/downloads/alandtse/tesla/total?style=for-the-badge
[download-latest]: https://img.shields.io/github/downloads/alandtse/tesla/latest/total?style=for-the-badge
