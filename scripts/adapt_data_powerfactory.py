import argparse
import pandas as pd


def adapt_data_pf(path):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adapt data exported from DIgSILENT PowerFactory to identpy standard')
    parser.add_argument('filepath', help='Path of datafile exported from PowerFactory', type=argparse.FileType('r'))

    args = parser.parse_args()
    adapt_data_pf(args.filepath)
