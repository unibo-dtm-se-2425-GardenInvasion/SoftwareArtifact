## [1.9.3](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.9.2...1.9.3) (2026-07-17)


### Bug Fixes

* **assets:** down-scale oversized background images to actual render size ([b3659e2](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/b3659e2a193d09a73d2bd35e2c24e8839db671ca))
* **assets:** re-encode 9 WebP-as-.png files to genuine PNG ([90b7c75](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/90b7c759eafa48ce216bc7538d189f8e04e4458a))
* **assets:** remove dead wallnut asset, normalize filename capitalization ([4603d8b](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/4603d8ba8cfefa07b0756f533ef1297a3e13e78a))
* **controller:** convert 13 print() calls missed by the earlier logger sweep ([52c46ec](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/52c46ec0caf5870bdb51b254c70d61441c110d1f))


### Performance improvements

* **view:** scale heart icon once per draw_hearts() call, not per heart ([656ec6f](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/656ec6f9bc77b3fc9572dc35b6a5b2a3d45cd2ae))


### Refactoring

* **view:** move pygame.display.flip() responsibility to the controller ([230deea](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/230deea0795eff0c7fecc24fc246053dc9ef63e7))

## [1.9.2](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.9.1...1.9.2) (2026-07-17)


### Bug Fixes

* **deps:** bump handlebars to 4.7.9 to fix AST-injection RCE ([4ae7a12](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/4ae7a129cf0bd9d7c093283abcc12d92e7239b50))
* **view:** remove debug hit-box circle from zombie projectiles ([6045056](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/6045056a3a37a00d95e9e2702197cd76194cf7d9))


### General maintenance

* remove leftover cookiecutter template scaffolding ([494b281](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/494b2815ec9e489f32a833f7f5959b344f4584c0))
* **tests:** drop unused pytest dep, guard visual debug script ([26faf73](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/26faf7379acb88c5c1b4a7ac5e0f61587d4d975a))


### Refactoring

* centralize contact email, fold in a missed blur duplicate ([463fe03](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/463fe038526d3b33675816c24a669b9050f1813f))
* **controller:** collapse the 5 collision-handler functions ([0649088](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/064908842d0dde2650eb51e2e0666f937c64301c))
* **controller:** extract repeated blur-background helper ([1a98725](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/1a987256345db9ea0eedfc4e3a177c4ad98887eb))
* **model:** remove dead code WaveManager.get_wave_info() ([c46196e](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/c46196e2fd6a18a2aa9376f13154f67c2134d40c))
* **model:** share base between GameOverModel and VictoryModel ([66d7e2c](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/66d7e2c7e5995cfe17c5070e278e22ae78f04fc6))
* route print() debug statements through the logger ([6e58a93](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/6e58a9385d045b577725195fda430d8dfbf4fd46))
* **view:** consolidate triplicated draw_selection_arrows() ([8e40c8b](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/8e40c8b1d86d55960433a2cd0fc757fe4dc911c9))
* **view:** consolidate triplicated render_text_with_outline() ([5e54f87](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/5e54f872d141101e016aaae4a06c4ced44b6ffcc))
* **view:** remove dead view modules, wire up zombie projectile draw ([7bd1826](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/7bd1826518e7ef5c5d9300175062835bf67ee0b0))

## [1.9.1](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.9.0...1.9.1) (2026-07-16)


### Bug Fixes

* **ci:** restore GITHUB_TOKEN in release workflow ([ea67066](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/ea67066c206bb934dbb31e89f1d6230b7e8b4df0))
* **controller:** stop re-creating SoundManager in run_game() ([0cf53fc](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/0cf53fc084295d6ffde4b17af802ab18ce26b6cc))
* **model:** propagate sound_manager when placing wall-nuts ([e997ff9](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/e997ff9817ad8e901497700ebc569978c6cb541a))
* **model:** resolve asset sprite paths relative to package, not cwd ([f4eb375](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/f4eb37518231a7474fd30d32f64e3827e109b2a1))
* **model:** stop fire-rate boost expiry from colliding with 0 sentinel ([c7ad736](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/c7ad736909088e3afd52f96f47b1729ac8d206b1))


### Tests

* merge TestWaveManagerVictory into test_wave_model and remove redundant file ([280811e](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/280811ea63f5236f959bada68ae8655c7f726ac9))
* remove duplicate TestWaveManagerVictory file, keep merged copy ([a5ddcef](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/a5ddcef99edf5bef658ab5210cb6fdfe3661c6f0))


### Build and continuous integration

* add TEST_PYPI_API_TOKEN secret to twine upload step ([ebc38b2](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/ebc38b2dcec5025ed2bd56463d37dc4460c27843))


### Style improvements

* clean up comments and remove print statements ([7edf01d](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/7edf01d940e174c6f1a37db3cc11f3674c2bb912))
* remove debug print statements ([e4e9aec](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/e4e9aecea0bf28916e24311e343e62743bb836e1))

## [1.9.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.8.0...1.9.0) (2026-02-22)


### Features

* add power-up system with fire rate boost and wallnut repair ([3837084](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/38370843121cd498a69c60388507e4cd94c13958))


### Documentation

* update root-graph and README links ([71d58be](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/71d58bee2eeeeacb4489489440b1e8b3a1be8e2b))

## [1.8.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.7.1...1.8.0) (2026-02-15)


### Features

* add victory screen with fade-in animation and sound ([97e1e5e](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/97e1e5ebee7b54a56a37be4e3a4d547e2c2bf224))

## [1.7.1](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.7.0...1.7.1) (2026-02-14)


### Bug Fixes

* **ci:** add build and twine to requirements-dev.txt ([2ebc6c8](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/2ebc6c806c169514ffa2c16bb2947ea35e63c03e))

## [1.7.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.6.0...1.7.0) (2026-02-14)


### Features

* add heart display to show player health in game ([5210ce4](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/5210ce44345002b08a7d88d37867ec5310dfa8ff))

## [1.6.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.5.1...1.6.0) (2026-02-12)


### Features

* remove wallnut-projectile collision detection ([0579583](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/0579583f45f6a6fd112df5a1cc633966f4f60b4e))

## [1.5.1](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.5.0...1.5.1) (2026-02-12)


### Bug Fixes

* restore plant shooting cooldown to original ([53e129f](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/53e129fd600e22a885719ac3aa0d88b596dd3c39))


### Tests

* fix plant shooting cooldown test timing ([b2b3b68](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/b2b3b68c5484478bf93e67f264d08d1f5c1acaf0))

## [1.5.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.4.0...1.5.0) (2026-02-05)


### Features

* add sprite rendering for zombies and projectiles ([0fc783b](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/0fc783baaca9e5b95aa4019b26344f88bb814292))


### Tests

* fix zombie and projectile tests for sprite rendering ([958c1de](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/958c1de393e9bc90a3e87a397c9a62fd444f6cdc))
* make zombie parameters optional in draw_game for backward compatibility ([ddf3a54](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/ddf3a54a142b23d53029a4c2ff039ab81f1c1091))

## [1.4.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.3.0...1.4.0) (2026-01-18)


### Features

* add game over screen with fade-in animation ([0fb0b80](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/0fb0b8048836726ee8f222e97741798bb4782f9a))


### General maintenance

* add zombie projectile sprite to assets ([2b91966](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/2b919666ad7f3cc735124dd278e0cddad9b80502))

## [1.3.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.2.0...1.3.0) (2026-01-17)


### Features

* implement zombie projectile → plant collision ([522482f](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/522482fb2f35706fc09be44eeac0b617a14b23e7))

## [1.2.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.1.1...1.2.0) (2026-01-16)


### Features

* implement collision system phase 1 - plant projectile vs zombie ([5b5c6cf](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/5b5c6cf1afe350ffd19960c02a88b22b823d644a))

## [1.1.1](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.1.0...1.1.1) (2026-01-15)


### Documentation

* increase sentence length in options_view.py ([0117e62](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/0117e62b7df402b662a7f40988a379a3067a53fa))
* update README with corrected link ([307ad99](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/307ad99dbca0410428145ba8ce88ae89adcc8e4b))

## [1.1.0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.0.1...1.1.0) (2026-01-15)


### Features

* implement 2-life-point system for plant and wallnuts ([4bdfa60](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/4bdfa605cfbf1a9346266ba79c0fd07e86a97575))


### Bug Fixes

* resolve merge conflicts from feature/wallnut merge ([39fdb62](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/39fdb6209ecd7678c8c61e4f92a6a842b929d21a))

## [1.0.1](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/compare/1.0.0...1.0.1) (2026-01-01)


### Bug Fixes

* **menu:** add mouse hover highlighting for main menu items ([358de4d](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/358de4d0b96b9fdcc4fa875e86b2b22778c00a05))


### Documentation

* **CHANGELOG.md:** clean up CHANGELOG.md and update workflow section ([047dbda](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/047dbda494adf3c7bc9190c68afced9553cb86e0))

## 1.0.0 (2025-12-30)


### Features

* add darker themed backgrounds for improved UI contrast ([130f2e5](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/130f2e53bb99815937a93ac4bf6f8d09194d0c39))
* **audio:** add background music system with volume control ([921ef4e](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/921ef4ec3883cd7e81ec7015dfc0bb975343c7a8))
* **options:** add player skin personalization system ([806eda8](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/806eda8f3874c6258392632d15d36fbfa8e7480d))
* **UI:** add text outline for improved readability on dark backgrounds ([91f991e](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/91f991e767ee1c9501814d37fe06345827ac5b94))


### Bug Fixes

* **ci:** add UTF-8 encoding for Windows test output ([c9bcfff](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/c9bcfff4ed00fcdd4c9eb4d74e0e045405c3ab8a))
* **ci:** handle audio initialization in headless CI environment ([bf995e6](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/bf995e68a89a1e09f83cc4c61550b910c1289bd2))
* **ci:** handle audio initialization in headless CI environment ([9205cb8](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/9205cb8d835f2ab47a937a01ae41dfbfdd3a0851))
* **ci:** use built-in GITHUB_TOKEN for semantic-release ([966fd1c](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/966fd1cbd1041f0bbfb9a9a4457fe7df1386ca48))
* **pause-menu:** fix mouse interaction with pause modal buttons ([5f2011b](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/5f2011b471edecd2474ea70707ee5462d83728d7))
* **pause-menu:** fix mouse interaction with pause modal buttons in rungame ([c22a0d5](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/c22a0d58b7b00506f742fef5ea360d24030ba0b0))


### Documentation

* **readme:** update game description and controls ([d492ca0](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/d492ca055d6b4076ebcdb46a8aab9b922ed5c61d))


### Tests

* **controller:** add controller unit tests covering all game interactions ([dec8c04](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/dec8c04e86ef9486c830cec41c4ce7b4d7726149))
* **model:** add unit tests for menu and options submenu ([c72e009](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/c72e009fc7135c851b35c2525df4611a12ad2fc3))
* **model:** add unit tests for player and projectile model ([9f46b48](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/9f46b481d8126d07b0fd017d100c6ccbfbfd2e31))
* **skin-personalization:** add comprehensive unit tests for skin selection feature ([4e6039f](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/4e6039f1b5796e3f9b38ddfd0b2bf473c70584b5))
* **view:** add unit tests for view rendering components ([1845ba1](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/1845ba1f4fdfc31a8df77333a64a46f8e1b0fad7))


### Build and continuous integration

* add required permissions to deploy job ([8d95815](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/8d9581537a2278da505525fbaca1780c483aaa4e))


### General maintenance

* **project:** rename main folder to GardenInvasion ([169ab03](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/169ab03ae228ac004acc02c196cf25f267dc8a60))
* **workflow:** update Python versions and Actions ([8745c9e](https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact/commit/8745c9e253c0c82073af02fc79ac1ce9bc8dfa16))
