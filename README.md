# advent-of-code2021

My Advent of Code 2021 solutions

## Add solution, test and input files for today

```
./new-day.sh
```

## Run unittests

_Tests are enabled for day 3 and after. This script simply wraps the command `python3 -m unittest dicover`._

```
./run-tests.sh [ -v ] [ -f ] [ -k _${day} ]
```

- `-v` produces verbose output
- `-f` fails fast
- `-k _${day}`: if a numerical value is substituted for `${day}`, the tests are run for that day only.

If the `-k …` filter option is omitted, all defined tests are run.

## Run solver

```
./run-solver.sh [ -v ] [ -e ] [ day ]
```

- `-v` produces verbose output (loglevel `DEBUG`)
- `-e` runs the solver with the example data
- `day`: if a numerical value is provided, the solver runs for that day instead of **today**.

## My results

- Succeeded in days 1-14
- Failed to find an own solution for day 15 part 1,
  adapted the solution from <https://github.com/macobo/aoc-2021/>
- Succeeded in day 16, 17 and 18
- Left day 19 for later
- Succeeded in day 20, but …

