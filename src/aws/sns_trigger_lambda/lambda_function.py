import time
import boto3
import os
import ast
from utils import boto3_utils

def lambda_handler(event, context):
    print('Incoming sns request {0}'.format(repr(event)))
    sns_msg = event["Records"][0]["Sns"]
    print(f'sns message: {sns_msg} ')
    message_attributes = sns_msg["MessageAttributes"]
    print(f'message_attributes: {message_attributes} ')
    print(event["Records"][0]["Sns"]["MessageAttributes"]["BikerideDatasource"]["Value"])
    producer_datasource = event["Records"][0]["Sns"]["MessageAttributes"]["BikerideDatasource"]["Value"]
    print(f'producer datasource : {producer_datasource}')

    # save this producer datasource to dynamodb
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    PRODUCER_INTERFACE_TABLE = os.environ['PRODUCER_INTERFACE_TABLE']
    dynamodb_table = dynamodb.Table(PRODUCER_INTERFACE_TABLE)
    partition_key = time.strftime("%Y-%m-%d")
    item_key = {
        'producer_datasource': producer_datasource,
        'partition_key': partition_key
    }

    update_expr = "SET datasource=:ds, create_data_time=:cdt"
    expr_attr_values = {
        ':ds': producer_datasource,
        ':cdt': current_time
    }

    response = boto3_utils.update_dynamodb_item(dynamodb_table, item_key, update_expr, expr_attr_values)
    print('updateResponse: ' + str(response))