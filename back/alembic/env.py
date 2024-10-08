from logging.config import fileConfig

from sqlalchemy import pool, create_engine, Column, Identity
from alembic import context


# Импортируйте все модели и Base из одного места
from app.db.db import Base
from app.db.models.groupModel import Group, ProjectGroup, UserGroup
from app.db.models.userModel import User
from app.db.models.projectModel import Project, UserProject

config = context.config

# Интерпретация конфигурации для логирования
fileConfig(config.config_file_name)

# Убедитесь, что target_metadata содержит метаданные всех моделей
target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    """Filter out identity column changes."""
    if type_ == "column" and isinstance(object, Column):
        # Ignore server_default changes on identity columns
        if isinstance(object.server_default, Identity):
            return False
    return True

def run_migrations_offline() -> None:
    """Запуск миграций в offline режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Запуск миграций в online режиме."""
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
