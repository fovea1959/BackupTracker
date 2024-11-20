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
                print(' ', hh, hh.job.job_description, hh.destination.destination_volume.volume_name + hh.destination.destination_directory)

        print ('x' * 80)
        for jj in dao.jobs().all():
            print(jj, jj.destination, jj.sources)
            for hh in dao.history_for_job(jj):
                print(' ', hh)


if __name__ == '__main__':
    main(sys.argv[1:])
