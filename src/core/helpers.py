from dotenv import dotenv_values, find_dotenv
from sqlalchemy import create_engine


def load_env_vals():
    vals = {}

    # Load the variables from the .env file
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        vals[key] = (value if value != "" else None)
    return vals


def create_db_connection(config):
    connect_str = f"mysql+pymysql://{config['DB_USERNAME']}:@{config['DB_HOST']}/vss365"
    # TODO: Use this instead of above line
    # connect_str = "mysql+pymysql://{}:{}@{}/vss365".format(
    #     config["DB_USERNAME"],
    #     config["DB_PASSWORD"],
    #     config["DB_HOST"]
    # )
    return connect_str, create_engine(connect_str)
