import datetime
import os
import sys
import time

import BackupTrackerEntities
import BackupTrackerDao

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


rr = [
    r'\\synology2\video',
    r'\\synology1\archive\r',
    r'\\synology1\music',
    r'\\synology1\video',
    r'[zalman]:\r'
]


def main(argv):
    os.remove('BackupTracker.db')
    engine = create_engine("sqlite:///BackupTracker.db", echo=True)
    BackupTrackerEntities.Base.metadata.create_all(engine)

    with (Session(engine) as session):
        dao = BackupTrackerDao.BackupTrackerDao(session)

        for r in rr:
            session.add(BackupTrackerEntities.Resource(resource_path=r))
        session.commit()

        resource_map = {}
        for resource in dao.resources():
            print(resource)
            resource_map[resource.resource_path] = resource

        r = dao.resource_by_name(r'[zalman]:\r')
        print('zalman', r)

        job = BackupTrackerEntities.Job(
            job_description='test job',
            job_tool='tool',
            destination=r,
            sources=[i for i in resource_map.values()]
        )
        session.add(job)
        session.commit()

        dao.record_job(job=job, when=datetime.datetime.now())
        session.commit()

        time.sleep(2.0)

        job.job_tool = 'new tool'
        dao.record_job(job=job, when=datetime.datetime.now())
        session.commit()

        job_record = dao.history_for_job(job=job)
        print("job_record", job_record)
        for r1 in job_record:
            print("job_record[]", r1)



if __name__ == '__main__':
    main(sys.argv[1:])
