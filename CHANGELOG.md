# CHANGELOG

## v3.15.3 (2023-08-27)

### Fix

- Catch jsondecode errors ([`42a7a17`](https://github.com/alandtse/tesla/commit/42a7a176314f058fd810238f1eaed61d64ab795e))
- Add missing CONFIG_SCHEMA and service translations ([#673](https://github.com/alandtse/tesla/issues/673)) ([`c5aad96`](https://github.com/alandtse/tesla/commit/c5aad9628333cd5752a795192244a6ee525b1a98))
- Remove TeslaMate MQTT warning at every HA startup ([#683](https://github.com/alandtse/tesla/issues/683)) ([`b993bc9`](https://github.com/alandtse/tesla/commit/b993bc94d60c85666216f41239255ce04fb9e932))

### Refactor

- Change MQTT-update logging to DEBUG ([#685](https://github.com/alandtse/tesla/issues/685)) ([`4e091c4`](https://github.com/alandtse/tesla/commit/4e091c4db55d7f6250ca3fb680c39b6aff78271d))

## v3.15.2 (2023-07-27)

### Build

- build: pre-commit autoupdate (#664)

- build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: 3.5.2 → 3.5.3](https://github.com/commitizen-tools/commitizen/compare/3.5.2...3.5.3)
- [github.com/psf/black: 23.3.0 → 23.7.0](https://github.com/psf/black/compare/23.3.0...23.7.0)
- [github.com/pre-commit/mirrors-prettier: v3.0.0-alpha.9-for-vscode → v3.0.0](https://github.com/pre-commit/mirrors-prettier/compare/v3.0.0-alpha.9-for-vscode...v3.0.0)
- [github.com/asottile/pyupgrade: v3.8.0 → v3.9.0](https://github.com/asottile/pyupgrade/compare/v3.8.0...v3.9.0)

* style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

---

Co-authored-by: pre-commit-ci[bot] &lt;66853113+pre-commit-ci[bot]@users.noreply.github.com&gt; ([`fe9050f`](https://github.com/alandtse/tesla/commit/fe9050ff279bff15d0ddfce324170a8505f1ac2d))

### Chore

- chore: release 2023-07-27

Merge pull request #675 from alandtse/dev ([`b02c0da`](https://github.com/alandtse/tesla/commit/b02c0da10113f405739ce7344e771e9271a04a24))

### Fix

- fix: bump teslajsonpy to 3.9.2 (#674)

fixes slow startup, fixes energy sites sometimes not coming available, improves performance
changelog: https://github.com/zabuldon/teslajsonpy/compare/v3.9.0...v3.9.2 ([`8ba3ed8`](https://github.com/alandtse/tesla/commit/8ba3ed83ed0002bab2fa4aaf654809079f0f775b))

### Refactor

- refactor: reduce code needed to construct entities (#672) ([`f0b97ba`](https://github.com/alandtse/tesla/commit/f0b97ba6e793611c0caccc4b620ab1dae66abee1))

- refactor: reduce entity creation code (#671)

followup to #670 ([`96fdb46`](https://github.com/alandtse/tesla/commit/96fdb463b97556f478c0b7a52982ae228aa679ad))

- refactor: cleanup entity construction (#670) ([`79eea25`](https://github.com/alandtse/tesla/commit/79eea252d69b5581658cdc7e823d5b39e111367a))

## v3.15.1 (2023-07-08)

### Fix

- fix: check if arrival time attribute is available

closes #661 ([`5936ea3`](https://github.com/alandtse/tesla/commit/5936ea39049aa3728f03b975d54d02a6387cf8e6))

### Unknown

- Merge pull request #663 from alandtse/dev

fix: check if arrival time attribute is available ([`2765a53`](https://github.com/alandtse/tesla/commit/2765a53173c5655ecf816e1d1313772333926ce1))

## v3.15.0 (2023-07-07)

### Build

- build: pre-commit autoupdate (#653)

updates:

- [github.com/asottile/pyupgrade: v3.7.0 → v3.8.0](https://github.com/asottile/pyupgrade/compare/v3.7.0...v3.8.0)

Co-authored-by: pre-commit-ci[bot] &lt;66853113+pre-commit-ci[bot]@users.noreply.github.com&gt;
Co-authored-by: Alan Tse &lt;alandtse@users.noreply.github.com&gt; ([`dc68774`](https://github.com/alandtse/tesla/commit/dc68774cbf1f87f931eeb45d8731a2629c674215))

- build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: 3.2.2 → 3.5.2](https://github.com/commitizen-tools/commitizen/compare/3.2.2...3.5.2)
- [github.com/asottile/pyupgrade: v3.6.0 → v3.7.0](https://github.com/asottile/pyupgrade/compare/v3.6.0...v3.7.0)
- [github.com/floatingpurr/sync_with_poetry: 1.0.0 → 1.1.0](https://github.com/floatingpurr/sync_with_poetry/compare/1.0.0...1.1.0) ([`ed73ecb`](https://github.com/alandtse/tesla/commit/ed73ecbc253e303c6466e8aad32d0df8565ff805))

### Feature

- feat: add minutes-to-arrival-attr (#657)

Adds new attribute to arrival time sensor.

closes #656 ([`672fc04`](https://github.com/alandtse/tesla/commit/672fc046ef5213b4d7dc62bf34bccae1b6245b7b))

### Unknown

- Merge pull request #660 from alandtse/dev

chore: release 2023-07-07 ([`c0a9d87`](https://github.com/alandtse/tesla/commit/c0a9d877c3a6bed0714dbb7a278aa2b318a35079))

- Merge pull request #642 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`be6533f`](https://github.com/alandtse/tesla/commit/be6533fc35710a93189484a20deced364906a619))

## v3.14.0 (2023-06-17)

### Ci

- ci: Update codeql.yml to latest template (#639)

- ci: Update codeql.yml to latest template

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

---

Co-authored-by: pre-commit-ci[bot] &lt;66853113+pre-commit-ci[bot]@users.noreply.github.com&gt; ([`39939d4`](https://github.com/alandtse/tesla/commit/39939d452d31552662310284e175704711433715))

### Feature

- feat: add car windows binary_sensors (#629)

- [Add] extra attributes for windows

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

- Update test_binary_sensor.py

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

- Update car.py

- Update custom_components/tesla_custom/binary_sensor.py

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

- Update custom_components/tesla_custom/binary_sensor.py

- Update tests/mock_data/car.py

- Update tests/test_binary_sensor.py

---

Co-authored-by: pre-commit-ci[bot] &lt;66853113+pre-commit-ci[bot]@users.noreply.github.com&gt;
Co-authored-by: Alan Tse &lt;alandtse@users.noreply.github.com&gt; ([`fdefa52`](https://github.com/alandtse/tesla/commit/fdefa52ff9a520848a50900b3b3d0c44d079e643))

### Fix

- fix: update battery remaining sensor to ENERGY_STORAGE (#632)

- Update battery remaining sensor to ENERGY_STORAGE

- Update battery_remaining to ENERGY_STORAGE device class

- Bump homeassistant version for ENERGY_STORAGE

- Update pyproject.toml

- Update manifest.json include homeassistant dependency

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

- Update manifest.json requirements &#34;homeassistant&gt;=2023.4.0&#34;

- Update pyproject.toml version 3.13.1

- Update manifest.json version 3.13.1

- Update manifest.json

- Update pyproject.toml

- Update hacs.json to &#34;homeassistant&#34;: &#34;2023.4.0&#34;,

- build: update deps

- test: fix native_value for battery update time

---

Co-authored-by: pre-commit-ci[bot] &lt;66853113+pre-commit-ci[bot]@users.noreply.github.com&gt;
Co-authored-by: Alan D. Tse &lt;alandtse@gmail.com&gt;
Co-authored-by: Alan Tse &lt;alandtse@users.noreply.github.com&gt; ([`ff960f0`](https://github.com/alandtse/tesla/commit/ff960f0fa26f784c06f1f9da095a34b357a00509))

- fix: fix variable heated steering for older cars (#638) ([`db1d6b8`](https://github.com/alandtse/tesla/commit/db1d6b8e71a17e3d2a2ad54109b9aa2409ba8a37))

### Unknown

- Merge pull request #640 from alandtse/dev

chore: release 2023-06-16 ([`708a7e6`](https://github.com/alandtse/tesla/commit/708a7e6c380f726b7d72d36bbadc0eba70d30576))

## v3.13.0 (2023-06-13)

### Build

- build: pre-commit autoupdate

updates:

- [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)
- [github.com/asottile/pyupgrade: v3.4.0 → v3.6.0](https://github.com/asottile/pyupgrade/compare/v3.4.0...v3.6.0) ([`b45d4c9`](https://github.com/alandtse/tesla/commit/b45d4c9c9df954626f63bcd354efcc0506ae8f1d))

* build: pre-commit autoupdate

updates:

- [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)
- [github.com/PyCQA/prospector: 1.10.1 → 1.10.2](https://github.com/PyCQA/prospector/compare/1.10.1...1.10.2)
- [github.com/floatingpurr/sync_with_poetry: 0.4.0 → 1.0.0](https://github.com/floatingpurr/sync_with_poetry/compare/0.4.0...1.0.0) ([`f968888`](https://github.com/alandtse/tesla/commit/f9688888c5713f9426d07ad3db0f4b79df76b860))

### Feature

- feat: add heated steering wheel select (#628)

- add heated steering wheel select

- cleaned up tests

- bump teslajsonpy

- bump teslajsonpy in poetry ([`96cbad6`](https://github.com/alandtse/tesla/commit/96cbad6ccd6058a550397796ccdba97c286db152))

### Fix

- fix: use async_write vs async_update (#626)

closes #606 ([`78b0641`](https://github.com/alandtse/tesla/commit/78b0641587940ee40a6a6a4414e3fba43c83631b))

### Style

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`cbe5934`](https://github.com/alandtse/tesla/commit/cbe59343b91d5e1b5be345fc8a187ce88bb12509))

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`7fa2863`](https://github.com/alandtse/tesla/commit/7fa2863b461b19d9d8f6b6069e2b97bb43ff138b))

### Unknown

- Merge pull request #631 from alandtse/dev

chore: 2023-06-13 release ([`24760f6`](https://github.com/alandtse/tesla/commit/24760f6f29d75b6a591585a95902159b94d80f26))

- Merge pull request #630 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`66850bb`](https://github.com/alandtse/tesla/commit/66850bb92faabb8dc7a1ebe06c8ccbfc0c5b19de))

- Merge pull request #620 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`a69a53d`](https://github.com/alandtse/tesla/commit/a69a53dc73844f12eb157989f107b4b2acb67a9c))

## v3.12.3 (2023-06-01)

### Build

- build: pre-commit autoupdate

updates:

- [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)
- [github.com/PyCQA/prospector: 1.10.0 → 1.10.1](https://github.com/PyCQA/prospector/compare/1.10.0...1.10.1) ([`856afb3`](https://github.com/alandtse/tesla/commit/856afb370b0e64cc9f540b9b575e202a6b550beb))

* build: Update container (#612) ([`5609d0d`](https://github.com/alandtse/tesla/commit/5609d0d327188ced206765cb5141b6b63583c46a))

* build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: 3.2.1 → 3.2.2](https://github.com/commitizen-tools/commitizen/compare/3.2.1...3.2.2)
- [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)
- [github.com/PyCQA/prospector: v1.9.0 → 1.10.0](https://github.com/PyCQA/prospector/compare/v1.9.0...1.10.0) ([`27cc2a6`](https://github.com/alandtse/tesla/commit/27cc2a6b23801861277342c666b8fb6ff8b4dc07))

* build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: 3.2.0 → 3.2.1](https://github.com/commitizen-tools/commitizen/compare/3.2.0...3.2.1)
- [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)
- [github.com/asottile/pyupgrade: v3.3.2 → v3.4.0](https://github.com/asottile/pyupgrade/compare/v3.3.2...v3.4.0) ([`a8dd631`](https://github.com/alandtse/tesla/commit/a8dd6310745815e852cce35108ec688cb4cff52e))

### Fix

- fix: ensure update_vehicles coordinator always polls (#622)

closes #621
closes #613 ([`544e862`](https://github.com/alandtse/tesla/commit/544e862c2057088a8426e9d6a1a1ec9dc3a94863))

- fix: debounce mqtt updates (#608) ([`ac31eca`](https://github.com/alandtse/tesla/commit/ac31eca927e6f8f8537b1fd1c154a7be267d3b76))

### Style

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`d38e096`](https://github.com/alandtse/tesla/commit/d38e09665d8c49bc398169f626c3b406213e1a13))

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`e02d398`](https://github.com/alandtse/tesla/commit/e02d398ef89b44d01aed68e8946d4a20a4a5fb75))

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`2bd50db`](https://github.com/alandtse/tesla/commit/2bd50db9a00a62ceabbb26bfaf9d83953142c950))

### Unknown

- Merge pull request #623 from alandtse/dev

chore: release 2023-05-31 ([`fc23631`](https://github.com/alandtse/tesla/commit/fc236317ebbad39925a5e00b60f860353a2c1cd3))

- Merge pull request #615 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`21a2f45`](https://github.com/alandtse/tesla/commit/21a2f45944e5a3b860b6ea1bfc1250db819de89d))

- Merge pull request #610 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`b1b1a41`](https://github.com/alandtse/tesla/commit/b1b1a418cf6d50aa143e395b91c9d2228ee3182d))

- Merge pull request #603 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`60e692b`](https://github.com/alandtse/tesla/commit/60e692b7ce22a3c285846d17f20cd02976cd2d0b))

## v3.12.2 (2023-05-06)

### Build

- build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: 3.0.1 → 3.2.0](https://github.com/commitizen-tools/commitizen/compare/3.0.1...3.2.0)
- [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)
- [github.com/asottile/pyupgrade: v3.3.1 → v3.3.2](https://github.com/asottile/pyupgrade/compare/v3.3.1...v3.3.2) ([`d43244d`](https://github.com/alandtse/tesla/commit/d43244d6a523e5fe4415219e1160f44eed5040b9))

### Fix

- fix: Update arrival with earlier charge complete and arrival times (#575)

closes #565 ([`92da756`](https://github.com/alandtse/tesla/commit/92da7566d8ef21378cf143de84865e6ca3938c4c))

### Style

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`7a1df4a`](https://github.com/alandtse/tesla/commit/7a1df4a48ea57eb287a2a7f6d3049d6fbd05ba13))

### Unknown

- Merge pull request #599 from alandtse/dev

chore: release 2023-05-06 ([`dc279a8`](https://github.com/alandtse/tesla/commit/dc279a8b4347da452f59ff5521a62be83edbd1f7))

- Merge pull request #592 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`9424627`](https://github.com/alandtse/tesla/commit/942462769b4e2fc896275e8bef6d2e31518c7728))

## v3.12.1 (2023-04-28)

### Build

- build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: v2.42.1 → 3.0.1](https://github.com/commitizen-tools/commitizen/compare/v2.42.1...3.0.1)
- [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)
- [github.com/pre-commit/mirrors-prettier: v3.0.0-alpha.6 → v3.0.0-alpha.9-for-vscode](https://github.com/pre-commit/mirrors-prettier/compare/v3.0.0-alpha.6...v3.0.0-alpha.9-for-vscode) ([`75c3117`](https://github.com/alandtse/tesla/commit/75c311769840dd274d23f760501be2c035f5934f))

### Chore

- chore: release 2023-04-27 ([`6509424`](https://github.com/alandtse/tesla/commit/650942429f7a56df8e87465e7cbf149a9b5db214))

### Fix

- fix: fix multiple cars for TeslaMate (#582)

closes #581 ([`9e9b949`](https://github.com/alandtse/tesla/commit/9e9b949709acdfc79517b4b0d9c245134ed42825))

- fix: bump teslajsonpy to fix climate_state error (#580) ([`e638177`](https://github.com/alandtse/tesla/commit/e638177a8e3eac52563e6cfd99633e4a75dd62a2))

### Style

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`68aa2ee`](https://github.com/alandtse/tesla/commit/68aa2ee908ef9fe62ea3fc881e154bac53d8b4a0))

### Unknown

- Merge pull request #571 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`b106d57`](https://github.com/alandtse/tesla/commit/b106d570ed6893fbb4e1208fb8c79b640ef6560e))

## v3.12.0 (2023-04-21)

### Build

- build: pre-commit autoupdate

updates:

- [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0) ([`c352889`](https://github.com/alandtse/tesla/commit/c3528895e6019263c65a48f68c8867b5b403de42))

### Feature

- feat: add more updates to TeslaMate (#572)

closes #573 ([`970759c`](https://github.com/alandtse/tesla/commit/970759c2219d3d7c24b3de66f80c8c888e1e56ee))

- feat: Add Shift State Sensor (#569)

closes #476 ([`72ac435`](https://github.com/alandtse/tesla/commit/72ac43541a96c988a103f7935118d8049a050504))

- feat: Add Car Data Update Time Sensor (#568) ([`437212b`](https://github.com/alandtse/tesla/commit/437212bb9deb3de391b6114b8fd10eac00e9b8ed))

- feat: Allow syncing with TeslaMate via MQTT (#564)

- Initial comit of TeslaMate connection

- More productionising of code.

- Update readme

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

- fix pre-commit issuesl

- Fix Tests.

- Fix manifest file for hassfest check

---

Co-authored-by: pre-commit-ci[bot] &lt;66853113+pre-commit-ci[bot]@users.noreply.github.com&gt; ([`36713fb`](https://github.com/alandtse/tesla/commit/36713fb8ad88f3182a56acab17a40a0575fb741f))

### Style

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`cdbeb77`](https://github.com/alandtse/tesla/commit/cdbeb77594c0ddaf59449eab360cc1df45cbac95))

### Unknown

- Merge pull request #577 from alandtse/dev

chore: release 2023-04-21 ([`4a32c69`](https://github.com/alandtse/tesla/commit/4a32c698314e1c0c4c57af0be4cc3441f4fbfaf1))

- Merge pull request #563 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`b90a793`](https://github.com/alandtse/tesla/commit/b90a7937d55b45b01d8d6496e8bd50229f7c636e))

## v3.11.0 (2023-03-26)

### Feature

- feat: split coordinator to avoid updating disabled cars and energy sites (#552) ([`41dfbcc`](https://github.com/alandtse/tesla/commit/41dfbccd07c1bf9b4300c8add77e9ae91c2a4820))

### Fix

- fix: use Home Assistant ssl context to avoid I/O (#550)

- Use Home Assistant ssl context

Creating an ssl context does I/O in the event loop
try to use the default on if its available to avoid
this.

- fix: git add ([`7386d43`](https://github.com/alandtse/tesla/commit/7386d430da675dd35c5d0bd131ca402fa92be4b2))

- fix: use async_create_background_task to close the httpx client (#551)

- Use async_create_background_task to close the httpx client

https://docs.python.org/3/library/asyncio-task.html#creating-tasks
&gt; Important Save a reference to the result of this function, to avoid a task disappearing mid-execution. The event loop only keeps weak references to tasks. A task that isn’t referenced elsewhere may get garbage collected at any time, even before it’s done. For reliable “fire-and-forget” background tasks, gather them in a collection:

- name is required ([`de0d838`](https://github.com/alandtse/tesla/commit/de0d838c5d8fc098906fc2ab9427d820b2a4e4ed))

### Unknown

- Merge pull request #554 from alandtse/dev

chore: release 2023-03-26 ([`648fe39`](https://github.com/alandtse/tesla/commit/648fe39fb13ff4fedd7ed696d068c8a436b9acce))

## v3.10.4 (2023-03-24)

### Build

- build: update bandit tests ([`c51ee7f`](https://github.com/alandtse/tesla/commit/c51ee7fdd5fe3860e37f425af4f2dd41f2cb2b40))

- build: update deps ([`671f60b`](https://github.com/alandtse/tesla/commit/671f60b823b14e00e16ec2695274bc8b8d35640e))

### Ci

- ci: add todo ([`d8896b0`](https://github.com/alandtse/tesla/commit/d8896b07f84ef2c78515778397aa5231bd85bf97))

### Fix

- fix: fix sharing of addresses and media (#545)

- fix: sharing of addresses and media
  bump teslajsonpy to v3.7.5

- chore: correct the version specification

- chore: bump teslajsonpy in manfist.json as well

- chore: poetry update teslajsonpy@3.7.5 ([`0cc8319`](https://github.com/alandtse/tesla/commit/0cc8319db47cbe0427cf71347e710da53e01fa59))

### Test

- test: skip test_distance_to_arrival if erroneous

test_distance_to_arrival runs fine indivdiaully but breaks in a group.
This is likely a transient async problem. ([`c9eabce`](https://github.com/alandtse/tesla/commit/c9eabcee3ba820d9599c26bdb57b174f781a39d7))

- test: change tests to numeric value equality ([`63c7c12`](https://github.com/alandtse/tesla/commit/63c7c12850d86fac54336538ec3d104e35c18611))

### Unknown

- Merge pull request #546 from alandtse/dev

chore: release 2023-03-23 ([`bf60f4b`](https://github.com/alandtse/tesla/commit/bf60f4b0138c44ec89f68a8cf9541d52dae73368))

- Merge pull request #536 from alandtse/test_ci

ci: fix broken tests ([`e017a6d`](https://github.com/alandtse/tesla/commit/e017a6d049a03d2df5afafa735ac10dd9b0c83f8))

- Merge branch &#39;dev&#39; into test_ci ([`7c9bdf6`](https://github.com/alandtse/tesla/commit/7c9bdf66fb8ba4637a43d0fb869e92b6f053fcbe))

## v3.10.3 (2023-03-14)

### Build

- build: pre-commit autoupdate (#533)

- build: pre-commit autoupdate

updates:

- [github.com/PyCQA/bandit: 1.7.4 → 1.7.5](https://github.com/PyCQA/bandit/compare/1.7.4...1.7.5)

* style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci

---

Co-authored-by: pre-commit-ci[bot] &lt;66853113+pre-commit-ci[bot]@users.noreply.github.com&gt; ([`8aaebde`](https://github.com/alandtse/tesla/commit/8aaebde955d53035384a525aae071dda24df2041))

- build: pre-commit autoupdate

updates:

- [github.com/pre-commit/mirrors-prettier: v3.0.0-alpha.4 → v3.0.0-alpha.6](https://github.com/pre-commit/mirrors-prettier/compare/v3.0.0-alpha.4...v3.0.0-alpha.6) ([`e2611d0`](https://github.com/alandtse/tesla/commit/e2611d0eed0185f0ddb488f97560f76c68b02505))

### Fix

- fix: memoize unique id (#534)

- Memorize unique id

- Slugify once instead of every state write ([`05f1689`](https://github.com/alandtse/tesla/commit/05f16899774afb80870ee34f83127ee462904db8))

### Unknown

- Merge pull request #535 from alandtse/dev

chore: release 2023-03-13 ([`47fd15a`](https://github.com/alandtse/tesla/commit/47fd15a4027461b453ff19b34dfddf6d8a55afd5))

- Merge branch &#39;dev&#39; into main ([`ca3907f`](https://github.com/alandtse/tesla/commit/ca3907f64e68e9f3241ca2447a7a1404e0247c62))

- Merge pull request #527 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`460fdec`](https://github.com/alandtse/tesla/commit/460fdece0b39846904b7a47490c16d1e1da995f2))

- Merge branch &#39;dev&#39; into main ([`03f32e3`](https://github.com/alandtse/tesla/commit/03f32e3a5fb3ea2af5062f497a2423c38881c78d))

## v3.10.2 (2023-03-05)

### Fix

- fix: bump teslajsonpy to 3.7.4

closes #525 ([`967ce66`](https://github.com/alandtse/tesla/commit/967ce66394de661aeed1b27b8d611d55ea7f238a))

### Unknown

- Merge pull request #519 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`14d4302`](https://github.com/alandtse/tesla/commit/14d43026fa59b9fd83aa33ad23c8831eae9a59e6))

- Merge branch &#39;dev&#39; into pre-commit-ci-update-config ([`a6bf993`](https://github.com/alandtse/tesla/commit/a6bf993836448b24fecfd48a5ecd89c40d79d574))

## v3.10.1 (2023-03-05)

### Build

- build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: v2.42.0 → v2.42.1](https://github.com/commitizen-tools/commitizen/compare/v2.42.0...v2.42.1) ([`fde7d78`](https://github.com/alandtse/tesla/commit/fde7d7879f5ea2c6083218a1f9c8b7c426bd4640))

### Fix

- fix: bump teslajsonpy to 3.7.3

Replaces json with orjson.

closes #524 ([`da8afd7`](https://github.com/alandtse/tesla/commit/da8afd7587165c07d0bdad2c2568a33d3128ee8e))

### Style

- style: sort manifest.json ([`6f1cc42`](https://github.com/alandtse/tesla/commit/6f1cc42f0abecd86ce95264fb79d52a8f6ebd279))

## v3.10.0 (2023-02-22)

### Build

- build: pre-commit autoupdate

updates:

- [github.com/PyCQA/prospector: v1.8.4 → v1.9.0](https://github.com/PyCQA/prospector/compare/v1.8.4...v1.9.0) ([`a21456c`](https://github.com/alandtse/tesla/commit/a21456c67da4ed13bedb98333ed36b4d9cb1b4d0))

* build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: v2.40.0 → v2.42.0](https://github.com/commitizen-tools/commitizen/compare/v2.40.0...v2.42.0) ([`c5407c5`](https://github.com/alandtse/tesla/commit/c5407c5248492bd8e4a95daae22a2215c48c08e3))

### Feature

- feat: add min_to_full_charge attribute (#505) ([`316ad90`](https://github.com/alandtse/tesla/commit/316ad90ce9cca78f5d7be6f0ce77432446639aef))

### Unknown

- Merge pull request #516 from alandtse/dev

2023-02-21 ([`8ab3339`](https://github.com/alandtse/tesla/commit/8ab33391578c70c3414d1629068d16e5f6b84775))

- Merge pull request #515 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`63f9375`](https://github.com/alandtse/tesla/commit/63f9375c782bad64e5322d64715b395aef80bbdb))

- Merge pull request #511 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`5a21bc2`](https://github.com/alandtse/tesla/commit/5a21bc264e2ed7c517383e37d3fa327e83e68c78))

- Merge pull request #502 from alandtse/main

Sync with main ([`cc9686d`](https://github.com/alandtse/tesla/commit/cc9686df498c55b8041cf27207b033a32b12d27f))

## v3.9.2 (2023-02-01)

### Build

- build: exclude changelog from prettier ([`74e161a`](https://github.com/alandtse/tesla/commit/74e161a73a609a1f9d68257a3435f221a1544f4a))

- build: pre-commit autoupdate

updates:

- [github.com/commitizen-tools/commitizen: v2.38.0 → v2.40.0](https://github.com/commitizen-tools/commitizen/compare/v2.38.0...v2.40.0)
- [github.com/psf/black: 23.1a1 → 22.12.0](https://github.com/psf/black/compare/23.1a1...22.12.0)
- [github.com/PyCQA/prospector: v1.8.3 → v1.8.4](https://github.com/PyCQA/prospector/compare/v1.8.3...v1.8.4)
- [github.com/PyCQA/isort: 5.11.4 → 5.12.0](https://github.com/PyCQA/isort/compare/5.11.4...5.12.0) ([`9f82417`](https://github.com/alandtse/tesla/commit/9f8241781262e1c778c62eeaec07a1e99e7dc946))

### Ci

- ci: bump actions/checkout ([`ff469ce`](https://github.com/alandtse/tesla/commit/ff469ce244ea8cca1c2e58e72ebe0f140de7162f))

### Documentation

- docs: Updated readme installation instructions (#495) ([`8d966c4`](https://github.com/alandtse/tesla/commit/8d966c49cb7d4f8d65d0d4ad6e1e486175fed61e))

### Fix

- fix: Bump teslajsonpy to fix charge current (#484)

closes #479 ([`fa4bb7e`](https://github.com/alandtse/tesla/commit/fa4bb7ed25f72d316dcc50b70342401b5bf92a5b))

- fix: switch to async_forward_entry_setups

closes #499 ([`3d62c3c`](https://github.com/alandtse/tesla/commit/3d62c3cfbd27978e60e62f7a0a37a5ed671fbdb8))

### Style

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`651d996`](https://github.com/alandtse/tesla/commit/651d996a435e47e2d8c2cda52a2e7af1f5ed6912))

### Unknown

- Merge pull request #501 from alandtse/dev

ci: bump actions/checkout ([`a715717`](https://github.com/alandtse/tesla/commit/a7157178ea301bb1af5c4c80bdc275ab307709ed))

- Merge pull request #500 from alandtse/dev

2023-01-31 ([`6bcee83`](https://github.com/alandtse/tesla/commit/6bcee83e13a20b19b796b740f257c387a8d4c52e))

- Merge pull request #471 from alandtse/pre-commit-ci-update-config

build: pre-commit autoupdate ([`ee84795`](https://github.com/alandtse/tesla/commit/ee84795a213012d54457dc77aeb030527a74c189))

- Merge branch &#39;dev&#39; into pre-commit-ci-update-config ([`e63a539`](https://github.com/alandtse/tesla/commit/e63a539cc325443911cb42ab67ddba64dfbb70ac))

## v3.9.1 (2022-12-30)

### Build

- build: update dev dependency syntax ([`977654b`](https://github.com/alandtse/tesla/commit/977654bd7ef8ff6dffaa17a13859daa9488e7b96))

- build: exclude vscode/launch.json ([`cc20a97`](https://github.com/alandtse/tesla/commit/cc20a97bdb90a3db31147a43ad71a94a931fc937))

### Ci

- ci: update precommit ([`852e4d6`](https://github.com/alandtse/tesla/commit/852e4d66e46d9db5fe351b6c1db34a01b5314847))

- ci: add support for pre-commit.ci ([`7df63ff`](https://github.com/alandtse/tesla/commit/7df63ffd209e22e126945f3a47c75b682bb8c4ad))

### Fix

- fix: handle None option_codes

closes #466 ([`47bb178`](https://github.com/alandtse/tesla/commit/47bb178ae779b281ad83fca5bccd2b84ea40e08f))

### Style

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`edd0e80`](https://github.com/alandtse/tesla/commit/edd0e8000976724645c1d106b5d1d87bbaae1da5))

- style: fix prospector errors ([`e6e56f8`](https://github.com/alandtse/tesla/commit/e6e56f83f92163b8847cd247b11225a2063eef92))

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`2a34979`](https://github.com/alandtse/tesla/commit/2a34979fc6d3e6fae5dc3d78c6076a115354b934))

- style: auto fixes from pre-commit.com hooks

for more information, see https://pre-commit.ci ([`4b79396`](https://github.com/alandtse/tesla/commit/4b7939669251895c87cf7f222167efaa009182ee))

### Unknown

- Merge pull request #469 from alandtse/dev

2022-12-29 ([`8afd0c9`](https://github.com/alandtse/tesla/commit/8afd0c9daed90407492cac49e09ac7b8b2467e5f))

- Merge pull request #467 from alandtse/teslajsonpy3.7.1 ([`c1fe52c`](https://github.com/alandtse/tesla/commit/c1fe52c72e75ac1011a3113186c635eb0fd131fa))

## v3.9.0 (2022-12-29)

### Feature

- feat: add emission test button (#454)

closes #438 ([`8d40beb`](https://github.com/alandtse/tesla/commit/8d40beb45790e06146991488934c24e1c3f4322d))

- feat: add scheduled departure and charge timestamp attributes (#458) ([`b979846`](https://github.com/alandtse/tesla/commit/b97984605f467776b1caa871f72f9534fd4496a8))

- feat: Add dynamic debug logging (#448) ([`d310ae5`](https://github.com/alandtse/tesla/commit/d310ae506afafd4a16e9a0bb07405b929625ebda))

### Fix

- fix: make destination location unknown after arrival (#460)

closes #455 ([`5781cea`](https://github.com/alandtse/tesla/commit/5781cea8515e451a4a2c8dbf0aa7e973094a7feb))

- fix: account for time passing between updates (#419) ([`02751a2`](https://github.com/alandtse/tesla/commit/02751a203a1d0dcfb6efd570cfb5246773f03e16))

- fix: replace deprecated is_metric (#343)

closes #326 ([`87005fc`](https://github.com/alandtse/tesla/commit/87005fc353102d46fcd95a20a173a007d6d41b00))

### Unknown

- Merge pull request #462 from alandtse/dev

2022-12-26 ([`5646d01`](https://github.com/alandtse/tesla/commit/5646d01d594426f3378ef0b07be724a8806d4485))

## v3.8.1 (2022-12-21)

### Fix

- fix: handle battery range attributes NoneType (#453)

closes #450 ([`90f7d0d`](https://github.com/alandtse/tesla/commit/90f7d0ddb9140dae92c446dd7274a7e27abd4f3d))

### Unknown

- Merge pull request #456 from alandtse/dev

fix: handle battery range attributes NoneType (#453) ([`30384c9`](https://github.com/alandtse/tesla/commit/30384c929e4747537d2b3b8851af18527e58bf01))

## v3.8.0 (2022-12-21)

### Feature

- feat: add user present and User ID (#446)

closes #221 ([`865c637`](https://github.com/alandtse/tesla/commit/865c6377649f1c0bf94f39d98a59e4e5d0891e31))

- feat: add estimated battery range attributes (#443)

closes #412 ([`7584fdc`](https://github.com/alandtse/tesla/commit/7584fdcdc64d1c752dc34bdafd08c47ded6526df))

- feat: add scheduled departure and charging (#441)

closes #164 ([`f555131`](https://github.com/alandtse/tesla/commit/f55513162e5cd03633156fa59073759ef7d7052b))

### Fix

- fix: remove state class from timestamp sensors (#440) ([`43f7169`](https://github.com/alandtse/tesla/commit/43f7169b6aa43c5fe08865e75b8172cbe231d5df))

### Unknown

- Merge pull request #449 from alandtse/dev

2022-12-20 ([`a1ad476`](https://github.com/alandtse/tesla/commit/a1ad476771048b2badbbd11b1f0e664d57bab1b1))

## v3.7.1 (2022-12-18)

### Documentation

- docs: update readme with new features ([`8a518c9`](https://github.com/alandtse/tesla/commit/8a518c93b05f31f2a0c9817d624a4b13dac944fc))

### Fix

- fix: fix seat map for auto climate command (#435)

closes #433 ([`c96e5b0`](https://github.com/alandtse/tesla/commit/c96e5b0ac2794f7569846af5cf78f6f8f6545e3d))

### Unknown

- Merge pull request #439 from alandtse/dev

2022-12-17 ([`4109059`](https://github.com/alandtse/tesla/commit/41090595fd8d4a6fee53c0795d188a9da6733c25))

## v3.7.0 (2022-12-11)

### Feature

- feat: add destination location entities (#423)

closes #384 ([`a4ec318`](https://github.com/alandtse/tesla/commit/a4ec318eb44838c6a6ad0164369e98aa563aff32))

### Unknown

- Merge pull request #424 from alandtse/dev

feat: add destination location entities (#423) ([`ae6f560`](https://github.com/alandtse/tesla/commit/ae6f5604a362ac14340bbd1dfa9c5e6e1c6454a8))

## v3.6.1 (2022-12-11)

### Fix

- fix: use old pressure consts for ha &lt; 2022.11 (#418)

closes #417 ([`ad9c41c`](https://github.com/alandtse/tesla/commit/ad9c41c71ea93db9294ff4203b61f1e6f6a4b697))

### Unknown

- Merge pull request #420 from alandtse/dev

fix: use old pressure consts for ha &lt; 2022.11 (#418) ([`47dc540`](https://github.com/alandtse/tesla/commit/47dc5408e2baad6ac62026fe03f46d3f843834db))

## v3.6.0 (2022-12-09)

### Build

- build(deps): bump certifi from 2022.9.24 to 2022.12.7 (#415)

Bumps [certifi](https://github.com/certifi/python-certifi) from 2022.9.24 to 2022.12.7.

- [Release notes](https://github.com/certifi/python-certifi/releases)
- [Commits](https://github.com/certifi/python-certifi/compare/2022.09.24...2022.12.07)

---

updated-dependencies:

- dependency-name: certifi
  dependency-type: indirect
  ...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`e2e1d55`](https://github.com/alandtse/tesla/commit/e2e1d55da2294e1fc08d72c308d86e17defb2472))

### Feature

- feat: add Auto seat heater option (#404)

closes #302 ([`7e02a42`](https://github.com/alandtse/tesla/commit/7e02a423cf59c8d70c58cc623da59389044da8b4))

- feat: add valet mode switch (#405)

closes #355 ([`01116d1`](https://github.com/alandtse/tesla/commit/01116d1ff5b5ea66bba6d73ad4089a2c38f03ffe))

### Fix

- fix: always show charge energy for current and last session (#414)

Fixes #295 and #413 ([`be6c1f0`](https://github.com/alandtse/tesla/commit/be6c1f09e51cb4954a67573bed04ea4151a488b0))

- fix: fix arrows for window cover (#407)

closes #394 ([`108567c`](https://github.com/alandtse/tesla/commit/108567cb1b53824665ebf2ae890efd1c4f0812e5))

- fix: turn climate on when turning seat heater on (#406)

closes #392 ([`78e90e4`](https://github.com/alandtse/tesla/commit/78e90e47f12a6f7288fe2d3b55e56984c2560628))

### Unknown

- Merge pull request #416 from alandtse/dev

2022-12-08 ([`79af2f6`](https://github.com/alandtse/tesla/commit/79af2f664f9bc713a9c00a67baecedcd7231af2d))

## v3.5.2 (2022-12-03)

### Fix

- fix: don&#39;t round when tpms is unavailable (#398)

Closes #397 ([`f5a3b0d`](https://github.com/alandtse/tesla/commit/f5a3b0d23071893d913895659efe3a4ced00bf79))

### Unknown

- Merge pull request #400 from alandtse/dev

fix: don&#39;t round when tpms is unavailable (#398) ([`3d7fce6`](https://github.com/alandtse/tesla/commit/3d7fce6c0dec7d7bf39fb17a9bc96756b7111dff))

## v3.5.1 (2022-12-03)

### Fix

- fix: set default pressure to PSI (#391)

Due to a HA limitation, this will only impact new sensors. Existing sensors will need to be manually set.

closes #388 ([`e4adef7`](https://github.com/alandtse/tesla/commit/e4adef75dbfef9e03b5f8b73b0621181acf3fab1))

### Unknown

- Merge pull request #393 from alandtse/dev

fix: set default pressure to PSI (#391) ([`886899c`](https://github.com/alandtse/tesla/commit/886899c10856968b6ce5956d6e75c741eedf557e))

## v3.5.0 (2022-12-01)

### Feature

- feat: add remote start button (#385)

closes #367 ([`42b7117`](https://github.com/alandtse/tesla/commit/42b7117fe16209ccf23070b22b58e576cd2709a8))

### Unknown

- Merge pull request #386 from alandtse/dev

feat: add remote start button (#385) ([`7217e5a`](https://github.com/alandtse/tesla/commit/7217e5aae5ac7ef2fd1477bc73a880ce622c4395))

## v3.4.0 (2022-11-30)

### Feature

- feat: add tpms pressure sensors (#376)

closes #160 ([`b2cbe95`](https://github.com/alandtse/tesla/commit/b2cbe9575ab6e2c4a780ec15f9ebc57f45235fa5))

- feat: add doors binary sensor (#377)

closes #310 ([`8b77e3c`](https://github.com/alandtse/tesla/commit/8b77e3c7b1aff6aa6761d8f86592b891099137d4))

### Unknown

- Merge pull request #381 from alandtse/dev

2022-11-29 ([`957c361`](https://github.com/alandtse/tesla/commit/957c361984558cb8a877cdd29687ca2c2f180061))

## v3.3.2 (2022-11-29)

### Fix

- fix: use utc time zone for charge complete sensor

Looks like HA stores all times in UTC then converts that value to the user&#39;s timezone. So using utcnow() instead of now() fixes the timezone issue with this sensor.

closes #374 ([`f13c618`](https://github.com/alandtse/tesla/commit/f13c618efe2071945eb5846fc0ff3c3b645da0f8))

### Unknown

- Merge pull request #380 from alandtse/dev

fix: use utc time zone for charge complete sensor ([`ecb0160`](https://github.com/alandtse/tesla/commit/ecb01606162456ed664eba56a3cecd4091e325b0))

## v3.3.1 (2022-11-27)

### Fix

- fix: change timestamp calculation

While charging the timestamp would continuously update. Now the value
will only update if charging, the remaining time is greater than 0 and
the timestamp is more than a minute different. The timestamp will report
unavailable if charging_state is unknown or stopped. It will remember
the last value only if charging completed. ([`5f92774`](https://github.com/alandtse/tesla/commit/5f9277425df93fa9ece48e2d2d27eedd433c9abb))

### Style

- style: black ([`19be990`](https://github.com/alandtse/tesla/commit/19be9906d5533512a0335d2087c913583ad95e37))

### Test

- test: change state tests to use HA constants ([`d31c021`](https://github.com/alandtse/tesla/commit/d31c021561ce4e25912c7594dd1fc0d2dcfbbe86))

### Unknown

- Merge pull request #373 from alandtse/dev

2022-11-26 ([`88f6454`](https://github.com/alandtse/tesla/commit/88f6454f81a708fa2342266b58d1e500bbfd9fcd))

## v3.3.0 (2022-11-27)

### Feature

- feat: add time to full charge sensor (#349)

closes #348 ([`fbcf5fe`](https://github.com/alandtse/tesla/commit/fbcf5fe9b8345a13f9fed94dc65e9f2c93a62601))

- feat: show software update statuses in version info (#370) ([`fac9dd1`](https://github.com/alandtse/tesla/commit/fac9dd12c1baa6e3676fb30face39514200d1606))

### Fix

- fix: handle unresponsive cars/systems during setup

At setup, proceed with creation of entities even if Tesla entities are
not responsive. They wlil be picked up when they become available

closes #315
closes #324 ([`4d1270b`](https://github.com/alandtse/tesla/commit/4d1270b426cef4a00b8e84644aafdaa3a47407ca))

### Unknown

- Merge pull request #372 from alandtse/dev

2022-11-26 ([`26bfdbe`](https://github.com/alandtse/tesla/commit/26bfdbefdec44aeceaaa0df9e9c8c68121a6a4f2))

## v3.2.0 (2022-11-21)

### Feature

- feat: add binary_sensor.&lt;car&gt;\_asleep (#361)

closes #360 ([`43deefb`](https://github.com/alandtse/tesla/commit/43deefb9a0b306c0d867413bfbc6ecb67b15fd50))

### Fix

- fix: persist entities when reloaded while car is asleep (#365)

Change behavior for auto creation of entities to create but disable until detected.

closes #293 ([`f0fc6e4`](https://github.com/alandtse/tesla/commit/f0fc6e49895547a3861a3592dcde7269b05b9305))

- fix: fix usable_battery_level to match app (#362) ([`c9e4abb`](https://github.com/alandtse/tesla/commit/c9e4abbacba8df7571943f3008eaa1df410c9b28))

- fix: update car-asleep binary sensor icon (#364) ([`30f319c`](https://github.com/alandtse/tesla/commit/30f319c893012c154faea0d5d6c3ef88efdb7ccd))

### Test

- test: Use hass built-in unit conversions for distance (#363) ([`00eeaa5`](https://github.com/alandtse/tesla/commit/00eeaa5651791dcc42d9ee054f43c1ff2329f099))

### Unknown

- Merge pull request #366 from alandtse/dev

2022-11-21 ([`97c5533`](https://github.com/alandtse/tesla/commit/97c55331bd93b9233f9b9a906bb11110f3965595))

## v3.1.0 (2022-11-14)

### Feature

- feat: Add window cover (#318)

closes #234 ([`bea6824`](https://github.com/alandtse/tesla/commit/bea68240d68e727e5cda803fe9df2b711ba0c6ff))

- feat: Add charge port latch lock

closes #323 ([`df7d06e`](https://github.com/alandtse/tesla/commit/df7d06ead2f7ddb499e9e254f645bd969886a86a))

### Fix

- fix: fix typo telsafi.com -&gt; teslafi.com (#314)

closes #319 ([`9c1514a`](https://github.com/alandtse/tesla/commit/9c1514a051a1f953ab91cd1463e03da350680eda))

### Unknown

- Merge pull request #347 from alandtse/dev

2022-11-14 ([`7c5a427`](https://github.com/alandtse/tesla/commit/7c5a4272b04d8704564fbf6825735ab0d8cd8e82))

## v3.0.2 (2022-10-27)

### Fix

- fix: add missing close_cover for frunks

closes #307 ([`3257775`](https://github.com/alandtse/tesla/commit/325777598d13b0e2ac3b817fb4996ab60e019b2f))

### Unknown

- Merge pull request #312 from alandtse/dev

fix: add missing close_cover for frunks ([`bf1c5be`](https://github.com/alandtse/tesla/commit/bf1c5be21731b4ceedbf46d455ac06151f4de920))

## v3.0.1 (2022-10-24)

### Ci

- ci: add linter for commits ([`d2e3f8c`](https://github.com/alandtse/tesla/commit/d2e3f8cb637e25c1323063b374bd6ebec32a10c5))

### Fix

- fix: add open feature for frunk ([`769858f`](https://github.com/alandtse/tesla/commit/769858f442a65ee0a5bd95ae7b6d797b02fc8088))

- fix: set sensor device class (#292)

closes #284 ([`658295f`](https://github.com/alandtse/tesla/commit/658295f785ae5348d73b1dc18f37ad14a1990f70))

- fix: use GPS coords from Tesla API (#289) ([`1bc6d7f`](https://github.com/alandtse/tesla/commit/1bc6d7fd64977844102e70a3a62fd553745a15ce))

- fix: use car distance units &amp; fix solar type

closes #284 ([`2617d71`](https://github.com/alandtse/tesla/commit/2617d71bbc8ff1bee247c599e11077617bf6eba5))

### Unknown

- Merge pull request #300 from alandtse/dev

2022-10-23 ([`1907eb5`](https://github.com/alandtse/tesla/commit/1907eb58241c1aa71b03afbf2c8bf629a2e9328b))

- Merge pull request #299 from shred86/add-frunk-close

fix: add open feature for frunk ([`97ad635`](https://github.com/alandtse/tesla/commit/97ad635d581eaa7ad659c1ce2b979f40760ac026))

- Merge pull request #291 from alandtse/revert-288-unit-reference

Revert &#34;Use car distance units &amp; remove solar type from model&#34; ([`38fa02b`](https://github.com/alandtse/tesla/commit/38fa02b9524253b431d8650c757d5f5d8ec0427d))

- Revert &#34;Use car distance units &amp; remove solar type from model&#34; ([`97539ea`](https://github.com/alandtse/tesla/commit/97539ea5f830f6cf47426617e8dbe8723c37abc6))

- Merge pull request #288 from shred86/unit-reference

Use car distance units &amp; remove solar type from model ([`6f0a4ae`](https://github.com/alandtse/tesla/commit/6f0a4aedfddc8566b4e513dda056539016a59df4))

- Use car distance units &amp; fix solar type ([`1da88e9`](https://github.com/alandtse/tesla/commit/1da88e9f3d525a23cbf525adf912f70d71d072b5))

## v3.0.0 (2022-10-22)

### Breaking

- feat!: rewrite to add support for energy sites (#250)

Added support for Tesla energy sites and updates to cars.

- Move car specific code out of `TeslaBaseEntity` to a newly created `TeslaCarEntity`.
- New `TeslaEnergyEntity` class which also inherits from `TeslaBaseEntity`.
- New `TeslaEnergyPowerSensor` class used for creating power sensors (solar, grid, load and battery).
- New `TeslaEnergyBattery` class for Powerwall battery percentage sensor.
- New `TeslaEnergyBatteryRemaining` class for Powerewall battery Watt hour remaining sensor.
- New `TeslaEnergyBackupReserve` class for Powerwall backup reserve percentage setting sensor.
- New `TeslaEnergyBatteryCharging` class for Powerwall battery charging binary sensor.
- New `TeslaEnergyGridStatus` class for Powerwall grid status binary sensor.
- New `TeslaEnergyGridCharging` class for Powerwall grid charging select.
- New `TeslaEnergyExportRule` class for Powerwall export rule select.
- New `TeslaEnergyOperationMode` class for Powerwall operation mode select.
- New `TeslaCarChargerPower` class for car charger power (kW).
- Updated properties and method calls to teslajsonpy to reflect the changes made to teslajsonpy.
- Added additional checks to only add entities for what a car actually has (seat heaters, heated steering wheel, HomeLink, etc.)
- Updated naming to align with [current](https://developers.home-assistant.io/docs/core/entity#entity-naming) Home Assistant convention.
- Changed unique IDs to use VIN + entity type for vehicles.
- Update class naming to `TeslaCar*` and `TeslaEnergy*` for all vehicle and energy site related classes respectively.
- Renamed `TeslaCarMileage` to `TeslaCarOdometer`.
- `TeslaCarParkingBrake` will indicate &#34;On&#34; when the car is on and in &#34;Park&#34; but also when the car is off (parking brake still engaged).
- Updated icons to better reflect entities purpose.
- Added a check to the car energy added sensor to report 0 unless the car is charging, then report the actual charge energy added. This is due to the Tesla API reporting a decreasing value over time when not charging causing issues with the HA sensor state class &#34;TOTAL_INCREASING&#34;.
- Removed extra state attributes that are already a separate entity (charge energy added, charge current request).
- Moved charger actual current, charger voltage and charger power extra state attributes from the charging rate to energy added entity.
- Updated `TeslaCarChargerConnection` device class to `PLUG`.
- Removed unused `helpers.py`.
- Cast vehicle ID and ID to a string in `TeslaCarOnline` extra state attributes to prevent HA from automatically formatting with commas.
- Check users HA unit system locale settings for determining to return miles vs kilometers.
- Vehicles will be forced to wake up the first time the integration is set up. For subsequent integration or HA restarts, vehicles will not be forced to wake up unless enabled in the configuration options (defaults to off).
- Added two new options, &#34;Include Vehicles&#34; and &#34;Include Energy Sites&#34; to the setup config flow. These will allow a user to include/exclude vehicles or energy sites. Defaults selected.
- Updated doc strings.
- Updated and added tests to cover changes.

- closes #79
- closes #93
- closes #101
- closes #173
- closes #204
- closes #222
- closes #226
- closes #271

BREAKING CHANGE: This is a rewrite. Multiple entitiy_ids were changed. It is recommended you remove and reinstall.
Changed trunk, frunk and charger door from lock to cover entities.
Created separate sensor (`TeslaCarChargerPower` class) for charger power.
Moved charger amps, charger volts and charger phases extra state attributes to the new charger power sensor.
Moved added range extra state attributes to the charger energy added sensor. ([`6a1f9c3`](https://github.com/alandtse/tesla/commit/6a1f9c3cb663ed5543a2e778bdbaf750699b1438))

### Build

- build: fix version in const.py ([`6226469`](https://github.com/alandtse/tesla/commit/622646932649e79900b984fddfd1875790a6eb58))

### Documentation

- docs: remove duplicate info from README (#278) ([`616d3a5`](https://github.com/alandtse/tesla/commit/616d3a5761432a06589bbad3f9bbe886f3621384))

### Unknown

- Merge pull request #281 from alandtse/dev

2022-10-21 ([`2e7554a`](https://github.com/alandtse/tesla/commit/2e7554aa3bae2cd87c2991501f5cdb42ceaa78fe))

## v2.4.4 (2022-10-10)

### Documentation

- docs: Update Danish Translation (#269) ([`73829e3`](https://github.com/alandtse/tesla/commit/73829e37c1e1a21715a069f6fed512b927d4a446))

### Fix

- fix: fix keyerror `charge_to_max_range`

Bump teslajsonpy to 2.4.5

closes #275 ([`0aa02c1`](https://github.com/alandtse/tesla/commit/0aa02c141680400b6ac10d43f8c99a474e379008))

### Unknown

- Merge pull request #277 from alandtse/dev

2022-10-10 ([`4c6697a`](https://github.com/alandtse/tesla/commit/4c6697ae2595887533983e9435276e7ae9f908d0))

## v2.4.3 (2022-09-11)

### Fix

- fix: fix Chinese location offset (#263)

closes #233

Co-authored-by: Emniroll &lt;emniroll@outlook.com&gt; ([`3feba57`](https://github.com/alandtse/tesla/commit/3feba57298de38a8fc3601e8d3080b97344f0a91))

### Unknown

- Merge pull request #264 from alandtse/dev

fix: fix Chinese location offset (#263) ([`2da3c54`](https://github.com/alandtse/tesla/commit/2da3c54cf5b12120b34ff46e67e423f18567370f))

## v2.4.2 (2022-08-29)

### Fix

- fix: fix grid status issue (#258)

closes #257 ([`f889173`](https://github.com/alandtse/tesla/commit/f88917321369d0faaf280e1139967eebf6df8be5))

### Unknown

- Merge pull request #259 from alandtse/dev

fix: fix grid status issue (#258) ([`bbf6538`](https://github.com/alandtse/tesla/commit/bbf653890286759dda0f4c0affa3a78b77d78735))

## v2.4.1 (2022-08-27)

### Fix

- fix: bump teslajsonpy to fix solar naming (#249)

closes #254 ([`26658bd`](https://github.com/alandtse/tesla/commit/26658bd46d56d4c94cc5b99cfbcfa56a1671ee36))

### Unknown

- Merge pull request #255 from alandtse/dev

fix: bump teslajsonpy to fix solar naming (#249) ([`bcfbc1a`](https://github.com/alandtse/tesla/commit/bcfbc1a5e8fc7b8b973fcba76640a718c5fa6cf2))

## v2.4.0 (2022-08-13)

### Ci

- ci: disable push validation on main

This was redundant since all PRs must be validated. ([`dd0fc31`](https://github.com/alandtse/tesla/commit/dd0fc31b26dc5a57f512d8207399bc0eb2beec3e))

### Feature

- feat: add solar power, grid power, load power sensors

Adds grid and home (load) power sensors for energy sites (solar systems) ([`57d6095`](https://github.com/alandtse/tesla/commit/57d6095a2b6cc17e57317eef800261b4bb47bf8c))

### Unknown

- Merge pull request #245 from alandtse/dev

2022-08-13 ([`2c6983e`](https://github.com/alandtse/tesla/commit/2c6983e9db1a9dedb4d146b9defd7a6d7adf6ce8))

- Merge branch &#39;dev&#39; of github.com:alandtse/tesla into dev ([`d8fd050`](https://github.com/alandtse/tesla/commit/d8fd05020162e100cfba93fbaff3b9a39fbeaee4))

## v2.3.1 (2022-07-10)

### Build

- build: bump precommit deps ([`651bbb9`](https://github.com/alandtse/tesla/commit/651bbb9593e91715369c5aab8e7a370b8920f2c7))

### Documentation

- docs: Update HACS URL (#220) ([`d93f36f`](https://github.com/alandtse/tesla/commit/d93f36f052af6ac69795ceff4a7aea73246778d0))

- docs: fix changelog for 2.3.0 ([`43870ee`](https://github.com/alandtse/tesla/commit/43870ee8e1cf2391a1b59d07de20bc71f4202114))

### Fix

- fix: use json in post requests

Tesla recently tightened requirements to always use json for post
requests.

Thanks to @haoboji for the fix.

closes #231 ([`867475f`](https://github.com/alandtse/tesla/commit/867475f94dd341f58ea0692e289abe2c895654b5))

### Unknown

- Merge pull request #232 from alandtse/dev

2022-07-09 ([`bd24ef0`](https://github.com/alandtse/tesla/commit/bd24ef0ea85c3ffaf6aa9197c4058b02d09a602e))

## v2.3.0 (2022-05-29)

### Build

- build: remove iot_class key ([`55a2ce8`](https://github.com/alandtse/tesla/commit/55a2ce80161a32e6b25d10667fb224859459af80))

- build: remove domains key ([`9074476`](https://github.com/alandtse/tesla/commit/907447658099e522cb401c3bbdd18e9dcc061bba))

### Feature

- feat: Add support for async_remove_config_entry_device (#218) ([`562c1b0`](https://github.com/alandtse/tesla/commit/562c1b0ce01ced7adb0743a39178a7e9951c5e35))

### Fix

- fix: improve handling on 0 Watts power reads

Bumps teslajsonpy to 2.2.1 ([`bf94f3b`](https://github.com/alandtse/tesla/commit/bf94f3b68ad7d55fb48add049b0c5b444adb55f8))

- fix: switch to non-deprecated async_get instead (#217)

Co-authored-by: Jasper Slits &lt;github@slits.nl&gt; ([`f82e030`](https://github.com/alandtse/tesla/commit/f82e030fca09b8a45497db5a63d7e37f9ae6f4d9))

- fix: use default if scan_interval settings missing

closes #214 ([`0d3d4ce`](https://github.com/alandtse/tesla/commit/0d3d4ce2947d311a6664cf77f97d9ab88433666a))

### Unknown

- Merge pull request #219 from alandtse/dev

2022-05-28 ([`c5a89db`](https://github.com/alandtse/tesla/commit/c5a89db61124bc892b7b8bf25cec6754d6c59a78))

- Merge pull request #215 from alandtse/#214

fix: use default if scan_interval settings missing ([`35447b0`](https://github.com/alandtse/tesla/commit/35447b0340cab93123313f3e36039d1c448398fc))

## v2.2.1 (2022-05-02)

### Fix

- fix: check vin before adjusting climate devices (#208)

Fixes bug where the wrong seat heater or steering wheel heater was impacted for accounts with multiple vehicles.

Fixes #207 ([`5c81955`](https://github.com/alandtse/tesla/commit/5c819554ef3d81446066262b4435066d17cf7a96))

### Unknown

- Merge pull request #209 from alandtse/dev

fix: check vin before adjusting climate devices (#208) ([`fcfb3b5`](https://github.com/alandtse/tesla/commit/fcfb3b5cbbf919e933b87793edb39941b7d6b7c4))

## v2.2.0 (2022-04-30)

### Feature

- feat: enable heated seat and steering wheel entities automatically (#205)

Entities that previously had to be manually enabled will automatically be enabled in HA. ([`ed975f3`](https://github.com/alandtse/tesla/commit/ed975f35fb7c6d33f2dc4b96a6862374279fe091))

### Unknown

- Merge pull request #206 from alandtse/dev

feat: enable heated seat and steering wheel entities automatically ([`34f0f87`](https://github.com/alandtse/tesla/commit/34f0f87122c1362054354d37d605db9f3b0e8896))

## v2.1.1 (2022-04-24)

### Documentation

- docs: change HA documentation link to wiki ([`98650f4`](https://github.com/alandtse/tesla/commit/98650f4c8656b5476bc2f48dded1786d110b1ffe))

### Fix

- fix: bump teslajsonpy to 2.0.3
  Fixes keyerror for vehicles lacking heated seats/steering wheels

closes #199 ([`5ca3899`](https://github.com/alandtse/tesla/commit/5ca3899491ef10535e963d511855f7cfba63c3ed))

### Unknown

- Merge pull request #201 from alandtse/dev

2022-04-24-2 ([`e23c8d3`](https://github.com/alandtse/tesla/commit/e23c8d3aa4d134c20197e2b9731d3445e78d7bf5))

- Merge pull request #200 from alandtse/#199

fix: bump teslajsonpy to 2.0.3 ([`2ff5d7b`](https://github.com/alandtse/tesla/commit/2ff5d7bd8bd1661783fb91739530ec7e4631026a))

## v2.1.0 (2022-04-24)

### Feature

- feat: add support for Heated Steering Wheel and Seats (#188) ([`c052539`](https://github.com/alandtse/tesla/commit/c0525396acaa3f8548632e8bef3c8c5210f25387))

### Fix

- fix: bump dependencies
  closes #193 ([`7dc5779`](https://github.com/alandtse/tesla/commit/7dc57792bd8df00c1b5ab7a58b32fe043eb08a83))

### Unknown

- Merge pull request #198 from alandtse/dev

2022-04-24 ([`ce07439`](https://github.com/alandtse/tesla/commit/ce0743912d03c72b062eb8acff9f556edcc41e34))

- Merge pull request #197 from alandtse/#193

fix: bump dependencies ([`b70960d`](https://github.com/alandtse/tesla/commit/b70960d741adde18ad638fcdce381933586e544b))

## v2.0.2 (2022-04-23)

### Fix

- fix: address sensor breaking change
  https://developers.home-assistant.io/blog/2021/08/12/sensor_temperature_conversion/

closes #191 ([`abc98f9`](https://github.com/alandtse/tesla/commit/abc98f9757be9eec6249c5144e42334c3e6f5c3f))

### Unknown

- Merge pull request #195 from alandtse/dev

2022-04-22 ([`6e7e5aa`](https://github.com/alandtse/tesla/commit/6e7e5aa00bfddf1ba7dcf17834055074d3339afa))

- Merge pull request #194 from alandtse/#191

fix: address sensor breaking change ([`3fa162f`](https://github.com/alandtse/tesla/commit/3fa162fc46542f149386c8e05867e601b46d65c5))

## v2.0.1 (2022-04-05)

### Build

- build: bump deps ([`ede7265`](https://github.com/alandtse/tesla/commit/ede72657e8bb5fd0123df428482f0b779d6b4b8f))

### Fix

- fix: bump teslajsonpy to 2.0.1

closes #183 ([`bab521c`](https://github.com/alandtse/tesla/commit/bab521c42bbfc62a11c5bbc0c25c5d6e5bd64e29))

### Unknown

- Merge pull request #186 from alandtse/dev

2022-04-04 ([`c6dbc3a`](https://github.com/alandtse/tesla/commit/c6dbc3ac1c50475f1b5b631c1e896c814878af92))

## v2.0.0 (2022-03-27)

### Breaking

- fix!: create json sensors for vehicle data

Add the ability for sensors to be disabled by default. Removes json attributes from online sensor and move to separate sensors.

BREAKING CHANGE: Online sensor will no longer have json vehicle data. Any scripts that relied on that json data will need to use the new vehicle data sensors. They will need to be enabled. ([`d13f828`](https://github.com/alandtse/tesla/commit/d13f828c0088560df62208b7b05e26497481d78b))

### Build

- build: fix pytest fixture for later versions

closes #170 ([`10ba368`](https://github.com/alandtse/tesla/commit/10ba36841f0d4ece1017d6e6a9b81a1320f87714))

### Feature

- feat: add trigger homelink button (disabled by default) (#168)

Homelink button is disabled by default because homelink is an optional accessory. ([`0a39370`](https://github.com/alandtse/tesla/commit/0a39370b40cdedaf60e88018defd2bf52afc6ea5))

## v1.7.0 (2022-03-25)

### Build

- build: disallow jinja&gt;=3.1.0

Deprecated contextfilter is removed and breaks HA testing ([`4ec3d09`](https://github.com/alandtse/tesla/commit/4ec3d0915dc170d533c78a3d6dcb6e18fc8690eb))

### Feature

- feat: force update when enabling polling switch

The polling switch can now be used to force an update by toggling off
to on. ([`0aca7a8`](https://github.com/alandtse/tesla/commit/0aca7a8d3acbf3794415ce085c5695f5496129f2))

### Fix

- fix: fix polling switch enable api call

Fix changes to function signature which broke the polling switch.

closes #142 ([`42f01d4`](https://github.com/alandtse/tesla/commit/42f01d4eb8db44cc98f50179b7e59b27455872d6))

### Unknown

- Merge pull request #171 from alandtse/dev

2022-03-24 ([`0ef48dc`](https://github.com/alandtse/tesla/commit/0ef48dc392d9d4c4086c67d6c01de67a67fd5602))

- Merge pull request #169 from alandtse/#142

fix: fix polling switch enable api call ([`f2e3b33`](https://github.com/alandtse/tesla/commit/f2e3b33757c04ee113bf8daca0a40168c8defbe6))

## v1.6.2 (2022-03-23)

### Fix

- fix: bump teslajsonpy to 1.9.0

Removes deprecated get_bearer_step
closes #165 ([`269e08c`](https://github.com/alandtse/tesla/commit/269e08cbbb7ca01e076c5e86a872c01f46b36376))

### Unknown

- Merge pull request #167 from alandtse/dev

2022-03-22 ([`87b3cb8`](https://github.com/alandtse/tesla/commit/87b3cb8a320aaced94005641d9ddade7c6978f46))

- Merge pull request #166 from alandtse/#165

fix: bump teslajsonpy to 1.9.0 ([`b437455`](https://github.com/alandtse/tesla/commit/b437455a95e1c278f7ee081b418a3fe3622bde15))

## v1.6.1 (2022-03-14)

### Documentation

- docs: note how to turn on climate via a scene (#155)

I had a heck of a time running down how to turn on my Tesla&#39;s climate via a scene; looks like [I&#39;m not alone](https://community.home-assistant.io/t/help-with-climate-automation-tesla/39644). Here&#39;s the scene that finally worked for me:

```yaml
- name: I&#39;m Getting Ready to Leave
  icon: &#34;mdi:car&#34;
  entities:
    climate.tesla_model_y_hvac_climate_system:
      state: heat_cool
```

Based on the docs I was expecting to need to set `state` to `on` and `hvac_mode` to `heat_cool`. ([`6da0204`](https://github.com/alandtse/tesla/commit/6da0204660bb861588d8e335eedee9407ed550cd))

### Fix

- fix: disable forced updated for device trackers (#158)

Forced updates are only needed if we are not polling. Since the coordinator
is effectively doing the polling instead of Home Assistant internals doing it
via should_poll set to True, we need to set the property manually to avoid
writing a state update every time the coordinator callback happens to avoid
a state changed event when nothing has really changed. ([`407d44e`](https://github.com/alandtse/tesla/commit/407d44e117706b0907dd20919194e22c18782028))

### Unknown

- Merge pull request #159 from alandtse/dev

fix: disable forced updated for device trackers (#158) ([`2f59bc2`](https://github.com/alandtse/tesla/commit/2f59bc239e5a09cf93f914d8c0961870f1a41136))

## v1.6.0 (2022-02-23)

### Documentation

- docs: document polling policy (#135)

- Update test_config_flow.py

Fix tests in config flow

- Update translations to add section for Polling Policy ([`004f265`](https://github.com/alandtse/tesla/commit/004f265ec0c6e25ce2d04cdeea9964cf1d1cac4e))

### Feature

- feat: add set by vin to update polling interval service (#149) ([`f278680`](https://github.com/alandtse/tesla/commit/f278680fe2db3eed6fc4d80d8abfa69f352e5516))

- feat: allow minimum dataCoordinator update interval at 10 seconds (#148) ([`0d87757`](https://github.com/alandtse/tesla/commit/0d87757ddd5d216043bd83d350492951a6f5ab80))

### Unknown

- Merge pull request #150 from alandtse/dev

2022-02-02 ([`0515f56`](https://github.com/alandtse/tesla/commit/0515f5684f487bbd0c5162bcbe9eb4a8b6b88f66))

## v1.5.0 (2022-01-15)

### Documentation

- docs: add chromium-tesla-token-generator to app list (#123)

- add chromium-tesla-token-generator to list

I just had great success using https://github.com/DoctorMcKay/chromium-tesla-token-generator to generate my refresh token. It also made it trivial to verify that my token was not being transmitted to a third party, which as a paranoid delusional I loved. :)

Thank you for this awesome integration!

- docs: update info.md

Co-authored-by: Alan Tse &lt;alandtse@users.noreply.github.com&gt; ([`33663fb`](https://github.com/alandtse/tesla/commit/33663fb9942d7d6f0ef4a119446132527a090e10))

### Feature

- feat: add set polling policy in configuration (#127) ([`2814149`](https://github.com/alandtse/tesla/commit/28141491eb8c5c3e53792ea900f91a1fc77c087c))

- feat: add polling interval service (#128) ([`3b2d8bc`](https://github.com/alandtse/tesla/commit/3b2d8bc4be6ba6d00e15356f94eed4c2d4dde9e1))

### Unknown

- Merge pull request #133 from alandtse/dev

2022-01-15 ([`04818c9`](https://github.com/alandtse/tesla/commit/04818c9ce4dc0a73a1a54f1c1ea2f41399753d01))

## v1.4.0 (2021-12-11)

### Build

- build: update deps ([`715540b`](https://github.com/alandtse/tesla/commit/715540b122b0cd70f3bd3ac3a5235288165bd334))

### Feature

- feat: add horn and flash lights buttons (#114)

This requires HA &gt;= 2021.12.x to have access to the buttons. For older versions of HA, you will see an error we cannot hide: `[homeassistant.setup] Setup failed for button: Integration not found.`

Co-authored-by: raphael &lt;raphael.dauchy@kwote.fr&gt;
Co-authored-by: Raph &lt;rafal83@users.noreply.github.com&gt; ([`1c39e63`](https://github.com/alandtse/tesla/commit/1c39e63b458fc70298ad7c16521a7612fcb8dd29))

- feat: expose charge_current_request_max attribute (#110)

Co-authored-by: Daniel Potts &lt;danielp@gh.st&gt; ([`a589539`](https://github.com/alandtse/tesla/commit/a5895394f2dc5006cb53a1d66083e6f10ab12fe3))

### Fix

- fix: allow specifying auth_domain

This is necessary for China which uses auth.tesla.cn.

closes #113 ([`22817bd`](https://github.com/alandtse/tesla/commit/22817bd88b16f50f1635c613b3a8a893b06b14af))

- fix: update ha state on command success

closes #102 ([`6ede864`](https://github.com/alandtse/tesla/commit/6ede864dbb0e6f51622a29099e32c468bb069b96))

### Refactor

- refactor: clean up code ([`cba719f`](https://github.com/alandtse/tesla/commit/cba719f6bffbb85d61f3c88825c88649c65a59bd))

- refactor: simplify is_locked ([`5dcaee6`](https://github.com/alandtse/tesla/commit/5dcaee62504ae5ec9e3278f06161a9368f4f2f59))

### Unknown

- Merge pull request #116 from alandtse/dev

2021-12-11 ([`59c6d2c`](https://github.com/alandtse/tesla/commit/59c6d2caac6697f0aaed28922e45aebe5f97d5ca))

- Merge pull request #115 from alandtse/#113

#113 ([`3458fa9`](https://github.com/alandtse/tesla/commit/3458fa9276471f6fb39a1248b4cdb2fc4af580fa))

- Merge pull request #112 from alandtse/#102

#102 ([`2f0c8e0`](https://github.com/alandtse/tesla/commit/2f0c8e070fd2e7192b1fb9337c52681cac19436d))

- Merge branch &#39;dev&#39; of github.com:alandtse/tesla into #102 ([`00bdcb1`](https://github.com/alandtse/tesla/commit/00bdcb15303d573681af33f029ae808d5fad01e9))

## v1.3.2 (2021-11-22)

### Documentation

- docs: add add integration link to info.md ([`5dd66ec`](https://github.com/alandtse/tesla/commit/5dd66eca42fc03b08b30f8e52d877952fa37e9a3))

- docs: add add-integration badge ([`4ae8227`](https://github.com/alandtse/tesla/commit/4ae822755e13b8e358b84c43d10ddacc04ed2f16))

### Fix

- fix: bump deps

This is a dummy commit to bump version based on:
https://github.com/alandtse/tesla/pull/98 ([`ccd2f53`](https://github.com/alandtse/tesla/commit/ccd2f534ab82f4bb400670bf6085e82529336f12))

### Refactor

- refactor: use http.HTTPStatus instead of const.HTTP\_\* (#87)

Addressing future HA change: https://github.com/home-assistant/core/pull/58380 ([`25466ce`](https://github.com/alandtse/tesla/commit/25466ced9a918be549b325e2b066badacde9bb24))

### Unknown

- Merge pull request #98 from alandtse/dev

fix: use http.httpstatus constant ([`6b92437`](https://github.com/alandtse/tesla/commit/6b92437d5b6ee6b00f7aa672c482c9762a140282))

- Improve documentation (#94)

- Update README.md

Initial insert of &#39;usage&#39; section to provide basic documentation for functionality. (Relates #65)

- Update README.md

Updated readme to reflect polling rather than scan, and updated some verbiage. ([`f289f40`](https://github.com/alandtse/tesla/commit/f289f401a9b5f3a7f0d7e3776b4e3e6ba52b0dd8))

## v1.3.1 (2021-10-22)

### Fix

- fix: bump telsajsonpy to 1.2.1
  closes #82 ([`a0723a4`](https://github.com/alandtse/tesla/commit/a0723a4ecdc16c1dc0765f74bc6d965c36a6e158))

### Unknown

- Merge pull request #84 from alandtse/dev

2021-10-21 ([`6135885`](https://github.com/alandtse/tesla/commit/6135885c5df35212040fa1d1aded123c55c677bb))

- Merge pull request #83 from alandtse/#82

fix: bump telsajsonpy to 1.2.1 ([`6e2488e`](https://github.com/alandtse/tesla/commit/6e2488ee41df93a408af5825dd6fe00137fc6a48))

## v1.3.0 (2021-10-21)

### Build

- build: update dev env to py3.9 ([`88ec031`](https://github.com/alandtse/tesla/commit/88ec031394958ccd77490f3270e1c7e3cebc1e24))

### Ci

- ci: simplify workflow to use actions ([`c087c95`](https://github.com/alandtse/tesla/commit/c087c95ac1b305a03cda4026bb6fc359be619413))

### Documentation

- docs: add Japanese translations (#75) ([`b938ab8`](https://github.com/alandtse/tesla/commit/b938ab8b47b41bfc641c846c27e5ecfd19514aec))

### Feature

- feat: bump teslajsonpy to 1.2.0
  Add vin, id, and vehicle_id to online sensor attributes for template use ([`7a1a1b6`](https://github.com/alandtse/tesla/commit/7a1a1b6f60c8cb7e907fcebe9f399597572b7eeb))

### Unknown

- Merge pull request #78 from alandtse/dev

2021-10-19 ([`b397465`](https://github.com/alandtse/tesla/commit/b39746566578265ded729c299836436870f55666))

- Merge pull request #81 from alandtse/online_attributes

ci: simplify workflow to use actions ([`85efbd9`](https://github.com/alandtse/tesla/commit/85efbd97989079b413521cac21fd44b530b1b922))

- Merge pull request #80 from alandtse/online_attributes

build: update dev env to py3.9 ([`03f9c65`](https://github.com/alandtse/tesla/commit/03f9c6587e0c0b5e7469f8189fa552b50b5964f0))

- Merge pull request #77 from alandtse/online_attributes

feat: bump teslajsonpy to 1.2.0 ([`7a9100a`](https://github.com/alandtse/tesla/commit/7a9100acdbbe0982285b1493f413cf7d742ba459))

## v1.2.1 (2021-10-19)

### Fix

- fix: bump teslajsonpy to 1.1.2
  closes #71
  closes #70 ([`697bb3e`](https://github.com/alandtse/tesla/commit/697bb3e4ca4c1823189f204a375f44a18ba1f875))

### Unknown

- Merge pull request #74 from alandtse/dev

2021-10-18 ([`7400fca`](https://github.com/alandtse/tesla/commit/7400fcae81fe5ce28fb745a783ee20cfccbbecf6))

- Merge pull request #73 from alandtse/api_service

fix: bump teslajsonpy to 1.1.2 ([`a657f75`](https://github.com/alandtse/tesla/commit/a657f75e65de250f8cfe38f02f3b38e3b1658a4c))

## v1.2.0 (2021-10-18)

### Documentation

- docs: fix changelog ([`e2e0f89`](https://github.com/alandtse/tesla/commit/e2e0f8920cac12612e1532de22e11bd5b45a37f7))

### Feature

- feat: add tesla_custom.api service
  This service allows access to the controller.api command. This allows
  the use of any command in the endpoints file. https://github.com/zabuldon/teslajsonpy/blob/master/teslajsonpy/endpoints.json

For documentation see https://teslajsonpy.readthedocs.io/en/latest/teslajsonpy/teslajsonpy.html#teslajsonpy.Controller.api ([`295ed08`](https://github.com/alandtse/tesla/commit/295ed08a69e403aec0f2a252bdeb42b06e46bba9))

### Unknown

- Merge pull request #69 from alandtse/dev

2021-10-17 2 ([`5d59021`](https://github.com/alandtse/tesla/commit/5d59021e4043d03106e91c444d2d048bb676e7f2))

- Merge pull request #68 from alandtse/api_service

feat: add tesla_custom.api service ([`f636565`](https://github.com/alandtse/tesla/commit/f636565a547fd5df12ddfd7d58094633a10ef31a))

## v1.1.2 (2021-10-18)

### Fix

- fix: bump teslajsonpy to 1.1.1
  closes #62 ([`ea54876`](https://github.com/alandtse/tesla/commit/ea5487642fbf51312198f66b32c46909a3adbc6b))

### Unknown

- Merge pull request #67 from alandtse/dev

2021-10-17 ([`736fb42`](https://github.com/alandtse/tesla/commit/736fb4277c1040fa780c43bc4da04567e362bef0))

- Merge pull request #66 from alandtse/#62

fix: bump teslajsonpy to 1.1.1 ([`aac1ee0`](https://github.com/alandtse/tesla/commit/aac1ee0fce11ad052dce6d97bc590208fccb0548))

## v1.1.1 (2021-10-13)

### Fix

- fix: bump teslajsonpy to 1.0.1

closes #61 ([`f41061c`](https://github.com/alandtse/tesla/commit/f41061c2ee0217a73af71cd0275f48290c05c11e))

### Unknown

- Merge pull request #63 from alandtse/#61

fix: bump teslajsonpy to 1.0.1 ([`b5b4534`](https://github.com/alandtse/tesla/commit/b5b45347918de938e3ca95f614279b81a800cff1))

## v1.1.0 (2021-10-11)

### Build

- build: bump deps ([`921ef8e`](https://github.com/alandtse/tesla/commit/921ef8e3b93b481582824ef7d3694dd154b3d272))

### Documentation

- docs: include teslafi for tokens (#54)

- Update README.md

Document TeslaFi as another source for tokens.

- Update strings.json

- Update info.md ([`f6ed61e`](https://github.com/alandtse/tesla/commit/f6ed61e65c3cb2c3183e4903d5cf2fd2cbe99e71))

- docs: add HACS Link (#48)

Add link and small instructions to add the repository in HACS. ([`f8c761e`](https://github.com/alandtse/tesla/commit/f8c761e3e6b41b736153866d134b811ac8bc6244))

- docs: specify platform for authentication apps (#43) ([`09fc04f`](https://github.com/alandtse/tesla/commit/09fc04ff2c3489582ebeb1b67fffc8b01c65a818))

### Feature

- feat: add support for Energy Sites (#58)

Add support for Tesla Solar ([`92e8672`](https://github.com/alandtse/tesla/commit/92e86723c46eb2c0f03314196a8f8a0f8e9b66a4))

### Unknown

- Merge pull request #59 from alandtse/dev

2021-10-11 ([`f735eb5`](https://github.com/alandtse/tesla/commit/f735eb5425f36819e0a231f639f86fa6df14ccbc))

- Merge pull request #44 from alandtse/dev

docs: specify platform for authentication apps (#43) ([`1113695`](https://github.com/alandtse/tesla/commit/1113695e7e37535cd7e36233a257b4ead2062f12))

## v1.0.0 (2021-09-11)

### Documentation

- docs: update documentations for refresh tokens ([`f4ac729`](https://github.com/alandtse/tesla/commit/f4ac729003c3fe4255a5b551a20d7d30b797430a))

### Feature

- feat: replace oauth proxy login with refresh token

Due to Tesla&#39;s use of recaptcha, we are abandoning any login logic
in the component. Instead, we will process a refresh token
generated by third-party apps (e.g., Tesla Tokens, Auth App for
Tesla).

closes #3
closes #12
closes #20
closes #25 ([`9ccb71e`](https://github.com/alandtse/tesla/commit/9ccb71e53266aab1de3cf88e7b3f7bddb19f264e))

### Fix

- fix: rename update switch to polling switch

The `update switch` was confusing since we use `update available` to describe whether a software update is available. We now clarify that this switch controls polling of a vehicle.

BREAKING CHANGE: `update_switch` has been renamed to `polling_switch`. While the UI name will change immediately if you have not modified it, the entity_id should not change unless you remove and reinstall the component.

closes #22

Co-authored-by: Andy Allsopp &lt;arallsopp@gmail.com&gt; ([`b09825c`](https://github.com/alandtse/tesla/commit/b09825c3eec63731e63c161d69ec9c26a7b615b5))

### Style

- style: add pytest to pre-commit ([`2230e39`](https://github.com/alandtse/tesla/commit/2230e39183ed3cbf749b35490d02f05505b77f92))

- style: match max-line-length with black ([`8909149`](https://github.com/alandtse/tesla/commit/890914905281a56baf3584706abe579df8569646))

### Unknown

- Merge pull request #31 from alandtse/dev

2021-09-10 ([`ff41fb2`](https://github.com/alandtse/tesla/commit/ff41fb213f6a5538f5b0682a208e6afc228a6a8c))

- Merge pull request #29 from alandtse/refresh_token

Switch to refresh token ([`37bce6a`](https://github.com/alandtse/tesla/commit/37bce6a83259f37d18b5d29bd9f291f1b8f4d343))

## v0.2.1 (2021-09-03)

### Build

- build(deps): bump deps ([`5692833`](https://github.com/alandtse/tesla/commit/569283392b206d6bdf853940474600ab71df54cb))

### Fix

- fix: update energy sensor for HA 2021.9
  This is not backwards compatible for HA 2021.8 ([`9cb6806`](https://github.com/alandtse/tesla/commit/9cb680693a18d98e51aadafa8e3e9a8bd920c7ab))

## v0.2.0 (2021-08-13)

### Feature

- feat: add charger_power attribute to rate sensor
  https://github.com/zabuldon/teslajsonpy/issues/204 ([`66228d1`](https://github.com/alandtse/tesla/commit/66228d1f5bb6d4d0fcf96f5df195e564a9d987d8))

- feat: add energy added sensor
  This allows Tesla information to be used with the Energy panel.
  https://github.com/home-assistant/core/issues/54054 ([`3b83613`](https://github.com/alandtse/tesla/commit/3b83613e2b66538a3f691667625041950ba40d75))

### Fix

- fix: bump teslajsonpy to 0.19.0
  closes #11 ([`7efd7a1`](https://github.com/alandtse/tesla/commit/7efd7a1a3440afbdc979e5679509b277df22ba68))

### Test

- test: fix tests ([`d2874e1`](https://github.com/alandtse/tesla/commit/d2874e1ca30aec7d40c3cf4df4adcd0e0969e7c1))

### Unknown

- Merge branch &#39;main&#39; of github.com:alandtse/tesla into main ([`e56b7ec`](https://github.com/alandtse/tesla/commit/e56b7eccb1b11919f756ae8860b26d1efc61d64e))

## v0.1.5 (2021-05-01)

### Build

- build(deps): update deps ([`021e547`](https://github.com/alandtse/tesla/commit/021e54781e0fa3790971d74241e98b3057bb6301))

### Fix

- fix: detect invalid tokens ([`90d0a72`](https://github.com/alandtse/tesla/commit/90d0a72d363a7e3a95babd90ab58d93a1b32107a))

## v0.1.4 (2021-05-01)

### Fix

- fix: fix additional httpx syntax errors for reauth ([`f10809a`](https://github.com/alandtse/tesla/commit/f10809aec6590c7f71f4c9b035bd6b0894e8c6c3))

### Unknown

- Merge branch &#39;main&#39; of github.com:alandtse/tesla into main ([`63c6639`](https://github.com/alandtse/tesla/commit/63c66394caa04fcbe971d0b5f9555623ca205e9f))

## v0.1.3 (2021-05-01)

### Fix

- fix: fix token refresh
  The code path for automatic token refreshes was still using aiohttp. ([`dec9a40`](https://github.com/alandtse/tesla/commit/dec9a4059f80fe8ee00423dbc26277dacb9b9b38))

### Unknown

- Merge branch &#39;main&#39; of github.com:alandtse/tesla into main ([`18766b4`](https://github.com/alandtse/tesla/commit/18766b43e11fd74534498edd6f69eb2a849d6c5c))

## v0.1.2 (2021-04-30)

### Build

- build(deps): update deps ([`79fa9d8`](https://github.com/alandtse/tesla/commit/79fa9d88a0a761f079bdc388a9d1957551e293b5))

### Fix

- fix: fix directory in zip
  Zip should now appropriately unzip in tesla_custom ([`d8b4fc6`](https://github.com/alandtse/tesla/commit/d8b4fc61ebd49f15ff41b41797f2c9fe1a1a5eb2))

### Unknown

- Merge branch &#39;main&#39; of github.com:alandtse/tesla into main ([`db16938`](https://github.com/alandtse/tesla/commit/db169384ba0b62e2a009830cbac767517155cdff))

## v0.1.1 (2021-04-30)

### Build

- build: set minimum HA requirement ([`bf34e49`](https://github.com/alandtse/tesla/commit/bf34e49031a00bbde8a8d69a06b96418e9df17b3))

- build: change to zip release ([`8411806`](https://github.com/alandtse/tesla/commit/8411806083b63e9f1c6b0435732e7cca5561c4f5))

### Documentation

- docs: update instructions for upgrading from core ([`3b67b24`](https://github.com/alandtse/tesla/commit/3b67b24460a4c07e75917d0b6dfd9bbb9f2ace5d))

### Fix

- fix: change structure to not override core
  This was required by https://github.com/home-assistant/wheels-custom-integrations/pull/383#issuecomment-829094337

Tesla in core will be non-functional regardless. ([`f173b68`](https://github.com/alandtse/tesla/commit/f173b6823a7c0f259ac2c5a94341820c6ae83fbf))

## v0.1.0 (2021-04-29)

### Feature

- feat: initial commit
  based on https://github.com/alandtse/home-assistant/tree/tesla_oauth_callback ([`c12aadf`](https://github.com/alandtse/tesla/commit/c12aadf808053cb67a1fb05d1b95940a0775a889))
