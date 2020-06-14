import re
import pathlib
import argparse

import pandas as pd


def adapt_data_pf(path, output_path=None):
    df = pd.read_csv(path, header=None)
    df = df[df[0] == 'other']
    df = df[df[1].str.startswith(' ')]

    df.reset_index(drop=True, inplace=True)

    data = df[1].to_list()
    data = [re.sub(r'^\s+', '', d) for d in data]
    data = [re.sub(r'\s+', ',', d) for d in data]

    if output_path:
        output_file = output_path / 'data_from_powerfactory.csv'
    else:
        output_file = 'data_from_powerfactory.csv'

    with open(output_file, 'w+') as f:
        print('% ' + data[0], file=f)
        for row in data[1:]:
            if row.startswith('Time'):
                continue
            print(row, file=f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adapt data exported from DIgSILENT PowerFactory to identpy standard')
    parser.add_argument('filepath', help='Path of datafile exported from PowerFactory', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output', help='Output path')

    args = parser.parse_args()

    if args.output:
        output = pathlib.Path(args.output)
        assert output.is_dir(), 'Output path must be a valid directory'
    else:
        dir_ = pathlib.Path(args.filepath.name)
        output = dir_.parent

    adapt_data_pf(args.filepath, output)
