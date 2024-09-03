from typing import List

from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Resources(Base):
    __tablename__ = 'resources'
    __table_args__ = (
        PrimaryKeyConstraint('resource_id', name='resources_pk'),
        Index('resources_resource_path_IDX', 'resource_path', unique=True)
    )

    resource_id = mapped_column(Integer)
    resource_path = mapped_column(Text, nullable=False)

    history: Mapped[List['History']] = relationship('History', uselist=True, back_populates='destination_resource')
    jobs: Mapped[List['Jobs']] = relationship('Jobs', uselist=True, back_populates='destination_resource')
    history_sources: Mapped[List['HistorySources']] = relationship('HistorySources', uselist=True, back_populates='source_resource')
    job_sources: Mapped[List['JobSources']] = relationship('JobSources', uselist=True, back_populates='source_resource')


class History(Base):
    __tablename__ = 'history'
    __table_args__ = (
        ForeignKeyConstraint(['destination_resource_id'], ['resources.resource_id'], name='history_resources_FK'),
    )

    history_id = mapped_column(Integer, primary_key=True)
    destination_resource_id = mapped_column(Integer, nullable=False)
    job_tool = mapped_column(Text, nullable=False)
    job_description = mapped_column(Text)

    destination_resource: Mapped['Resources'] = relationship('Resources', back_populates='history')
    history_sources: Mapped[List['HistorySources']] = relationship('HistorySources', uselist=True, back_populates='history')


class Jobs(Base):
    __tablename__ = 'jobs'
    __table_args__ = (
        ForeignKeyConstraint(['destination_resource_id'], ['resources.resource_id'], name='jobs_resources_FK'),
    )

    job_id = mapped_column(Integer, primary_key=True)
    destination_resource_id = mapped_column(Integer, nullable=False)
    job_tool = mapped_column(Text, nullable=False)
    job_description = mapped_column(Text)

    destination_resource: Mapped['Resources'] = relationship('Resources', back_populates='jobs')
    job_sources: Mapped[List['JobSources']] = relationship('JobSources', uselist=True, back_populates='job')


class HistorySources(Base):
    __tablename__ = 'history_sources'
    __table_args__ = (
        ForeignKeyConstraint(['history_id'], ['history.history_id'], name='history_sources_history_FK'),
        ForeignKeyConstraint(['source_resource_id'], ['resources.resource_id'], name='history_sources_resources_FK'),
        Index('history_sources_history_id_IDX', 'history_id', 'source_resource_id', unique=True)
    )

    history_source_id = mapped_column(Integer, primary_key=True)
    history_id = mapped_column(Integer, nullable=False)
    source_resource_id = mapped_column(Integer, nullable=False)

    history: Mapped['History'] = relationship('History', back_populates='history_sources')
    source_resource: Mapped['Resources'] = relationship('Resources', back_populates='history_sources')


class JobSources(Base):
    __tablename__ = 'job_sources'
    __table_args__ = (
        ForeignKeyConstraint(['job_id'], ['jobs.job_id'], name='job_sources_jobs_FK'),
        ForeignKeyConstraint(['source_resource_id'], ['resources.resource_id'], name='job_sources_resources_FK'),
        Index('job_sources_job_id_IDX', 'job_id', 'source_resource_id', unique=True)
    )

    job_source_id = mapped_column(Integer, primary_key=True)
    job_id = mapped_column(Integer, nullable=False)
    source_resource_id = mapped_column(Integer, nullable=False)

    job: Mapped['Jobs'] = relationship('Jobs', back_populates='job_sources')
    source_resource: Mapped['Resources'] = relationship('Resources', back_populates='job_sources')
