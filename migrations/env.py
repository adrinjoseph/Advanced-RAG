from alembic import context
from sqlalchemy import create_engine, pool

from advanced_rag.config import get_settings
from advanced_rag.db import models as _models  # noqa: F401
from advanced_rag.db.base import Base

config = context.config
settings = get_settings()
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without opening a database connection."""
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against the configured database."""
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        poolclass=pool.NullPool,
    )

    try:
        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
