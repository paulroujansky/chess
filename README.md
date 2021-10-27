# Chess game

This repository contains code that enables to play chess against a computer.

# Installation

## Clone the repository

Use the following command to clone the repository with HTTPS:
```
git clone https://github.com/paulroujansky/chess.git
```

or the following command with SSH:
```
git clone git@github.com:paulroujansky/chess.git
```

## Set up a virtual environment

Use the following command to set up a new virtual environment:
```
python -m venv venv
source venv/bin/activate
```

## Install dependencies

In order to install them manually, run the following command:
```
pip install -r requirements.txt
```

# Run an example

Run the following command to run an example game (computer vs computer):
```
python example_game.py
```

# Contribution guidelines

## Tests

Before committing, from within the main directory, run:

```
python -m pytest
```

This will run [`pytest`](https://docs.pytest.org/en/latest/), and run all the existing unit tests to make sure you haven't broken any of the existing codebase.

# To-do :memo:
- add tests
- add a GUI
- enable to play back a party from history
- add basic strategy
