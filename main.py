import re, threading, win32gui, os, time
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
        print("Wow!")
        while self.gui.title == None:
            time.sleep(1)
        self.hwnd = GetHwnds(self.gui.title)
        self.frames = Capture(self.hwnd.game, 30, False)
        self.inputs = Inputs(self.hwnd.input, self.hwnd.game)
        self.dungeon = self.timer(35)
        self.train = self.timer(3)
        self.event = self.timer(60)
        self.check = threading.Thread(target=self.check_fail)
        self.check.setDaemon(True)
        self.check.start()
        while True:
            time.sleep(1)
            if self.gui.mode.get() == True:
                self.gui.print_finder(" ")
                self.selection()
            elif self.gui.mode.get() == False:
                self.background_ad_skip()
                
                
    def selection(self):
        self.gui.print_line("doing selection mode")
        current_time = time.time()
        time.sleep(1)
        print(self.where_am_i())
        
        if self.where_am_i() in ["playstore", "home"]:
            time.sleep(4)
            if self.where_am_i() in ["playstore", "home"]:
                self.restart_game()          
        elif self.where_am_i() == "ad":
            time.sleep(10)
            if self.where_am_i() == "ad":
                self.skip_ad()
        #while self.where_am_i() in ["shop", "card", "fairies", "character", "dungeon"]:
        #    time.sleep(10)
        
        counter = 0
        self.return_home()
        while self.frames.extract_pixel(45, 139) != [61, 127, 197]:
            self.do_buffs()
            counter =+ 1
            if counter>10:
                self.restart_game()
        
        #counter = 0
        #game.return_home()
        #while game.frames.extract_pixel(85, 949) != [33, 36, 57]:
        #    game.do_shop()
        #    counter =+ 1
        #    if counter>10:
        #        game.restart_game()
        
        self.inputs.tap(508, 214) #rush
        if self.where_am_i() == "main":
            time.sleep(2)
            print(str(int(((35*60)-(current_time-self.dungeon))/60))+"min left on dungeon")
            if (35*60)<(current_time-self.dungeon): # 35min
                c = self.do_dungeons()
                if c != 'Failed':
                    self.dungeon = time.time()
            time.sleep(2)
            print(str(int(((3*60)-(current_time-self.train))/60))+"min left on train")
            if (3*60)<(current_time-self.train): # 3min
                d = self.do_train()
                if d != 'Failed':
                    self.train = time.time()
            time.sleep(2)
            print(str(int(((60*60)-(current_time-self.event))/60))+"min left on event check")
            if (60*60)<(current_time-self.event): # 60min
                d = self.do_event_check()
                if d != 'Failed':
                    self.event = time.time()
                
    def selection2(self):
        time.sleep(5)

 
        while True:
            current_time = time.time()
            time.sleep(1)
            print(self.where_am_i())
            
            if self.where_am_i() in ["playstore", "home"]:
                time.sleep(4)
                if self.where_am_i() in ["playstore", "home"]:
                    self.restart_game()          
            elif self.where_am_i() == "ad":
                time.sleep(10)
                if self.where_am_i() == "ad":
                    self.skip_ad()
            #while self.where_am_i() in ["shop", "card", "fairies", "character", "dungeon"]:
            #    time.sleep(10)
            
            counter = 0
            self.return_home()
            while self.frames.extract_pixel(45, 139) != [61, 127, 197]:
                self.do_buffs()
                counter =+ 1
                if counter>10:
                    self.restart_game()
            
            #counter = 0
            #game.return_home()
            #while game.frames.extract_pixel(85, 949) != [33, 36, 57]:
            #    game.do_shop()
            #    counter =+ 1
            #    if counter>10:
            #        game.restart_game()
            
            self.inputs.tap(508, 214) #rush
            if self.where_am_i() == "main":
                time.sleep(2)
                print(str(int(((180*60)-(current_time-prestige))/60))+"min left on return")
                if (180*60)<(current_time-prestige): # 60min
                    b = self.do_prestige()
                    if b != 'Failed':
                        prestige = time.time()
                time.sleep(2)
                print(str(int(((35*60)-(current_time-dungeon))/60))+"min left on dungeon")
                if (35*60)<(current_time-dungeon): # 35min
                    c = self.do_dungeons()
                    if c != 'Failed':
                        dungeon = time.time()
                time.sleep(2)
                print(str(int(((3*60)-(current_time-train))/60))+"min left on train")
                if (3*60)<(current_time-train): # 3min
                    d = self.do_train()
                    if d != 'Failed':
                        train = time.time()
                time.sleep(2)
                print(str(int(((60*60)-(current_time-event))/60))+"min left on event check")
                if (60*60)<(current_time-event): # 60min
                    d = self.do_event_check()
                    if d != 'Failed':
                        event = time.time()


    def where_am_i(self): # HERE ITS HEIGHT THEN WIDTH from top left
        x_button = [176, 176, 206]
        black = [0, 0, 0]
        
        if (self.frames.extract_pixel(119, 93) == self.frames.extract_pixel(67, 506) == self.frames.extract_pixel(488, 517) == self.frames.extract_pixel(483, 168) == self.frames.extract_pixel(106, 889) == self.frames.extract_pixel(484, 885) == black):
            return "brokenad"
        elif self.frames.extract_pixel(282, 337) == black and self.frames.extract_pixel(281, 319) == [173, 211, 255]:
            return "buff"
        elif (self.frames.extract_pixel(371,230) == [140, 150, 156]) or (self.frames.extract_pixel(542, 592) == [16, 32, 57]) or((self.frames.extract_pixel(277, 295) == black)and(self.frames.extract_pixel(163, 246) == [140, 150, 156])):
            return "reward"
        elif self.frames.extract_pixel(35,858) == [123, 199, 231]:
            if self.frames.extract_pixel(366,91) == black:
                return "doingdungeon"
            return "main"
        elif self.frames.extract_pixel(55, 943) == x_button:
            return "shop"
        elif self.frames.extract_pixel(168, 943) == x_button:
            return "card"
        elif self.frames.extract_pixel(277, 943) == x_button:
            return "character"
        elif self.frames.extract_pixel(390, 943) == x_button:
            return "fairies"
        elif self.frames.extract_pixel(500, 943) == x_button or self.frames.extract_pixel(500, 943) == [41, 65, 107]:
            return "dungeon"
        else:
            return "ad"
        
    def restart_game(self):
        print("Restarting...")
        self.inputs.tap(107, 67)
        time.sleep(1)
        
        print("Loading...")
        timer = time.time()
        currtime = time.time()
        while (self.where_am_i() != "main") and (60>(currtime-timer)):
            currtime = time.time()
            time.sleep(1)
            if self.frames.extract_pixel(320,626) == [115, 190, 231]:
                self.restart_game()
                return
            if (30<(currtime-timer)) or (self.where_am_i() in ["reward", "buff"]):
                print("Attempting to close popups")
                self.inputs.tap(992, 279)
                time.sleep(2)
                if (30<(currtime-timer)) or (self.where_am_i() in ["reward", "buff"]):
                    self.inputs.key('k')
        if self.where_am_i() != 'main':
            self.restart_game()
            return
        else:
            print("Restart finished")
            
    # returns to the main menu screen
    def return_home(self):
        timer = time.time()
        while self.where_am_i() != "main":
            currtime = time.time()
            self.inputs.key('k')
            time.sleep(0.5)
            if 20<(currtime-timer):
                self.restart_game()
            
    def skip_ad(self):  
        best_loc = (0, 0) # tuple coordinates
        best_val = 0
        best_pic = None
        threshold = 0.75
        needles = tuple(os.listdir('needles/'))
        timer = time.time()
        print("Waiting for ad to progress...")
        time.sleep(10)
        while not best_val>threshold:
            print('Scanning...')
            #self.inputs.tap(260, 20)
            currtime = time.time()
            if 120<(currtime-timer): # if 2 minutes pass without success restart
                self.restart_game()
                return 'Failed'
            if self.where_am_i() == "main":
                print('Returned to main')
                return 'Failed'
            elif self.where_am_i() != "ad":
                return 'Failed'
            for i in needles:
                time.sleep(0.1)
                locations, values = self.frames.find_all_needle('needles/', i, threshold, values=True)
                if len(locations)>0: # add another check for locations in middle of game as the close button is usually towards the corners : DONE
                    for k in range(len(locations)):
                        if (values[k] > threshold) and (values[k] > best_val) and (locations[k][1]>32): # last check for the memu exit button
                            if not (70 <= locations[k][0] <= 485) and not (140 <= locations[k][1] <= 930):
                                best_val = values[k]
                                best_loc = locations[k]
                                best_pic = i
                                print("New best match: " +str(best_val)+ " at:" + str(best_loc))
            time.sleep(1)
        print("Scan successful")
        print(best_loc)
        
        # google ad displays x immediately so, have to wait until it finishes, theyre mostly 30s long
        if best_pic == 'exitad1.JPG': 
            time.sleep(20)
            print("Closing google ad...")
            self.inputs.tap(best_loc[0], best_loc[1])
            return
        
        # double confirm for these, generally it would just search for it again but this faster
        elif best_pic in ('exitad0.JPG', 'exitad8.JPG', 'exitad11.JPG',' exitad12.JPG', 'exitad15.JPG'): 
            print("Closing double confirm ad...")
            self.inputs.tap(best_loc[0], best_loc[1])
            time.sleep(8)
            self.inputs.tap(best_loc[0], best_loc[1])
            return
    
        
        # trying to close uncommon ad
        print("Closing misc ad...")
        self.inputs.tap(best_loc[0], best_loc[1])
        time.sleep(1)

        
        timer = time.time()
        while self.where_am_i() == "ad":
            currtime = time.time()
            if 60<(currtime-timer): # if 1 minutes pass without success restart
                self.restart_game()
                return 'Failed'
    
    def broken_ad(self):
        if self.where_am_i() == "brokenad": 
            time.sleep(4)
            if self.where_am_i() == "brokenad": 
                return True
            
        return False

    def do_buffs(self):
        print("Checking buffs...")
        needles = tuple(os.listdir('buff/'))
        for i in needles:
            try_successful = False
            while not try_successful:
                
                if self.where_am_i() != "buff":
                    self.return_home()
                    self.inputs.tap(50, 138)
                    time.sleep(1)
                time.sleep(1)
                result = self.frames.find_needle('buff/', i, 0.9, True)
                
                if result:
                    print("Activating buff...")
                    self.inputs.tap(result[0], result[1])
                    time.sleep(3)

                    if self.broken_ad():
                        self.restart_game()
                        break
                    elif self.where_am_i() == 'ad':
                        time.sleep(3)
                        print("Skipping ad...")
                        if self.skip_ad() == 'Failed':
                            try_successful = False
                            break
                        print("Activated: "+ i[:-4])
                        try_successful = True
                else:
                    try_successful = True

        self.return_home()
        print("Buffs active")
        
    def do_dungeons(self):  
        print("Checking dungeons")
        needles = tuple(os.listdir('dungeon/'))
        done_dungeon = False # if manages to check on all dungeons and doesnt do any set true
        while not done_dungeon:
            done_dungeon = True
            for i in needles:
                try_successful = False
                while not try_successful:
                    if self.where_am_i() != "dungeon":
                        self.return_home()
                        self.inputs.tap(500, 943)
                        time.sleep(1)
                    time.sleep(2)
                    print(i)
                    result = self.frames.find_needle('dungeon/', i, 0.87, True)
                    
                    if result:
                        print("Found dungeon...")
                        self.inputs.tap(result[0], result[1])
                        time.sleep(1.5)
                        self.inputs.key('n')
                        if 'ad' in i:
                            time.sleep(3)
                            if self.broken_ad():
                                self.restart_game()
                                break
                            print("Skipping ad...")
                            if self.skip_ad() == 'Failed':
                                try_successful = False
                            time.sleep(3)
                        else:
                            time.sleep(4)
                        if self.where_am_i() == "doingdungeon":
                            timer = time.time()
                            while self.where_am_i() == "doingdungeon":
                                currtime = time.time()
                                print("Waiting...")
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

        print("No available dungeons left")    
        
    def check_fail(self):
        while True:
            if self.gui.prestige.get() == True:
                result = self.frames.find_needle('prestige/', 'timesup.PNG', 0.95)
                if result != False:
                    self.do_prestige()
                time.sleep(1)
            else:
                time.sleep(1)
            
        
    def do_prestige(self):
        print("Returning...")
        self.inputs.tap(514, 140)
        time.sleep(1)
        if self.frames.extract_pixel(346,960) == [165, 178, 189]:
            time.sleep(1)
            self.inputs.tap(279, 968)
            time.sleep(15)
            self.inputs.tap(279, 968)
            time.sleep(5)
            if self.frames.extract_pixel(211,514) == [99, 195, 255]:
                print("Rush available")
                self.inputs.tap(508, 214)
                time.sleep(1.5)
                self.inputs.tap(280, 909)
                time.sleep(0.3)
                self.inputs.tap(280, 909)
                time.sleep(0.3)
                self.inputs.tap(280, 909)
                time.sleep(0.3)
                self.inputs.tap(280, 909)
                time.sleep(0.3)
                self.inputs.tap(280, 909)
                time.sleep(0.3)
                self.inputs.tap(280, 909)
                time.sleep(0.3)
                self.inputs.tap(280, 909)
                
            time.sleep(5)
            print("Return finished")
        else:
            time.sleep(1)
            self.inputs.tap(507, 432)
            print("Cant Return yet")
            time.sleep(2)
    
    def do_train(self):
        print("Training...")
        self.return_home()
        self.inputs.key('m')
        time.sleep(12)
        print("Trained")
        
    def do_shop(self):
        print("Claiming rewards...")
        self.return_home()
        self.inputs.tap(85, 949)
        time.sleep(1)
        self.inputs.tap(182, 879)
        self.inputs.key('l')
        time.sleep(10)
        self.inputs.tap(126, 298)
        time.sleep(3)
        while self.where_am_i() == "ad":
            self.skip_ad()
            time.sleep(1)
        time.sleep(2)
        self.inputs.key('k')
        if self.where_am_i() != "shop":
            self.inputs.tap(85, 949)
        time.sleep(1)
        self.inputs.tap(378, 877)
        time.sleep(2)
        self.inputs.tap(123, 414)
        time.sleep(3)
        while self.where_am_i() == "ad":
            self.skip_ad()
            time.sleep(1)
        time.sleep(2)
        self.return_home()
        print("Rewards claimed")
        
    def do_event_check(self):
        self.return_home()
        time.sleep(2)
        self.inputs.tap(41, 490)
        time.sleep(1)
        self.inputs.tap(357, 935)
        time.sleep(2)
        if self.frames.extract_pixel(169,551) != [156, 174, 189]:
            print("Claiming...")
            self.inputs.tap(190, 539)
            time.sleep(2)
            result = self.skip_ad()
            time.sleep(2)
            self.return_home()
            return result
        else:
            print("No reward")
            time.sleep(2)
            self.return_home()
            return
        
    def timer(self, minutes):
        return (time.time())-(minutes*60)

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
                            self.gui.print_finder("New best match: " +str(round(best_val, 2))+ " at:" + str(best_loc))
                            success = True
        time.sleep(2)
        if success:
            # google ad displays x immediately so, have to wait until it finishes, theyre mostly 30s long
            if best_pic == 'exitad1.JPG': 
                time.sleep(27)
                self.gui.print_finder("Closing google ad at:"+ str(best_loc))
                self.inputs.tap(best_loc[0], best_loc[1])
            
            # double confirm for these, generally it would just search for it again but this faster
            elif best_pic in ('exitad0.JPG', 'exitad8.JPG', 'exitad11.JPG',' exitad12.JPG', 'exitad15.JPG'): 
                self.gui.print_finder("Closing double confirm ad at:"+ str(best_loc))
                self.inputs.tap(best_loc[0], best_loc[1])
                time.sleep(8)
                self.inputs.tap(best_loc[0], best_loc[1])
            else:
                # trying to close uncommon ad
                self.gui.print_finder("Closing misc ad at:"+ str(best_loc))
                self.inputs.tap(best_loc[0], best_loc[1])
                time.sleep(1)

# main process
def main():
    #initial setups
    game = Game()
    game.start()
    game.gui.run() # mainloop close program shutdown
    if game.frames in globals():
        game.frames.update.join()
        if game.frames.output in globals():
            game.frames.output.join()
    game.join()
    print("end")


if __name__ == "__main__":
    main()