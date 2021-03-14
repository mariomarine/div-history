import boto3
import progressbar
import os

FILENAME = 'getStockDividends.zip'
BUCKET = 'divdata'
FUNCTION = 'getStockDividends'

def update_s3():
    s3client = boto3.client('s3')
    local_filename = FILENAME

    file_info = os.stat(local_filename)

    up_progress = progressbar.progressbar.ProgressBar(maxval=file_info.st_size)

    print('Uploading: ' + local_filename)

    up_progress.start()

    def upload_progress(chunk):
        up_progress.update(up_progress.currval + chunk)

    s3client.upload_file(local_filename, BUCKET, local_filename, Callback=upload_progress)
    up_progress.finish()

def update_lambda():

    lambdaclient = boto3.client('lambda', region_name='us-east-1')

    lambdaclient.update_function_code(FunctionName=FUNCTION, S3Bucket=BUCKET, S3Key=FILENAME)

if __name__ == "__main__":
    update_s3()
    update_lambda()

