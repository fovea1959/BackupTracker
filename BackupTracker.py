import logging
import sys
import wx
import wx.dataview

import BackupTrackerDao
import BackupTrackerEntities
import BackupTrackerWx

from sqlalchemy import create_engine

from sqlalchemy.orm import Session

from BackupTrackerEntities import *


class EditJobDialog(BackupTrackerWx.EditJobDialog):
    def __init__(self, parent=None, job=None, sources=None, destinations=None):
        super().__init__(parent=parent)

        if sources is None:
            sources = []
        self.m_sourcesCheckList.Clear()
        for ss in sources:  # type: Source
            self.m_sourcesCheckList.Append(ss.source_path)

        if destinations is None:
            destinations = []
        self.m_destination.Clear()
        for dd in destinations:  # type: Destination
            self.m_destination.Append(dd.destination_path)


class BackupTrackerMainFrame(BackupTrackerWx.BackupTrackerMainFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.jobs: List[Job] = []
        self.sources: List[Source] = []
        self.session: typing.Optional[Session] = None
        self.dao: typing.Optional[BackupTrackerDao.BackupTrackerDao] = None

    def onFileOpen(self, event):
        self.load_from_database()

    def onAddJob(self, event):
        with EditJobDialog(self, sources=self.dao.sources().all(), destinations=self.dao.destinations().all()) as dlg:
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

    def onSourceSelected(self, event: wx.dataview.DataViewEvent):
        clicked_source: BackupTrackerEntities.Source = self.sources[self.m_dataViewSources.GetSelectedRow()]
        logging.debug("source selected: %s", self.m_dataViewJobs.GetSelection())
        logging.debug("selectedRow %s", self.m_dataViewJobs.GetSelectedRow())
        logging.debug("selection name = %s", clicked_source)

        self.m_dataViewSourceHistory.DeleteAllItems()
        history = sorted(clicked_source.history, key=lambda hh: hh.when, reverse=True)
        for h in history:  # type: BackupTrackerEntities.History
            dt = str(h.when)
            self.m_dataViewSourceHistory.AppendItem([dt, h.job_tool, h.operation, h.destination.destination_path])

    def onSourceContext( self, event ):
        logging.debug("on source context: %s", event)
        self.m_sourcesPanel.PopupMenu(self.m_menu3, event.GetPosition())

    def load_from_database(self):
        if self.session is not None:
            self.session.close()
        engine = create_engine("sqlite:///BackupTracker.db", echo=False)
        self.session = Session(engine)
        self.dao = BackupTrackerDao.BackupTrackerDao(self.session)

        self.jobs = self.dao.jobs().all()
        logging.debug("jobs = %s %s", type(self.jobs), self.jobs)
        for job in self.jobs:
            self.m_dataViewJobs.AppendItem([job.job_description, job.job_tool, job.destination.destination_path])

        self.sources = self.dao.sources().all()
        self.m_dataViewSources.DeleteAllItems()
        for source in self.sources:
            self.m_dataViewSources.AppendItem([source.source_path])


def main(args):
    app = wx.App(False)
    frame = BackupTrackerMainFrame(parent=None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])
