import re
import pathlib
import argparse

import pandas as pd


def adapt_data_pf(path, output_path=None, time_step=None, initial_time=0, final_time=1):
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

    pat = re.compile(r'(^\"other\","\s+)(.*)(\"$)')
    with open(path, 'r') as file:
        data = [re.search(pat, row).group(2).split() for row in file.read().split('\n') if re.search(pat, row)]

    cols = data[0]
    data = [d for d in data if 'Time' not in d]

    df1 = pd.DataFrame(data, columns=cols, dtype=float)
    df1.set_index('Time', inplace=True)

    df1.to_csv(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adapt data exported from DIgSILENT PowerFactory to identpy standard')
    parser.add_argument('filepath', help='Path of datafile exported from PowerFactory', type=str)
    parser.add_argument('-o', '--output', help='Output path', type=str, default=None)
    parser.add_argument('-t', '--time_step', help='Time step between data points', type=float, default=None)

    args = parser.parse_args()

    adapt_data_pf(args.filepath, args.output, args.time_step)
