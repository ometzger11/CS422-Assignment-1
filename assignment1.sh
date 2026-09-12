#!/bin/sh

VENV_DIR="./pyenv"

if [ ! -d $VENV_DIR ]; then
	echo "First Run Setup"
	echo "===============\n"

	echo "Creating Python Virtual Enviroment"
	python3 -m venv $VENV_DIR

	echo "Installing dependencies"
	$VENV_DIR/bin/pip install geopy geonamescache numpy matplotlib

	echo "Done with first run setup\n"
fi

echo "Running Part 1"
echo "==============\n"

$VENV_DIR/bin/python3 ping.py

echo
echo "Running Part 2"
echo "==============\n"

$VENV_DIR/bin/python3 traceroute_plot.py
