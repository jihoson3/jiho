import game_framework
import gameover_state
import clear_state
import jwerly_state
from pico2d import *

name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    image=load_image('stageclear.png')



def exit():
    global image
    del(image)



def update():
    global logo_time



def draw():
    global image
    clear_canvas()
    image.draw(400,300)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()



def pause(): pass


def resume(): pass

