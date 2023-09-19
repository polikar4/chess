import turtle as t

size_square = 60

class Figure(): pass
class Drow(): pass

class Pole():
    figure: Figure = []
    drow: Drow = None

    def __init__(self, drow: Drow):

        self.drow = drow
        screen = t.Screen()
        NameGifFile = ['P','B','K','O','Q','R']
        for name in NameGifFile:
            screen.addshape(name + '.gif')
            screen.addshape(name * 2 + '.gif')

    def FigureInPosition(self, x: int, y: int) -> Figure:
        for f in self.figure:
            if(f.position_x == x and f.position_y == y):
                return f
        return None

    def NormalFigurePosition(self) -> None:
        for i in range(8):
            self.figure.append(Pawn(i+1,7,self,"p"))
            self.figure.append(Pawn(i+1,2,self,"P"))
        self.figure.append(Rook(1,1,self,"R"))
        self.figure.append(Rook(8,1,self,"R"))
        self.figure.append(Rook(1,8,self,"r"))
        self.figure.append(Rook(8,8,self,"r"))

        self.figure.append(Knight(2,1,self,"K"))
        self.figure.append(Knight(7,1,self,"K"))
        self.figure.append(Knight(2,8,self,"k"))
        self.figure.append(Knight(7,8,self,"k"))

        self.figure.append(Bishop(3,1,self,"B"))
        self.figure.append(Bishop(6,1,self,"B"))
        self.figure.append(Bishop(3,8,self,"b"))
        self.figure.append(Bishop(6,8,self,"b"))

        self.figure.append(King(5,1,self,"O"))
        self.figure.append(King(5,8,self,"o"))

        self.figure.append(Queen(4,1,self,"Q"))
        self.figure.append(Queen(4,8,self,"q"))
    
    def EatingFigure(self, x: int, y: int) -> None:
        for i in range(len(self.figure)):
            if(self.figure[i].position_x == x and self.figure[i].position_y == y):
                self.figure.pop(i)
                break
    
    def DrowPole(self) -> None:
        self.drow.DrowPole(self)

    def AttackCell(self, x: int, y: int, white: bool) -> bool:
        pass

    def СheckСheck(self, pole, white: bool) -> bool:
        king = None
        for f in pole.figure:
            if(f.name_figure == ("O" if white else "o")):
                king = f
                break

        for j in range(4): 
            for i in range(1,8):
                f = self.FigureInPosition(king.position_x + i * (j%2) * (j - 2),
                 king.position_y + i * ((j+1)%2) * (j - 1))
                if( f != None and (f.name_figure == ("Q" if not king.white else "q")
                or f.name_figure == ("R" if not king.white else "R"))):
                    return True
                if(f != None and f.white == king.white):
                    break

        for j in range(4): 
            for i in range(1,8):
                f = self.FigureInPosition(king.position_x + (i if j%2 == 0 else -i),
                 king.position_y + (i if j > 1 else -i))
                if( f != None and f.name_figure == ("B" if not king.white else "b")):
                    return True
                if(f != None and f.white == king.white):
                    break
        


        return False


class Figure():
    position_x:int  = 0
    position_y:int = 0
    name_figure:str = 'P'
    active:bool = False
    white:bool = True
    startposition:bool = True
    pole:Pole

    def __init__(self,x: int, y: int, pole: Pole, name = 'P'):
        self.pole = pole
        self.position_x = x
        self.position_y = y
        self.name_figure = name
        self.white = (True if ord(name) < 90 else False)

    def MoveToPosition(self, x: int, y: int) -> bool:
        pass


class Knight(Figure):
    def MoveToPosition(self, x: int, y: int) -> bool:
        if(min(abs(x - self.position_x), abs(y - self.position_y)) != 1 or
            max(abs(x - self.position_x), abs(y - self.position_y)) != 2):
            return False
        self.pole.EatingFigure(x,y)
        self.position_x = x
        self.position_y = y
        return True


class Rook(Figure):
    def MoveToPosition(self, x: int, y: int) -> bool:
        if not (x == self.position_x or y == self.position_y):
            return False
        
        if(x == self.position_x):
            y_min = min(y, self.position_y) + 1
            y_max = max(y, self.position_y) - 1
            for i in range(y_min,y_max):
                if(self.pole.FigureInPosition(x,i) != None):
                    return False
        else:
            x_min = min(x, self.position_x) + 1
            x_max = max(x, self.position_x) - 1
            for i in range(x_min,x_max):
                if(self.pole.FigureInPosition(y,i) != None):
                    return False

        self.pole.EatingFigure(x,y)
        self.position_x = x
        self.position_y = y
        self.startposition = False  
        return True


class Bishop(Figure):
    def MoveToPosition(self, x: int, y: int) -> bool:
        if (abs(x - self.position_x) != abs(y - self.position_y)):
            return False
        
        for i in range(min(x,self.position_x) + 1, max(x,self.position_x) - 1):
            if(self.pole.FigureInPosition(i, 
            min(y, self.position_y) + (i if self.position_y > y else -i)) 
            != None):
                return False

        self.pole.EatingFigure(x,y)
        self.position_x = x
        self.position_y = y
        return True


class Queen(Figure):
    def MoveToPosition(self, x: int, y: int) -> bool:
        if ((not (x == self.position_x or y == self.position_y))
            and (abs(x - self.position_x) != abs(y - self.position_y))):
            return False
        
        if(abs(x - self.position_x) != abs(y - self.position_y)): #rook move
            if(x == self.position_x):
                y_min = min(y, self.position_y) + 1
                y_max = max(y, self.position_y) - 1
                for i in range(y_min,y_max):
                    if(self.pole.FigureInPosition(x,i) != None):
                        return False
            else:
                x_min = min(x, self.position_x) + 1
                x_max = max(x, self.position_x) - 1
                for i in range(x_min,x_max):
                    if(self.pole.FigureInPosition(y,i) != None):
                        return False
        else:                                                    #Bishop move
            for i in range(min(x,self.position_x) + 1, max(x,self.position_x) - 1):
                if(self.pole.FigureInPosition(i,
                min(y, self.position_y) + (i if self.position_y > y else -i)) 
                    != None):
                    return False

        self.pole.EatingFigure(x,y)
        self.position_x = x
        self.position_y = y
        return True


class King(Figure):
    def MoveToPosition(self, x: int, y: int) -> bool:
        if(max(abs(x - self.position_x), abs(y - self.position_y)) > 1):
            return False

        self.pole.EatingFigure(x,y)
        self.position_x = x
        self.position_y = y
        self.startposition = False
        return True


class Pawn(Figure):
    def MoveToPosition(self, x: int, y: int) -> bool:
        figure = self.pole.FigureInPosition(x, y)
        if(figure == None):
            if(self.position_x == x and self.position_y + (1 if self.white else -1) == y):
                self.position_y = y
                self.startposition = False
                return True
            
            if(self.position_x == x and self.position_y + (2 if self.white else -2) == y and self.startposition):
                self.position_y = y
                self.startposition = False
                return True
        elif(figure.white != self.white):
            if((self.position_x + 1 == x or self.position_x - 1 == x) 
                    and self.position_y + (1 if self.white else -1) == y):
                self.pole.EatingFigure(x,y)
                self.position_y = y
                self.position_x = x
                self.startposition = False
                return True

        return False
                

class Drow():
    old_figure: Figure = []

    def __init__(self):
        t.hideturtle()
        t.tracer(0)                       #mega speed drow
        t.setup(size_square*10,size_square*10)                  #size window
        t.bgcolor("#707070")              #color background
        t.penup()
            
    def DrowPole(self, pole: Pole) -> None:
        self.DrowTable()    
        self.DrowFigures(pole)
        self.UpdateOldFigure(pole.figure, pole)

    def UpdateOldFigure(self, figures, pole: Pole) -> None:
        self.old_figure = []
        for f in figures:
            self.old_figure.append(Figure(f.position_x, f.position_y, pole, f.name_figure))

    def ActiveFigure(self, f_active: Figure, f_inactive: Figure = None) -> None:
        if(f_active != None):
            self.DrowSquare((f_active.position_x - 1) * size_square,
            (f_active.position_y - 1) * size_square, size_square, "#007000")
            self.DrowFigure(f_active.position_x,f_active.position_y,f_active.name_figure)

        if(f_inactive != None):
            self.DrowSquare((f_inactive.position_x - 1) * size_square, (f_inactive.position_y - 1) * size_square,
                            size_square, 
                            "#505050" if (f_inactive.position_x + f_inactive.position_y)% 2 == 0 else "#808080" )
            self.DrowFigure(f_inactive.position_x,f_inactive.position_y,f_inactive.name_figure)        

    def DrowCheck(self, pole: Pole, white: bool) -> None:
        king = None
        for f in pole.figure:
            if(f.name_figure == ("O" if white else "o")):
                king = f
        
        self.DrowSquare((king.position_x - 1) * size_square, 
                        (king.position_y - 1) * size_square,
                         size_square,
                         "#700000")
        
        self.DrowFigure(king.position_x, king.position_y, king.name_figure)

    def UpdatePole(self, pole: Pole) -> None:
        if(len(self.old_figure) == len(pole.figure)):
            for i in range(len(pole.figure)):
                f1 = self.old_figure[i]
                f2 = pole.figure[i]
                if(f1.position_x != f2.position_x or f1.position_y != f2.position_y):
                    self.DrowSquare((f1.position_x - 1) * size_square, (f1.position_y - 1) * size_square,
                        size_square, "#505050" if (f1.position_x + f1.position_y)% 2 == 0 else "#808080" )
                    string = ""
                    if ord(f2.name_figure) > 90:
                        string = chr(ord(f2.name_figure) - 32)
                        string += string
                    else:
                        string = f2.name_figure
                    self.DrowFigure(f2.position_x,f2.position_y,string)
        else:
            f1 = None
            f2 = None 
            for f_old in self.old_figure:
                for f_act in pole.figure:
                    if(f_old.position_x == f_act.position_x and 
                    f_old.position_y == f_act.position_y and
                    f_old.white != f_act.white):
                        f1 = f_old
                        f2 = f_act
            
            for i in range(len(self.old_figure)):
                if(f1.position_x == self.old_figure[i].position_x 
                and f1.position_y == self.old_figure[i].position_y):
                    self.old_figure.pop(i)
                    break

            for i in range(len(self.old_figure)):
                if(pole.figure[i].position_x != self.old_figure[i].position_x 
                or pole.figure[i].position_y != self.old_figure[i].position_y):
                    self.DrowSquare((self.old_figure[i].position_x - 1) * size_square, 
                                    (self.old_figure[i].position_y - 1) * size_square,
                                    size_square,
                                    "#505050" if (self.old_figure[i].position_x + self.old_figure[i].position_y)% 2 == 0 else "#808080" )

            self.DrowSquare((f1.position_x - 1) * size_square, (f1.position_y - 1) * size_square,
                        size_square, "#505050" if (f1.position_x + f1.position_y)% 2 == 0 else "#808080" )
            self.DrowSquare((f2.position_x - 1) * size_square, (f2.position_y - 1) * size_square,
                        size_square, "#505050" if (f2.position_x + f2.position_y)% 2 == 0 else "#808080" )
            
            string = ""
            if ord(f2.name_figure) > 90:
                string = chr(ord(f2.name_figure) - 32)
                string += string
            else:
                string = f2.name_figure
            self.DrowFigure(f2.position_x,f2.position_y,string)

        


        self.UpdateOldFigure(pole.figure, pole)
        for f in pole.figure:
            f.active = False     

    def DrowFigures(self, pole: Pole) -> None:
        for f in pole.figure:
            if(f.active):
                self.DrowSquare((f.position_x - 1) * size_square, (f.position_y - 1) 
                * size_square,size_square, "#007000")

            self.DrowFigure(f.position_x, f.position_y, f.name_figure)
        
    def DrowFigure(self, x: int, y: int, name: str) -> None:
        t.tracer(1)       # stop mega speed

        string = ""
        if ord(name) > 90:
            string = chr(ord(name) - 32)
            string += string
        else:
            string = name

        player = t.Turtle()
        player.penup()
        player.speed(0)
        player.goto((x-1)*size_square+size_square/2-size_square*4,(y-1)*size_square+size_square/2-size_square*4)
        player.shape(string + '.gif')

        t.tracer(0) #mega speed drow

    def DrowTable(self) -> None:
        for i in range(8): # 
            for j in range(8):
                self.DrowSquare(size_square * i, size_square* j, size_square,
                "#505050" if (i + j)%2 == 0 else "#808080")

    def GoTo(self,x,y) -> None:
        t.goto(x - size_square*4,y - size_square*4)
    
    def DrowSquare(self,x,y,size, color = "#505050") -> None:
        t.color(color,color) 
        self.GoTo(x,y)
        t.pendown()
        t.begin_fill()
        self.GoTo(x,y+size)
        self.GoTo(x+size,y+size)        
        self.GoTo(x+size,y)
        t.end_fill()
        t.penup()

    def DrowСircle(self,x,y,radius = size_square * 0.15, color = "#101010") -> None:
        t.color(color,color) 
        self.GoTo(x + size_square/2,y + (size_square - radius*2) / 2)
        t.pendown()
        t.begin_fill()
        t.circle(radius)
        t.end_fill()
        t.penup()


class Gamer():
    white:bool = False
    people:bool = True
    active:bool = False
    move:bool = False
    pole:Pole = None

    def __init__(self, White: bool, People: bool, pole: Pole):
        self.people = People
        self.white = White
        self.active = self.white
        self.pole = pole
    
    def TapInHisFigure(self,x,y) -> bool:
        for f in self.pole.figure:
            if(f.position_x == x and f.position_y == y and f.white == self.white):
                return True
        return False

    def TapToScreen(self,x,y) -> bool:
        if(self.pole.СheckСheck(self.pole, self.white)):
            self.pole.drow.DrowCheck(self.pole, self.white)
        # Get Info
        pos_x = (int)((x + size_square*4) / size_square + 1)
        pos_y = (int)((y + size_square*4) / size_square + 1)
        if(pos_x < 1 or pos_x > 8 or pos_y < 0 or pos_y > 8):
            return True

        not_figure_active_two = True
        have_active_figure = False
        active_figure: Figure
        for f in self.pole.figure:
            if(f.white == self.white and f.active):
                have_active_figure = True
                active_figure = f


        # If in his figure
        if(self.TapInHisFigure(pos_x,pos_y)):
            # if have active figure 
            if(have_active_figure):
                f_act = None
                f_pass = None

                for f in self.pole.figure:
                    if(f.active ):
                        f.active = False
                        f_pass = f
                        if(f.position_x == pos_x and f.position_y == pos_y):
                            not_figure_active_two = False
                            

                for f in self.pole.figure:
                    if(f.position_x == pos_x and f.position_y == pos_y and not_figure_active_two):
                        f.active = True
                        f_act = f

                self.pole.drow.ActiveFigure(f_act, f_pass)
            # if not have active figure
            else: 
                for f in self.pole.figure:
                    if(f.position_x == pos_x and f.position_y == pos_y):
                        f.active = True
                        self.pole.drow.ActiveFigure(f)
                        
        else:
            if(have_active_figure and active_figure.MoveToPosition(pos_x, pos_y)):
                self.pole.drow.UpdatePole(self.pole)

                if(self.pole.СheckСheck(self.pole, not self.white)):
                    self.pole.drow.DrowCheck(self.pole, not self.white)
                return False

        if(not have_active_figure):
            return True

        
        
        return True


def TapToScreen(x,y) -> bool:
    if(gamer1.active):
        gamer1.active = gamer1.TapToScreen(x,y)
        gamer2.active = not gamer1.active
    else:
        gamer2.active = gamer2.TapToScreen(x,y)
        gamer1.active = not gamer2.active


if "__main__" == __name__:
    pole = Pole(Drow())
    pole.NormalFigurePosition()
    pole.DrowPole()

    gamer1 = Gamer(True, True, pole)
    gamer2 = Gamer(False,True, pole)

    t.onscreenclick(TapToScreen) #function tap to deck

    t.mainloop()
