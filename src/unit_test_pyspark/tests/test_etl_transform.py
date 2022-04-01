import pytest
from bigdata.etl_transform import sample_transform

'''
Setting up Docker to run your PySpark unit tests.
The next piece of unit testing PySpark code is having somewhere to test it that ins’t a production environment, 
somewhere anyone can do it, Docker of course. You will need

Dockerfile
Docker compose file
The Dockerfile doesn’t need to be rocket science, a little Ubuntu, Java, Python, Spark …
run in the folder with Dockerfile file:
 docker build --tag spark-test .
 - docker build -t spark-test -f src/unit_test_pyspark/Dockerfile .
 - docker run -it  spark-test --> t, the docker image tag and i, for interactive session
'''


# ['Candy', 'Company', 'SalesCount', 'Sales']
@pytest.mark.usefixtures("spark_session")
def test_sample_transform(spark_session):
    test_df = spark_session.createDataFrame(
        [
            ('MilkChocolate', 'Cadbury', 5),
            ('MilkChocolate', 'Hershey', 50),
            ('MilkChocolate', 'Hershey', 40),
            ('MilkChocolate', 'Nestle', 75),
            ('Eclairs', 'Cadbury', 5),
            ('Kisses', 'Hershey', 50),
            ('Nuggets', 'Hershey', 100),
            ('Kitkat', 'Nestle', 20)
        ],
        ['Candy', 'Company', 'SalesCount']
    )
    new_df = sample_transform(test_df, 'MilkChocolate')
    assert new_df.count() == 2
    assert new_df.toPandas().to_dict('list')['Sales'][0] == 90