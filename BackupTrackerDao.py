import datetime
import typing

import BackupTrackerEntities

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine.result import ScalarResult


class BackupTrackerDao:
    def __init__(self, session: Session = None):
        self.session = session

    def sources(self):
        stmt = select(BackupTrackerEntities.Source)
        resources = self.session.scalars(stmt)
        return resources

    def source_by_name(self, name: str = None):
        stmt = select(BackupTrackerEntities.Source).where(BackupTrackerEntities.Source.source_path == name)
        result = self.session.scalars(stmt).first()
        return result

    def destinations(self):
        stmt = select(BackupTrackerEntities.Destination)
        resources = self.session.scalars(stmt)
        return resources

    def destination_by_name(self, name: str = None):
        stmt = select(BackupTrackerEntities.Destination).where(BackupTrackerEntities.Destination.destination_path == name)
        result = self.session.scalars(stmt).first()
        return result

    def jobs(self) -> ScalarResult[BackupTrackerEntities.Job]:
        stmt = select(BackupTrackerEntities.Job)
        result = self.session.scalars(stmt)
        return result

    def job_by_name(self, name: str = None):
        stmt = select(BackupTrackerEntities.Job).where(BackupTrackerEntities.Job.job_description == name)
        result = self.session.scalars(stmt).first()
        return result

    def record_job(self, job: BackupTrackerEntities.Job = None, operation: str = None, when: datetime.datetime = None):
        h = BackupTrackerEntities.History()
        h.job_id = job.job_id
        h.job_description = job.job_description
        h.job_tool = job.job_tool
        h.operation = operation
        h.destination = job.destination
        h.sources = job.sources
        h.when = when
        self.session.add(h)
        return h

    def history_for_job(self, job: BackupTrackerEntities.Job = None):
        stmt = select(BackupTrackerEntities.History).where(BackupTrackerEntities.History.job_id == job.job_id)
        result = self.session.scalars(stmt)
        return result

