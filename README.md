# advent-of-code2021

my Advent of code 2021 solutions

## Add solution, test and input files for today

```
./new-day.sh
```

## Run unittests:

_Tests are enabled for day 3 and after_

```
./run-tests.sh -vk _${day}
```

`day` is a day number, eg. 7 or 11, but the options can be omitted as well.
In that case, solutions for all days are tested.

## Run today’s example

```
solutions/day${day}.py -v inputs/${day}.example
```

## Go for today’s solution

```
solutions/day${day}.py -v inputs/${day}.txt
```
