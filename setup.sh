#!/bin/bash

echo "Vorbereitung des Systems..."
sudo apt-get update
sudo apt-get install -y python3-venv python3-dev build-essential cmake libglib2.0-dev libgirepository1.0-dev libcairo2-dev

#echo "Erstellen eines virtuellen Umfelds..."
#python3 -m venv venv

#echo "Aktivieren des virtuellen Umfelds..."
#source venv/bin/activate

echo "Pip und Setuptools aktualisieren..."
pip3 install --upgrade pip setuptools

echo "Installieren von scikit-build und Cython..."
pip3 install scikit-build cython

echo "Installieren der Abhängigkeiten..."
pip3 install -r requirements.txt

echo "Setup abgeschlossen. Du kannst jetzt die Anwendung starten."
