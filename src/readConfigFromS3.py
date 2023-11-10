import ast
import os

import boto3


def read_app_config_from_s3(config_prefix:str)->dict:
    bucket_name = os.environ['s3Bucket']
    s3_client = boto3.client('s3')
    data = read_s3_object(s3_client=s3_client,bucket_name=bucket_name,s3_object_key=config_prefix)
    config_dict = ast.literal_eval(data)
    #print('config_dict {0}'.format(config_dict))
    return config_dict

def read_s3_object(s3_client,bucket_name,s3_object_key):
    pass

def run(config_prefix:str ) ->dict:
    value = read_app_config_from_s3(config_prefix)
    print(value)
    return value