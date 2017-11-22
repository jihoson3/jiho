import game_framework
import title_state
import collision
import gameover_state
import main_state3
from pico2d import *

import main_state


lands=[]
spears=[]
doors=[]
ledders=[]
bows=[]
stones=[]
mls=[]
current_time_jones=0.0
current_time_stone=0.0
name = "MainState"
image = None
class Field:
    def __init__(self):
        self.image = load_image('back.png')
        self.field_draw_x=4400

    def draw(self):
        self.image.draw(self.field_draw_x, 300)


class Jones:
    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH=20.0
    RUN_SPEED_MPM=(RUN_SPEED_KMPH *1000.0/60.0)
    RUN_SPEED_MPS=(RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS=(RUN_SPEED_MPS *PIXEL_PER_METER)
    image = None
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, RIGHT_USE_ROPE, LEFT_USE_ROPE,UPDOWN_RUN,UPDOWN_STAND = 0, 1, 2, 3,4,5,6,7


    def __init__(self):
        self.x, self.y = 400, 400
        self.current_time_jones=0.0
        self.state = self.RIGHT_STAND
        self.jump=False
        self.frame = 0
        self.rope_time=0.0
        self.dead=False
        self.total_frames=0.0
        self.fst_y=0
        self.fst_field_x=0
        self.ondoor=False
        self.onledder=False
        if Jones.image == None:
            Jones.image=load_image("jones_.png")
    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN, self.UPDOWN_RUN, self.UPDOWN_STAND):
                self.state=self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND ,self.LEFT_STAND , self.LEFT_RUN, self.UPDOWN_RUN, self.UPDOWN_STAND):
                self.state=self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state=self.LEFT_STAND
        elif (event.type, event.key)==(SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state=self.RIGHT_STAND
        elif (event.type, event.key)==(SDL_KEYDOWN, SDLK_SPACE): #로프기능
            self.fst_y=self.y
            self.jump=True
        for ledder in ledders:
           if (event.type, event.key)==(SDL_KEYDOWN, SDLK_UP) and collision.collide(jones,ledder):
                self.state=self.UPDOWN_RUN
           if (event.type, event.key)==(SDL_KEYUP, SDLK_UP) and collision.collide(jones,ledder):
               self.state=self.UPDOWN_STAND
           if (event.type,event.key)==(SDL_KEYUP,SDLK_UP) and not collision.collide(jones,ledder):
               self.state=self.RIGHT_STAND
        if (event.type, event.key)==(SDL_KEYDOWN, SDLK_UP):
               if self.ondoor:
                   game_framework.change_state(main_state3)


    def get_bb(self):
        return self.x-15,self.y-31,self.x+15,self.y+31
    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def update(self,frame_time):
        global lands
        distance=Jones.RUN_SPEED_PPS*frame_time
        #gravity_distance=Jones.GRAVITY_PPS*frame_time
        self.total_frames+=1.0
        self.frame=(self.frame+1)%7

        if self.state==self.RIGHT_RUN:
            for i in lands:
                i.x-=distance
            for spear in spears:
                spear.x-=distance
            for door in doors:
                door.x-=distance
            for ledder in ledders:
                ledder.x-=distance
            for bow in bows:
                bow.x-=distance
            for stone in stones:
                stone.x-=distance
            for ml in mls:
                ml.x-=distance
            field.field_draw_x-=distance
        elif self.state==self.RIGHT_USE_ROPE:
            self.y+=5
            if((jones.fst_field_x-field.field_draw_x)<200):
               for i in lands:
                   i.x-=distance
               for spear in spears:
                   spear.x-=distance
               for door in doors:
                    door.x-=distance
               for ledder in ledders:
                    ledder.x-=distance
               for bow in bows:
                   bow.x-=distance

               field.field_draw_x-=distance
            else:
                self.state=self.RIGHT_STAND
        elif self.state == self.LEFT_RUN:
            for i in lands:
                i.x+=distance
            for spear in spears:
                spear.x+=distance
            for door in doors:
                door.x+=distance
            for ledder in ledders:
                ledder.x+=distance
            for bow in bows:
                bow.x+=distance
            for stone in stones:
                stone.x+=distance
            for ml in mls:
                ml.x+=distance
            field.field_draw_x += distance
        elif self.state==self.LEFT_USE_ROPE:
            self.y+=5
            if((field.field_draw_x-jones.fst_field_x)<200):
               for i in lands:
                   i.x+=distance
               for spear in spears:
                   spear.x+=distance
               for door in doors:
                    door.x+=distance
               for ledder in ledders:
                    ledder.x+=distance
               field.field_draw_x+=distance
            else:
                self.state=self.LEFT_STAND
        elif self.state==self.UPDOWN_RUN:
            self.y+=distance
        if self.jump:
            self.y+=distance
            if self.y>self.fst_y+90:
                self.jump=False

        print(jones.x,jones.y)
    def draw(self):
        #self.image.clip_draw(self.state*350+self.frame*50, 0, 50, 62, self.x, self.y)
        if self.state in (self.RIGHT_RUN, self.LEFT_RUN):
            self.image.clip_draw(self.frame*30,self.state*48,30,48,self.x,self.y)
        elif self.state in (self.RIGHT_STAND, self.LEFT_STAND):
            self.image.clip_draw(0, (self.state-2) * 48, 30, 48, self.x, self.y)



class Land:
    image=None
    def __init__(self,x,y):
        self.x=x
        self.y=y-40
        lands.append(self)
        if Land.image==None:
            Land.image=load_image('land4.png')
        #for land in range(self.x-80,self.x+80):
            #Land.is_land.append(land)
        #Land.is_land.append(self.x)
    def draw(self):
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-250, self.y+20, self.x+250, self.y+30
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

def make_land():
    global land1,land2,land3,land4,land5,land6,land7,land8,land9, land10, land11, land12,land13
    land1 = Land(400, 90) #바닥
    land2 = Land(900, 90)
    land3 = Land(1400,50)
    land4 = Land(2000,50)
    land5 = Land(2400,90)
    land6= Land(2900,90)
    land7=Land(3500,90)
    land8= Land(4000,90)
    land9=Land(4900,70)
    land11=Land(5200,70)
    land12=Land(5800,70)
    land13=Land(4100,350)
    land10=Land(1650,350)
class Move_land:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fst_x=x
        self.dir=0
        self.frame=0
        mls.append(self)
        if Move_land.image == None:
            Move_land.image = load_image('land4.png')


    def draw(self):
        self.image.clip_draw(0,0,100,60,self.x, self.y)
    def update(self):
        if self.dir==0:
            self.x+=1
            self.frame+=1
            if self.frame>200:
                self.dir=1
                self.frame=0
        elif self.dir==1:
            self.x-=1
            self.frame+=1
            if self.frame>200:
                self.dir=0
                self.frame=0




    def get_bb(self):
        return self.x - 50, self.y + 20, self.x + 50, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def make_ml():
    global ml1,ml2, ml3
    ml1=Move_land(4300,200)
    ml2=Move_land(400,200)




class Spear:
    image=None
    def __init__(self,x,y):
        self.x=x
        self.y=y
        spears.append(self)
        if Spear.image==None:
            Spear.image=load_image('spear_.png')
        #for land in range(self.x-80,self.x+80):
            #Land.is_land.append(land)
        #Land.is_land.append(self.x)
    def draw(self):
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-20, self.y-12, self.x+20, self.y+12
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
def make_spear():
    global spear1,spear2, spear3, spear4, spear5,spear6,spear7,spear8,spear9,spear10
    spear1=Spear(500,90)
    spear2=Spear(600,90)
    spear6=Spear(720,90)
    spear8=Spear(950,90)
    spear7=Spear(1100,90)
    spear3=Spear(2000,50)
    spear4=Spear(3800,90)
    spear5=Spear(4200,90)
class Door:
    image=None
    def __init__(self,x,y):
        self.x=x
        self.y=y
        doors.append(self)
        if Door.image==None:
            Door.image=load_image('door.png')
    def draw(self):
        self.image.draw(self.x,self.y)
    def get_bb(self):
        return self.x-65, self.y-100, self.x+65, self.y+100
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
def make_door():
    global door1,door2,door3
    door1=Door(5000,110)

class Ledder:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        ledders.append(self)
        if Ledder.image == None:
            Ledder.image = load_image('ladder_.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def make_Ledder():
    global ledder1,ledder2,ledder3,ledder4,ledder5,ledder6,ledder7,ledder8,ledder9,ledder10,ledder11,ledder12,ledder13
    ledder1=Ledder(1500,100)
    ledder2=Ledder(1500,150)
    ledder3=Ledder(1500,200)
    ledder4=Ledder(1500,250)
    ledder5=Ledder(1500,300)
    ledder6=Ledder(2100,70)
    ledder7=Ledder(2100,120)
    ledder8=Ledder(4000,70)
    ledder9=Ledder(4000,120)
    ledder10=Ledder(4000,150)
    ledder11=Ledder(4000,200)
    ledder12=Ledder(4000,250)
    ledder13=Ledder(4000,300)

class Bow:
    image = None
    bow_trigger=False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        bows.append(self)
        if Bow.image == None:
            Bow.image = load_image('bow.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 20, self.y - 12, self.x + 20, self.y + 12

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def make_bow():
    global bow1,bow2,bow3,bow4,bow5,bow6
    bow1=Bow(2500,120)
    bow2=Bow(3000,90)
    bow4=Bow(3400,90)
    bow3=Bow(3800,90)
    bow5=Bow(4200,110)
    bow6=Bow(4400,90)


class Stone:
    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotateangle=0
        self.total_frames=0
        self.Stone_trigger=False
        stones.append(self)
        if Stone.image == None:
            Stone.image = load_image('stone_.png')
    def update(self,frame_time):
        distance = Stone.RUN_SPEED_PPS * frame_time
        self.total_frames += 1.0
        self.rotateangle-=0.01
        if(self.Stone_trigger):
            for land in lands:
                if collision.collide(self,land) and self.x<4300:
                    self.x+=distance
                    return
            self.y-=2


    def draw(self):
        #self.image.draw(self.x, self.y)
        self.image.rotate_draw(self.rotateangle, self.x, self.y)

    def get_bb(self):
        return self.x - 80, self.y - 90, self.x + 80, self.y + 90

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def make_stone():
    global stone1
    stone1=Stone(2400,700)


def get_frame_time_jones():
    global current_time_jones
    frame_time = get_time() - current_time_jones
    current_time_jones += frame_time
    return frame_time
def get_frame_time_stone():
    global current_time_stone
    frame_time = get_time() - current_time_stone
    current_time_stone += frame_time
    return frame_time

def enter():
    global jones,field,lands,spears,doors,mls,stones
    field=Field()
    jones=Jones()
    make_land()
    make_spear()
    make_door()
    make_Ledder()
    make_ml()
    make_stone()
    make_bow()
    print(type(lands))




def exit():
    global jones,field,lands,spears,doors
    del(jones)
    del(field)
    del(lands)
    del(spears)
    del(doors)
    close_canvas()


def update():
    print(stone1.Stone_trigger)
    print(field.field_draw_x)
    jones.update(get_frame_time_jones())
    stone1.update(get_frame_time_stone())
    if jones.y<-10 or jones.dead: #게임오버 조건
        game_framework.push_state(gameover_state)

    if(collision.collide(jones,door1)):
        jones.ondoor=True
    else:
        jones.ondoor=False
    #for ledder in ledders:
    #    if(collision.collide(jones,ledder)):
    #        jones.onledder=True

    for spear in spears:
        if(collision.collide(jones, spear)):
           print("collision")
           #jones.dead=True
    #for ml in mls:
     #   ml.update()
    for bow in bows:
        if(collision.collide(jones,bow)):
            print("collision")
            #jones.deae=True
    if field.field_draw_x<3000:
        for bow in bows:
            bow.bow_trigger=True
    if field.field_draw_x<2300:
        for stone in stones:
            stone1.Stone_trigger=True
    for bow in bows:
        if bow.bow_trigger:
            bow.x-=1
    for land in lands :
        if(collision.collide(jones,land)):
           return
    for ml in mls:
        if (collision.collide(jones, ml)):
            if ml.dir==0:
                jones.x+=1

                field.field_draw_x -= 1
            elif ml.dir==1:
                jones.x-=1

                field.field_draw_x += 1
            return
    if jones.state==Jones.UPDOWN_RUN:
        return
    if jones.state==Jones.UPDOWN_STAND:
        return
    if jones.jump:
        return

    jones.y-=2

def draw():
    global jones,lands,doors,ledders,bows,stones
    clear_canvas()
    field.draw()
    jones.draw_bb()
    for land in lands:
        land.draw()
        land.draw_bb()
    for spear in spears:
        spear.draw()
        spear.draw_bb()
    for door in doors:
        door.draw()
    for ledder in ledders:
        ledder.draw()
    for bow in bows:
        bow.draw()
        bow.draw_bb()
    for stone in stones:
        stone.draw()
    for ladder in ledders:
        ladder.draw()
        ladder.draw_bb()
    #for ml in mls:
     #   ml.draw()
      #  ml.draw_bb()
    for bow in bows:
        bow.draw()
    jones.draw()
    for stone in stones:
        stone.draw()
        stone.draw_bb()

    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN , SDLK_ESCAPE):
                game_framework.quit()
            else:
                jones.handle_event(event)




def pause(): pass


def resume(): pass
