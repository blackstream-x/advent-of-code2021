#!/bin/bash

day=$(date +%d | bc)

todays_solution=solutions/day${day}.py

if [ -f ${todays_solution} ] ; then
    echo "${todays_solution} already exists!"
else
    cp -p solutions/template.py ${todays_solution}
fi
