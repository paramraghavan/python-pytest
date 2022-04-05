import pytest
from bigdata.etl_transform import sample_transform, company_with_max_avg_sales, process_providers_json_by_group


# ['Candy', 'Company', 'SalesCount', 'Sales']
@pytest.mark.usefixtures("spark_session")
# @pytest.mark.skip("WIP")
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


@pytest.mark.usefixtures("spark_session")
#@pytest.mark.skip("WIP")
def test_company_with_max_avg_sales(spark_session):
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
    val = company_with_max_avg_sales(test_df, spark_session)
    assert val == 60

@pytest.mark.usefixtures("spark_session")
# @pytest.mark.skip("WIP")
def test_process_providers_json_by_group(spark_session):
    sql_mailbox_providers_domain_df = process_providers_json_by_group(spark_session,  mailbox_providers_path ='data/mailbox-providers/providers.json' , group='gmail')
    rows = sql_mailbox_providers_domain_df.select('domain').collect()

    final_list = []
    for i in rows:
        final_list.append(i[0])
    print(final_list)
    assert  final_list == ['gmail.com', 'googlemail.com']