import os
from sqlalchemy import create_engine


def get_sqlalchemy_engine():
    # database_url = os.getenv("DATABASE_URL")
    database_url = "postgresql://webprojectdb_udvp_user:yB8mCdSTTHAyvgAHjJR8dtbbMC92LJ3y@dpg-d0d6jqhr0fns7383qd50-a.frankfurt-postgres.render.com/webprojectdb_udvp"

    if not database_url:
        raise ValueError("DATABASE_URL не задан в переменных окружения")

    return create_engine(
        database_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        connect_args={
            "sslmode": "require"
        }
    )
