import writeToS3 as s3
import csv
import pandas as pd
import argparse

def main(remoteReadPath, column):
    filename = remoteReadPath.split('/')[-2] + '.csv'
    s3.downloadToDisk(filename=filename, localpath='data/', remotepath=remoteReadPath)

    Array = []
    try:
        with open('data/' + filename,'r',encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    Array.append(row)
            except Exception as e:
                pass
    except:
        with open('data/' + filename,'r',encoding="ISO-8859-1") as f:
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
    args = parser.parse_args()

    main(args.remoteReadPath, args.column)