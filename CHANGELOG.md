# Changelog

<!--next-version-placeholder-->

## v2.3.0 (2022-05-29)
### Feature
* Add support for async_remove_config_entry_device ([#218](https://github.com/alandtse/tesla/issues/218)) ([`562c1b0`](https://github.com/alandtse/tesla/commit/562c1b0ce01ced7adb0743a39178a7e9951c5e35))

### Fix
* Improve handling on 0 Watts power reads ([`bf94f3b`](https://github.com/alandtse/tesla/commit/bf94f3b68ad7d55fb48add049b0c5b444adb55f8))
* Switch to non-deprecated async_get instead ([#217](https://github.com/alandtse/tesla/issues/217)) ([`f82e030`](https://github.com/alandtse/tesla/commit/f82e030fca09b8a45497db5a63d7e37f9ae6f4d9))
* Use default if scan_interval settings missing ([`0d3d4ce`](https://github.com/alandtse/tesla/commit/0d3d4ce2947d311a6664cf77f97d9ab88433666a))

## v2.2.1 (2022-05-02)
### Fix
* Check vin before adjusting climate devices ([#208](https://github.com/alandtse/tesla/issues/208)) ([`5c81955`](https://github.com/alandtse/tesla/commit/5c819554ef3d81446066262b4435066d17cf7a96))

## v2.2.0 (2022-04-30)
### Feature
* Enable heated seat and steering wheel entities automatically ([#205](https://github.com/alandtse/tesla/issues/205)) ([`ed975f3`](https://github.com/alandtse/tesla/commit/ed975f35fb7c6d33f2dc4b96a6862374279fe091))

## v2.1.1 (2022-04-24)

### Fix

- Bump teslajsonpy to 2.0.3 ([`5ca3899`](https://github.com/alandtse/tesla/commit/5ca3899491ef10535e963d511855f7cfba63c3ed))

### Documentation

- Change HA documentation link to wiki ([`98650f4`](https://github.com/alandtse/tesla/commit/98650f4c8656b5476bc2f48dded1786d110b1ffe))

## v2.1.0 (2022-04-24)

### Feature

- Add support for Heated Steering Wheel and Seats ([#188](https://github.com/alandtse/tesla/issues/188)) ([`c052539`](https://github.com/alandtse/tesla/commit/c0525396acaa3f8548632e8bef3c8c5210f25387))

### Fix

- Bump dependencies ([`7dc5779`](https://github.com/alandtse/tesla/commit/7dc57792bd8df00c1b5ab7a58b32fe043eb08a83))

## v2.0.2 (2022-04-23)

### Fix

- Address sensor breaking change ([`abc98f9`](https://github.com/alandtse/tesla/commit/abc98f9757be9eec6249c5144e42334c3e6f5c3f))

## v2.0.1 (2022-04-05)

### Fix

- Bump teslajsonpy to 2.0.1 ([`bab521c`](https://github.com/alandtse/tesla/commit/bab521c42bbfc62a11c5bbc0c25c5d6e5bd64e29))

## v2.0.0 (2022-03-27)

### Feature

- Add trigger homelink button (disabled by default) ([#168](https://github.com/alandtse/tesla/issues/168)) ([`0a39370`](https://github.com/alandtse/tesla/commit/0a39370b40cdedaf60e88018defd2bf52afc6ea5))

### Fix

- Create json sensors for vehicle data ([`d13f828`](https://github.com/alandtse/tesla/commit/d13f828c0088560df62208b7b05e26497481d78b))

### Breaking

- Online sensor will no longer have json vehicle data. Any scripts that relied on that json data will need to use the new vehicle data sensors. They will need to be enabled. ([`d13f828`](https://github.com/alandtse/tesla/commit/d13f828c0088560df62208b7b05e26497481d78b))

## v1.7.0 (2022-03-25)

### Feature

- Force update when enabling polling switch ([`0aca7a8`](https://github.com/alandtse/tesla/commit/0aca7a8d3acbf3794415ce085c5695f5496129f2))

### Fix

- Fix polling switch enable api call ([`42f01d4`](https://github.com/alandtse/tesla/commit/42f01d4eb8db44cc98f50179b7e59b27455872d6))

## v1.6.2 (2022-03-23)

### Fix

- Bump teslajsonpy to 1.9.0 ([`269e08c`](https://github.com/alandtse/tesla/commit/269e08cbbb7ca01e076c5e86a872c01f46b36376))

## v1.6.1 (2022-03-14)

### Fix

- Disable forced updated for device trackers ([#158](https://github.com/alandtse/tesla/issues/158)) ([`407d44e`](https://github.com/alandtse/tesla/commit/407d44e117706b0907dd20919194e22c18782028))

### Documentation

- Note how to turn on climate via a scene ([#155](https://github.com/alandtse/tesla/issues/155)) ([`6da0204`](https://github.com/alandtse/tesla/commit/6da0204660bb861588d8e335eedee9407ed550cd))

## v1.6.0 (2022-02-23)

### Feature

- Add set by vin to update polling interval service ([#149](https://github.com/alandtse/tesla/issues/149)) ([`f278680`](https://github.com/alandtse/tesla/commit/f278680fe2db3eed6fc4d80d8abfa69f352e5516))
- Allow minimum dataCoordinator update interval at 10 seconds ([#148](https://github.com/alandtse/tesla/issues/148)) ([`0d87757`](https://github.com/alandtse/tesla/commit/0d87757ddd5d216043bd83d350492951a6f5ab80))

### Documentation

- Document polling policy ([#135](https://github.com/alandtse/tesla/issues/135)) ([`004f265`](https://github.com/alandtse/tesla/commit/004f265ec0c6e25ce2d04cdeea9964cf1d1cac4e))

## v1.5.0 (2022-01-15)

### Feature

- Add set polling policy in configuration ([#127](https://github.com/alandtse/tesla/issues/127)) ([`2814149`](https://github.com/alandtse/tesla/commit/28141491eb8c5c3e53792ea900f91a1fc77c087c))
- Add polling interval service ([#128](https://github.com/alandtse/tesla/issues/128)) ([`3b2d8bc`](https://github.com/alandtse/tesla/commit/3b2d8bc4be6ba6d00e15356f94eed4c2d4dde9e1))

### Documentation

- Add chromium-tesla-token-generator to app list ([#123](https://github.com/alandtse/tesla/issues/123)) ([`33663fb`](https://github.com/alandtse/tesla/commit/33663fb9942d7d6f0ef4a119446132527a090e10))

## v1.4.0 (2021-12-11)

### Feature

- Add horn and flash lights buttons ([#114](https://github.com/alandtse/tesla/issues/114)) ([`1c39e63`](https://github.com/alandtse/tesla/commit/1c39e63b458fc70298ad7c16521a7612fcb8dd29))
- Expose charge_current_request_max attribute ([#110](https://github.com/alandtse/tesla/issues/110)) ([`a589539`](https://github.com/alandtse/tesla/commit/a5895394f2dc5006cb53a1d66083e6f10ab12fe3))

### Fix

- Allow specifying auth_domain ([`22817bd`](https://github.com/alandtse/tesla/commit/22817bd88b16f50f1635c613b3a8a893b06b14af))
- Update ha state on command success ([`6ede864`](https://github.com/alandtse/tesla/commit/6ede864dbb0e6f51622a29099e32c468bb069b96))

### Refactor

- Clean up code ([`cba719f`](https://github.com/alandtse/tesla/commit/cba719f6bffbb85d61f3c88825c88649c65a59bd))
- Simplify is_locked ([`5dcaee6`](https://github.com/alandtse/tesla/commit/5dcaee62504ae5ec9e3278f06161a9368f4f2f59))

## v1.3.2 (2021-11-22)

### Fix

- Bump deps ([`ccd2f53`](https://github.com/alandtse/tesla/commit/ccd2f534ab82f4bb400670bf6085e82529336f12))

### Documentation

- Add add integration link to info.md ([`5dd66ec`](https://github.com/alandtse/tesla/commit/5dd66eca42fc03b08b30f8e52d877952fa37e9a3))
- Add add-integration badge ([`4ae8227`](https://github.com/alandtse/tesla/commit/4ae822755e13b8e358b84c43d10ddacc04ed2f16))

### Refactor

- Use http.HTTPStatus instead of const.HTTP\_\* ([#87](https://github.com/alandtse/tesla/issues/87)) ([`25466ce`](https://github.com/alandtse/tesla/commit/25466ced9a918be549b325e2b066badacde9bb24))

## v1.3.1 (2021-10-22)

### Fix

- Bump telsajsonpy to 1.2.1 ([`a0723a4`](https://github.com/alandtse/tesla/commit/a0723a4ecdc16c1dc0765f74bc6d965c36a6e158))

## v1.3.0 (2021-10-21)

### Feature

- Bump teslajsonpy to 1.2.0 ([`7a1a1b6`](https://github.com/alandtse/tesla/commit/7a1a1b6f60c8cb7e907fcebe9f399597572b7eeb))

### Documentation

- Add Japanese translations ([#75](https://github.com/alandtse/tesla/issues/75)) ([`b938ab8`](https://github.com/alandtse/tesla/commit/b938ab8b47b41bfc641c846c27e5ecfd19514aec))

## v1.2.1 (2021-10-19)

### Fix

- Bump teslajsonpy to 1.1.2 ([`697bb3e`](https://github.com/alandtse/tesla/commit/697bb3e4ca4c1823189f204a375f44a18ba1f875))

## v1.2.0 (2021-10-18)

### Feature

- Add tesla_custom.api service ([`295ed08`](https://github.com/alandtse/tesla/commit/295ed08a69e403aec0f2a252bdeb42b06e46bba9))

### Documentation

- Fix changelog ([`e2e0f89`](https://github.com/alandtse/tesla/commit/e2e0f8920cac12612e1532de22e11bd5b45a37f7))

## v1.1.2 (2021-10-18)

### Fix

- Bump teslajsonpy to 1.1.1 ([`ea5487`](https://github.com/alandtse/tesla/commit/ea5487642fbf51312198f66b32c46909a3adbc6b))

## v1.1.1 (2021-10-13)

### Fix

- Bump teslajsonpy to 1.0.1 ([`f41061c`](https://github.com/alandtse/tesla/commit/f41061c2ee0217a73af71cd0275f48290c05c11e))

## v1.1.0 (2021-10-11)

### Feature

- Add support for Energy Sites ([#58](https://github.com/alandtse/tesla/issues/58)) ([`92e8672`](https://github.com/alandtse/tesla/commit/92e86723c46eb2c0f03314196a8f8a0f8e9b66a4))

### Documentation

- Include teslafi for tokens ([#54](https://github.com/alandtse/tesla/issues/54)) ([`f6ed61e`](https://github.com/alandtse/tesla/commit/f6ed61e65c3cb2c3183e4903d5cf2fd2cbe99e71))
- Add HACS Link ([#48](https://github.com/alandtse/tesla/issues/48)) ([`f8c761e`](https://github.com/alandtse/tesla/commit/f8c761e3e6b41b736153866d134b811ac8bc6244))
- Specify platform for authentication apps ([#43](https://github.com/alandtse/tesla/issues/43)) ([`09fc04f`](https://github.com/alandtse/tesla/commit/09fc04ff2c3489582ebeb1b67fffc8b01c65a818))

## v1.0.0 (2021-09-11)

### Feature

- Replace oauth proxy login with refresh token ([`9ccb71e`](https://github.com/alandtse/tesla/commit/9ccb71e53266aab1de3cf88e7b3f7bddb19f264e))

### Fix

- Rename update switch to polling switch ([`b09825c`](https://github.com/alandtse/tesla/commit/b09825c3eec63731e63c161d69ec9c26a7b615b5))

### Breaking

- `update_switch` has been renamed to `polling_switch`. While the UI name will change immediately if you have not modified it, the entity_id should not change unless you remove and reinstall the component. ([`b09825c`](https://github.com/alandtse/tesla/commit/b09825c3eec63731e63c161d69ec9c26a7b615b5))

### Documentation

- Update documentations for refresh tokens ([`f4ac729`](https://github.com/alandtse/tesla/commit/f4ac729003c3fe4255a5b551a20d7d30b797430a))

## v0.2.1 (2021-09-03)

### Fix

- Update energy sensor for HA 2021.9 ([`9cb6806`](https://github.com/alandtse/tesla/commit/9cb680693a18d98e51aadafa8e3e9a8bd920c7ab))

## v0.2.0 (2021-08-13)

### Feature

- Add charger_power attribute to rate sensor ([`66228d1`](https://github.com/alandtse/tesla/commit/66228d1f5bb6d4d0fcf96f5df195e564a9d987d8))
- Add energy added sensor ([`3b83613`](https://github.com/alandtse/tesla/commit/3b83613e2b66538a3f691667625041950ba40d75))

### Fix

- Bump teslajsonpy to 0.19.0 ([`7efd7a1`](https://github.com/alandtse/tesla/commit/7efd7a1a3440afbdc979e5679509b277df22ba68))

## v0.1.5 (2021-05-01)

### Fix

- Detect invalid tokens ([`90d0a72`](https://github.com/alandtse/tesla/commit/90d0a72d363a7e3a95babd90ab58d93a1b32107a))

## v0.1.4 (2021-05-01)

### Fix

- Fix additional httpx syntax errors for reauth ([`f10809a`](https://github.com/alandtse/tesla/commit/f10809aec6590c7f71f4c9b035bd6b0894e8c6c3))

## v0.1.3 (2021-05-01)

### Fix

- Fix token refresh ([`dec9a40`](https://github.com/alandtse/tesla/commit/dec9a4059f80fe8ee00423dbc26277dacb9b9b38))

## v0.1.2 (2021-04-30)

### Fix

- Fix directory in zip ([`d8b4fc6`](https://github.com/alandtse/tesla/commit/d8b4fc61ebd49f15ff41b41797f2c9fe1a1a5eb2))

## v0.1.1 (2021-04-30)

### Fix

- Change structure to not override core ([`f173b68`](https://github.com/alandtse/tesla/commit/f173b6823a7c0f259ac2c5a94341820c6ae83fbf))

### Documentation

- Update instructions for upgrading from core ([`3b67b24`](https://github.com/alandtse/tesla/commit/3b67b24460a4c07e75917d0b6dfd9bbb9f2ace5d))

## v0.1.0 (2021-04-29)

### Feature

- Initial commit ([`c12aadf`](https://github.com/alandtse/tesla/commit/c12aadf808053cb67a1fb05d1b95940a0775a889))
