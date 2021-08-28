[![GitHub Release][releases-shield]][releases]
![GitHub all releases][download-all]
![GitHub release (latest by SemVer)][download-latest]
[![GitHub Activity][commits-shield]][commits]

[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

A fork of the [official Tesla integration](https://www.home-assistant.io/integrations/tesla/) in Home Assistant to use an oauth proxy for logins.

This fork uses an oauth proxy instead of screen scraping which was [rejected by HA](https://github.com/home-assistant/core/pull/46558#issuecomment-822858608). The oauth proxy sits as a middleman between Home Assistant and Tesla to intercept login credentials such as your account and password. Due to the way the HTTP server works in Home Assistant, the auth endpoint cannot be turned off although we protect access by requiring knowledge of a ongoing config flow id. However, for maximum security, restart Home Assistant to completely disable the proxy server.

To the extent the official component adds features unrelated to the login, we will attempt to keep up to date. Users are welcome to port any fixes in this custom integration into HA. Please note that this component will not have the same quality or support as the official component. Do not report issues to Home Assistant.

{% if not installed %}

## Installation

1. Click install.
2. Reboot Home Assistant.
3. [Hard refresh the browser][hard-refresh].
4. In the HomeAssistant UI go to "Configuration" -> "Integrations" click "+" and search for "Tesla Custom Integration". If you are replacing core, remove the core integration before installing.

{% endif %}

_Component built with [integration_blueprint][integration_blueprint]._

<!---->

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[buymecoffee]: https://www.buymeacoffee.com/alandtse
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/alandtse/tesla.svg?style=for-the-badge
[commits]: https://github.com/alandtse/tesla/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/alandtse/tesla.svg?style=for-the-badge
[license]: LICENSE
[maintenance-shield]: https://img.shields.io/badge/maintainer-Alan%20Tse%20%40alandtse-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/alandtse/tesla.svg?style=for-the-badge
[releases]: https://github.com/alandtse/tesla/releases
[user_profile]: https://github.com/alandtse
[download-all]: https://img.shields.io/github/downloads/alandtse/tesla/total?style=for-the-badge
[download-latest]: https://img.shields.io/github/downloads/alandtse/tesla/latest/total?style=for-the-badge
[hard-refresh]: https://fabricdigital.co.nz/blog/how-to-hard-refresh-your-browser-and-clear-cache
