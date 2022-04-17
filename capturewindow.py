import win32con, win32gui, win32ui, time, threading, cv2
import numpy as np
import re

#def threaded(fn):
#    def wrapper(*args, **kwargs):
#        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
#        thread.start()
#        return thread
#    return wrapper

class Capture():
    
    frame = 0
    rate = 30
    window = 0
    width = 0
    height = 0
    
    def __init__(self, windowhandle, rate=30, video=True):
        self.windowhandle = windowhandle
        self.rate = rate
        self.pos = threading.Thread(target=self.update_pos, daemon=True)
        self.pos.start()
        time.sleep(0.5)
        self.width = self.window[2]-self.window[0]
        self.height = self.window[3]-self.window[1]
        time.sleep(0.5)
        self.update = threading.Thread(target=self.update_frame, daemon=True)
        self.update.start()
        time.sleep(0.5)
        if video:
            self.output = threading.Thread(target=self.video_output, daemon=True)
            self.output.start()
        time.sleep(0.5)
        print("Initialization complete.")
    
    def update_pos(self):
        while True:
            self.window = win32gui.GetWindowRect(self.windowhandle)
            time.sleep(0.5)
    
    def update_frame(self):
        print("Capture running.")
        while True:
            self.frame = self.window_image()
            time.sleep(1./self.rate)
    
    
    def video_output(self):
        print("Video output running.")
        while True:
            cv2.imshow('Press Q to close window', self.frame)
            time.sleep(1./self.rate)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                time.sleep(0.5)
                cv2.destroyAllWindows()
                print("Video output closed.")
                break
    
    def window_image(self):
        # We do some magic # getting bitmap data
        wDC = win32gui.GetWindowDC(self.windowhandle)
        dcObj  = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(bmp)
        cDC.BitBlt((0, 0), (self.width, self.height), dcObj, (0, 0), win32con.SRCCOPY)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8') # convert bits into np array
        img.shape = (self.height, self.width, 4)
        
        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.windowhandle, wDC)
        win32gui.DeleteObject(bmp.GetHandle()) 
        
        img = img[...,:3] # slows down but needed for matchtemplate
        return np.ascontiguousarray(img)
    
    # returns one most likely match above threshold
    def find_needle(self, where, what, threshold=0.95, gray=False):
        needle = str(where) + str(what)
        img = cv2.imread(needle, 1)
        if gray:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray, img, cv2.TM_CCOEFF_NORMED)
        else:
            result = cv2.matchTemplate(self.frame, img, cv2.TM_CCOEFF_NORMED)
            
        _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
        
        if maxVal > threshold:
            print(str(what) +": "+ str(round(maxVal, 3)) + " at:" + str(maxLoc))
            return maxLoc
        else:
            return False
        
    def extract_pixel(self, x, y):
        temp = str(self.frame[y, x])
        return [int(s) for s in re.findall(r'\b\d+\b', temp)]
    
    # returns all matches above threshold
    def find_all_needle(self, where, what, threshold=0.85, values=False):
        needle = str(where) + str(what)
        img = cv2.imread(needle, 1)
        result = cv2.matchTemplate(self.frame, img, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold) # extract all locations where threshold is met
        if values is True:
            values = result[locations] # save the values at those locations
            locations = list(zip(*locations[::-1]))
            return locations, values
        else:
            locations = list(zip(*locations[::-1]))
            return locations
                
                
                