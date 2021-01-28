#v.0.8
#from tkinter import *
from tkinter import Tk, messagebox, font, ttk, StringVar, IntVar, Canvas, Toplevel, HORIZONTAL, GROOVE
from random import randrange
from json import dump, load
from diceystring import dicey_string
from tooltip import create_tooltip

#window
root = Tk()
root.title("Dicey")
root.resizable(width = False, height = False)

#defaults
n1 = "Igor"
n2 = "Thijs"
fnt50 = font.Font(family = "Courier", size = 50)
fnt18 = font.Font(family = "Courier", size = 18)
ttk.Style().configure("TCheckbutton", font = "Courier 25", relief = GROOVE, indicatordiameter = 20)
ttk.Style().configure("TRadiobutton", font = "Courier 20", relief = GROOVE, indicatordiameter = 20)
ttk.Style().configure("TLabel", font = "Courier 20")
ttk.Style().configure("TButton", font = "Arial 16")
ttk.Style().configure("TNotebook.Tab", font = "Courier 20 bold")
wav = [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
tsu = [-5, -5, -5, -5, -5, 5, 5, 5, 5, 5]
#globals
e_n1 = StringVar(value = n1)
e_n2 = StringVar(value = n2)
cheat_mod = IntVar(value = 1)
anims = IntVar(value = 0)
c_anims = IntVar(value = 0)
anims_mod = IntVar(value = 50)
lang = IntVar(value = 0)

#Save on exit
def save_on_exit():
    try:
        data = {"names": {"n1": e_n1.get(), "n2": e_n2.get()}, 
                "cheat": cheat_mod.get(), 
                "anims": {"anims": anims.get(), "c_anims": c_anims.get(), "anims_mod": anims_mod.get()}, 
                "lang": lang.get()}
        with open("dicey.json",  "w") as save_file:
            dump(data, save_file)
    except:
        with open("dicey.json",  "w") as save_file:
            dump(d_ui["err"], save_file)
    root.destroy()
    
#Load on start
def load_on_start():
    try:
        with open("dicey.json",  "r") as save_file:
            data = load(save_file)
        e_n1.set(data["names"]["n1"])
        e_n2.set(data["names"]["n2"])
        cheat_mod.set(data["cheat"])
        anims.set(data["anims"]["anims"])
        c_anims.set(data["anims"]["c_anims"])
        anims_mod.set(data["anims"]["anims_mod"])
        lang.set(data["lang"])
    except:
        pass
    
load_on_start()

#canvas width
def get_canvas_width():
    l = len(max(d_list, key = len))
    f = fnt50.measure("0")
    width = (l + max(len(e_n1.get()), len(e_n2.get())) - 2) * f
    return width

#Load translation
def load_translation():
    def_list = ["There is no God.",
                "{} is really right!",
                "{} is a little bit right...",
                "No one is right.",
                "{} is a little bit right...",
                "{} is really right!"]
    def_ui = {"err": "Error occured, restart the app.", 
              "b1": "Hold RMB for help.",
              "set_w": "Settings",
 
              "tab1": "Options",
              "tab1_l1": "Renaming",
              "tab1_l2": "First",
              "tab1_l3": "Second",
              "tab1_l4": "Cheats",
              "tab1_r1": "None",
              "tab1_r2": "Double the chances",
              "tab1_r3": "Triple the chances",
              
              "tab2": "Animations",
              "tab2_l1": "Text",
              "tab2_r1": "None",
              "tab2_r2": "Tw",
              "tab2_r3": "Wave",
              "tab2_r4": "Tsunami",
              "tab2_l2": "Color",
              "tab2_r11": "None",
              "tab2_r12": "Glow",
              "tab2_r13": "Scan",
              "tab2_r14": "Fade",
              "tab2_l3": "Speed:{:3}   ",
              
              "tab3": "Lang",
              "tab3_r1": "English",
              "tab3_r2": "Dutch",
              "tab3_r3": "Russian",
              "tab3_l": "* Restart is required!"}
    def_popup = {"b1": "Press space / click with LMB \nor press ESC for options menu!",  
                "dlc5_err_nl": "File Dicey_nl.json was not found.", 
                "dlc5_err_ru": "File Dicey_ru.json was not found."}
    d_list = def_list
    d_ui = def_ui
    d_popup = def_popup
    def nl_or_ru(loc):
        try:
            with open("dicey_" + loc + ".json",  "r") as lang_file:
                data = load(lang_file)
                for i in range(6):
                    d_list[i] = data["d_list"][i]
                d_ui.update(data["d_ui"])
                d_popup.update(data["d_popup"])
        except FileNotFoundError:
            messagebox.showerror(title = "File error", message = d_popup["dlc5_err_" + loc])
            lang.set(0)
    if lang.get() == 1:
        nl_or_ru("nl")
    elif lang.get() == 2:
        nl_or_ru("ru")
    return d_list, d_ui, d_popup
    
d_list,  d_ui, d_popup = load_translation()

#canvas    
c = Canvas(root, width = get_canvas_width(),
            height = 200, bg = "gray92", confine = True)
ct = dicey_string(c, d_ui["b1"], get_canvas_width() // 2, 100, fnt50)
c.grid()
c_tt = create_tooltip(c,  d_popup["b1"])

#DO THE THING
def do_the_thing(event):
    var = randrange(6) + randrange(cheat_mod.get())
    if var > 5:
        var = 5
    delay = (40 + abs(100 - anims_mod.get())) // 2
    if var == 0 or var == 3:
        tmp = d_list[var]
    elif var == 1 or var == 2:
        tmp = d_list[var].format(e_n1.get())
    elif var == 4 or var == 5:
        tmp = d_list[var].format(e_n2.get())
    if anims.get() == 0:
        count = 1
        ct.change_string(None, tmp)
    elif anims.get() == 1:
        count = 1
        ct.a_tw(None, delay, tmp)
    elif anims.get() == 2:
        count = 2
        ct.a_wave(None, delay, 3, wav, "^", tmp)
    elif anims.get() == 3:
        count = 1
        ct.a_wave(None, delay, 2, tsu, "~", tmp)
    if c_anims.get() == 1:
        ct.c_glow(None, delay, count, 0)
    elif c_anims.get() == 2:
        ct.c_glow(None, delay, count, 1)
    elif c_anims.get() == 3:
        ct.c_fade(None, delay, count)

#settings window    
class settings_window(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.draw_widgets()
    def change_state(self, *widgets, b):
        s = "!" * b
        for widget in widgets:
            widget.state([s + "disabled"])
    def close(self):
        c.configure(width = get_canvas_width())
        ct.x = get_canvas_width() // 2
        self.withdraw()
        self.grab_release()
    def reopen(self):
        self.deiconify()
        self.grab_set()
    def draw_widgets(self):
        self.resizable(width = False, height = False)
        self.transient(root)
        self.grab_set()
        self.title(d_ui["set_w"])
        tv = ttk.Notebook(self)
        tv.grid()
        #tab1 names
        tab1 = ttk.Frame(tv)
        tv.add(tab1, text = d_ui["tab1"])
        tab1_l1 = ttk.Label(tab1, text = d_ui["tab1_l1"])
        tab1_l1.grid(row = 0,  column = 0, sticky = "w")
        tab1_l2 = ttk.Label(tab1, text = d_ui["tab1_l2"])
        tab1_l2.grid(row = 1,  column = 0)
        tab1_l3 = ttk.Label(tab1, text = d_ui["tab1_l3"])
        tab1_l3.grid(row = 2,  column = 0)
        tab1_b1 = ttk.Button(tab1, text = u"\u21BB", width = 0, command = lambda: e_n1.set(n1))
        tab1_b1.grid(row = 1, column = 2, sticky = "w")
        tab1_b2 = ttk.Button(tab1, text = u"\u21BB", width = 0, command = lambda: e_n2.set(n2))
        tab1_b2.grid(row = 2, column = 2, sticky = "w")
        tab1_e1 = ttk.Entry(tab1, font = fnt18, textvariable = e_n1, width = 12)
        tab1_e1.grid(row = 1, column = 1)
        tab1_e2 = ttk.Entry(tab1, font = fnt18, textvariable = e_n2, width = 12)
        tab1_e2.grid(row = 2, column = 1)
        e_n1.trace('w', lambda *args: e_n1.set(e_n1.get()[:12]))
        e_n2.trace('w', lambda *args: e_n2.set(e_n2.get()[:12]))
        #separator
        ttk.Separator(tab1).grid(row = 3, sticky = "ew", columnspan = 5)
        #tab1 cheats
        tab1_l4 = ttk.Label(tab1, text = d_ui["tab1_l4"])
        tab1_l4.grid(row = 5, column = 0, sticky = "w")
        tab1_r1 = ttk.Radiobutton(tab1, text = d_ui["tab1_r1"], cursor = "hand1",
                                  variable = cheat_mod, value = 1)
        tab1_r1.grid(row = 6, column = 0, sticky = "w", columnspan = 2)
        tab1_r2 = ttk.Radiobutton(tab1, text = d_ui["tab1_r2"], cursor = "hand1",
                                  variable = cheat_mod, value = 3)
        tab1_r2.grid(row = 7, column = 0, sticky = "w", columnspan = 2)
        tab1_r3 = ttk.Radiobutton(tab1, text = d_ui["tab1_r3"], cursor = "hand1",
                                  variable = cheat_mod, value = 4)
        tab1_r3.grid(row = 8, column = 0, sticky = "w", columnspan = 2)
        #tab2 anims
        tab2 = ttk.Frame(tv) 
        tv.add(tab2, text = d_ui["tab2"])
        tab2_l1 = ttk.Label(tab2, text = d_ui["tab2_l1"])
        tab2_l1.grid(row = 0,  column = 0, sticky = "w")
        tab2_r1 = ttk.Radiobutton(tab2, text = d_ui["tab2_r1"], variable = anims, 
                                  value = 0, cursor = "hand1")
        tab2_r1.grid(row = 1, column = 0, sticky = "w")
        tab2_r2 = ttk.Radiobutton(tab2, text = d_ui["tab2_r2"], variable = anims, 
                                  value = 1, cursor = "hand1")
        tab2_r2.grid(row = 2, column = 0, sticky = "w")
        tab2_r3 = ttk.Radiobutton(tab2, text = d_ui["tab2_r3"], variable = anims, 
                                  value = 2, cursor = "hand1")
        tab2_r3.grid(row = 3, column = 0, sticky = "w")
        tab2_r4 = ttk.Radiobutton(tab2, text = d_ui["tab2_r4"], variable = anims, 
                                  value = 3, cursor = "hand1")
        tab2_r4.grid(row = 4, column = 0, sticky = "w")
        #tab2 color
        tab2_l2 = ttk.Label(tab2, text = d_ui["tab2_l2"])
        tab2_l2.grid(row = 0,  column = 1, sticky = "w")
        tab2_r11 = ttk.Radiobutton(tab2, text = d_ui["tab2_r11"], variable = c_anims, 
                                  value = 0, cursor = "hand1") 
        tab2_r11.grid(row = 1, column = 1, sticky = "w")
        tab2_r12 = ttk.Radiobutton(tab2, text = d_ui["tab2_r12"], variable = c_anims, 
                                  value = 1, cursor = "hand1")
        tab2_r12.grid(row = 2, column = 1, sticky = "w")
        tab2_r13 = ttk.Radiobutton(tab2, text = d_ui["tab2_r13"], variable = c_anims, 
                                  value = 2, cursor = "hand1")
        tab2_r13.grid(row = 3, column = 1, sticky = "w")
        tab2_r14 = ttk.Radiobutton(tab2, text = d_ui["tab2_r14"], variable = c_anims, 
                                  value = 3, cursor = "hand1")
        tab2_r14.grid(row = 4, column = 1, sticky = "w")
        #separator
        ttk.Separator(tab2).grid(row = 5, sticky = "ew", columnspan = 5)
        #tab2 speed
        tab2_l3 = ttk.Label(tab2, text = d_ui["tab2_l3"].format(anims_mod.get()))
        tab2_l3.grid(row = 6, column = 0, sticky = "w")
        tab2_s = ttk.Scale(tab2, from_ = 1, to = 100, variable = anims_mod, 
                           orient = HORIZONTAL, length = 200)
        tab2_s.grid(row = 7, column = 0, columnspan = 3, sticky = "w")
        anims_mod.trace('w', lambda *args: tab2_l3.config(text = d_ui["tab2_l3"].format(anims_mod.get())))
        #tab3 translations
        tab3 = ttk.Frame(tv)
        tv.add(tab3, text = d_ui["tab3"])
        tab3_r1 = ttk.Radiobutton(tab3, text = d_ui["tab3_r1"], variable = lang, 
                                  value = 0, cursor = "hand1")
        tab3_r1.grid(row = 1, column = 0, sticky = "w")
        tab3_r2 = ttk.Radiobutton(tab3, text = d_ui["tab3_r2"], variable = lang, 
                                  value = 1, cursor = "hand1")
        tab3_r2.grid(row = 2, column = 0, sticky = "w")
        tab3_r3 = ttk.Radiobutton(tab3, text = d_ui["tab3_r3"], variable = lang, 
                                  value = 2, cursor = "hand1")
        tab3_r3.grid(row = 3, column = 0, sticky = "w")
        tab3_l = ttk.Label(tab3, text = d_ui["tab3_l"])
        tab3_l.grid(row = 5, column = 0, sticky = "w")
        #on closing the settings window
        self.protocol("WM_DELETE_WINDOW", self.close)
        
def call_settings(event):    
    set_w.reopen()

set_w = settings_window()
root.after(10, set_w.close)

#hotkeys    
root.bind("<Escape>",  call_settings)
root.bind("<space>",  do_the_thing)
c.bind("<Button-1>",  do_the_thing)
    
#save and exit
root.protocol("WM_DELETE_WINDOW", save_on_exit)
    
root.mainloop()


