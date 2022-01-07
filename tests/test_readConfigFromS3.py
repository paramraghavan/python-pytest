import readConfigFromS3


'''
This is used when we read want mock reading the some config from s3 or any other service. This config read may
be happening in some module, all we do here is patch that module, like in this case we are modify retunr value of the
function - read_app_config_from_s3
'''
def test_lambda_handler(mocker):

    mocker.patch.object(readConfigFromS3, 'read_app_config_from_s3')

    config = \
        {
            "dbInfo":
                {
                    "host": "localhost",
                    "database": "mydatabaseName",
                    "username": "myusername",
                    "password": "pass123",
                    "port": "0001"
                },
            "emailInfo": {
                "username": "myemail@gmail.com",
                "password": "myemailpasword",
                "smtp": "smtp.yahoo.com"
            }
        }

    readConfigFromS3.read_app_config_from_s3.return_value = config

    result = readConfigFromS3.run()

    assert result == config