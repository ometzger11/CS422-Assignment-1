#!/bin/sh

VENV_DIR="./pyenv"

if [ ! -d $VENV_DIR ]; then
	echo "First run: Creating Python Virtual Enviroment"
	python3 -m venv $VENV_DIR

	echo "Installing dependencies"
	$VENV_DIR/bin/pip install geopy geonamescache numpy matplotlib

	echo "Done with first-time setup\n"
fi

echo "Run ping"
echo "Run traceroute"
