import tkinter as tk
import tkinter.ttk as ttk
import operator

class TailedGUI():
    title = None
    console = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    output_lookup = ()
    button_lookup = ()
    
    def __init__(self):
        # build ui
        self.window = tk.Tk()
        
        # vars
        self.mode = tk.BooleanVar(self.window, True)
        
        
        self.training = tk.BooleanVar(self.window, True)
        self.shop = tk.BooleanVar(self.window, True)
        self.buff = tk.BooleanVar(self.window, True)
        self.prestige = tk.BooleanVar(self.window, True)
        self.rush = tk.BooleanVar(self.window, True)
        self.event = tk.BooleanVar(self.window, True)
        self.dungeon = tk.BooleanVar(self.window, True)
        self.fairy = tk.BooleanVar(self.window, True)
        self.monster = tk.BooleanVar(self.window, True)
        self.consolidate = tk.BooleanVar(self.window, True)
        default = tk.StringVar(self.window, value='(Tailed)')
        self.backgroundbuff = tk.BooleanVar(self.window, False)

        
        # entry
        self.entry = tk.Entry(self.window)
        self.entry.configure(background='#3c3c3c', borderwidth='0', font='{arial} 17 {bold}', foreground='#c8c8c8', textvariable=default)
        self.entry.configure(justify='center', width='16')
        self.entry.grid(column='0', ipadx='0', ipady='6', padx='32', pady='32', row='16', sticky='w')
        
        # button
        self.button1 = tk.Button(self.window)
        self.button1.configure(activebackground='#5a5a5a', background='#3c3c3c', borderwidth='0', font='{arial} 14 {bold}')
        self.button1.configure(foreground='#c8c8c8', justify='left', text='Set and Start')
        self.button1.grid(column='1', ipady='3', row='16', sticky='w')
        self.button1.configure(command=self.set_title)
        
        self.button2 = tk.Button(self.window)
        self.button2.configure(activebackground='#5a5a5a', background='#3c3c3c', borderwidth='0', font='{arial} 14 {bold}')
        self.button2.configure(foreground='#c8c8c8', justify='left', text='Switch')
        self.button2.grid(column='1', ipady='3', padx='140', row='16', sticky='w')
        self.button2.configure(command=self.switch_mode)
        
        # radiobuttons
        self.radiobutton1 = ttk.Radiobutton(self.window)
        self.radiobutton1.configure(text='Selection', value='1', variable=self.mode, command=lambda: self.switch_boxes('normal', 'disabled', True))
        self.radiobutton1.grid(column='0', ipadx='2', ipady='2', padx='32', pady='8', row='1', sticky='w')
        
        self.radiobutton2 = ttk.Radiobutton(self.window)
        self.radiobutton2.configure(text='Skip Ad Only', value='0', variable=self.mode, command=lambda: self.switch_boxes('disabled', 'normal', False))
        self.radiobutton2.grid(column='0', ipadx='2', ipady='2', padx='32', pady='8', row='1', sticky='e')
        
        # checkbuttons
        self.checkbutton1 = ttk.Checkbutton(self.window)
        self.checkbutton1.configure(offvalue=False, onvalue=True, text='Auto Consolidate', variable=self.consolidate)
        self.checkbutton1.grid(column='0', padx='32', pady='2', row='11', sticky='w')
        
        self.checkbutton2 = ttk.Checkbutton(self.window)
        self.checkbutton2.configure(offvalue=False, onvalue=True, text='Training', variable=self.training)
        self.checkbutton2.grid(column='0', padx='32', pady='2', row='2', sticky='w')
        
        self.checkbutton3 = ttk.Checkbutton(self.window)
        self.checkbutton3.configure(offvalue=False, onvalue=True, text='Shop Rewards', variable=self.shop)
        self.checkbutton3.grid(column='0', padx='32', pady='2', row='3', sticky='w')
        
        self.checkbutton4 = ttk.Checkbutton(self.window)
        self.checkbutton4.configure(offvalue=False, onvalue=True, text='Buffs', variable=self.buff)
        self.checkbutton4.grid(column='0', padx='32', pady='2', row='4', sticky='w')
        
        self.checkbutton5 = ttk.Checkbutton(self.window)
        self.checkbutton5.configure(offvalue=False, onvalue=True, text='Return', variable=self.prestige)
        self.checkbutton5.grid(column='0', padx='32', pady='2', row='5', sticky='w')
        
        self.checkbutton6 = ttk.Checkbutton(self.window)
        self.checkbutton6.configure(offvalue=False, onvalue=True, text='Rush', variable=self.rush)
        self.checkbutton6.grid(column='0', padx='32', pady='2', row='6', sticky='w')
        
        self.checkbutton7 = ttk.Checkbutton(self.window)
        self.checkbutton7.configure(offvalue=False, onvalue=True, text='Event', variable=self.event)
        self.checkbutton7.grid(column='0', padx='32', pady='2', row='7', sticky='w')
        
        self.checkbutton8 = ttk.Checkbutton(self.window)
        self.checkbutton8.configure(offvalue=False, onvalue=True, text='Dungeon', variable=self.dungeon)
        self.checkbutton8.grid(column='0', padx='32', pady='2', row='8', sticky='w')
        
        self.checkbutton9 = ttk.Checkbutton(self.window)
        self.checkbutton9.configure(offvalue=False, onvalue=True, text='Fairies', variable=self.fairy)
        self.checkbutton9.grid(column='0', padx='32', pady='2', row='9', sticky='w')
        
        self.checkbutton10 = ttk.Checkbutton(self.window)
        self.checkbutton10.configure(offvalue=False, onvalue=True, text='Monster Card', variable=self.monster)
        self.checkbutton10.grid(column='0', padx='32', pady='2', row='10', sticky='w')
        
        
        self.checkbutton11 = ttk.Checkbutton(self.window)
        self.checkbutton11.configure(offvalue=False, onvalue=True, text='+Buffs', state='disabled', variable=self.backgroundbuff)
        self.checkbutton11.grid(column='0', padx='69', pady='2', row='2', sticky='e')
        
        # console
        self.label1 = ttk.Label(self.window)
        self.label1.configure(background='#1e1e1e', font='{Arial} 12 {bold}', foreground='#c8c8c8', text='Program output')
        self.label1.grid(column='1', row='1', sticky='w')

        self.label2 = ttk.Label(self.window)
        self.label2.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label2.configure(justify='left', text=' ' , wraplength='320')
        self.label2.grid(column='1', padx='8', row='2', sticky='w')
        
        self.label3 = ttk.Label(self.window)
        self.label3.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label3.configure(justify='left', text=' ' , wraplength='320')
        self.label3.grid(column='1', padx='8', row='3', sticky='w')
        
        self.label4 = ttk.Label(self.window)
        self.label4.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label4.configure(justify='left', text=' ' , wraplength='320')
        self.label4.grid(column='1', padx='8', row='4', sticky='w')
        
        self.label5 = ttk.Label(self.window)
        self.label5.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label5.configure(justify='left', text=' ' , wraplength='320')
        self.label5.grid(column='1', padx='8', row='5', sticky='w')
        
        self.label6 = ttk.Label(self.window)
        self.label6.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label6.configure(justify='left', text=' ' , wraplength='320')
        self.label6.grid(column='1', padx='8', row='6', sticky='w')
        
        self.label7 = ttk.Label(self.window)
        self.label7.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label7.configure(justify='left', text=' ' , wraplength='320')
        self.label7.grid(column='1', padx='8', row='7', sticky='w')
        
        self.label8 = ttk.Label(self.window)
        self.label8.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label8.configure(justify='left', text=' ' , wraplength='320')
        self.label8.grid(column='1', padx='8', row='8', sticky='w')
        
        self.label9 = ttk.Label(self.window)
        self.label9.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label9.configure(justify='left', text=' ' , wraplength='320')
        self.label9.grid(column='1', padx='8', row='9', sticky='w')
        
        self.label10 = ttk.Label(self.window)
        self.label10.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label10.configure(justify='left', text=' ' , wraplength='320')
        self.label10.grid(column='1', padx='8', row='10', sticky='w')
        
        self.label11 = ttk.Label(self.window)
        self.label11.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label11.configure(justify='left', text=' ' , wraplength='320')
        self.label11.grid(column='1', padx='8', row='11', sticky='w')
        
        self.label12 = ttk.Label(self.window)
        self.label12.configure(background='#1e1e1e', font='{Arial} 12 {bold}', foreground='#c8c8c8', text='Find output')
        self.label12.grid(column='1', pady='8', row='14', sticky='w')
        
        self.label13 = ttk.Label(self.window)
        self.label13.configure(anchor='w', background='#1e1e1e', font='systemfixed', foreground='#c8c8c8')
        self.label13.configure(justify='left', text=' ' , wraplength='320')
        self.label13.grid(column='1', padx='8', row='15', sticky='w')
        
        self.output_lookup = (self.label11, self.label10, self.label9, self.label8, self.label7, self.label6, self.label5, self.label4, self.label3, self.label2, self.label1)
        self.button_lookup = (self.checkbutton1, self.checkbutton2, self.checkbutton3, self.checkbutton4, self.checkbutton5, self.checkbutton6, self.checkbutton7, self.checkbutton8, self.checkbutton9, self.checkbutton10)
        self.vars_lookup = (self.training,self.shop,self.buff,self.prestige,self.rush,self.event,self.dungeon,self.fairy,self.monster,self.consolidate,self.backgroundbuff)
        
        # etc
        self.window.configure(background='#1e1e1e', height='480', padx='32', pady='32')
        self.window.configure(width='640')
        self.window.geometry('640x480')
        self.window.iconphoto(True, tk.PhotoImage(file='icon.png'))
        self.window.maxsize(640, 480)
        self.window.minsize(640, 480)
        self.window.resizable(False, False)
        self.window.title('Tailed Bot')

    
    def run(self):
        self.window.mainloop()
        
    def switch_boxes(self, new_state1, new_state2, new_bool):
        for i in self.button_lookup:
            i.configure(state=new_state1)
        self.checkbutton11.configure(state=new_state2)
        for i in self.vars_lookup:
            i.set(new_bool)
        self.backgroundbuff.set(operator.not_(new_bool))
         
    
    def set_title(self):
        self.title = self.entry.get()
        self.entry.configure(state='disabled')
         

    def switch_mode(self):
        if self.mode.get() is True:
            self.mode.set(False)
            self.switch_boxes('disabled', 'normal', False)
        elif self.mode.get() is False:
            self.mode.set(True)
            self.switch_boxes('normal', 'disabled', True)
         
    
    def update_output(self):
        for i in range(len(self.console)):
            self.output_lookup[i].configure(text=str(self.console[i]))
    
    def print_line(self, var):
        self.console.insert(0, var)
        self.console = self.console[:-1]
        self.update_output()
        
    def print_finder(self, var):
        self.label13.configure(text=str(var))
    
    def print_matching(self):
        pass

