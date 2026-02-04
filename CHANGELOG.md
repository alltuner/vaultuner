# Changelog

## [0.1.8](https://github.com/alltuner/vaultuner/compare/v0.1.7...v0.1.8) (2026-02-04)


### Miscellaneous Chores

* **deps:** update actions/checkout action to v6 ([#30](https://github.com/alltuner/vaultuner/issues/30)) ([88f2170](https://github.com/alltuner/vaultuner/commit/88f21709566826128cb99cbc5bbab3119a9f1f90))
* **deps:** update astral-sh/setup-uv action to v7 ([#31](https://github.com/alltuner/vaultuner/issues/31)) ([92128d0](https://github.com/alltuner/vaultuner/commit/92128d003dcf47544e47b912bd1b064ce43e907d))


### Documentation Updates

* use custom domain vaultuner.alltuner.com ([#32](https://github.com/alltuner/vaultuner/issues/32)) ([b703bc7](https://github.com/alltuner/vaultuner/commit/b703bc77155fa988e1d0fc44941b77942fcda098))

## [0.1.7](https://github.com/alltuner/vaultuner/compare/v0.1.6...v0.1.7) (2026-02-04)


### Documentation Updates

* add --python 3.12 flag to install commands ([#28](https://github.com/alltuner/vaultuner/issues/28)) ([978d997](https://github.com/alltuner/vaultuner/commit/978d997cfd601e012b83dbe800e506a0e212b460))

## [0.1.6](https://github.com/alltuner/vaultuner/compare/v0.1.5...v0.1.6) (2026-02-04)


### Bug Fixes

* trigger PyPI publish from release-please outputs ([#26](https://github.com/alltuner/vaultuner/issues/26)) ([9ce8d5c](https://github.com/alltuner/vaultuner/commit/9ce8d5c8cb6a37aab1b5ad7155006ac408f8caf6))

## [0.1.5](https://github.com/alltuner/vaultuner/compare/v0.1.4...v0.1.5) (2026-02-04)


### Bug Fixes

* security review fixes and PyPI release setup ([#20](https://github.com/alltuner/vaultuner/issues/20)) ([d7bc294](https://github.com/alltuner/vaultuner/commit/d7bc2949d0ae4eb70b7044a76e846d18fa681773))


### Miscellaneous Chores

* **deps:** update actions/setup-python action to v6 ([#21](https://github.com/alltuner/vaultuner/issues/21)) ([206bd4e](https://github.com/alltuner/vaultuner/commit/206bd4e9dd44bbbae53d876e10fdca9ca32bf9cb))
* **deps:** update actions/upload-pages-artifact action to v4 ([#22](https://github.com/alltuner/vaultuner/issues/22)) ([595bcd9](https://github.com/alltuner/vaultuner/commit/595bcd9139199f5f1798b379c7e4c06844aad744))
* ignore Python version in Renovate ([#24](https://github.com/alltuner/vaultuner/issues/24)) ([36bd468](https://github.com/alltuner/vaultuner/commit/36bd4681a8a016f1f38b09c9f3f36f8ee0c65231))


### Documentation Updates

* add credits ([#25](https://github.com/alltuner/vaultuner/issues/25)) ([89223d4](https://github.com/alltuner/vaultuner/commit/89223d492bc2ab8dc46198120d4d47722812007e))

## [0.1.4](https://github.com/alltuner/vaultuner/compare/v0.1.3...v0.1.4) (2026-02-04)


### Bug Fixes

* check for darwin before using keyring ([#14](https://github.com/alltuner/vaultuner/issues/14)) ([56d79a4](https://github.com/alltuner/vaultuner/commit/56d79a48fa35b86ecb5cd91c7f60e52152881ec7))


### Miscellaneous Chores

* bump dev dependencies ([#17](https://github.com/alltuner/vaultuner/issues/17)) ([1eeae06](https://github.com/alltuner/vaultuner/commit/1eeae069f26e6ab59b7278b8345e32498bb6b5f8))
* **deps:** update actions/checkout action to v6 ([#19](https://github.com/alltuner/vaultuner/issues/19)) ([89b5987](https://github.com/alltuner/vaultuner/commit/89b598732c2a355ace9953f506974ab75bb054dd))


### Documentation Updates

* prepare for release with license, readme, and mkdocs ([#16](https://github.com/alltuner/vaultuner/issues/16)) ([bed5d27](https://github.com/alltuner/vaultuner/commit/bed5d27b9e58251a7ab133117098b0f246d1f751))

## [0.1.3](https://github.com/alltuner/vaultuner/compare/v0.1.2...v0.1.3) (2026-02-04)


### Code Refactoring

* batch import after collecting user choices ([#10](https://github.com/alltuner/vaultuner/issues/10)) ([ae28d25](https://github.com/alltuner/vaultuner/commit/ae28d25ac3ae4c9fefed917aa61be71fe12657f6))
* use single 'vaultuner' project for all secrets ([#12](https://github.com/alltuner/vaultuner/issues/12)) ([7a8cd32](https://github.com/alltuner/vaultuner/commit/7a8cd32be3f468fd2b8887ef8614a22b52e1d411))

## [0.1.2](https://github.com/alltuner/vaultuner/compare/v0.1.1...v0.1.2) (2026-02-04)


### Features

* add --version flag to CLI ([#9](https://github.com/alltuner/vaultuner/issues/9)) ([a0ba157](https://github.com/alltuner/vaultuner/commit/a0ba157d79977c1dd348442233010551223d4924))
* add import command to load secrets from .env file ([#7](https://github.com/alltuner/vaultuner/issues/7)) ([c58a0e6](https://github.com/alltuner/vaultuner/commit/c58a0e6926ecd0e14b37e986f897ec9850aa2a59))

## [0.1.1](https://github.com/alltuner/vaultuner/compare/v0.1.0...v0.1.1) (2026-02-04)


### CI/CD Changes

* add prek and pre-commit config ([#3](https://github.com/alltuner/vaultuner/issues/3)) ([d42ec4a](https://github.com/alltuner/vaultuner/commit/d42ec4a57fc5893d9deea18cf9032ef9a9af3593))
* add release-please and README ([8f2c3e4](https://github.com/alltuner/vaultuner/commit/8f2c3e4f8685b700935912263905c394e472585c))


### Tests

* add comprehensive test suite with pytest ([a58cdcc](https://github.com/alltuner/vaultuner/commit/a58cdcc61833c8c6315a7e520269a6c1739a5529))
