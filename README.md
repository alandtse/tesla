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
-  [Tesla Tokens](https://play.google.com/store/apps/details?id=net.leveugle.teslatokens)
-  [Auth App for Tesla](https://apps.apple.com/us/app/auth-app-for-tesla/id1552058613)
## Installation

1. Use HACS after adding this `https://github.com/custom-components/tesla` as a custom repository. Skip to 7.
2. If no HACS, use the tool of choice to open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
3. If you do not have a `custom_components` directory (folder) there, you need to create it.
4. In the `custom_components` directory (folder) create a new folder called `tesla_custom`.
5. Download _all_ the files from the `custom_components/tesla_custom/` directory (folder) in this repository.
6. Place the files you downloaded in the new directory (folder) you created.
7. Restart Home Assistant.
8. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Tesla Custom Integration".

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

_Component built with [integration_blueprint][integration_blueprint]._

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[buymecoffee]: https://www.buymeacoffee.com/alandtse
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/w/custom-components/tesla?style=for-the-badge
[commits]: https://github.com/custom-components/tesla/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: LICENSE
[license-shield]: https://img.shields.io/github/license/custom-components/tesla.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Alan%20Tse%20%40alandtse-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/tesla.svg?style=for-the-badge
[releases]: https://github.com/custom-components/tesla/releases
[download-all]: https://img.shields.io/github/downloads/custom-components/tesla/total?style=for-the-badge
[download-latest]: https://img.shields.io/github/downloads/custom-components/tesla/latest/total?style=for-the-badge
