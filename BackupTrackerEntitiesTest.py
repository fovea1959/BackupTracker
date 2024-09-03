import sys

import BackupTrackerEntities

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

def main(argv):
    engine = create_engine("sqlite:///BackupTracker.db", echo=True)
    with Session(engine) as session:
        stmt = select(BackupTrackerEntities.Resources)
        for resource in session.scalars(stmt):
            print(resource)


if __name__ == '__main__':
    main(sys.argv[1:])
