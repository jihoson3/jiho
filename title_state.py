import game_framework
from pico2d import *

import main_state2



name = "TitleState"
image = None



def enter():
    global image
    image=load_image('title.png')



def exit():
    global image
    del(image)
    close_canvas()


def update():
    pass


def draw():
    global image
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
                game_framework.push_state(main_state2)



def pause(): pass


def resume(): pass
