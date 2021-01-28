from tkinter import Toplevel, Label

class create_tooltip(object):
    def __init__(self, widget, text = 'widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Button-3>", self.enter)
        self.widget.bind("<ButtonRelease-3>", self.close)
    def enter(self, event = None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("all")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 50
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text = self.text, justify = 'left',
                            background = 'yellow', relief = 'solid', borderwidth = 1,
                            font = ("Courier", "20"))
        label.grid(ipadx = 1)
    def close(self, event = None):
        if self.tw:
            self.tw.destroy()