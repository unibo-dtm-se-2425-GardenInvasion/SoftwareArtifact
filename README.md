# Garden Invasion
A Python implementation with PyGame of space invader using the texture of plants vs zombies.

## Relevant features
FEATURES TO ADD
- All your project code into a single main package (`my_project/`)
- All your project tests into a single test package (`test/`)
- Unit testing support via [`unittest`](https://docs.python.org/3/library/unittest.html)
- Automatic testing on all branches via GitHub Actions
- Semi-automatic versioning via Git
- Packaging support via [`setuptools`](https://setuptools.pypa.io/en/latest/setuptools.html)
- Automatic release on [PyPi](https://pypi.org/) via GitHub Actions
- Docker image support via `Dockerfile`
- Automatic release on [DockerHub](https://hub.docker.com/) via GitHub Actions
- Support for semi-automatic development environment management via [Pyenv](https://github.com/pyenv/pyenv)
- Automatic dependencies updates via [Renovate](https://docs.renovatebot.com/)
- Automatic conversion of `TODO` comments into GitHub issues via the `alstr/todo-to-issue-action`

## Project structure 
TO UPDATE TO THE FINAL PROJECT STRUCTURE INSIDE THE REPOSITORY
OLD ONE - Overview:
```bash
<root directory>
├── my_project/             # main package (should be named after your project)
│   ├── __init__.py         # python package marker
│   └── __main__.py         # application entry point
├── test/                   # test package (should contain unit tests)
├── .github/                # configuration of GitHub CI
│   └── workflows/          # configuration of GitHub Workflows
│       ├── check.yml       # runs tests on multiple OS and versions of Python
│       └── deploy.yml      # if check succeeds, and the current branch is one of {main, master}, triggers automatic releas on PyPi
├── MANIFEST.in             # file stating what to include/exclude in releases 
├── LICENSE                 # license file (Apache 2.0 by default)
├── pyproject.toml          # declares build dependencies
├── renovate.json           # configuration of Renovate bot, for automatic dependency updates
├── requirements-dev.txt    # declares development dependencies
├── requirements.txt        # declares runtime dependencies
├── setup.py                # configuration of the package to be released on Pypi
└── Dockerfile              # configuration of the Docker image to be realsed on Dockerhub
```

## Game Controls   
TO UPDATE ONCE DECIDED THE CONTROLS
- xx

## Links 
TO UPDATE ONCE DECIDED WHAT TO ADD HERE
- Report

## Version History