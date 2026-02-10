

import snowflake.connector

def get_connection():
    return snowflake.connector.connect(
        user="LALIT23",
        password="Lalit12345678*",
        account="JMCVEEC-YO11161",
        warehouse="MY_WH",
        database="COMPANY_DB",
        schema="HR_SCHEMA"
    )
