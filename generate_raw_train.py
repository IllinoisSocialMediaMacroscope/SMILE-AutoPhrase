import argparse
import csv

import pandas as pd

from writeToS3 import WriteToS3


def main(s3, remoteReadPath, column):
    filename = remoteReadPath.split('/')[-2] + '.csv'
    s3.downloadToDisk(filename=filename, localpath='data/', remotepath=remoteReadPath)

    Array = []
    try:
        with open('data/' + filename,'r',encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    Array.append(row)
            except Exception as e:
                pass
    except:
        with open('data/' + filename,'r',encoding="ISO-8859-1", errors="ignore") as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    Array.append(row)
            except Exception as e:
                pass

    df = pd.DataFrame(Array[1:],columns=Array[0])
    df[df[column]!=''][column].dropna().astype('str').to_csv('data/raw_train.txt', index=False)

    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--remoteReadPath', required=True)
    parser.add_argument('--column', required=True)
    params = vars(parser.parse_args())

    if 'HOST_IP' in params.keys():
        HOST_IP = params['HOST_IP']
        params.pop('HOST_IP', None)
    else:
        HOST_IP = None

    if 'AWS_ACCESSKEY' in params.keys():
        AWS_ACCESSKEY = params['AWS_ACCESSKEY']
        params.pop('AWS_ACCESSKEY', None)
    else:
        AWS_ACCESSKEY = None

    if 'AWS_ACCESSKEYSECRET' in params.keys():
        AWS_ACCESSKEYSECRET = params['AWS_ACCESSKEYSECRET']
        params.pop('AWS_ACCESSKEYSECRET', None)
    else:
        AWS_ACCESSKEYSECRET = None

    if 'BUCKET_NAME' in params.keys():
        BUCKET_NAME = params['BUCKET_NAME']
        params.pop('BUCKET_NAME', None)
    else:
        BUCKET_NAME = None

    s3 = WriteToS3(HOST_IP, AWS_ACCESSKEY, AWS_ACCESSKEYSECRET, BUCKET_NAME)
    main(s3, params['remoteReadPath'], params['column'])
