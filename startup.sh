#!/bin/bash

cd ~/Desktop/IoT/
source ./venv/bin/activate
sudo python3 home.py & sudo python3 weather.py & sudo python3 door.py
