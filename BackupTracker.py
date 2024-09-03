import sys
import wx

import BackupTrackerData
import BackupTrackerWx


class BackupTrackerMainFrame (BackupTrackerWx.BackupTrackerMainFrame):
    pass


def main(args):
    app = wx.App(False)
    frame = BackupTrackerMainFrame(parent=None)
    for r in BackupTrackerData.get_resources():
        frame.m_dataViewResourcesName.

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main(sys.argv[1:])
    