# -*- coding: utf-8 -*-
"""Convert the Yelp Dataset Challenge dataset from json format to csv.

Copyright 2011 Yelp

Modified from:
  https://github.com/Yelp/dataset-examples/blob/master/json_to_csv_converter.py

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.
See the License for the specific language governing permissions and
limitations under the License.

For more information on the Yelp Dataset Challenge please visit http://yelp.com/dataset_challenge

"""
import argparse
import collections
import csv
import sys
import simplejson as json


def read_and_write_file(json_in, csv_out, column_names):
    """Read in the json dataset file and write it out to a csv file, given the column names."""

    if type(json_in) == str:
        json_in = open(json_in)

    if type(csv_out) == str:
        csv_out = open(csv_out, 'w')

    sorted_col_names = list(column_names)
    sorted_col_names.sort()

    csv_file = csv.writer(csv_out)
    csv_file.writerow(sorted_col_names)

    c = 0

    for line in json_in:
        line_contents = json.loads(line)
        csv_file.writerow(get_row(line_contents, sorted_col_names))
        c += 1

    return c


def get_superset_of_column_names_from_file(json_in, max_lines = -1, max_depth = -1):
    """Read in the json dataset file and return the superset of column names."""
    column_names = set()

    if type(json_in) == str:
        json_in = open(json_in)

    c = 0

    for line in json_in:

        if max_lines > 0 and c > max_lines:
            break
        c += 1

        line_contents = json.loads(line)
        column_names.update(
            set(get_column_names(line_contents, max_depth = max_depth).keys())
        )

    return column_names


def get_column_names(line_contents, parent_key='', depth = 0, max_depth = -1):
    """Return a list of flattened key names given a dict.

    Example:

        line_contents = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }

        will return: ['a.b', 'a.c']

    These will be the column names for the eventual csv file.

    """
    column_names = []
    for k, v in line_contents.items():
        column_name = "{0}.{1}".format(parent_key, k) if parent_key else k
        if isinstance(v, collections.MutableMapping):
            if (max_depth < 0 or depth < max_depth):
                column_names.extend(
                    get_column_names(v, parent_key=column_name, depth = depth+1, max_depth=max_depth).items()
                )
            else:
                column_names.append((column_name, v))
        else:
            column_names.append((column_name, v))
    return dict(column_names)


def get_nested_value(d, key):
    """Return a dictionary item given a dictionary `d` and a flattened key from `get_column_names`.

    Example:

        d = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        key = 'a.b'

        will return: 2

    """
    if '.' not in key:
        if key not in d:
            return None
        return d[key]
    base_key, sub_key = key.split('.', 1)
    if base_key not in d:
        return None
    sub_dict = d[base_key]
    return get_nested_value(sub_dict, sub_key)


def get_row(line_contents, column_names):
    """Return a csv compatible row given column names and a dict."""
    row = []
    for column_name in column_names:
        line_value = get_nested_value(
            line_contents,
            column_name,
        )
        if isinstance(line_value, str):
            row.append('{0}'.format(line_value.encode('utf-8')))
        elif line_value is not None:
            row.append('{0}'.format(line_value))
        else:
            row.append('')
    return row


if __name__ == '__main__':
    """Convert a yelp dataset file from json to csv."""

    if sys.version_info[0] != 3:
        print("This script requires Python 3")
        exit()

    parser = argparse.ArgumentParser(
        description='Convert Yelp Dataset Challenge data from JSON format to CSV.',
    )

    parser.add_argument(
        'json_file',
        type=str,
        help='The json file to convert.',
    )

    args = parser.parse_args()

    json_file = args.json_file
    csv_file = '{0}.csv'.format(json_file.split('.json')[0])

    column_names = get_superset_of_column_names_from_file(json_file)
    read_and_write_file(json_file, csv_file, column_names)