import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

# Import your models
from app.database import Base
from app import models  # noqa: F401 - imported for side effects

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def get_database_url():
    """Get database URL from environment or config."""
    # First try environment variable
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    
    # Fallback to config file
    database_url = config.get_main_option("sqlalchemy.url")
    if database_url:
        return database_url
    
    raise ValueError(
        "DATABASE_URL environment variable or sqlalchemy.url config option must be set"
    )


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
