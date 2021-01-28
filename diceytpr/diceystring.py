from tkinter import Tk, font,  Canvas,  BooleanVar,  CENTER
from random import randrange

words = ["omg tis here string.", 
        "tis string looks longer, nay?", 
        "tis be short!", 
        "be like medium or so, ya?"]
wav = [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
tsu = [-5, -5, -5, -5, -5, 5, 5, 5, 5, 5]
wid = 1200

class dicey_string(object):
    def __init__(self, c, txt, x, y, fnt):
        self.c = c
        self.x = x
        self.y = y
        self.txt = txt
        self.list = []
        self.fnt = fnt
        self.change_length()
        self.load_letters()
        self.a_in_progress = False
        self.c_in_progress = False

    class letters(object):
        def __init__(self, c, x, y, txt, fnt):
            self.c = c
            self.fnt = fnt
            self.letter = c.create_text(x, y, text = txt, justify = CENTER, font = fnt, anchor = "w")
            self.def_x = 0
            self.def_y = y
        def reset_letter(self):
            self.c.itemconfigure(self.letter, text = " ")
        def load_letter(self, txt):
            self.c.itemconfigure(self.letter, text = txt)
        def set_def_coords(self,  x, y, i, txt):
            self.def_x = x - self.fnt.measure(txt) // 2 + self.fnt.measure(txt[:i])
            self.def_y = y
            self.c.coords(self.letter, self.def_x, self.def_y)
        def remove_letter(self):
            self.c.delete(self.letter)

    def clear_letters(self):
        for i in range(len(self.list)):
            self.list[i].reset_letter()
    def spacify(self):
        mx = len(self.list) - len(self.txt)
        space1 = " " * (mx - mx // 2)
        space2 = " " * (mx // 2)
        self.txt = space1 + self.txt + space2
    def change_length(self):
        diff = len(self.txt) - len(self.list)
        if diff > 0:
            for i in range(diff):
                self.list.append(self.letters(self.c, self.x, self.y, " ", self.fnt))
        elif diff < 0:
            self.spacify()
    def load_letter(self, i, txt):
        self.list[i].load_letter(txt)
        self.list[i].set_def_coords(self.x, self.y, i, self.txt)
    def load_letters(self):
        for i in range(len(self.txt)):
            self.load_letter(i, self.txt[i])
    def change_string(self, event, txt):
        self.txt = txt
        self.change_length()
        self.clear_letters()
        self.load_letters()
    def a_rst(self):
        self.a_in_progress = False
    def c_rst(self):
        self.c_in_progress = False
    def a_tw(self, event, delay, txt):
        if not self.a_in_progress and not self.c_in_progress:
            self.a_in_progress = True
            l = len(txt) + 1
            self.c.after(l * delay, self.a_rst)
            for i in range(l):
                self.c.after(i * delay, lambda i=i: self.change_string(None, txt[:i]))
    def a_wave(self, event, delay, count, wav, foam, txt):
        if not self.a_in_progress and not self.c_in_progress:
            self.a_in_progress = True
            self.txt = txt
            self.change_length()
            l = len(self.txt)
            lw = len(wav)
            self.c.after(count * delay * lw + l * 25, self.a_rst)
            for i in range(l):
                f = 0
                self.c.after(delay + i * 25, lambda i=i: self.load_letter(i, foam))
                self.c.after(delay * lw + i * 25, lambda i=i: self.load_letter(i, self.txt[i]))
                for z in range(count * lw):
                    move_letter = lambda i=i, f=f: self.c.move(self.list[i].letter, 0, wav[f] * 10)
                    self.c.after(i * 25 + delay * z, move_letter)
                    f += 1
                    if f == lw:
                        f = 0
    def c_glow(self, event, delay, count, typ):
        if not self.c_in_progress:
            self.c_in_progress = True
            l = len(self.txt)
            hold = ((l * delay + 510 // 2) * typ + (510 * delay // 20) * (1 - typ))
            c3 = "00"
            self.c.after(count * hold * 2, self.c_rst)
            def update_color(c1, c2, c3, i):
                self.c.itemconfigure(self.list[i].letter, fill = "#" + c1 + c2 + c3)
            def color_loops(z):
                for i in range(l):
                    c1 = '{:02x}'.format(255 - abs(z - 255))
                    c2 = '{:02x}'.format(abs(z // 2))
                    self.c.after((i * delay + z // 2) * typ + (z * delay // 20) * (1 - typ), lambda c1=c1,c2=c2,c3=c3,i=i: update_color(c3, c1, c2, i))
                for i in range(l):
                    c1 = '{:02x}'.format(255 - abs(z - 255))
                    c2 = '{:02x}'.format(abs((z // 2) - 255))
                    self.c.after((i * delay + z // 2 + hold // 4) * typ + (z * delay // 20 + hold) * (1 - typ), lambda c1=c1,c2=c2,c3=c3,i=i: update_color(c1, c3, c2, i))
            for f in range(count):
                for z in range(10, 510, 20):
                    self.c.after((hold + hold * (1 - typ)) * f, lambda z=z: color_loops(z))
    def c_fade(self, event, delay, count):
        if not self.c_in_progress:
            self.c_in_progress = True
            l = len(self.txt)
            hold = (l * delay // 4 + 476)
            self.c.after(count * hold * 2, self.c_rst)
            def update_color(c1, i):
                self.c.itemconfigure(self.list[i].letter, fill = "#" + c1 + c1 + c1)
            def color_loops(z):
                for i in range(l):
                    c1 = '{:02x}'.format(z)
                    self.c.after((i * delay // 4 + z), lambda c1=c1,i=i: update_color(c1, i))
                for i in range(l):
                    c1 = '{:02x}'.format(abs(z - 238))
                    self.c.after((i * delay // 4 + z + hold), lambda c1=c1,i=i: update_color(c1, i))
            for f in range(count):
                for z in range(1, 238, 5):
                    self.c.after((hold * 2) * f, lambda z=z: color_loops(z))
if __name__ == "__main__":
    root = Tk()
    root.grid()
    c = Canvas(root , width = wid , height = 200)
    c.grid()
    fnt = font.Font(family="Courier", size = 50)
    in_progress = BooleanVar(False)
    wtf = dicey_string(c, words[0], wid // 2, 100, fnt)
    def two(event):
        wtf.a_wave(event, 20, 4, wav, "^", words[randrange(4)])
        wtf.c_fade(None, 20, 1)

    c.bind_all("1", lambda event: wtf.a_wave(event, 20, 4, wav, "^", words[randrange(4)]))
    c.bind_all("2", lambda event: wtf.a_wave(event, 20, 3, tsu, "~", words[randrange(4)]))
    c.bind_all("3", lambda event: wtf.a_tw(event, 50, words[randrange(4)]))
    c.bind_all("4", lambda event: wtf.change_string(event, words[randrange(4)]))
    c.bind_all("5", lambda event: wtf.c_glow(event, 50, 2, 0))
    c.bind_all("6", lambda event: wtf.c_glow(event, 50, 2, 1))
    c.bind_all("7", two)
    c.bind_all("8", lambda event: wtf.c_fade(event, 50, 1))
        
    root.mainloop()
