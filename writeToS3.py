import mimetypes
import os

import boto3
from botocore.client import Config


class WriteToS3:

    def __init__(self, HOST_IP=None, AWS_ACCESSKEY=None, AWS_ACCESSKEYSECRET=None, BUCKET_NAME=None):

        # local minio s3
        if HOST_IP and AWS_ACCESSKEY and AWS_ACCESSKEYSECRET and BUCKET_NAME:
            self.client = boto3.client('s3', endpoint_url='http://' + HOST_IP + ':9000',
                                       aws_access_key_id=AWS_ACCESSKEY,
                                       aws_secret_access_key=AWS_ACCESSKEYSECRET,
                                       config=Config(signature_version='s3v4'))
            self.bucket_name = BUCKET_NAME

        # remote aws s3
        else:
            self.client = boto3.client('s3')
            self.bucket_name = 'macroscope-smile'

    def upload(self, localpath, remotepath, filename):
        content_type = mimetypes.guess_type(os.path.join(localpath, filename))[0]
        print(filename, content_type)
        if content_type == None:
            extra_args = {'ContentType': 'application/octet-stream'}
        else:
            extra_args = {'ContentType': content_type}

        self.client.upload_file(os.path.join(localpath, filename),
                                self.bucket_name,
                                os.path.join(remotepath, filename),
                                ExtraArgs=extra_args)

    def createDirectory(self, DirectoryName):
        self.client.put_object(Bucket=self.bucket_name, Key=DirectoryName)

    def generate_downloads(self, remotepath, filename):
        url = self.client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': os.path.join(remotepath, filename)
            },
            ExpiresIn=604800  # one week
        )

        return url

    def downloadToDisk(self, filename, localpath, remotepath):
        with open(os.path.join(localpath, filename), 'wb') as f:
            self.client.download_fileobj(self.bucket_name,
                                         os.path.join(remotepath, filename), f)

    def getObject(self, remoteKey):
        obj = self.client.get_object(Bucket=self.bucket_name, Key=remoteKey)

    def putObject(self, body, remoteKey):
        # bytes or seekable file-like object
        obj = self.client.put_object(Bucket=self.bucket_name,
                                     Body=body, Key=remoteKey)
        print(obj['Body'].read())

    def listDir(self, remoteClass):
        objects = self.client.list_objects(Bucket=self.bucket_name,
                                           Prefix=remoteClass,
                                           Delimiter='/')
        foldernames = []
        for o in objects.get('CommonPrefixes'):
            foldernames.append(o.get('Prefix'))

        # only return the list of foldernames
        return foldernames

    def listFiles(self, foldernames):
        objects = self.client.list_objects(Bucket=self.bucket_name,
                                           Prefix=foldernames)

        # return rich information about the files
        return objects.get('Contents')
