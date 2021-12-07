#!/bin/bash

if [ -z "$1" ] ; then
    day=$(date +%d | bc)
else
    day=$(echo $1 | bc)
fi

todays_solution=solutions/day${day}.py

if [ -f ${todays_solution} ] ; then
    echo "${todays_solution} already exists!"
else
    sed "s/\$DAY/${day}/g" solutions/template > ${todays_solution}
    chmod +x ${todays_solution}
fi

todays_test=tests/test_${day}.py

if [ -f ${todays_test} ] ; then
    echo "${todays_test} already exists!"
else
    sed "s/\$DAY/${day}/g" tests/template > ${todays_test}
fi

todays_example_input=inputs/${day}.example
todays_puzzle_input=inputs/${day}.txt

touch ${todays_example_input}
touch ${todays_puzzle_input}
