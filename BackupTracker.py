import logging
import sys
import wx
import wx.dataview

import BackupTrackerDao
import BackupTrackerWx

from sqlalchemy import create_engine

from sqlalchemy.orm import Session

from BackupTrackerEntities import *


class EditJobDialog(BackupTrackerWx.EditJobDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.m_sourcesCheckList.Clear()
        for i in range(10):
            self.m_sourcesCheckList.Append(str(i))


class BackupTrackerMainFrame(BackupTrackerWx.BackupTrackerMainFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.jobs: List[Job] = []
        self.session: typing.Optional[Session] = None
        self.dao: typing.Optional[BackupTrackerDao.BackupTrackerDao] = None

        for column in self.m_dataViewJobs.Columns:
            column.SetSortable(sortable=True)

    def onFileOpen(self, event):
        self.load_from_database()

    def onAddJob(self, event):
        with EditJobDialog(self) as dlg:
            # show as modal dialog
            result = dlg.ShowModal()
            logging.debug(f"weighin dialog box {result}")

    def onJobSelected(self, event: wx.dataview.DataViewEvent):
        clicked_job = self.jobs[self.m_dataViewJobs.GetSelectedRow()]
        logging.debug("job selected: %s", self.m_dataViewJobs.GetSelection())
        logging.debug("selectedRow %s", self.m_dataViewJobs.GetSelectedRow())
        logging.debug("selection name = %s", clicked_job)

        self.m_dataViewListJobHistory.DeleteAllItems()
        history = self.dao.history_for_job(clicked_job)
        for h in history:
            dt = str(h.when)
            self.m_dataViewListJobHistory.AppendItem([dt, h.operation])

    def load_from_database(self):
        if self.session is not None:
            self.session.close()
        engine = create_engine("sqlite:///BackupTracker.db", echo=True)
        self.session = Session(engine)
        self.dao = BackupTrackerDao.BackupTrackerDao(self.session)

        self.m_dataViewJobs.DeleteAllItems()
        self.jobs = self.dao.jobs().all()
        logging.debug("jobs = %s %s", type(self.jobs), self.jobs)
        for job in self.jobs:
            self.m_dataViewJobs.AppendItem([job.job_description, job.job_tool, job.destination.destination_path])


def main(args):
    app = wx.App(False)
    frame = BackupTrackerMainFrame(parent=None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])
    