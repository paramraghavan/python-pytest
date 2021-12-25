<pre>
npm install -g serverless
serverless create --template aws-python3 --name numpy-test --path numpy-test

cd aws
virtualenv venv --python=python3
venv\Scripts\activate

(venv) pip install numpy
(venv) pip freeze > requirements.txt
(venv) type requirements.txt

Our last step before deploying is to add the serverless-python-requirements plugin. Create a 
package.json file for saving your node dependencies. Accept the defaults, then install the 
plugin.

(venv) npm init # creates package.json

# lambda deployed 
(venv) $ serverless deploy # sls print, serverless deploy -v --stage dev
#serverless package -v --stage dev ****
~~~~~~~~
(venv) serverless invoke -f numpy --log

</pre>
[Also see](https://www.serverless.com/framework/docs/providers/aws/events/sns)