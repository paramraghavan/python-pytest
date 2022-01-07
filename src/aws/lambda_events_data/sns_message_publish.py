import json
import boto3

message = 'Updated AnnualSurvery data source file.'
client = boto3.client('sns')
arn = 'arn:aws:sns:us-east-1:687162148361:dispatch'
response = client.publish(
    TargetArn=arn,
    Message= message,
    Subject = 'AnnualSurveryDatasource File update.',
    MessageStructure='string',
    MessageAttributes={
                        'AnnualSurveryDatasource': {
                            'DataType': 'String',
                            'StringValue': 'sample987/input/annual-enterprise-survey-2020-financial-year-provisional.csv'
                        }
                    },
)

print(f'response {response}')