#!/usr/bin/python3

from pathlib import Path
from datetime import datetime
import stat
import os
import argparse


def main():
    global args
    args = parse_cmd()
    call_list_files(args.FILE)


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recursive",
                        help="If given, the `-r` option will make `mini-ls` "
                             "run recursively on any directory it comes "
                             "across.",
                        action="store_true")
    parser.add_argument("--FILE",
                        nargs='*',
                        help="FILE can be zero or more arguments. If zero args"
                             " are given, `mini-ls` will list information "
                             "about the current directory.")
    args = parser.parse_args()
    return args


def call_list_files(path_list):
    if path_list is None:
        list_files('.')
    else:
        for path in path_list:
            print("\n" + path + ":")
            list_files(path)


def list_files(path):
    entries = Path(path)
    try:
        for entry in entries.iterdir():
            print_files_in_path(path, entry)
            if entry.is_dir() and args.recursive:
                list_files(entry)
    except PermissionError as pe:
        print("ERROR:", pe)
    except FileNotFoundError as ff:
        print("ERROR:", ff)


def print_files_in_path(path, entry):
    file_time = convert_date(entry.stat().st_mtime)
    try:
        file_permission = oct(stat.S_IMODE(os.stat(entry).st_mode))[-3:]
        print(file_permission, entry.owner(), file_time, entry)
    except PermissionError as pe:
        print("ERROR:", entry, pe)


def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%b %d %Y %H:%M')
    return formated_date


main()
