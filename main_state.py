import game_framework
import title_state
from pico2d import *

import main_state


current_time=0.0
name = "MainState"
image = None

class Jones:
    PIXEL_PER_METER = (10.0/0.3)
    RUN_SPEED_KMPH=20.0
    RUN_SPEED_MPM=(RUN_SPEED_KMPH *1000.0/60.0)
    RUN_SPEED_MPS=(RUN_SPEED_MPM/60.0)
    RUN_SPEED_PPS=(RUN_SPEED_MPS *PIXEL_PER_METER)
    GRAVITY_KMPH=40.0
    GRAVITY_MPM=(GRAVITY_KMPH*1000.0/60.0)
    GRAVITY_MPS=(GRAVITY_MPM/60.0)
    GRAVITY_PPS=(GRAVITY_MPS*PIXEL_PER_METER)
    image = None
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 3, 0, 2, 1


    def __init__(self):
        self.x, self.y = 30, 400
        self.state = self.RIGHT_STAND
        self.frame = 0
        self.total_frames=0.0
        if Jones.image == None:
            Jones.image=load_image("jones_move.png")
    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN):
                self.state=self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND ,self.LEFT_STAND , self.LEFT_RUN):
                self.state=self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state=self.LEFT_STAND
        elif (event.type, event.key)==(SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state=self.RIGHT_STAND
        elif (event.type, event.key)==(SDL_KEYDOWN, SDLK_SPACE):
            if self.state in (self.RIGHT_RUN, self.LEFT_RUN):
                pass

    def update(self,frame_time):
        distance=Jones.RUN_SPEED_PPS*frame_time
        gravity_distance=Jones.GRAVITY_PPS*frame_time
        self.total_frames+=1.0
        self.frame=(self.frame+1)%7
        if not (Land.is_land[0]>=self.x-80 and Land.is_land[0]<=self.x+80):
            self.y -= gravity_distance
        if self.state==self.RIGHT_RUN:
            self.x=min(800,self.x+distance)
        elif self.state == self.LEFT_RUN:
            self.x=max(0,self.x-distance)
        print(jones.x,jones.y)
    def draw(self):
        self.image.clip_draw(self.state*350+self.frame*50, 0, 50, 62, self.x, self.y)

class Land:
    image=None
    is_land=[]
    def __init__(self,x,y):
        self.x=x
        self.y=y
        if Land.image==None:
            Land.image=load_image('tile2.png')
        #for land in range(self.x-80,self.x+80):
            #Land.is_land.append(land)
        Land.is_land.append(self.x)
    def draw(self):
        self.image.draw(self.x,self.y)


def linear_search(element, my_list):
    for i in range(len(my_list)):
        if element == my_list[i]:
            return i
    return None



def get_frame_time():
    global current_time
    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time

def enter():
    global jones,land1,land2
    jones=Jones()
    land1=Land(80,90)
    land2=Land(160,90)



def exit():
    global jones
    del(jones)
    close_canvas()


def update():
    jones.update(get_frame_time())


def draw():
    global jones,land1
    clear_canvas()
    jones.draw()
    land1.draw()
    land2.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN , SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title_state)
            else:
                jones.handle_event(event)




def pause(): pass


def resume(): pass
