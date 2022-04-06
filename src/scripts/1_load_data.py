import argparse
from data import load_data, preprocess
from utils.constants import *






def main(args):
    args = vars(args)
    print('Running main',args)

    load_data.fetch_data_from_local(folder='data/raw_mat/', pattern='LLV', )
    dfBpAll, dfImuAll = load_data.load_dataframe_from_mat(folder='data/raw_mat/', pattern='LLV')

    dfAll = preprocess.merge_imu_vcg_with_heartbeats(dfBpAll, dfImuAll)
    if args['output.file_type'] == 'csv':
        dfAll.to_csv(path=args['output.file_path'])
    elif args['output.file_type'] == 'pickle':
        dfAll.to_pickle(path=args['output.file_path'])
    # dfAll = load_data.load_dataframe_from_pickle(folder='data/interim/', pattern='LLV')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='A tutorial of argparse!')

    parser.add_argument("--download.source", default='local', type=str, help="This is the folder in which to search")
    parser.add_argument("--download.out_folder", default=f'{os.environ["PROJECT_PATH"]}/data/raw', type=str, help="This is the folder in which to search")
    parser.add_argument("--input.folder", default=f'{os.environ["PROJECT_PATH"]}/data/raw', type=str, help="This is the folder in which to search")
    parser.add_argument("--input.pattern", default=load_data.FILE_PATTERN_MAT, type=str, help="This is the file regex pattern to use when searching for files")
    parser.add_argument("--input.limit_files", default=10, type=int, help="This is the limit_files variable")
    parser.add_argument("--preprocess.type", default='merge_imu_vcg_with_heartbeats', type=str, help="This is the preprocess type variable")
    parser.add_argument("--output.file_type", default='pickle', type=str, help="Output file type")
    parser.add_argument("--output.file_path", default=f'{os.environ["PROJECT_PATH"]}/data/unnamed.processed-data.pickle', type=str, help="Output file path")

    args = parser.parse_args()

    main(args)