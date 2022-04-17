import win32gui, time

class GetHwnds:
    game = 0
    input = 0
    
    def __init__(self, parentgame_window_name=None, childinput_window_name=False, wait=False): # parent main window, child window that accepts inputs, if wait true wait until the window appears
        if parentgame_window_name is None: 
            self.game = win32gui.GetDesktopWindow()
        else:
            if wait:
                while not self.game:
                    self.game = win32gui.FindWindow(None, parentgame_window_name)
                    time.sleep(0.1)
            else:
                self.game = win32gui.FindWindow(None, parentgame_window_name)
                if not self.game:
                    raise Exception(f"Window not found: {parentgame_window_name}")
            time.sleep(0.3)
            if childinput_window_name:
                self.childname = childinput_window_name
                self.get_child_hwnd(self.game)
                if not self.input:
                    raise Exception(f"Input window not found: {self.childname}")
        
    def callback(self, hwnd, param):
        if win32gui.GetWindowText(hwnd) == self.childname: # "MainWindowWindow" memu input window that works with win api
            self.input = hwnd
        if param[0] >= 0:
            if param[1] == param[0]:
                return 0
            param[1] += 1

    def get_child_hwnd(self, parent_hwnd):
        cur_child = 0
        param = [1, cur_child]
        win32gui.EnumChildWindows(parent_hwnd, self.callback, param)
        