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
          'BikerideDatasource': {
            'Type': 'String',
            'Value': 'arn:aws:s3:::sample987/input/bikeride.csv'
          }
        }
      }
    }
  ]
}


print(event["Records"][0]["Sns"]["MessageAttributes"]["BikerideDatasource"]["Value"])
