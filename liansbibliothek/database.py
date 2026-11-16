import os

from sqlalchemy import URL, create_engine

password = os.environ.get("LIANE_MYSQL_PASSWORD")
if not password:
    raise RuntimeError(
        "Set LIANE_MYSQL_PASSWORD in the terminal before starting the app."
    )

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=password,
    host="127.0.0.1",
    port=3306,
    database="lianes_bibliothek",
)

engine = create_engine(connection_url, pool_pre_ping=True)
