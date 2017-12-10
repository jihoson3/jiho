import game_framework
import gameover_state
import clear_state
from pico2d import *

current_time_jones=0.0
class JwerlyField:
    def __init__(self):
        self.image = load_image('jwerly_field.png')
        self.bgm=load_music('jwerly_bgm.mp3')
        self.bgm.set_volume(64)
        self.bgm.play()

    def draw(self):
        self.image.draw(400, 300)
class Gold:
    def __init__(self):
        self.image=load_image('golden_cup.png')
    def draw(self):
        self.image.draw(400,200)
class Jone:
    image=None
    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3

    def __init__(self):
        self.x,self.y=100,150
        self.frame=0
        self.total_frames = 0.0
        self.state=self.RIGHT_STAND
        if Jone.image==None:
            Jone.image=load_image('jones_.png')
    def  handle_event(self,event):
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
    def update(self,frame_time):
        distance = Jone.RUN_SPEED_PPS * frame_time
        self.total_frames += 1.0

        self.frame = (self.frame + 1) % 8
        if self.state == self.RIGHT_RUN:
            self.x = min(800, self.x + distance)
        elif self.state == self.LEFT_RUN:
            self.x = max(0, self.x - distance)
        if self.x>400:
            game_framework.push_state(clear_state)

    def draw(self):
        if self.state in (self.RIGHT_RUN, self.LEFT_RUN):
            self.image.clip_draw(self.frame*30,self.state*48,30,48,self.x,self.y)
        elif self.state in (self.RIGHT_STAND, self.LEFT_STAND):
            self.image.clip_draw(0, (self.state-2) * 48, 30, 48, self.x, self.y)


def get_frame_time_jones():
    global current_time_jones
    frame_time = get_time() - current_time_jones
    current_time_jones += frame_time
    return frame_time



def enter():
    global jone
    global jwerlyfield
    global gold
    jwerlyfield=JwerlyField()
    jone=Jone()
    gold=Gold()






def exit():
    global jone,jwerlyfield,gold
    del(jone)
    del(jwerlyfield)
    del(gold)


    close_canvas()


def update():
    global jone
    jone.update(get_frame_time_jones())




def draw():
    clear_canvas()
    global jone,jwerlyfield
    jwerlyfield.draw()
    gold.draw()
    jone.draw()
    update_canvas()


def handle_events():
    global jone
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            jone.handle_event(event)




def pause(): pass


def resume(): pass


