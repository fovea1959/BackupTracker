import sys
import wx

import BackupTrackerWx


def main(args):
    app = wx.App(False)
    frame = BackupTrackerWx.MyFrame1(parent=None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main(sys.argv[1:])