import wx.adv
import wx

from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))

TRAY_TOOLTIP = 'Name' 
TRAY_ICON = '/home/maeve/Code/HorizonsThemer/icon.png'

import wx.adv
import wx
TRAY_TOOLTIP = 'Name' 
TRAY_ICON = 'icon.png' 

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.COUNT = 0
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        #self.Bind(None, None)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Next Wallpaper', self.next_wallpaper)
        create_menu_item(menu, 'Last Wallpaper', self.last_wallpaper)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)
 
    def on_left(self, event):
        pass

    def next_wallpaper(self, event):
        self.COUNT += 1
        print(self.COUNT)

    def last_wallpaper(self, event):
        self.COUNT -= 1
        print(self.COUNT)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
