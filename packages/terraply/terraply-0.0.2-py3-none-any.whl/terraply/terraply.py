#!/usr/bin/env python

import argparse
import fnmatch
import os
import re
import subprocess
import sys

parser = argparse.ArgumentParser(prog='Terraply')
parser.add_argument('-target', action='append', type=str,
                    help="A globable list of targets. If ommitted all targets will be considered.")
parser.add_argument('-exclude', action='append', type=str,
                    help="A globable list of targets to exclude")
parser.add_argument('-summary', nargs='?', const=1, type=int,
                    help="Does not print apply output over the specified amount")

def main():
    # Get the arguments
    args, unknownargs = parser.parse_known_args()

    # List the state
    output = subprocess.run(["terraform", "state", "list"], stdout=subprocess.PIPE)
    original_state_list = set(output.stdout.decode('utf-8').split())

    # Remove anything that matches data
    original_state_list.difference_update(set(fnmatch.filter(list(original_state_list), '*data.*')))

    # Glob the targets to filter the state
    filtered_state_list = set()
    if args.target:
        for t in args.target:
            # Terraform syntax adds an implicit wildcard to the end
            filtered_state_list.update(fnmatch.filter(original_state_list, t+'*'))
    else:
        filtered_state_list.update(original_state_list)

    # Exclude any that match the exclude glob
    if args.exclude:
        for e in args.exclude:
            # Terraform syntax adds an implicit wildcard to the end
            filtered_state_list.difference_update(set(fnmatch.filter(list(filtered_state_list), e+'*')))

    # Reduce state to least common denominator

    #break the original list into key value pairs then the filtered list into key value pairs
    original_dict = {}
    for x in original_state_list:
        PATTERN = re.compile(r'''((?:[^\."']|"[^"]*"|'[^']*')+)''')
        a = PATTERN.split(x)[1::2]
        #a = x.split('.')
        for i in range(2, len(a)+1):
            root = '.'.join(a[:i])
            if root not in original_dict:
                original_dict[root] = set()

            original_dict[root].add(x)

    filtered_dict = {}
    for x in filtered_state_list:
        PATTERN = re.compile(r'''((?:[^\."']|"[^"]*"|'[^']*')+)''')
        a = PATTERN.split(x)[1::2]
        for i in range(2, len(a)+1):
            root = '.'.join(a[:i])
            if root not in filtered_dict:
                filtered_dict[root] = set()

            filtered_dict[root].add(x)

    simplify_list = []
    for key in filtered_dict:
        if len(filtered_dict[key]) == len(original_dict[key]):
            simplify_list.append(key)

    # Now because we know all of these are simplifiable if the parent is in the list than it can
    # be blindly removed
    simplest_list = []
    for s in simplify_list:
        PATTERN = re.compile(r'''((?:[^\."']|"[^"]*"|'[^']*')+)''')
        a = PATTERN.split(s)[1::2]

        # if you parent is in the list remove don't add yourself
        if '.'.join(a[:-1]) not in simplify_list:
            simplest_list.append(s)

    targets = []
    for n in simplest_list:
        targets.append('-target')
        targets.append(n)

    command = ["terraform"] +  unknownargs +  targets

    # Call terraform with the new target list
    if args.summary:
        with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            waiting = False
            line_buf = ""
            line_count = 0
            for line in p.stdout:
                if waiting:
                    if "  # " in line or "Plan" in line:
                        if line_count > args.summary:
                            pass
                            #sys.stdout.write("    Skipping long change summary...")
                        else:
                            sys.stdout.write(line_buf)

                        sys.stdout.write(line)

                        if "Plan" in line:
                            waiting= False
                            line_buf = ""
                            line_count = 0
                        else:
                            line_buf = ""
                            line_count = 0
                    else:
                        line_buf += line
                        line_count += 1
                else:
                    if "  # " in line:
                        sys.stdout.write(line)
                        waiting=True
                        line_buf = ""
                        line_count = 0
                    else:
                        sys.stdout.write(line)
    else:
        subprocess.run(command)

if __name__ == "__main__":
    main()

