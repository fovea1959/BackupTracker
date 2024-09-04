import datetime
import os
import sys

import BackupTrackerEntities

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

    with Session(engine) as session:
        last_resource = None
        for r in rr:
            last_resource = BackupTrackerEntities.Resource(resource_path=r)
            session.add(last_resource)
        session.commit()

        stmt = select(BackupTrackerEntities.Resource)
        resource_map = {}
        for resource in session.scalars(stmt):
            print(resource)
            resource_map[resource.resource_path] = resource

        stmt = select(BackupTrackerEntities.Resource).where(BackupTrackerEntities.Resource.resource_path == r'[zalman]:\r')
        r = None
        for resource in session.scalars(stmt):
            r = resource

        print('zalman', r)

        history = BackupTrackerEntities.History(
            when=datetime.datetime.now(),
            job_tool='tool',
            job_description='description',
            destination=r,
            sources=[i for i in resource_map.values()]
        )
        session.add(history)

        session.commit()




if __name__ == '__main__':
    main(sys.argv[1:])
