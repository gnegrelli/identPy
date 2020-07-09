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
    cols = data[0].split()
    data = [d.split() for d in data if 'Time' not in d]

    with open(output, 'w+') as f:
        print('% ' + ','.join(cols), file=f)
        for row in data:
            print(','.join(row), file=f)

    df1 = pd.DataFrame(data, columns=cols, dtype=float)

    df1.set_index('Time', inplace=True)
    print(df1.head())

    t = df1.index[0] + time_step
    while len(df1.loc[df1.index > t]):
        print(t)
        A = df1.loc[df1.index <= t].iloc[-1]
        B = df1.loc[df1.index > t].iloc[0]
        print(A.name, B.name)
        print(A)
        print(B)
        print(A + (B - A) * (t - A.name) / (B.name - A.name))
        print(30 * '~')
        t += time_step


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adapt data exported from DIgSILENT PowerFactory to identpy standard')
    parser.add_argument('filepath', help='Path of datafile exported from PowerFactory', type=str)
    parser.add_argument('-o', '--output', help='Output path', type=str, default=None)
    parser.add_argument('-t', '--time_step', help='Time step between data points', type=float, default=None)

    args = parser.parse_args()

    adapt_data_pf(args.filepath, args.output, args.time_step)
