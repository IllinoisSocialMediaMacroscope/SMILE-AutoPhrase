import writeToS3 as s3
from os import listdir
from os.path import isfile, join
import argparse
import json
import notification as n

def main(remoteSavePath):

    output = {}

    for file in listdir('results'):
        if isfile(join('results', file)):
            s3.upload('results', remoteSavePath, file)

            if file == 'config.json':
                output['config'] = s3.generate_downloads(remoteSavePath, file)
            elif file == 'div.html':
                output['visualization'] = s3.generate_downloads(remoteSavePath, file)
            elif file == 'AutoPhrase_multi-words.txt':
                output['multi-words'] = s3.generate_downloads(remoteSavePath, file)
            elif file == 'AutoPhrase_single-word.txt':
                output['single-word'] = s3.generate_downloads(remoteSavePath, file)
            elif file == 'AutoPhrase.txt':
                output['autophrase'] = s3.generate_downloads(remoteSavePath, file)
            elif file == 'segmentation.model':
                output['model'] = s3.generate_downloads(remoteSavePath, file)
            elif file == 'token_mapping.txt':
                output['token-mapping'] = s3.generate_downloads(remoteSavePath, file)
            else:
                output['misc'] = s3.generate_downloads(remoteSavePath, file)

    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--remoteSavePath', required=True)
    parser.add_argument('--remoteReadPath', required=True)
    parser.add_argument('--column', required=True)
    parser.add_argument('--minSup', required=True)
    parser.add_argument('--email', required=True)
    parser.add_argument('--sessionURL', required=True)
    args = parser.parse_args()

    # save parameters
    fname = 'config.json'
    with open(join('results', fname), "w") as f:
        json.dump(vars(args), f)

    links = main(args.remoteSavePath)
    n.notification(args.email, case=3, filename=args.remoteSavePath, links=links,
                   sessionURL=args.sessionURL)