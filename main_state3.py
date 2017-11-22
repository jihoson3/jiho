import game_framework
import title_state
import collision
import gameover_state
import main_state3
from pico2d import *

import main_state

lands = []
spears = []
doors = []
current_time = 0.0
name = "MainState"
image = None


class Field:
    def __init__(self):
        self.image = load_image('stage.png')
        self.field_draw_x = 4400

    def draw(self):
        self.image.draw(self.field_draw_x, 300)


class Jones:
    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    GRAVITY_KMPH = 40.0
    GRAVITY_MPM = (GRAVITY_KMPH * 1000.0 / 60.0)
    GRAVITY_MPS = (GRAVITY_MPM / 60.0)
    GRAVITY_PPS = (GRAVITY_MPS * PIXEL_PER_METER)
    image = None
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, RIGHT_USE_ROPE, LEFT_USE_ROPE = 3, 0, 2, 1, 4, 5

    def __init__(self):
        self.x, self.y = 400, 400
        self.state = self.RIGHT_STAND
        self.is_jump = False
        self.frame = 0
        self.rope_time = 0.0
        self.dead = False
        self.total_frames = 0.0
        self.fst_field_x = 0
        self.ondoor = False
        if Jones.image == None:
            Jones.image = load_image("test2.png")

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN):
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.LEFT_RUN):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state = self.RIGHT_STAND
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):  # 로프기능
            if self.state in (self.RIGHT_RUN, self.RIGHT_STAND):
                self.state = self.RIGHT_USE_ROPE
                self.fst_field_x = field.field_draw_x
            if self.state in (self.LEFT_RUN, self.LEFT_STAND):
                self.state = self.LEFT_USE_ROPE
                self.fst_field_x = field.field_draw_x
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.ondoor:
                game_framework.change_state(main_state3)

    def get_bb(self):
        return self.x - 15, self.y - 31, self.x + 15, self.y + 31

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def update(self, frame_time):
        global lands
        distance = Jones.RUN_SPEED_PPS * frame_time
        gravity_distance = Jones.GRAVITY_PPS * frame_time
        self.total_frames += 1.0
        self.frame = (self.frame + 1) % 7

        if self.state == self.RIGHT_RUN:
            for i in lands:
                i.x -= distance
            for spear in spears:
                spear.x -= distance
            field.field_draw_x -= distance
        elif self.state == self.RIGHT_USE_ROPE:
            self.y += 5
            if ((jones.fst_field_x - field.field_draw_x) < 200):
                for i in lands:
                    i.x -= distance
                for spear in spears:
                    spear.x -= distance
                field.field_draw_x -= distance
            else:
                self.state = self.RIGHT_STAND
        elif self.state == self.LEFT_RUN:
            for i in lands:
                i.x += distance
            for spear in spears:
                spear.x += distance
            field.field_draw_x += distance
        elif self.state == self.LEFT_USE_ROPE:
            self.y += 5
            if ((field.field_draw_x - jones.fst_field_x) < 200):
                for i in lands:
                    i.x += distance
                for spear in spears:
                    spear.x += distance
                field.field_draw_x += distance
            else:
                self.state = self.LEFT_STAND

        print(jones.x, jones.y)

    def draw(self):
        # self.image.clip_draw(self.state*350+self.frame*50, 0, 50, 62, self.x, self.y)
        self.image.clip_draw(self.frame * 30, 0, 30, 48, self.x, self.y)


class Land:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y - 40
        lands.append(self)
        if Land.image == None:
            Land.image = load_image('land.png')
            # for land in range(self.x-80,self.x+80):
            # Land.is_land.append(land)
            # Land.is_land.append(self.x)

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 250, self.y - 30, self.x + 250, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def make_land():
    global land1, land2, land3, land4, land5, land6, land7, land8, land9, land10, land11, land12
    land1 = Land(400, 90)  # 바닥
    land2 = Land(900, 90)
    land3 = Land(1400, 50)
    land4 = Land(2000, 50)
    land5 = Land(2400, 90)
    land6 = Land(2900, 90)
    land7 = Land(3500, 90)
    land8 = Land(4000, 90)
    land9 = Land(4600, 70)
    land10 = Land(1650, 350)


class Spear:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        spears.append(self)
        if Spear.image == None:
            Spear.image = load_image('Spear.png')
            # for land in range(self.x-80,self.x+80):
            # Land.is_land.append(land)
            # Land.is_land.append(self.x)

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 25, self.y - 15, self.x + 25, self.y + 15

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def make_spear():
    global spear1, spear2, spear3, spear4, spear5
    spear1 = Spear(500, 90)
    spear2 = Spear(600, 90)
    spear3 = Spear(2000, 50)
    spear4 = Spear(3800, 90)
    spear5 = Spear(4200, 90)


class Door:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y + 20
        doors.append(self)
        if Door.image == None:
            Door.image = load_image('door.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 65, self.y - 100, self.x + 65, self.y + 100

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def make_door():
    global door1
    door1 = Door(4600, 70)


def get_frame_time():
    global current_time
    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def enter():
    global jones, field, lands, spears, doors
    field = Field()
    jones = Jones()
    make_land()
    make_spear()
    make_door()
    print(type(lands))


def exit():
    global jones
    del (jones)
    close_canvas()


def update():
    jones.update(get_frame_time())
    if jones.y < -10 or jones.dead:  # 게임오버 조건
        game_framework.push_state(gameover_state)
    for door in doors:
        if (collision.collide(jones, door)):
            jones.ondoor = True
    for spear in spears:
        if (collision.collide(jones, spear)):
            print("collision")
            # jones.dead=True
    for land in lands:
        if (collision.collide(jones, land)):
            return

    jones.y -= 5


def draw():
    global jones, lands
    clear_canvas()
    field.draw()
    jones.draw()
    jones.draw_bb()
    for land in lands:
        land.draw()
        land.draw_bb()
    for spear in spears:
        spear.draw()
        spear.draw_bb()
    for door in doors:
        door.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                jones.handle_event(event)


def pause(): pass


def resume(): pass
