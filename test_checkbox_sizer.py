#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# from https://discuss.wxpython.org/t/dynamic-scrolled-window-with-a-static-area/34746/7

import wx
import wx.lib.scrolledpanel as scrolled


class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)

        self.scroll = scrolled.ScrolledPanel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)

        self.panel = wx.Panel(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)

        self.checkbox_1 = wx.CheckBox(self.scroll, wx.ID_ANY, "aaaaaaaa")
        self.checkbox_2 = wx.CheckBox(self.scroll, wx.ID_ANY, "bbbbbbbb")
        self.checkbox_3 = wx.CheckBox(self.scroll, wx.ID_ANY, "cccccccccccccccc")
        self.checkbox_4 = wx.CheckBox(self.scroll, wx.ID_ANY, "ddddd")
        self.checkbox_5 = wx.CheckBox(self.scroll, wx.ID_ANY, "eeeeeeeee")
        self.checkbox_6 = wx.CheckBox(self.scroll, wx.ID_ANY, "aaaaaaaa")
        self.checkbox_7 = wx.CheckBox(self.scroll, wx.ID_ANY, "bbbbbbbb")
        self.checkbox_8 = wx.CheckBox(self.scroll, wx.ID_ANY, "ccccccccccccccccggggggggggggggggggggggggg")
        self.checkbox_9 = wx.CheckBox(self.scroll, wx.ID_ANY, "ddddd")
        self.checkbox_10 = wx.CheckBox(self.scroll, wx.ID_ANY, "eeeeeeeee")
        self.checkbox_11 = wx.CheckBox(self.scroll, wx.ID_ANY, "aaaaaaaa")
        self.checkbox_12 = wx.CheckBox(self.scroll, wx.ID_ANY, "bbbbbbbb")
        self.checkbox_13 = wx.CheckBox(self.scroll, wx.ID_ANY, "cccccccccccccccc")
        self.checkbox_14 = wx.CheckBox(self.scroll, wx.ID_ANY, "ddddd")
        self.checkbox_15 = wx.CheckBox(self.scroll, wx.ID_ANY, "eeeeeeeee")
        self.checkbox_16 = wx.CheckBox(self.scroll, wx.ID_ANY, "aaaaaaaa")
        self.checkbox_17 = wx.CheckBox(self.scroll, wx.ID_ANY, "bbbbbbbb")
        self.checkbox_18 = wx.CheckBox(self.scroll, wx.ID_ANY, "cccccccccccccccc")
        self.checkbox_19 = wx.CheckBox(self.scroll, wx.ID_ANY, "ddddd")
        self.checkbox_20 = wx.CheckBox(self.scroll, wx.ID_ANY, "eeeeeeeee")
        self.checkbox_21 = wx.CheckBox(self.scroll, wx.ID_ANY, "eeeeeeeee")
        self.checkbox_22 = wx.CheckBox(self.scroll, wx.ID_ANY, "aaaaaaaa")
        self.checkbox_23 = wx.CheckBox(self.scroll, wx.ID_ANY, "bbbbbbbb")
        self.checkbox_24 = wx.CheckBox(self.scroll, wx.ID_ANY, "cccccccccccccccc")
        self.checkbox_25 = wx.CheckBox(self.scroll, wx.ID_ANY, "25ddddd")
        self.checkbox_26 = wx.CheckBox(self.scroll, wx.ID_ANY, "26eeeeeeeee")
        self.checkbox_27 = wx.CheckBox(self.scroll, wx.ID_ANY, "27eeeeeeeee")
        self.checkbox_28 = wx.CheckBox(self.scroll, wx.ID_ANY, "28aaaaaaaa")
        self.checkbox_29 = wx.CheckBox(self.scroll, wx.ID_ANY, "29bbbbbbbb")
        self.checkbox_30 = wx.CheckBox(self.scroll, wx.ID_ANY, "30cccccccccccccccc")
        self.checkbox_31 = wx.CheckBox(self.scroll, wx.ID_ANY, "31ddddd")

        self.button1 = wx.Button(self.panel, wx.ID_ANY, "button_1")
        self.button2 = wx.Button(self.panel, wx.ID_ANY, "button_2")

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("dialog")

        self.scroll.SetScrollRate(0, 25)

    def __do_layout(self):
        sizer_general = wx.BoxSizer(wx.VERTICAL)

        sizer_main = wx.StaticBox(self.scroll, wx.ID_ANY, "Select some boxes : ")
        sizer_corp = wx.StaticBoxSizer(sizer_main, wx.VERTICAL)

        sizer_list = wx.BoxSizer(wx.VERTICAL)
        sizer_list.Add((-1, 15))

        sizer_list.Add(self.checkbox_1, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_2, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_3, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_4, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_5, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_6, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_7, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_8, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_9, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_10, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_11, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_12, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_13, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_14, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_15, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_16, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_17, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_18, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_19, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_20, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_21, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_22, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_23, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_24, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_25, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_26, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_27, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_28, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_29, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_30, 0, wx.ALL, 5)
        sizer_list.Add(self.checkbox_31, 0, wx.ALL, 5)

        sizer_corp.Add(sizer_list, 0, wx.ALL, 5)

        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        sizer_buttons.Add(self.button1, 0, wx.ALL | wx.CENTER, 5)
        sizer_buttons.Add(self.button2, 0, wx.ALL | wx.CENTER, 5)

        sizer_general.Add(self.scroll, 1, wx.ALL | wx.EXPAND, 20)
        sizer_general.Add((15, 15))
        sizer_general.Add(self.panel, 0, wx.ALL | wx.EXPAND, 5)
        sizer_general.Add((5, 5))

        self.scroll.SetSizer(sizer_corp)
        self.scroll.SetAutoLayout(1)
        self.scroll.SetupScrolling(scroll_y=True)

        self.panel.SetSizer(sizer_buttons)
        self.panel.SetAutoLayout(1)

        self.SetSizer(sizer_general)
        self.Layout()


class MyApp(wx.App):
    def OnInit(self):
        self.dialog = MyDialog(None, wx.ID_ANY, "")
        self.SetTopWindow(self.dialog)
        self.dialog.ShowModal()
        self.dialog.Destroy()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
