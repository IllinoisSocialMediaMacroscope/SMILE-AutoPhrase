import writeToS3 as s3
from os import listdir
from os.path import isfile, join
import argparse
import json

def main(remoteSavePath):
    for file in listdir('results'):
        if isfile(join('results', file)):
            s3.upload('results', remoteSavePath, file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--remoteSavePath', required=True)
    parser.add_argument('--remoteReadPath', required=True)
    parser.add_argument('--column', required=True)
    parser.add_argument('--minSup', required=True)
    args = parser.parse_args()

    # save parameters
    fname = 'config.json'
    with open(join('results', fname), "w") as f:
        json.dump(vars(args), f)

    main(args.remoteSavePath)