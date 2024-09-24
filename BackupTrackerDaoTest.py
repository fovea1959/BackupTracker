import datetime
import sys

import BackupTrackerDao
import BackupTrackerEntities

from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.orm import Session


class BackupTrackerDaoTest(BackupTrackerDao.BackupTrackerDao):
    pass


def main(argv):
    engine = create_engine("sqlite:///BackupTracker.db", echo=False)

    with (Session(engine) as session):
        dao = BackupTrackerDaoTest(session)

        sources = dao.sources().all()
        for ss in sources:
            print(ss)
            sorted_history = sorted(ss.history, key=lambda s: s.when, reverse=True)
            for hh in sorted_history: # type: BackupTrackerEntities.History
                w: datetime.datetime = hh.when
                print(' ', hh, hh.destination.destination_path)


if __name__ == '__main__':
    main(sys.argv[1:])
