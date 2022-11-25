from fastapi_template.app.util.snowflake import SnowflakeGenerator


def test_snowflake():
    data = SnowflakeGenerator(10)
    print(next(data))
