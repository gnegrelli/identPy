import re
import pathlib
import argparse

import pandas as pd


def adapt_data_pf(path, output_path=None, time_step=None):
    assert pathlib.Path(path).is_file(), 'Filepath \'{}\' does not exist'.format(path)
    assert path.endswith('.csv'), 'Only .csv files are supported'

    assert isinstance(output_path, str) or output_path is None, 'Path of output must be a string'

    assert isinstance(time_step, float) and time_step > 0, 'Value of time step must be a positive real number'

    # Get path where file will be saved
    if output_path:
        output = pathlib.Path(output_path)
        assert output.is_dir(), 'Output path must be a valid directory'
    else:
        output = pathlib.Path(path).parent
    output = output / 'data_from_powerfactory.csv'

    df = pd.read_csv(path, header=None)
    df = df[(df[0] == 'other') & (df[1].str.startswith(' '))]

    df.reset_index(drop=True, inplace=True)

    data = df[1].to_list()
    data = [re.sub(r'^\s+', '', d) for d in data]
    data = [re.sub(r'\s+', ',', d) for d in data]

    with open(output, 'w+') as f:
        print('% ' + data[0], file=f)
        for row in data[1:]:
            if row.startswith('Time'):
                continue
            print(row, file=f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adapt data exported from DIgSILENT PowerFactory to identpy standard')
    parser.add_argument('filepath', help='Path of datafile exported from PowerFactory', type=str)
    parser.add_argument('-o', '--output', help='Output path', type=str, default=None)
    parser.add_argument('-t', '--time_step', help='Time step between data points', type=float, default=None)

    args = parser.parse_args()

    adapt_data_pf(args.filepath, args.output, args.time_step)
