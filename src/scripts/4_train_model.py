from math import exp
from utils.constants import *
import argparse
import plotly.express as px
from data import load_data, preprocess
import json


def main(args):
    args = vars(args)
    print('Running main',args)
    print('Fetching data')
    dfAll = load_data.load_dataframe_from_pickle(folder=args['input.folder'],pattern=args['input.data_path'])
    dfImu = dfAll[INDICIES + INFO_COLS + IMU_COLS]
    dfBp = dfAll[INDICIES + INFO_COLS + BP_COLS]
    
    #### Splitting ####
    print('Split Experiment')
    from models import experiments
    splitting_config = json.loads(experiments.DEFAULTS['split_by_group'])
    sampleRandTestInds = getattr(experiments, splitting_config['function'])(dfBp=dfBp, **splitting_config['kwargs'])

    sampleExpDfs = experiments.get_experiment(sampleRandTestInds[0], dfImu, dfBp)
    dfSplits = pd.concat([
        dfBp.groupby(INDICIES).last().merge(sampleRandTestInds[0]['train'], on=INDICIES, how='right').assign(split_type='train'),
        dfBp.groupby(INDICIES).last().merge(sampleRandTestInds[0]['test'], on=INDICIES, how='right').assign(split_type='test')
        # experiments.get_experiment_df(dfBp, sampleRandTestInds[0]['train']).assign(split_type='train'),
        # experiments.get_experiment_df(dfBp, sampleRandTestInds[0]['test']).assign(split_type='test')
    ], axis=0)
    
    print('Outputting Splits Overview')
    fig = chart_splits(dfSplits)
    fig.write_html(args['output.file_path'])

    # print('Done!',len(sampleExpDfs))
    
    pass

def chart_splits(dfSplits):

    dfSplits['set_name'] = dfSplits.file + '-' + dfSplits.split_type
    dfSplits = dfSplits.sort_values(['set_name','heartbeat'])

    return px.scatter(
        dfSplits, 
        y='sbp', x='heartbeat',
        color='file', 
        symbol = dfSplits['split_type'],
        symbol_sequence= ['circle-open', 'circle']
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Input dataset and model configurations, train model and save trained model weights!')

    parser.add_argument("--input.folder", default=f'{os.environ["PROJECT_PATH"]}/data/', type=str, help="This parameter points to the specific folder in which to search")
    parser.add_argument("--input.data_path", default='unnamed.processed-data.pickle', type=str, help="Points to the specific file to load within the input folder")
    parser.add_argument("--experiment.split_type", default='split_by_group', type=str, help="Indicates which strategy to use when generating splits")
    parser.add_argument("--experiment.configuration", default=f'{os.environ["PROJECT_PATH"]}/data/', type=str, help="Additional configurations for train & test splitting configuration")
    parser.add_argument("--model.type", default=f'{os.environ["PROJECT_PATH"]}/data/', type=str, help="Overarching model type - analytical, machine learning, deep learning")
    parser.add_argument("--model.configuration", default=f'{os.environ["PROJECT_PATH"]}/data/', type=str, help="Additional details for model configuration")
    parser.add_argument("--model.pipeline", default=f'{os.environ["PROJECT_PATH"]}/data/', type=str, help="The most flexible approach to pipeline creation for modeling")
    parser.add_argument("--output.model_path", default=f'{os.environ["PROJECT_PATH"]}/data/', type=str, help="The destination folder path in which to save the model snapshot")
    parser.add_argument("--output.file_path", default=f'{os.environ["PROJECT_PATH"]}/reports/figures/unnamed.splits.html', type=str, help="The output resulting predictions file path to save the results")

    args = parser.parse_args()

    main(args)