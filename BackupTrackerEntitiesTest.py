import datetime
import os
import sys

import dateutil.parser

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import BackupTrackerEntities
import BackupTrackerDao

SS_S1_ARCHIVE_R = r'\\synology1\archive\r'
SS_S1_HOMES = r'\\synology1\homes'
SS_S1_HOUSEHOLD = r'\\synology1\household'
SS_S1_MUSIC = r'\\synology1\music'
SS_S1_PHOTOS = r'\\synology1\photos'

SS_S2_BACKUP_SETS = r'\\synology2\backup_sets'
SS_S2_VIDEO = r'\\synology2\video'

DD_ZALMAN_R = r'[zalman]:\r'
DD_ZALMAN_MUSIC = r'[zalman]:\music',
DD_WD_BLUE = r'bk_synology1_wd_blue.hbk'
DD_WX42_S1 = r'[WD-WX42D24ML7N4]:\WD-WX42D24ML7N4_synology1'
DD_WX42_S2 = r'[WD-WX42D24ML7N4]:\WD-WX42D24ML7N4_synology2'
DD_WD_BLACK = r'bk_video_wd_black'

jj = {
    'bkp_synology1_wd_blue': ((SS_S1_HOMES, SS_S1_HOUSEHOLD, SS_S1_PHOTOS), DD_WD_BLUE, 'hyperbackup', (
        ('integrity check', '2024-08-30 16:48'),
        ('backup', '2024-08-30 13:16'),
    ), {}),
    'WD-WX42D24ML7N4_synology1': ((SS_S1_HOMES, SS_S1_HOUSEHOLD, SS_S1_PHOTOS), DD_WX42_S1, 'hyperbackup', (
        ('backup', '2024-08-09 13:55'),
    ), {}),
    'WD-WX42D24ML7N4_synology2': ((SS_S2_BACKUP_SETS, SS_S2_VIDEO), DD_WX42_S2, 'hyperbackup', (
        ('backup', '2024-08-30 11:57'),
    ), {}),
    'bkp_video_wd_black': ((SS_S2_BACKUP_SETS, SS_S2_VIDEO), DD_WX42_S2, 'hyperbackup', (
        ('backup', '2024-08-30 14:12'),
        ('integrity check', '2020-10-18 13:36'),
    ), {}),
    'desktop/zalman_r': ((SS_S1_ARCHIVE_R, ), DD_ZALMAN_R, 'jfilesync', (
        ('backup', '2024-08-30'),
        ('backup', '2019-07-19 15:22'),
        ('backup', '2019-06-19 15:22'),
    ), {})
}


def main(argv):
    os.remove('BackupTracker.db')
    engine = create_engine("sqlite:///BackupTracker.db", echo=True)
    BackupTrackerEntities.Base.metadata.create_all(engine)

    ss = set()
    dd = set()
    for vtuple in jj.values():
        for s1 in vtuple[0]:
            ss.add(s1)
        dd.add(vtuple[1])
    print(ss)
    print(dd)

    with (Session(engine) as session):
        dao = BackupTrackerDao.BackupTrackerDao(session)

        for s in ss:
            session.add(BackupTrackerEntities.Source(source_path=s))
        for d in dd:
            session.add(BackupTrackerEntities.Destination(destination_path=d))
        session.commit()

        # add jobs
        for k, vtuple in jj.items():
            job = BackupTrackerEntities.Job(
                job_description=k,
                job_tool=vtuple[2],
                destination=dao.destination_by_name(vtuple[1]),
                sources=[dao.source_by_name(s1) for s1 in vtuple[0]]
            )
            session.add(job)
        session.commit()

        # add history
        for k, vtuple in jj.items():
            job = dao.job_by_name(k)

            for op, ts in vtuple[3]:
                when = dateutil.parser.parse(ts)
                dao.record_job(job=job, operation=op, when=when)
        session.commit()


if __name__ == '__main__':
    main(sys.argv[1:])
