from datetime import datetime as datetime
from typing import Optional

from lnschema_core._timestamps import CreatedAt
from lnschema_core._users import CreatedBy
from sqlmodel import Field, SQLModel


class version_tvhn(SQLModel, table=True):  # type: ignore
    """Schema module versions deployed in a given instance.

    Migrations of the schema module add rows to this table, storing the schema
    module version to which we migrated along with the user who performed the
    migration.
    """

    v: Optional[str] = Field(primary_key=True)
    """Python package version of `lnschema_core`."""
    migration: Optional[str] = None
    """Migration script reference of the latest migration leading up to the Python package version."""  # noqa
    user_id: str = CreatedBy
    """Link to user."""
    created_at: datetime = CreatedAt
    """Time of creation."""


class migration_tvhn(SQLModel, table=True):  # type: ignore
    """Latest migration.

    This stores the reference to the latest migration script deployed.
    """

    version_num: Optional[str] = Field(primary_key=True)
    """Reference to the last-run migration script."""
