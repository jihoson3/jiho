import game_framework
import title_state
from pico2d import*

import main_state2

import game_framework
from pico2d import *

import main_state



name = "TitleState"
image = None


def enter():
    global over_state_time, image
    #over_state_time = 0.0
    image=load_image('gameover.png')




def exit():
    global image
    del (image)



def update():
    global over_state_time
    #over_state_time+=0.1


def draw():
    global over_state_time, image
    clear_canvas()
    image.draw(400,300)
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
                close_canvas()
                open_canvas()
                game_framework.run(main_state2)



def pause(): pass


def resume(): pass
