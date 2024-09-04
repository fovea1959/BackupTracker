import datetime

import BackupTrackerEntities

from sqlalchemy.orm import Session
from sqlalchemy import select


class BackupTrackerDao:
    def __init__(self, session: Session = None):
        self.session = session

    def resources(self):
        stmt = select(BackupTrackerEntities.Resource)
        resources = self.session.scalars(stmt)
        return resources

    def resource_by_name(self, name: str = None):
        stmt = select(BackupTrackerEntities.Resource).where(BackupTrackerEntities.Resource.resource_path == name)
        result = self.session.scalars(stmt).first()
        return result

    def job_by_name(self, name: str = None):
        stmt = select(BackupTrackerEntities.Job).where(BackupTrackerEntities.Job.job_description == name)
        result = self.session.scalars(stmt).first()
        return result

    def record_job(self, job: BackupTrackerEntities.Job = None, when: datetime.datetime = None):
        h = BackupTrackerEntities.History()
        h.job = job
        h.job_description = job.job_description
        h.job_tool = job.job_tool
        h.destination = job.destination
        h.sources = job.sources
        h.when = when
        self.session.add(h)
        return h

    def history_for_job(self, job: BackupTrackerEntities.Job = None):
        stmt = select(BackupTrackerEntities.History).where(BackupTrackerEntities.History.job_id == job.job_id)
        result = self.session.scalars(stmt)
        return result

