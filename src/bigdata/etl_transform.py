import pyspark.sql.functions as F
from pyspark.sql import DataFrame


'''
When it comes to unit testing PySpark pipeline code, there is at least baseline that must be followed. 
The critical ETL transforms of a PySpark script should be encapsulated inside a method/function, like we have it here
in sample_transform.

        ['Candy', 'Company', 'SalesCount', 'Sales']
'''
def sample_transform(input_df: DataFrame, candy:str) -> DataFrame:
    inter_df = input_df.where(input_df['Candy'] == \
                              F.lit(candy)).groupBy('Company').agg(F.sum('SalesCount').alias('Sales'))
    output_df = inter_df.select('Company', 'Sales', \
                                F.when(F.col('Sales') > 10, 'yes').otherwise('no').alias('indicator')).where(
                F.col('indicator') == F.lit('yes'))
    return output_df


def company_with_max_avg_sales(input_df: DataFrame, spark_session) -> float:
    # Register the DataFrame as a SQL temporary view
    input_df.createOrReplaceTempView("temp")
    sql = 'select Company, avg(SalesCount) over ' \
          '(partition by Company order by Company) as max_of_avg from temp order by max_of_avg desc limit 1'
    sql_df = spark_session.sql(sql)
    sql_df.show()
    ret_val = None
    if sql_df:
        ret_val = sql_df.toPandas().to_dict('list')['max_of_avg'][0]
    return ret_val


from pyspark.sql.functions import explode

def process_providers_json_by_group(spark_session, mailbox_providers_path ='/app/data/mailbox-providers/providers.json' , group='gmail')->DataFrame:
    mailbox_providers_df = spark_session.read.json(mailbox_providers_path)
    mailbox_providers_df.printSchema()
    mailbox_providers_df.show()
    exploded_mailbox_providers_df = mailbox_providers_df.withColumn('domains', explode('domains')). \
        withColumnRenamed('domains', 'domain')
    exploded_mailbox_providers_df.show()
    exploded_mailbox_providers_df.createOrReplaceTempView("mailbox_providers")
    sql = f"SELECT domain FROM mailbox_providers where group = '{group}'"
    print(sql)
    sql_mailbox_providers_domain_df = spark_session.sql(sql)
    sql_mailbox_providers_domain_df.show()

    return sql_mailbox_providers_domain_df


