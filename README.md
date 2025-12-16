#   Garden Invasion

Battle endless hordes of zombies launching deadly projectiles—strategically place tough wall-nuts to shield yourself while unleashing rapid-fire counterattacks in this addictive tower defense shooter!

Garden Invasion is a Python implementation with PyGame of space invader using the texture of plants vs zombies.

## How to install the Garden Invasion
You can choose to install it either from *PyPI* or from *GitHub*

### PyPI
to test
```bash
pip install GardenInvasion 
```

### GitHub

#### 1. Clone the repository locally: 
to test
```bash
git clone https://github.com/unibo-dtm-se-2425-GardenInvasion/SoftwareArtifact.git
```     
#### 2. Move into artifact:
```bash
cd artifact
```
#### 3. Install the required dependencies (for tests and not):
```bash
pip install -r requirements.txt
```
Tests reasons:
```bash
pip install -r requirements-dev.txt
```

## How to launch the Garden Invasion

```bash
python -m GardenInvasion
```
This action will execute the file GardenInvasion/__main__.py

## Project structure 
Overview:
```bash
<root directory>
├── GardenInvasion/             # main package 
│   ├── Assets/
│   ├── Controller/
│   ├── Model/
│   ├── View/
│   ├── Utilities/
│   ├── __init__.py         # python package marker
│   └── __main__.py         # application entry point
├── test/                   # test package
├── .github/                # configuration of GitHub CI
│   └── workflows/          # configuration of GitHub Workflows
│       ├── check.yml       # runs tests on multiple OS and versions of Python
│       └── deploy.yml      # if check succeeds, and the current branch is one of {main, master}, triggers automatic releas on PyPi
├── .gitignore              # XXX
├── .python-version         # XXX
├── CHANGELOG.md            # XXX
├── LICENSE                 # license file (Apache 2.0 by default)
├── MANIFEST.in             # file stating what to include/exclude in releases 
├── package-lock.json       # XXX
├── package.json            # XXX
├── pyproject.toml          # declares build dependencies
├── README.md               # XXX
├── release.config.js       # XXX
├── rename-template.sh      # XXX
├── renovate.json           # configuration of Renovate bot, for automatic dependency updates
├── requirements-dev.txt    # declares development dependencies
├── requirements.txt        # declares runtime dependencies
└── setup.py                # configuration of the package to be released on Pypi
```

## Game Controls   
- Move Left:	A ←
- Move Right:	D →	
- Pause Menu	ESC	
- Quit Game:	
    - ESC → Quit → Confirm
    - X button

Notes:
- Wallnuts automatically spawn in 4 defensive slots above the player at game start
- Player auto-shoots projectiles continuously with cooldown
- ESC always shows pause menu during gameplay
- All menus support both keyboard and mouse navigation
- X button or ESC + Quit exits the game with confirmation dialog

## Links 
TO UPDATE ONCE DECIDED WHAT TO ADD HERE
- Report link

## Version History