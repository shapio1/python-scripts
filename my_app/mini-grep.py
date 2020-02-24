#!/usr/bin/python3

import re
import argparse
import sys
import fileinput


def main():
    parse_cmd()
    check_regex(pattern)
    call_search_file(files_list)


def parse_cmd():
    global files_list
    global pattern
    global omits_line_num
    parser = argparse.ArgumentParser()
    parser.add_argument("-q",
                        help="If given, the `-q` options only outputs lines"
                             " but omits the matching line numbers.",
                        action="store_true")
    parser.add_argument("--FILE",
                        nargs='*',
                        help="FILE can be zero or more arguments. If zero args"
                             " are given, `mini-grep` will parse entries from "
                             "the standard input.")
    parser.add_argument("-e", help="PATTERN has to be a valid regex")
    args = parser.parse_args()
    pattern = args.e
    omits_line_num = args.q
    files_list = args.FILE


def check_regex(regex_string):
    try:
        re.compile(regex_string)
    except re.error:
        print('ERROR: invalid regex: {}: {}'.format(regex_string, re.error))
        sys.exit()


def call_search_file(files_list):
    if files_list is None:
        search_file('-', pattern, omits_line_num)
    else:
        for file in files_list:
            search_file(file, pattern, omits_line_num)


def search_file(file, pattern_to_search, omits_line_num):
    try:
        for line in fileinput.input(file):
            line = line.strip()
            if re.search(pattern_to_search, line):
                if omits_line_num:
                    print(line)
                else:
                    print(fileinput.filelineno(), line)
        fileinput.close()
    except FileNotFoundError as file_error:
        print("ERROR:", file_error)
    except OSError as os_error:
        print("ERROR:", os_error)


main()
