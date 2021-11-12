import tkinter as tk

Gravity = 5
Obstruction = 0.9
Elasticity = 2/3

class Object(tk.Tk):
    def __init__(self, image, applyGravity=True, groundBounce=True):
        self.applyGravity = applyGravity
        self.groundBounce = groundBounce
        
        self.window = tk.Tk()
        self.Xspeed, self.Yspeed = 0, 0
        self.x, self.y = None, None
        self.canMove = True
        self.moveFrame = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        self.tataCharacter = tk.PhotoImage(file="images\\"+image,format="png")
        self.size = self.tataCharacter.width(), self.tataCharacter.height()
        self.windowsize = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        
        # self.window.title(image.replace(".png", ""))

        self.window.config(highlightbackground="green")
        self.label = tk.Label(self.window,bd=0,bg="green",cursor="hand2")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-transparentcolor","green")
        self.label.configure(image=self.tataCharacter)
        self.label.pack()
        self.window.wm_attributes("-topmost", 1)
        self.window.geometry("{0}x{1}+{2}+0".format(str(self.size[0]), str(self.size[1]), int((self.windowsize[0]-self.size[0])/2)))
        
        self.window.bind("<ButtonPress-1>", self.Mouse_Startmove)
        self.window.bind("<ButtonRelease-1>", self.Mouse_Stopmove)
        self.window.bind("<B1-Motion>", self.Mouse_moving)

    def Mouse_Startmove(self, event):
        self.x = event.x
        self.y = event.y
        self.Xspeed, self.Yspeed = 0, 0
        self.canMove = False

    def Mouse_Stopmove(self, event):
        self.x = None
        self.y = None
        self.canMove = True

    def Mouse_moving(self, event):
        if not self.canMove:
            self.moveFrame.pop(0)
            self.moveFrame.append([event.x - self.x, event.y - self.y])
            x = self.window.winfo_x() + self.moveFrame[7][0]
            y = self.window.winfo_y() + self.moveFrame[7][1]
            if x < 0:
                x = 0
            elif x > self.windowsize[0] - self.size[0]:
                x = self.windowsize[0] - self.size[0]
            if y < 0:
                y = 0
            elif y > self.windowsize[1] - self.size[1]:
                y = self.windowsize[1] - self.size[1]
            self.window.geometry(f"+{x}+{y}")
    
    def Falling(self):
        if self.window.winfo_y() < self.windowsize[1] - self.size[1] and self.applyGravity:
            if self.Yspeed > 0:
                self.Yspeed -= 1
            self.Yspeed += Gravity
    
    def processMove(self):
        if self.canMove:
            self.Falling()
            for each in self.moveFrame:
                self.Xspeed += each[0]
                self.Yspeed += each[1]
            self.moveFrame = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        moveX, moveY = self.Xspeed, self.Yspeed
        x, y = self.window.winfo_x() + moveX, self.window.winfo_y() + moveY
        if x < 0:
            x = 0
            self.Xspeed = -self.Xspeed * Elasticity
            self.Yspeed *= Obstruction
        elif x > self.windowsize[0] - self.size[0]:
            x = self.windowsize[0] - self.size[0]
            self.Xspeed = -self.Xspeed * Elasticity
            self.Yspeed *= Obstruction
        if y < 0:
            y = 0
            self.Yspeed = -self.Yspeed * Elasticity
            self.Xspeed *= Obstruction
        elif y > self.windowsize[1] - self.size[1]:
            if self.groundBounce and abs(self.Yspeed) > Gravity and not (int(self.Yspeed) > (Gravity -1) and int(self.Yspeed) <= (Gravity)*2):
                self.Yspeed = -self.Yspeed * Elasticity
            else:
                self.Yspeed = 0
            y = self.windowsize[1] - self.size[1]
            self.Xspeed *= Obstruction
        self.Xspeed = self.Xspeed * Obstruction
        self.Yspeed = self.Yspeed * Obstruction
        if self.Xspeed < 0 and self.Xspeed > -0.5:
            self.Xspeed = 0
        if self.Yspeed < 0 and self.Yspeed > -0.5:
            self.Yspeed = 0
        x, y = int(x), int(y)
        self.window.geometry(f"+{x}+{y}")
        self.window.after(40,self.processMove)
        


if __name__ == "__main__": # 1280, 720  1215, 620
    Tata = Object("tata.png", True, True)
    Tata.window.after(33,Tata.processMove)
    Tata.window.mainloop()
    input("")
