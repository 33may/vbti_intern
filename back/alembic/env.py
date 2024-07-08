import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import your models here
from app.db.models.userModel import Base as UserBase
# Import other models similarly if you have more
# from app.db.models.otherModel import Base as OtherBase

# Combine all the metadata
target_metadata = UserBase.metadata
# If you have more models, combine their metadata like this:
# target_metadata = [UserBase.metadata, OtherBase.metadata]

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # Extract the URL from the configuration
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
