import datetime
import typing

import sqlalchemy.orm.exc

from typing import List

from sqlalchemy import Column, Integer, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.orm.base import Mapped


class Base(DeclarativeBase):
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        # Helper for __repr__
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


class SourceHistoryAssociation(Base):
    __tablename__ = "history_sources"
    history_id: Mapped[int] = mapped_column(ForeignKey("history.history_id"), primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.source_id"), primary_key=True)

    # association between SourceHistoryAssociation -> Source
    sources: Mapped["Source"] = relationship(back_populates="history_associations")
    # association between SourceHistoryAssociation -> History
    history: Mapped["History"] = relationship(back_populates="source_associations")


class Source(Base):
    __tablename__ = 'sources'

    source_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_path: Mapped[str] = mapped_column(Text, unique=True)

    def __repr__(self):
        return self._repr(resource_id=self.source_id, resource_path=self.source_path)

    # many-to-many relationship to Job, bypassing the `JobSourceAssociation` class
    jobs: Mapped[List["Job"]] = relationship(
        secondary="job_sources", back_populates="sources"
    )

    # association between Source -> SourceHistoryAssociation -> History
    job_associations: Mapped[List["JobSourceAssociation"]] = relationship(
        back_populates="sources"
    )

    # many-to-many relationship to History, bypassing the `SourceHistoryAssociation` class
    history: Mapped[List["History"]] = relationship(
        secondary="history_sources", back_populates="sources"
    )

    # association between Source -> SourceHistoryAssociation -> History
    history_associations: Mapped[List["SourceHistoryAssociation"]] = relationship(
        back_populates="sources"
    )


class JobSourceAssociation(Base):
    __tablename__ = "job_sources"
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id"), primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.source_id"), primary_key=True)

    # association between JobSourceAssociation -> Job
    jobs: Mapped["Job"] = relationship(back_populates="source_associations")
    # association between JobSourceAssociation -> Source
    sources: Mapped["Source"] = relationship(back_populates="job_associations")


class Job(Base):
    __tablename__ = 'jobs'

    job_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_tool: Mapped[str] = mapped_column(Text, nullable=False)
    job_description: Mapped[str] = mapped_column(Text)

    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.destination_id"))
    destination: Mapped["Destination"] = relationship()

    # many-to-many relationship to Sources, bypassing the `JobSourceAssociation` class
    sources: Mapped[List["Source"]] = relationship(
        secondary="job_sources", back_populates="jobs"
    )

    # association between Job -> JobSourceAssociation -> Source
    source_associations: Mapped[List["JobSourceAssociation"]] = relationship(
        back_populates="jobs"
    )

    def __repr__(self):
        return self._repr(job_id=self.job_id, job_description=self.job_description)


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

    # many-to-many relationship to Sources, bypassing the `JobSourceAssociation` class
    sources: Mapped[List["Source"]] = relationship(
        secondary="history_sources", back_populates="history"
    )

    # association between Job -> JobSourceAssociation -> Source
    source_associations: Mapped[List["SourceHistoryAssociation"]] = relationship(
        back_populates="history"
    )

    def __repr__(self):
        w: datetime.datetime = self.when
        return self._repr(history_id=self.history_id, job_id=self.job_id, tool=self.job_tool, when=w.isoformat(), operation=self.operation)
