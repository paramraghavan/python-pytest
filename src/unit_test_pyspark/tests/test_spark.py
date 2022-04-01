import pytest
from pyspark import sql

@pytest.mark.usefixtures("spark_session")
def test_create_session(spark_session):
    assert isinstance(spark_session, sql.SparkSession) == True
    assert spark_session.sparkContext.appName == 'test'
    assert spark_session.version == '3.2.1'