
import argparse


def main(args):

    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Input time series dataset and calculate appropriate features!')

    parser.add_argument("--input.file_path", default='./data/raw', type=str, help="This is the folder in which to search")
    parser.add_argument("--feature.type", default='merge_imu_vcg_with_heartbeats', type=str, help="This is the preprocess type variable")
    parser.add_argument("--feature.configuration", default='merge_imu_vcg_with_heartbeats', type=str, help="This is the preprocess type variable")
    parser.add_argument("--output.file_path", default='data/unnamed.processed-data.pickle', type=str, help="Output file path")

    args = parser.parse_args()

    main(args)