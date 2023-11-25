- [Serverless install guide](https://www.serverless.com/framework/docs/getting-started)
- [Serveless Hello World](https://www.serverless.com/framework/docs/providers/aws/examples/hello-world/python)
- [Serverless Example(s)](https://github.com/serverless/examples/)
- [Serverless Tutorial](https://www.serverless.com/examples)

<pre>
npm install -g serverless
serverless create --template aws-python3 --name aws --path aws

cd aws
virtualenv venv --python=python3
venv\Scripts\activate

(venv) pip freeze > requirements.txt
(venv) type requirements.txt

Our last step before deploying is to add the serverless-python-requirements plugin. Create a 
package.json file for saving your node dependencies. Accept the defaults, then install the 
plugin.

(venv) npm init # creates package.json
# update serverless.yml as needed, this one works for me

# lambda deployed 
(venv) $ serverless deploy # sls print, serverless deploy -v --stage dev
#serverless package -v --stage dev ****
~~~~~~~~
</pre>
- Also attach [this policy](src/aws/sns_lambda_trigger_policy.json) file to your aws cli account, modify as need be.
  > ! Note: the permissions granted here are generous as this just throw away code, go with least restricted  permissions first and 
  > add permissions to policy as needed.
 
 - Also note the requirement.txt is empty as we are uisng boto3 library and it is abailable by default.

[Also see](https://www.serverless.com/framework/docs/providers/aws/events/sns)
