#!/bin/bash

while [ true ]
do  
    wget -q -O bg.jpg $(python scraper.py) 
    feh --bg-fill bg.jpg
    rm bg.jpg
    sleep 600
done