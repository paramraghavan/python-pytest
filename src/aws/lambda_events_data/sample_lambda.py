event = \
{
  'Records': [
    {
      'EventSource': 'aws:sns',
      'EventVersion': '1.0',
      'EventSubscriptionArn': 'arn:aws:sns:us-east-1:aws-acct:dispatch:3c1c7634-edb6-43e2-9b09-93e781z1149x',
      'Sns': {
        'Type': 'Notification',
        'MessageId': 'a214a4ec-56d1-5ac8-82de-feacd0b8f24e',
        'TopicArn': 'arn:aws:sns:us-east-1:687162148361:dispatch',
        'Subject': 'Bike Ride File update',
        'Message': 'Updated bikeride data source file',
        'Timestamp': '2021-12-25T02:38:33.781Z',
        'SignatureVersion': '1',
        'Signature': 'KaXj1bIdKiXby8ky911hRvJKaApLtAg0Rzipvj7RlWgdV1ZPZK9HtNEXmiYP9T0GiD4PNmxydaHDewe2nJlk/cx2lsGoMzXnSaiRPb1Cx7km7xexxvmCSOxFpu3ZAVQGsf1iYKDKuxTjXdCfJ5qLdjkAxLMsHCcP+y/lrh0uIDDAvS4gLMbkPwHaNnTYcjBh2WnPYgEWu9gHa3B9xgafRhz2TW4Bio26wAUWO+LlyT3xRjQrypI6fE1qd0/P5KqZTf7o3SZeBqI+2mYH0SC7w80VQ1rUsKwAc7oMGkqDlerGbAxT89TPcB74O+FpCiQs+hmEN2cDzLjxKo6ZMsxaAA==',
        'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem',
        'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:aws-acct:dispatch:3c1c7634-edb6-43e2-9b09-14e741a1149z',
        'MessageAttributes': {
          'AnnualSurveryDatasource': {
            'Type': 'String',
            'Value': 'sample987/input/annual-enterprise-survey-2020-financial-year-provisional.csv'
          }
        }
      }
    }
  ]
}


datasource = event["Records"][0]["Sns"]["MessageAttributes"]["AnnualSurveryDatasource"]["Value"]
print(f"bucket: {datasource.split('/')[0]}" )
print(f"key: {datasource.split('/',1)[1:]}" )
print(type(datasource.split('/',1)[1:][0]))

# KeySchema = [
#   {
#     'AttributeName': 'datasource',
#     'KeyType': 'HASH'
#   },
#   {
#     'AttributeName': 'partitionkey',
#     'KeyType': 'RANGE'
#   }
# ]

key_schema = []
key_schema.append({'AttributeName': 'datasource', 'KeyType': 'HASH'})
key_schema.append({'AttributeName': 'partitionkey',  'KeyType': 'RANGE'})

print(key_schema)

# AttributeDefinitions = [
#   {
#     'AttributeName': 'datasource',
#     'AttributeType': 'S'
#   },
#   {
#     'AttributeName': 'partitionkey',
#     'AttributeType': 'S'
#   },
# ]


attribute_definations = []
attribute_definations.append({'AttributeName': 'datasource', 'AttributeType': 'S'})
attribute_definations.append({'AttributeName': 'partitionkey',  'AttributeType': 'S'})

print(attribute_definations)

input_event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:687162148361:dispatch:3c1c7634-edb6-43e2-9b09-02e781a1148b', 'Sns': {'Type': 'Notification', 'MessageId': '07826c52-ed6c-5f38-a87c-3616966df04a', 'TopicArn': 'arn:aws:sns:us-east-1:687162148361:dispatch', 'Subject': 'AnnualSurveryDatasource File update.', 'Message': 'Updated AnnualSurvery data source file.', 'Timestamp': '2021-12-28T02:38:57.644Z', 'SignatureVersion': '1', 'Signature': 'gRhDfpman0zibBR4B7VKgef7mAN7L4KaC8hYXkOfs5knRmmQ+q5YIt7Z5nGFKqxZiR1RWFujioABD478ogq0zfUmJxkhVO+KtJSQvuM7+Sg82fd4q1t9pAf/zuBwqwSPKg0wABjWaI5LSjYV/A+tq/HEQ2eoZLTCQfgBWCkxQKprrqyxiHiHdE2wzPnjFnwY/a4uRYSFnO6X0p3hablKX+5XO8uqtyHD6I6OmaAd3mf9ppSGnETJO/1NSRykQBi4MWrxlKVBgB6UrHhYM0zpCpb6yFS9iVEDMKR6Ow/hjLRYP0Lg9N+kWRkxDXMTdQ0LOwqc7UnyvfFDnw8lUUFKAg==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:687162148361:dispatch:3c1c7634-edb6-43e2-9b09-02e781a1148b', 'MessageAttributes': {'AnnualSurveryDatasource': {'Type': 'String', 'Value': 'sample987/input/annual-enterprise-survey-2020-financial-year-provisional.csv'}}}}]}

print(type(input_event))

bucket = 'abc'
key = 'dig/in/a.csv'

val = f's3://{bucket}/{key}'
print(val)