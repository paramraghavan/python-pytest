# python-unittest
python aws unit testing  - pytest, mock, moto, botocore.stub


## Use case 1
sns triggers lambda. Sns messgae which is read in  lambda has the s3 location with lambda and lambda saves the s3 location into dynamo db table

## Use Case 2
lambda to check the batch job status, with 3 retry attempt with 10 second backoff interval.


## Use Case 3
It's like use case 1, except that the S3 needs a cross account bucket access and s3 metadata has cehcksum value which needs to read and stored into dynamo db




