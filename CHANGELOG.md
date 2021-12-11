# Changelog

<!--next-version-placeholder-->

## v1.4.0 (2021-12-11)
### Feature
* Add horn and flash lights buttons ([#114](https://github.com/alandtse/tesla/issues/114)) ([`1c39e63`](https://github.com/alandtse/tesla/commit/1c39e63b458fc70298ad7c16521a7612fcb8dd29))
* Expose charge_current_request_max attribute ([#110](https://github.com/alandtse/tesla/issues/110)) ([`a589539`](https://github.com/alandtse/tesla/commit/a5895394f2dc5006cb53a1d66083e6f10ab12fe3))

### Fix
* Allow specifying auth_domain ([`22817bd`](https://github.com/alandtse/tesla/commit/22817bd88b16f50f1635c613b3a8a893b06b14af))
* Update ha state on command success ([`6ede864`](https://github.com/alandtse/tesla/commit/6ede864dbb0e6f51622a29099e32c468bb069b96))

### Refactor
* Clean up code ([`cba719f`](https://github.com/alandtse/tesla/commit/cba719f6bffbb85d61f3c88825c88649c65a59bd))
* Simplify is_locked ([`5dcaee6`](https://github.com/alandtse/tesla/commit/5dcaee62504ae5ec9e3278f06161a9368f4f2f59))

## v1.3.2 (2021-11-22)
### Fix
* Bump deps ([`ccd2f53`](https://github.com/alandtse/tesla/commit/ccd2f534ab82f4bb400670bf6085e82529336f12))

### Documentation
* Add add integration link to info.md ([`5dd66ec`](https://github.com/alandtse/tesla/commit/5dd66eca42fc03b08b30f8e52d877952fa37e9a3))
* Add add-integration badge ([`4ae8227`](https://github.com/alandtse/tesla/commit/4ae822755e13b8e358b84c43d10ddacc04ed2f16))

### Refactor
* Use http.HTTPStatus instead of const.HTTP_* ([#87](https://github.com/alandtse/tesla/issues/87)) ([`25466ce`](https://github.com/alandtse/tesla/commit/25466ced9a918be549b325e2b066badacde9bb24))

## v1.3.1 (2021-10-22)
### Fix
* Bump telsajsonpy to 1.2.1 ([`a0723a4`](https://github.com/alandtse/tesla/commit/a0723a4ecdc16c1dc0765f74bc6d965c36a6e158))

## v1.3.0 (2021-10-21)
### Feature
* Bump teslajsonpy to 1.2.0 ([`7a1a1b6`](https://github.com/alandtse/tesla/commit/7a1a1b6f60c8cb7e907fcebe9f399597572b7eeb))

### Documentation
* Add Japanese translations ([#75](https://github.com/alandtse/tesla/issues/75)) ([`b938ab8`](https://github.com/alandtse/tesla/commit/b938ab8b47b41bfc641c846c27e5ecfd19514aec))

## v1.2.1 (2021-10-19)
### Fix
* Bump teslajsonpy to 1.1.2 ([`697bb3e`](https://github.com/alandtse/tesla/commit/697bb3e4ca4c1823189f204a375f44a18ba1f875))

## v1.2.0 (2021-10-18)
### Feature
* Add tesla_custom.api service ([`295ed08`](https://github.com/alandtse/tesla/commit/295ed08a69e403aec0f2a252bdeb42b06e46bba9))

### Documentation
* Fix changelog ([`e2e0f89`](https://github.com/alandtse/tesla/commit/e2e0f8920cac12612e1532de22e11bd5b45a37f7))

## v1.1.2 (2021-10-18)
### Fix
* Bump teslajsonpy to 1.1.1 ([`ea5487`](https://github.com/alandtse/tesla/commit/ea5487642fbf51312198f66b32c46909a3adbc6b))

## v1.1.1 (2021-10-13)
### Fix
* Bump teslajsonpy to 1.0.1 ([`f41061c`](https://github.com/alandtse/tesla/commit/f41061c2ee0217a73af71cd0275f48290c05c11e))

## v1.1.0 (2021-10-11)
### Feature
* Add support for Energy Sites ([#58](https://github.com/alandtse/tesla/issues/58)) ([`92e8672`](https://github.com/alandtse/tesla/commit/92e86723c46eb2c0f03314196a8f8a0f8e9b66a4))

### Documentation
* Include teslafi for tokens ([#54](https://github.com/alandtse/tesla/issues/54)) ([`f6ed61e`](https://github.com/alandtse/tesla/commit/f6ed61e65c3cb2c3183e4903d5cf2fd2cbe99e71))
* Add HACS Link ([#48](https://github.com/alandtse/tesla/issues/48)) ([`f8c761e`](https://github.com/alandtse/tesla/commit/f8c761e3e6b41b736153866d134b811ac8bc6244))
* Specify platform for authentication apps ([#43](https://github.com/alandtse/tesla/issues/43)) ([`09fc04f`](https://github.com/alandtse/tesla/commit/09fc04ff2c3489582ebeb1b67fffc8b01c65a818))

## v1.0.0 (2021-09-11)
### Feature
* Replace oauth proxy login with refresh token ([`9ccb71e`](https://github.com/alandtse/tesla/commit/9ccb71e53266aab1de3cf88e7b3f7bddb19f264e))

### Fix
* Rename update switch to polling switch ([`b09825c`](https://github.com/alandtse/tesla/commit/b09825c3eec63731e63c161d69ec9c26a7b615b5))

### Breaking
* `update_switch` has been renamed to `polling_switch`. While the UI name will change immediately if you have not modified it, the entity_id should not change unless you remove and reinstall the component. ([`b09825c`](https://github.com/alandtse/tesla/commit/b09825c3eec63731e63c161d69ec9c26a7b615b5))

### Documentation
* Update documentations for refresh tokens ([`f4ac729`](https://github.com/alandtse/tesla/commit/f4ac729003c3fe4255a5b551a20d7d30b797430a))

## v0.2.1 (2021-09-03)
### Fix
* Update energy sensor for HA 2021.9 ([`9cb6806`](https://github.com/alandtse/tesla/commit/9cb680693a18d98e51aadafa8e3e9a8bd920c7ab))

## v0.2.0 (2021-08-13)
### Feature
* Add charger_power attribute to rate sensor ([`66228d1`](https://github.com/alandtse/tesla/commit/66228d1f5bb6d4d0fcf96f5df195e564a9d987d8))
* Add energy added sensor ([`3b83613`](https://github.com/alandtse/tesla/commit/3b83613e2b66538a3f691667625041950ba40d75))

### Fix
* Bump teslajsonpy to 0.19.0 ([`7efd7a1`](https://github.com/alandtse/tesla/commit/7efd7a1a3440afbdc979e5679509b277df22ba68))

## v0.1.5 (2021-05-01)
### Fix
* Detect invalid tokens ([`90d0a72`](https://github.com/alandtse/tesla/commit/90d0a72d363a7e3a95babd90ab58d93a1b32107a))

## v0.1.4 (2021-05-01)
### Fix
* Fix additional httpx syntax errors for reauth ([`f10809a`](https://github.com/alandtse/tesla/commit/f10809aec6590c7f71f4c9b035bd6b0894e8c6c3))

## v0.1.3 (2021-05-01)
### Fix
* Fix token refresh ([`dec9a40`](https://github.com/alandtse/tesla/commit/dec9a4059f80fe8ee00423dbc26277dacb9b9b38))

## v0.1.2 (2021-04-30)
### Fix
* Fix directory in zip ([`d8b4fc6`](https://github.com/alandtse/tesla/commit/d8b4fc61ebd49f15ff41b41797f2c9fe1a1a5eb2))

## v0.1.1 (2021-04-30)
### Fix
* Change structure to not override core ([`f173b68`](https://github.com/alandtse/tesla/commit/f173b6823a7c0f259ac2c5a94341820c6ae83fbf))

### Documentation
* Update instructions for upgrading from core ([`3b67b24`](https://github.com/alandtse/tesla/commit/3b67b24460a4c07e75917d0b6dfd9bbb9f2ace5d))

## v0.1.0 (2021-04-29)
### Feature
* Initial commit ([`c12aadf`](https://github.com/alandtse/tesla/commit/c12aadf808053cb67a1fb05d1b95940a0775a889))
