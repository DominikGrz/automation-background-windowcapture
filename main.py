import re, threading, win32gui, os, time, keyboard
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from hwndsframe import GetHwnds
from capturewindow import Capture
from inputmodule import Inputs
from gui import TailedGUI


class Game(threading.Thread):
    
    hwnd = None
    inputs = None
    frames = None
    
    def __init__(self):
        self.gui = TailedGUI()
        threading.Thread.__init__(self)

        
    def run(self):
        while self.gui.title is None:
            time.sleep(1)
        self.hwnd = GetHwnds(self.gui.title, 'MainWindowWindow', False)
        self.frames = Capture(self.hwnd.game, 30, False)
        self.inputs = Inputs(self.hwnd.input, self.hwnd.game)
        self.dungeon = self.timer(35)
        self.train = self.timer(5)
        self.checktrigger = True
        self.check = threading.Thread(target=self.check_fail, daemon=True)
        self.check.start()
        self.values = threading.Thread(target=self.find_values, daemon=True)
        self.values.start()
        while True:
            time.sleep(1)
            if self.gui.mode.get() is True:
                self.gui.print_finder(' ')
                self.selection()
            elif self.gui.mode.get() is False:
                self.background_ad_skip()
            elif not self.gui.window.winfo_exists():
                break
    
    # helper
    def timer_print(self, minutes, what):
        return str(int(((minutes*60)-(time.time()-what))/60))
    def timer_compare(self, minutes, what):    
        return (minutes*60)<(time.time()-what)
    def timer(self, minutes):
        return (time.time())-(minutes*60)

    #mostly main
    def return_to(self, where):
        timer = time.time()
        while self.where_am_i() != where:
            currtime = time.time()
            self.inputs.key('k')
            time.sleep(1)
            if 20<(currtime-timer):
                self.restart_game()
    
    # main automation
    def selection(self):
        if self.where_am_i() != 'main':
            self.return_to('main')
        if self.frames.extract_pixel(43, 134) == [152, 152, 160] and self.gui.buff.get(): #check buff icon
            self.do_buffs()
            if self.where_am_i() != 'main':
                self.return_to('main')
        if self.frames.extract_pixel(79, 948) == [231, 242, 231] and self.gui.shop.get(): #check checkmark icon
            self.do_shop()
            if self.where_am_i() != 'main':
                self.return_to('main')
        if self.frames.extract_pixel(512, 209) == [84, 164, 229] and self.gui.rush.get(): #check rush icon
            self.inputs.tap(508, 214)
            time.sleep(7)
        if not self.checktrigger and self.gui.prestige.get(): # prestige
            self.do_prestige()
            self.checktrigger = True
            time.sleep(1)
            
        if self.timer_compare(35, self.dungeon) and self.gui.dungeon.get(): # DUNGEON
            if self.do_dungeons():
                self.dungeon = time.time()
        elif self.gui.dungeon.get():
            self.gui.print_line(f"Dungeon cd: {self.timer_print(35, self.dungeon)}min")
            time.sleep(3)
            
        if self.timer_compare(5, self.train) and self.gui.training.get(): # TRAINING
            if self.do_train():
                self.train = time.time()
        elif self.gui.training.get():
            self.gui.print_line(f"Train cd: {self.timer_print(5, self.train)}min")
            time.sleep(3)

    # helper to find values
    def find_values(self):
        while True:
            if keyboard.is_pressed('w'):
                cur_x, cur_y = win32gui.GetCursorPos()
                win_x, win_y, _, _ = self.frames.window

                offset_x = (1920+cur_x)-(1920+win_x)
                offset_y = cur_y-win_y
                if (0 < offset_x < self.frames.width) and (0 < offset_y < self.frames.height):
                    rgb = self.frames.extract_pixel(offset_x, offset_y)
                    print(f"({offset_x}, {offset_y}) == {rgb}")
                    time.sleep(1)
            else:
                time.sleep(0.2)
    
    #check if a stage has been failed
    def check_fail(self):
        while True:
            if self.checktrigger:
                try:
                    if self.gui.prestige.get() is True:
                        result = self.frames.find_needle('prestige/', 'timesup.PNG', 0.95)
                        if result != False:
                            self.checktrigger = False
                        time.sleep(1)
                    else:
                        time.sleep(1)
                except:
                    break
            else:
                    time.sleep(1)

    # helper if multiple values to check
    def e_p(self, list, color):
        for i in list:
            if self.frames.extract_pixel(i[0], i[1]) != color:
                return False
        return True

    # return where the main screen is located at
    def where_am_i(self, counter=0):
        if self.e_p([(117,211),(405,220),(117,546),(427,542),(137,769),(431,752),(276, 503),(8, 38)], [0, 0, 0]): # black screen  
            if self.frames.extract_pixel(118, 351) != [0, 0, 0]: # stage transition
                time.sleep(4)
                return self.where_am_i()
            elif counter == 3:
                return 'brokenad'
            else:
                time.sleep(3)
                counter += 1
                return self.where_am_i(counter)
        elif self.frames.extract_pixel(265, 272) == [66, 117, 99]:
            return 'buff'
        elif self.frames.extract_pixel(385, 248) == [140, 158, 160]: # dungeon rewards
            return 'reward'
        elif self.frames.extract_pixel(288, 387) == [6, 6, 6]: # offline rewards
            return 'reward'
        elif self.frames.extract_pixel(394, 256) == [85, 83, 93]: # shop rewards
            return 'reward'
        elif self.frames.extract_pixel(496, 966) == [82, 81, 82]: # currently inside a dungeon
            return 'doingdungeon'
        elif self.frames.extract_pixel(42, 980) == [33, 42, 74]: # currently inside a tower
            return 'doingdungeon'
        elif self.frames.extract_pixel(498, 128) == [22, 45, 63]:
            return 'main'
        elif self.frames.extract_pixel(54, 941) == [196, 194, 221]:
            return 'shop'
        elif self.frames.extract_pixel(165, 941) == [196, 196, 219]:
            return 'card'
        elif self.frames.extract_pixel(276, 941) == [196, 197, 217]:
            return 'character'
        elif self.frames.extract_pixel(387, 941) == [196, 198, 216]:
            return 'fairies'
        elif self.frames.extract_pixel(498, 941) == [196, 198, 216]:
            return 'dungeon'
        else:
            return 'ad'
    
    # restarts the game
    def restart_game(self):
        self.gui.print_line('Restarting...')
        self.inputs.tap(107, 67)
        time.sleep(1)
        
        self.gui.print_line('Loading...')
        timer = time.time()
        currtime = time.time()
        while (self.where_am_i() != 'main') and (60>(currtime-timer)):
            currtime = time.time()
            time.sleep(1)
            if self.frames.extract_pixel(320,626) == [115, 190, 231]:
                self.restart_game()
                return
            if (30<(currtime-timer)) or (self.where_am_i() in ['reward', 'buff']):
                self.gui.print_line('Attempting to close popups')
                self.inputs.tap(992, 279)
                time.sleep(2)
                if (30<(currtime-timer)) or (self.where_am_i() in ['reward', 'buff']):
                    self.inputs.key('k')
        if self.where_am_i() != 'main':
            self.restart_game()
            return
        else:
            self.gui.print_line('Restart finished')
            
    # buff module
    def do_buffs(self):
        self.gui.print_line('Checking buffs...')
        needles = tuple(os.listdir('buff/'))
        for i in needles:
            try_successful = False
            while not try_successful:
                time.sleep(2)
                if self.where_am_i() != 'buff':
                    if self.where_am_i() != 'main':
                        self.return_to('main')
                        time.sleep(1)
                    time.sleep(1)
                    self.inputs.tap(44, 136)
                time.sleep(3)
                result = self.frames.find_needle('buff/', i, 0.8, True)
                
                if result:
                    self.gui.print_line('Activating buff...')
                    self.inputs.tap(result[0], result[1])
                    time.sleep(3)

                    if self.broken_ad():
                        self.restart_game()
                        break
                    elif self.where_am_i() == 'ad':
                        time.sleep(3)
                        self.gui.print_line('Skipping ad...')
                        if self.skip_ad() is False:
                            try_successful = False
                            break
                        self.gui.print_line('Activated: '+ i[:-4])
                        try_successful = True
                else:
                    try_successful = True

        if self.where_am_i() != 'main':
            self.return_to('main')
            time.sleep(1)
        if self.frames.extract_pixel(43, 134) == [152, 152, 160]:
            self.do_buffs()
        self.gui.print_line('Buffs active')
    
    #dungeon module
    def do_dungeons(self):  
        self.gui.print_line('Checking dungeons')
        needles = tuple(os.listdir('dungeon/'))
        done_dungeon = False # if manages to check on all dungeons and doesnt do any set true
        while not done_dungeon:
            done_dungeon = True
            for i in needles:
                try_successful = False
                while not try_successful:
                    if self.where_am_i() != 'dungeon':
                        self.return_to('main')
                        self.inputs.tap(500, 943)
                        time.sleep(1)
                    time.sleep(0.5)
                    result = self.frames.find_needle('dungeon/', i, 0.87, True)
                    
                    if result:
                        self.gui.print_line('Found dungeon...')
                        self.inputs.tap(result[0], result[1])
                        time.sleep(1.5)
                        self.inputs.key('n')
                        if 'ad' in i:
                            time.sleep(3)
                            if self.broken_ad():
                                self.restart_game()
                                break
                            self.gui.print_line('Skipping ad...')
                            if self.skip_ad(0.5) is False:
                                try_successful = False
                            time.sleep(3)
                        else:
                            time.sleep(4)
                        if self.where_am_i() == 'doingdungeon':
                            timer = time.time()
                            while self.where_am_i() == 'doingdungeon':
                                currtime = time.time()
                                self.gui.print_line('Waiting...')
                                time.sleep(5)
                                if 200<(currtime-timer):
                                    self.restart_game()
                                    try_successful = False
                                    break
                            time.sleep(4)
                            self.inputs.key('k')
                            try_successful = True
                            done_dungeon = False
                            time.sleep(1)
                    else:
                        try_successful = True

        self.gui.print_line('No available dungeons left')
        return True
        
    #prestige module
    def do_prestige(self):
        self.gui.print_line('Returning...')
        self.inputs.tap(514, 140)
        time.sleep(1)
        if self.frames.extract_pixel(346,960) == [165, 178, 189]:
            time.sleep(1)
            self.inputs.tap(279, 968)
            time.sleep(15)
            self.inputs.tap(279, 968)
            time.sleep(5)
            self.gui.print_line('Return finished')
        else:
            time.sleep(1)
            self.inputs.tap(507, 432)
            self.gui.print_line('Cant Return yet')
            time.sleep(2)
    
    #train module
    def do_train(self):
        self.gui.print_line('Training...')
        if self.where_am_i() != 'main':
            self.return_to('main')
        self.inputs.key('m')
        time.sleep(12)
        self.gui.print_line('Trained')
        return True
    
    #shop module
    def do_shop(self):
        self.gui.print_line('Claiming rewards...')
        self.inputs.key('l')
        time.sleep(13)
        while self.where_am_i() == 'ad':
            self.skip_ad()
            time.sleep(1)
        time.sleep(2)
        if self.where_am_i() != 'main':
            self.return_to('main')
        self.inputs.key('j')
        time.sleep(13)
        while self.where_am_i() == 'ad':
            self.skip_ad()
            time.sleep(1)
        time.sleep(2)
        if self.where_am_i() != 'main':
            self.return_to('main')
        self.gui.print_line('Rewards claimed')
    
    # old event
    def do_event_check(self):
        if self.where_am_i() != 'main':
            self.return_to('main')
        time.sleep(2)
        self.inputs.tap(41, 490)
        time.sleep(1)
        self.inputs.tap(357, 935)
        time.sleep(2)
        if self.frames.extract_pixel(169,551) != [156, 174, 189]:
            self.gui.print_line('Claiming...')
            self.inputs.tap(190, 539)
            time.sleep(2)
            result = self.skip_ad()
            time.sleep(2)
            if self.where_am_i() != 'main':
                self.return_to('main')
            return result
        else:
            self.gui.print_line('No reward')
            time.sleep(2)
            if self.where_am_i() != 'main':
                self.return_to('main')
            return
    
    # skips mosts ads using match template
    def skip_ad(self, delay=2):  
        best_loc = (0, 0) # tuple coordinates
        best_val = 0
        best_pic = None
        threshold = 0.75
        needles = tuple(os.listdir('needles/'))
        timer = time.time()
        self.gui.print_finder('Waiting for ad to progress...')
        time.sleep(10)
        while not best_val>threshold:
            self.gui.print_finder('Scanning...')
            #self.inputs.tap(260, 20)
            currtime = time.time()
            if 120<(currtime-timer): # if 2 minutes pass without success restart
                self.restart_game()
                return False
            if self.where_am_i() != 'ad':
                self.gui.print_finder('Returned to main')
                return False
            for i in needles:
                time.sleep(0.1)
                locations, values = self.frames.find_all_needle('needles/', i, threshold, values=True)
                if len(locations)>0: # add another check for locations in middle of game as the close button is usually towards the corners : DONE
                    for k in range(len(locations)):
                        if (values[k] > threshold) and (values[k] > best_val) and (locations[k][1]>32): # last check for the memu exit button
                            if not (70 <= locations[k][0] <= 485) and not (140 <= locations[k][1] <= 930):
                                best_val = round(values[k], 2)
                                best_loc = locations[k]
                                best_pic = i
                                self.gui.print_finder(f"New best match: {best_val} at: {best_loc}")
            time.sleep(delay)
        self.gui.print_finder(f'Scan successful, at {best_loc}')
        # google ad displays x immediately so, have to wait until it finishes, theyre mostly 5-30s long
        if best_pic == 'exitad1.JPG': 
            time.sleep(20)
            self.gui.print_finder('Closing google ad...')
            self.inputs.tap(best_loc[0], best_loc[1])
            return
        # double confirm for these
        elif best_pic in ('exitad0.JPG', 'exitad8.JPG', 'exitad11.JPG',' exitad12.JPG', 'exitad15.JPG'): 
            self.gui.print_finder('Closing double confirm ad...')
            self.inputs.tap(best_loc[0], best_loc[1])
            time.sleep(8)
            self.inputs.tap(best_loc[0], best_loc[1])
            return
        # trying to close uncommon ad
        self.gui.print_finder('Closing misc ad...')
        self.inputs.tap(best_loc[0], best_loc[1])
        time.sleep(1)

        timer = time.time()
        while self.where_am_i() == 'ad':
            currtime = time.time()
            if 60<(currtime-timer): # if 1 minutes pass without success restart
                self.restart_game()
                return False
    
    def broken_ad(self):
        if self.where_am_i() == 'brokenad': 
            time.sleep(4)
            if self.where_am_i() == 'brokenad': 
                return True
            
        return False
    
    def background_ad_skip(self):
        needles = tuple(os.listdir('needles/'))
        threshold = 0.75
        best_loc = (0, 0) # tuple coordinates
        best_val = 0
        best_pic = None
        success = False
        self.gui.print_finder('Scanning...')
        for i in needles:
            time.sleep(0.1)
            locations, values = self.frames.find_all_needle('needles/', i, threshold, values=True)
            if len(locations)>0: # add another check for locations in middle of game as the close button is usually towards the corners : DONE
                for k in range(len(locations)):
                    if (values[k] > threshold) and (values[k] > best_val) and (locations[k][1]>32): # last check to skip the memu exit button
                        if not (70 <= locations[k][0] <= 485) and not (140 <= locations[k][1] <= 930):
                            best_val = values[k]
                            best_loc = locations[k]
                            best_pic = i
                            self.gui.print_finder(f"New best match: {round(best_val, 2)} at: {best_loc}")
                            success = True
        time.sleep(2)
        if success:
            # google ad displays x immediately so, have to wait until it finishes, theyre mostly 30s long
            if best_pic == 'exitad1.JPG': 
                time.sleep(27)
                self.gui.print_finder(f"Closing google ad at: {best_loc}")
                self.inputs.tap(best_loc[0], best_loc[1])
            
            # double confirm for these, generally it would just search for it again but this faster
            elif best_pic in ('exitad0.JPG', 'exitad8.JPG', 'exitad11.JPG',' exitad12.JPG', 'exitad15.JPG'): 
                self.gui.print_finder(f"Closing double confirm ad at: {best_loc}")
                self.inputs.tap(best_loc[0], best_loc[1])
                time.sleep(8)
                self.inputs.tap(best_loc[0], best_loc[1])
            else:
                # trying to close uncommon ad
                self.gui.print_finder(f"Closing misc ad at: {best_loc}")
                self.inputs.tap(best_loc[0], best_loc[1])
                time.sleep(1)

# main process
def main():
    #initial setups
    game = Game()
    game.start()
    game.gui.run() # mainloop close program shutdown
    try:
        game.check.join()
    except:
        pass
    try:
        game.frames.output.join()
    except:
        pass
    try:
        game.frames.update.join()
    except:
        pass
    try:
        game.values.join()
    except:
        pass
    try:
        game.frames.pos.join()
    except:
        pass
    game.join()
    
    print('end')


if __name__ == '__main__':
    main()