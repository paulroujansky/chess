[![unit-tests](https://github.com/paulroujansky/chess/actions/workflows/main.yml/badge.svg)](https://github.com/paulroujansky/chess/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/paulroujansky/chess/branch/master/graph/badge.svg)](https://codecov.io/gh/paulroujansky/chess)

# <img src="static/img/chess_pieces/black_knight.png" style="vertical-align:middle" height=33 /> <span style="">Chess engine</span>

This repository contains code that enables to play chess against a computer.

# Installation

## Clone the repository

Use the following command to clone the repository with HTTPS:

    git clone https://github.com/paulroujansky/chess.git

or the following command with SSH:

    git clone git@github.com:paulroujansky/chess.git


## Set up a virtual environment

Use the following command to set up a new virtual environment:

    python -m venv venv
    source venv/bin/activate


## Install dependencies

Use the following command to install dependencies:

    pip install -r requirements.txt


# Usage

## CLI

Install the following requirements:

    pip install -r requirements-mpl.txt

Use the following command to run an example game (computer vs computer):

    python example_game.py

Use the following command to play against computer using CLI:

    python example_game_human.py

## GUI

Install the following requirements:

    pip install -r requirements-qt.txt

Use the following command to play against computer (or human) using GUI:

    python gui_qt.py

# Contribution guidelines

## Tests

Before committing, from within the main directory, run:

    python -m pytest

This will run [`pytest`](https://docs.pytest.org/en/latest/), and run all the existing unit tests to make sure you haven't broken any of the existing codebase.

## Code formatting

Before committing, from within the main directory, run the following in order to format the code with [Black](https://github.com/psf/black):

    black .

## Notes

Sounds were picked from [chess.com](https://www.chess.com/).


# To-do :memo:
- [ ] package repo
- [ ] add unit tests
- [ ] enable to play back a party from history
- [ ] add basic strategy
