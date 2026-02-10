

import snowflake.connector

def get_connection():
    return snowflake.connector.connect(
        user="*",
        password="*",
        account="*",
        warehouse="*",
        database="*",
        schema="*"
    )
