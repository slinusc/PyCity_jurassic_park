import tkinter as tk


class StatusBar(tk.Frame):
    def __init__(self, master, fg, bg):
        tk.Frame.__init__(self, master, background=bg)
        self.label = tk.Label(self, text='mouse hover over cells for cell info',
                              fg=fg, bg=bg)
        self.label.pack(side=tk.LEFT)
        self.pack(side=tk.BOTTOM, fill=tk.X)
        
    def set(self, text):
        self.label.config(text=text)
 
    def clear(self):
        self.label.config(text="")

if __name__ == '__main__':

 
    class Window:   
        def __init__(self, master):
            self.frame = tk.Frame(master)
            b1 = tk.Button(self.frame, text="Button 1", command=self.handleButtonOne)
            b1.pack(padx=30, pady=20)
             
            b2 = tk.Button(self.frame, text="Button 2", command=self.handleButtonTwo)
            b2.pack(padx=30, pady=20)
     
            self.status = StatusBar(self.frame, 'red', 'yellow' )
            self.frame.pack(expand=True, fill=tk.BOTH)
     
        def handleButtonOne(self):
            self.status.set("Button 1 was clicked")
     
        def handleButtonTwo(self):
            self.status.set("Button 2 was clicked")
     
    root = tk.Tk()
    window = Window(root)
    root.mainloop()