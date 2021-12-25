import time
import botocore



def update_dynamodb_item(dynamo_table,item_key,expr,expr_attr_values):
    response = dynamo_table.update_item(
        Key=item_key,
        UpdateExpression=expr,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="UPDATED_NEW"
    )
    return response