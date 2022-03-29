import win32gui

class GetHwnds:
    game = 0
    input = 0

    def __init__(self, window_name=None):
        if window_name is None:
            self.game = win32gui.GetDesktopWindow()
        else:
            self.game = win32gui.FindWindow(None, window_name)
            if not self.game:
                raise Exception('Window not found: {}'.format(window_name))
        self.get_child_hwnd(self.game)
        
    def callback(self, hwnd, param):
        if win32gui.GetWindowText(hwnd) == "MainWindowWindow": # memu input window that works with win api
            self.input = hwnd
        if param[0] >= 0:
            if param[1] == param[0]:
                return 0
            param[1] += 1

    def get_child_hwnd(self, parent_hwnd):
        cur_child = 0
        param = [1, cur_child]
        win32gui.EnumChildWindows(parent_hwnd, self.callback, param)
        