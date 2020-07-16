import re
import pathlib
import argparse

import numpy as np
import pandas as pd


def adapt_data_pf(path, output_path=None, time_step=None, initial_time=None, final_time=None):
    assert pathlib.Path(path).is_file(), 'Filepath \'{}\' does not exist'.format(path)
    assert path.endswith('.csv'), 'Only .csv files are supported'

    assert isinstance(output_path, str) or output_path is None, 'Path of output must be a string'

    if time_step is not None:
        assert isinstance(time_step, (float, int)) and time_step > 0, 'Time step must be a positive real number'

    if initial_time is not None:
        assert isinstance(initial_time, (float, int)), 'Initial time must be a real number'

    if final_time is not None:
        assert isinstance(final_time, (float, int)), 'Final time must be a real number'

    # Get path where file will be saved
    if output_path:
        output = pathlib.Path(output_path)
        assert output.is_dir(), 'Output path must be a valid directory'
    else:
        output = pathlib.Path(path).parent
    output = output / 'data_from_powerfactory.csv'

    # Get relevant data from file
    pat = re.compile(r'(^\"other\","\s+)(.*)(\"$)')
    with open(path, 'r') as file:
        data = [re.search(pat, row).group(2).split() for row in file.read().split('\n') if re.search(pat, row)]

    # Create dataframe from data
    df = pd.DataFrame(data=[d for d in data if 'Time' not in d], columns=data[0], dtype=float)
    df.set_index('Time', inplace=True)

    # Convert data recorded in degrees to radians and save in new column
    for col in df.columns:
        if '/deg' in col:
            df[col.replace('deg', 'rad')] = df[col]*np.pi/180

    # Get value of initial instant
    t = df.index[0]
    if initial_time is not None:
        t = max(t, initial_time)

    # Get value of final instant
    tf = df.index[-1]
    if final_time is not None:
        tf = min(tf, final_time)

    if time_step is None:
        # If no adjustments in time step are needed, save dataframe in output
        df[(df.index >= t) & (df.index <= tf)].to_csv(output, float_format='%.6f')
    else:
        # Create dataframe for time step adjustments
        df_adj = pd.DataFrame(columns=df.columns)
        df_adj.index.name = df.index.name

        while len(df.loc[df.index > t]) and t <= tf:
            # Get values on dataframe for instants immediately before and after time 't'
            prior = df.loc[df.index <= t].iloc[-1]
            post = df.loc[df.index > t].iloc[0]

            # Interpolate values and save result on adjusted dataframe
            df_adj.loc[t] = prior + (post - prior) * (t - prior.name) / (post.name - prior.name)
            t = round(t + time_step, 6)

        # Save adjusted dataframe in output
        df_adj.to_csv(output, float_format='%.6f')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adapt data exported from DIgSILENT PowerFactory to identpy standard')
    parser.add_argument('filepath', help='Path of datafile exported from PowerFactory', type=str)
    parser.add_argument('-o', '--output', help='Output path', type=str, default=None)
    parser.add_argument('-t', '--time_step', help='Time step between data points', type=float, default=None)
    parser.add_argument('-i', '--initial_time', help='Initial instant of timeseries', type=float, default=None)
    parser.add_argument('-f', '--final_time', help='Final instant of timeseries', type=float, default=None)

    args = parser.parse_args()

    adapt_data_pf(args.filepath, args.output, args.time_step, args.initial_time, args.final_time)
