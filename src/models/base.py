from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata_obj = MetaData(schema="verifix")

class Base(DeclarativeBase):
  metadata = metadata_obj

  @classmethod
  def nonprimary_columns(cls):
    columns = cls.__table__.columns

    return [
      column.key for column in columns if not column.primary_key
    ]