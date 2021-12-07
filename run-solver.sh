#!/bin/bash

exit_usage() {
    cat <<EOF
Usage: $0 [ -h ] [ -e ] [ -v ] [ date ]

Positional argument:
    date
        If provided, run the solver for the given day instead of today

Options:
    -h
        Show this help message and exit
    -e
        Use example data instead of the real puzzle data
    -v
        Show debug messages

EOF
    exit 0
}

example_data="false"
verbose=""

while getopts ":hev" opt ; do
    case $opt in
        h)
            exit_usage
            ;;
        e)
            example_data="true"
            ;;
        v)
            verbose="-v"
            ;;
        ?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done

shift $((OPTIND - 1))

if [ -z "$1" ] ; then
    day=$(date +%d | bc)
else
    day=$(echo $1 | bc)
fi

if ${example_data} ; then
    data_file="inputs/${day}.example"
else
    data_file="inputs/${day}.txt"
fi

command="$(echo solutions/day${day}.py ${verbose} "${data_file}")"

echo "Running command: ${command}"
echo

${command}
exit $?
