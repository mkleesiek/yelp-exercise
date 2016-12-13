import JsonToCsvConverter
import tarfile
import argparse
import sys
import os
import re

if __name__ == '__main__':
    """Open a yelp dataset TAR file and convert JSON entries to CSV files."""

    if sys.version_info[0] != 3:
        print("This script requires Python 3")
        exit()

    parser = argparse.ArgumentParser(
        description='Convert Yelp Dataset Challenge TAR file to single CSV files.'
    )

    parser.add_argument(
        'tar_file',
        type=str,
        help='The TAR file to convert.'
    )

    args = parser.parse_args()

    tar_file = args.tar_file
    dest_dir = os.path.join(os.path.dirname(tar_file), tar_file.split('.')[0])
    os.makedirs(dest_dir, exist_ok=True)

    print('Reading TAR file: {0} ...'.format(tar_file))
    print('Output directory: {0}'.format(dest_dir))

    tar = tarfile.open(tar_file)
    for member in tar.getmembers():

        filename = member.name.lower()

        if not filename.endswith('.json'):
            continue

        base = re.split('[\W_]+', filename)[-2]

        print('Parsing TAR entry {0} ...'.format(member.name))
        json_file = tar.extractfile(member)

        csv_file = os.path.join(dest_dir, '{0}.csv'.format(base))
        column_names = JsonToCsvConverter.get_superset_of_column_names_from_file(json_file, 1000, 1)
        json_file.seek(0)
        number_of_lines = JsonToCsvConverter.read_and_write_file(json_file, csv_file, column_names)
        print('  {0} lines written to {1}.csv.'.format(number_of_lines, base))

    tar.close()
