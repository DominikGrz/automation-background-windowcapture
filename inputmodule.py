import win32api, win32con, time

class Inputs:
    input_lookup = {
            'l':0x4C, #gear shop
            'j':0x4A, #gems shop
            'n':0x4E, #confirm
            'p':0x50, #
            'k':0x4B, #returnold
            'm':0x4D, #train
            'o':0x4F, #home
            'h':0x48, #chest
            }
    
    def __init__(self, mouse, keyboard):
        self.mouse = mouse
        self.keyboard = keyboard
    
    def key(self, key):
        if key in self.input_lookup:
            win32api.SendMessage(self.keyboard, win32con.WM_KEYDOWN, self.input_lookup.get(key), 0)
            time.sleep(0.05)
            win32api.SendMessage(self.keyboard, win32con.WM_KEYUP, self.input_lookup.get(key), 65539)
        else:
            raise Exception(f"Key: {key} not found in dict")

            
    def tap(self, x, y):
        win32api.SendMessage(self.mouse, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x,y))
        time.sleep(0.1)
        win32api.SendMessage(self.mouse, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x,y))
        time.sleep(0.1)
        
        
    def drag(self, move, to):
        win32api.SendMessage(self.mouse, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(move[0] ,move[1]))
        time.sleep(0.07)
        win32api.SendMessage(self.mouse, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(to[0] ,to[1]))

    
    #def click2(hwnd, x_y):
    #    win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, win32api.MAKELONG(x_y[0],x_y[1]))
    #    time.sleep(0.1)
    #    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x_y[0],x_y[1]))
    #    time.sleep(0.1)
    #    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x_y[0],x_y[1]))
    #    time.sleep(0.3)
