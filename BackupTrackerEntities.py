import datetime
import typing

import sqlalchemy.orm.exc

from typing import List

from sqlalchemy import Column, Integer, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
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


class Destination(Base):
    __tablename__ = 'destinations'

    destination_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_path: Mapped[str] = mapped_column(Text, unique=True)

    def __repr__(self):
        return self._repr(resource_id=self.destination_id, resource_path=self.destination_path)


class Source(Base):
    __tablename__ = 'sources'

    source_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_path: Mapped[str] = mapped_column(Text, unique=True)

    def __repr__(self):
        return self._repr(resource_id=self.source_id, resource_path=self.source_path)


job_source_association_table = Table(
    "job_sources",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.job_id")),
    Column("source_id", ForeignKey("sources.source_id")),
)


class Job(Base):
    __tablename__ = 'jobs'

    job_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_tool: Mapped[str] = mapped_column(Text, nullable=False)
    job_description: Mapped[str] = mapped_column(Text)

    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.destination_id"))
    destination: Mapped["Destination"] = relationship()

    sources: Mapped[List[Source]] = relationship(secondary=job_source_association_table)


history_source_association_table = Table(
    "history_sources",
    Base.metadata,
    Column("history_id", ForeignKey("history.history_id")),
    Column("source_id", ForeignKey("sources.source_id")),
)


class History(Base):
    __tablename__ = 'history'

    history_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id"))
    job: Mapped["Job"] = relationship()

    job_tool: Mapped[str] = mapped_column(Text, nullable=False)
    job_description: Mapped[str] = mapped_column(Text)
    when: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    operation: Mapped[str] = mapped_column(Text)

    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.destination_id"))
    destination: Mapped["Destination"] = relationship()

    sources: Mapped[List[Source]] = relationship(secondary=history_source_association_table)

    def __repr__(self):
        return self._repr(history_id=self.history_id, job_id=self.job_id)
