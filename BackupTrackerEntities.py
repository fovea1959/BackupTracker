import datetime
import typing

import sqlalchemy.orm.exc

from typing import List

from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.orm.base import Mapped


class Base(DeclarativeBase):
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except sqlalchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"


class Resource(Base):
    __tablename__ = 'resources'

    resource_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_path: Mapped[str] = mapped_column(Text, unique=True)

    def __repr__(self):
        return self._repr(resource_id=self.resource_id, resource_path=self.resource_path)


class History(Base):
    __tablename__ = 'history'

    history_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_tool: Mapped[str] = mapped_column(Text, nullable=False)
    job_description: Mapped[str] = mapped_column(Text)
    when: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    destination_resource_id: Mapped[int] = mapped_column(ForeignKey("resources.resource_id"))
    destination: Mapped["Resource"] = relationship()
