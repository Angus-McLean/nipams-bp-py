from utils.constants import *
import argparse
import plotly.express as px
from data import load_data



def main(args):
    args = vars(args)
    print('Running main',args)
    print('Fetching data')
    dfAll = load_data.load_dataframe_from_pickle(folder=args['input.folder'],pattern=args['input.data_path'])
    
    # fig = px.line(dfAll, x='ts', y='az')

    df_ = dfAll[dfAll.file.sample().values[0] == dfAll.file]
    df_ = df_.reset_index(drop=True)
    fig = px.line(df_.select_dtypes(include=np.number).sort_values('ts').drop('ts',axis=1))
    
    print('Outputting TimeSeries Overview!')
    fig.write_html(args['output.file_path']+'.html')


    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Input time series dataset and export html file with time series overview!')

    parser.add_argument("--input.folder", default=f'{os.environ["PROJECT_PATH"]}/data/', type=str, help="This is the folder in which to search")
    parser.add_argument("--input.data_path", default='unnamed.processed-data.pickle', type=str, help="Points to the specific file to load within the input folder")
    parser.add_argument("--chart.type", default='timeline', type=str, help="This is the chart type parameter, defaults to timeline")
    parser.add_argument("--chart.configuration", default="""{"kwargs": {
        "indices" : ["file", "heartbeat"], 
        "split_kwargs" : {"n_splits":4, "test_size":0.2, "random_state":0}
    }}""", type=str, help="This is the additional chart configurations in JSON form")
    parser.add_argument("--output.file_path", default=f'{os.environ["PROJECT_PATH"]}/reports/figures/unnamed.timeseries.html', type=str, help="Output Chart file path")

    args = parser.parse_args()

    main(args)