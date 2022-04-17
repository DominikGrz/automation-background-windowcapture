# Automated game on android over Memu Emulator

__hwndsframe.py__ - grabs needed window handles with __winapi__

__inputmodule.py__ - used to input mouse click and keyboard strokes using __winapi__

__capturewindow.py__ - using direct windows api calls allows to capture specific windows __fast__, even when in background or off the screen, also contains opencv match template functions

__gui.py__ - main window with options to set title and different modes using __tkinter__

-all of these can be used together with hwndsframe.py in other projects seperately


__main.py__ - contains the main code specific to the game, functions to do specific actions in the game, __skip ads__ using match template
