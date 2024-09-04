import logging
import sys
import typing
import wx

import BackupTrackerDao
import BackupTrackerWx

from sqlalchemy import create_engine

from sqlalchemy.orm import Session

from BackupTrackerEntities import *


class BackupTrackerMainFrame (BackupTrackerWx.BackupTrackerMainFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.jobs: List[Job] = []
        self.session: typing.Optional[Session] = None
        self.dao: typing.Optional[BackupTrackerDao.BackupTrackerDao] = None

        for column in self.m_dataViewJobs.Columns:
            column.SetSortable(sortable=True)

    def onFileOpen(self, event):
        self.load_from_database()

    def load_from_database(self):
        if self.session is not None:
            self.session.close()
        engine = create_engine("sqlite:///BackupTracker.db", echo=True)
        self.session = Session(engine)
        self.dao = BackupTrackerDao.BackupTrackerDao(self.session)

        self.m_dataViewJobs.DeleteAllItems()
        self.jobs = self.dao.jobs()
        for job in self.jobs:
            self.m_dataViewJobs.AppendItem([job.job_description, job.job_tool, job.destination.destination_path])



def main(args):
    app = wx.App(False)
    frame = BackupTrackerMainFrame(parent=None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main(sys.argv[1:])
    