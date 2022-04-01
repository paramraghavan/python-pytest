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