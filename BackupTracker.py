import sys
import wx

import BackupTrackerData
import BackupTrackerWx


class BackupTrackerMainFrame (BackupTrackerWx.BackupTrackerMainFrame):
    pass


def main(args):
    app = wx.App(False)
    frame = BackupTrackerMainFrame(parent=None)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main(sys.argv[1:])
    