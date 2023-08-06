def test_pyspark(df,column_name):
    return df.select(column_name)