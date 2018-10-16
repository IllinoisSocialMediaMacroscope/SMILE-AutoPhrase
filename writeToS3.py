import boto3
import os
import mimetypes

client = boto3.client('s3')
bucket_name = 'macroscope-smile'

def upload(localpath, remotepath, filename):
    content_type = mimetypes.guess_type(os.path.join(localpath,filename))[0]
    print(filename, content_type)
    if content_type == None:
        extra_args = {'ContentType':'application/json'}
    else:
        extra_args = {'ContentType':content_type}
    
    client.upload_file(os.path.join(localpath, filename),
                       bucket_name,
                       os.path.join(remotepath, filename),
                       ExtraArgs=extra_args)


def createDirectory(DirectoryName):
    client.put_object(Bucket=bucket_name, Key=DirectoryName)


def generate_downloads(remotepath, filename):
    url = client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': os.path.join(remotepath, filename)
                },
                ExpiresIn=604800  # one week
    )

    return url


def downloadToDisk(filename, localpath, remotepath):
    with open(os.path.join(localpath, filename), 'wb') as f:
        client.download_fileobj(bucket_name,
                                os.path.join(remotepath, filename), f)


def getObject(remoteKey):
    obj = client.get_object(Bucket=bucket_name, Key=remoteKey)


def putObject(body, remoteKey):
    # bytes or seekable file-like object
    obj = client.put_object(Bucket=bucket_name,
                            Body=body, Key=remoteKey)
    print(obj['Body'].read())


# def checkExist(remotepath, filename):
#     results = client.list_objects(Bucket=bucket_name, Prefix=os.path.join(remotepath, filename))
#     print(results)
#     if 'Contents' in results:
#         return True
#     else:
#         return False

def listDir(remoteClass):
    objects = client.list_objects(Bucket=bucket_name,
                                  Prefix=remoteClass,
                                  Delimiter='/')
    foldernames = []
    for o in objects.get('CommonPrefixes'):
        foldernames.append(o.get('Prefix'))

    # only return the list of foldernames
    return foldernames


def listFiles(foldernames):
    objects = client.list_objects(Bucket=bucket_name,
                                  Prefix=foldernames)

    # return rich information about the files
    return objects.get('Contents')
