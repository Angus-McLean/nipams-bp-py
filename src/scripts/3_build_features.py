import argparse
from data import load_data
from features import tsfel_vectorizer


def main(args):
    args = vars(args)
    dfAll = load_data.load_dataframe_from_pickle(path=args['input.file_path'])
    
    dfVectors = tsfel_vectorizer.panelTSDataToVectors(dfAll, domains=args['feature.domains'])
    
    dfVectors.reset_index().to_feather(path=f"{args['output.file_path']}.feather")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Input time series dataset and calculate appropriate features!')

    parser.add_argument("--input.file_path", default=f'data/interim/unnamed.processed-data.pickle', type=str, help="This parameter points to the specific preprocessed dataset file")
    # parser.add_argument("--feature.type", default='merge_imu_vcg_with_heartbeats', type=str, help="Overarching type of featurizing being calculated")
    parser.add_argument("--feature.domains", default=['statistical'], type=list, nargs='+', help="Generic feature generation domains array")
    parser.add_argument("--output.file_path", default='data/vectors/unnamed.features.feather', type=str, help="Output file path")

    args = parser.parse_args()

    main(args)
