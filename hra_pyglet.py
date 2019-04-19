import math
from random import randrange, choice


import pyglet
from pyglet.window import key


# Setting of input variables
WIDTH = 800
HEIGHT = 600
SPEED = 125
SPEED_KOEF = [1]

FROG_WIDTH = 80
FROG_HEIGHT = 80

PRINCESS_WIDTH = 150
PRINCESS_HEIGHT = 150

DONUTS = []
DONUTS_COORDINATES = []

SCORE = [0, 3]
FONT_SIZE = 42
TEXT_INDENTATION = 30

GAME = ['menu']
pressed_keys = set()


# DEFINITIONS of FUNCTIONS
def on_key_press(symbol, modifiers):
    '''
    On key press - move left, right, up or down.
    Or pres ENTER to go between GAME and MENU.
    '''
    if symbol == key.LEFT:
        pressed_keys.add(('left', 0))
    if symbol == key.RIGHT:
        pressed_keys.add(('right', 0))
    if symbol == key.UP:
        pressed_keys.add(('up', 0))
    if symbol == key.DOWN:
        pressed_keys.add(('down', 0))
    if symbol == key.ENTER:
        pressed_keys.add(('enter', 0))


def on_key_release(symbol, modifiers):
    '''
    On key release - stop move.
    '''
    if symbol == key.LEFT:
        pressed_keys.discard(('left', 0))
    if symbol == key.RIGHT:
        pressed_keys.discard(('right', 0))
    if symbol == key.UP:
        pressed_keys.discard(('up', 0))
    if symbol == key.DOWN:
        pressed_keys.discard(('down', 0))


def reset():
    '''
    Reset Princess and Frog position.
    '''
    SPEED_KOEF[0] = 1
    princess_right.x, princess_right.y = -150, 150
    princess_left.x, princess_left.y = WIDTH, HEIGHT - 300
    frog.x, frog.y = WIDTH // 2, HEIGHT // 2


def restore_conditions(t):
    '''
    When GAME = game:
    Princess movement, Frog movement, Limits of frog movement outside
    the playing field and what hapend, when Princess catches Frog or
    Frog eats Donut.

    When GAME = menu:
    Press Enter to continue in game.

    When GAME = game over:
    Lifes = 0. Press Enter to go to the Menu.

    When GAME = gotcha:
    The Princess catched The Frog. One life down.
    Press enter to continue in game.
    '''
    if GAME[0] == 'game':
        # Princess move
        princess_right.x = princess_right.x + t * SPEED * SPEED_KOEF[0]
        if princess_right.x > WIDTH:
            princess_right.y = choice([10, 100, 200, 300, 400])
            princess_right.x = -150 + t * SPEED * SPEED_KOEF[0]
        princess_left.x = princess_left.x - t * SPEED * SPEED_KOEF[0]
        if princess_left.x < -150:
            princess_left.y = HEIGHT - PRINCESS_HEIGHT - choice([10, 100, 200, 300, 400])
            princess_left.x = WIDTH - t * SPEED * SPEED_KOEF[0]

        # Frog move
        if ('up', 0) in pressed_keys:
            frog.y += SPEED * t * 2
        if ('down', 0) in pressed_keys:
            frog.y -= SPEED * t * 2
        if ('left', 0) in pressed_keys:
            frog.x -= SPEED * t * 2
        if ('right', 0) in pressed_keys:
            frog.x += SPEED * t * 2

        # Limits of frog movement outside the playing field
        if frog.x < 0:
            frog.x = 0
        if frog.x > (WIDTH - FROG_WIDTH):
            frog.x = (WIDTH - FROG_WIDTH)
        if frog.y < 0:
            frog.y = 0
        if frog.y > (HEIGHT - FROG_HEIGHT):
            frog.y = (HEIGHT - FROG_HEIGHT)

        # When Princess catches Frog
        if (princess_left.x - FROG_WIDTH - 10) < frog.x < (princess_left.x + PRINCESS_WIDTH - 10) \
           and (princess_left.y - FROG_HEIGHT + 10) < frog.y < (princess_left.y + PRINCESS_HEIGHT - 10):
            SCORE[1] -= 1  # One life down
            if SCORE[1] == 0:
                GAME[0] = 'game over'
            else:
                GAME[0] = 'gotcha'

        if (princess_right.x - FROG_WIDTH - 10) < frog.x < (princess_right.x + PRINCESS_WIDTH - 10) \
           and (princess_right.y - FROG_HEIGHT + 10) < frog.y < (princess_right.y + PRINCESS_HEIGHT - 10):
            SCORE[1] -= 1  # One life down
            if SCORE[1] == 0:
                GAME[0] = 'game over'
            else:
                GAME[0] = 'gotcha'

        # When Frog eats Donut
        for x, y in DONUTS_COORDINATES:
            if (x - FROG_WIDTH - 20) < frog.x < (x+30) and (y - FROG_HEIGHT - 20) < frog.y < (y+20):
                SCORE[0] += 1
                if SCORE[0] % 10 == 0:  # When Frog eats 10 Donuts = One life up
                    SCORE[1] += 1
                    SPEED_KOEF[0] += 0.1  # When Frog eats 10 Donuts = Princess speed up
                del DONUTS[DONUTS_COORDINATES.index((x,y))]
                del DONUTS_COORDINATES[DONUTS_COORDINATES.index((x,y))]

        # Image HEART for lifes, Image Donuts on plate for score
        heart.x, heart.y = TEXT_INDENTATION + 70, HEIGHT - TEXT_INDENTATION - FONT_SIZE
        donuts_plate.x, donuts_plate.y = WIDTH - 70, HEIGHT - TEXT_INDENTATION - FONT_SIZE

        # Press ENTER to go to the MENU
        if ('enter', 0) in pressed_keys:
            GAME[0] = 'menu'
            pressed_keys.discard(('enter', 0))

    if GAME[0] == 'menu':
        # Press ENTER to go to the GAME
        menu.x, menu.y = (WIDTH - menu.width)//2, (HEIGHT - menu.height)//2
        if ('enter', 0) in pressed_keys:
            GAME[0] = 'game'
            pressed_keys.discard(('enter', 0))

    if GAME[0] == 'gotcha':
        princess_frog_right.x, princess_frog_right.y = HEIGHT//2-100, WIDTH * 0.45
        gotcha.x, gotcha.y = (WIDTH - gotcha.width)//2, (HEIGHT - gotcha.height) // 2
        if ('enter', 0) in pressed_keys:
            reset()
            GAME[0] = 'game'
            pressed_keys.discard(('enter', 0))

    if GAME[0] == 'game over':
        wedding.x, wedding.y = (WIDTH - wedding.width)//2, (HEIGHT - wedding.height)//2
        game_over.x = (WIDTH - game_over.width)//2
        SCORE[0] = 0
        SCORE[1] = 3
        if ('enter', 0) in pressed_keys:
            reset()
            DONUTS.clear()
            DONUTS_COORDINATES.clear()
            GAME[0] = 'menu'
            pressed_keys.discard(('enter', 0))


def changing_donuts(t):
    '''
    Maximum of Donuts on the playfiel is MAX_DONUTS.
    '''
    if GAME[0] == 'game':
        MAX_DONUTS = 10
        if len(DONUTS) < MAX_DONUTS:
            donut_image = pyglet.image.load(str('images/donuts/{}.png'.format(choice([1, 2, 3, 4, 5, 6]))))
            donut_image.texture.width = 50
            donut_image.texture.height = 50
            x, y = randrange(0, WIDTH-20), randrange(0, HEIGHT-20)
            DONUTS.append(pyglet.sprite.Sprite(donut_image, x, y, batch=batch))
            DONUTS_COORDINATES.append((x, y))


def draw_text(text, x, y, anchor_x):
    '''
    Draw text in playfield.
    '''
    text = pyglet.text.Label(
        text,
        font_name='League Gothic',
        font_size=FONT_SIZE,
        x=x, y=y, anchor_x=anchor_x)
    text.draw()


def on_draw():
    window.clear()
    if GAME[0] == 'game':
        draw_text(str(SCORE[0]),
                      x = WIDTH - TEXT_INDENTATION - 50,
                      y = HEIGHT - TEXT_INDENTATION - FONT_SIZE,
                      anchor_x = 'right')
        draw_text(str(SCORE[1]),
                      x = TEXT_INDENTATION,
                      y = HEIGHT - TEXT_INDENTATION - FONT_SIZE,
                      anchor_x = 'left')
        heart.draw()
        donuts_plate.draw()
        batch.draw()
        princess_right.draw()
        princess_left.draw()
        frog.draw()

    if GAME[0] == 'menu':
        menu.draw()

    if GAME[0] == 'game over':
        wedding.draw()
        game_over.draw()

    if GAME[0] == 'gotcha':
        gotcha.draw()
        princess_frog_right.draw()


def change_frog_image(t):
    frog.image = frog_left_image
    pyglet.clock.schedule_once(change_frog_image_back, 0.5)


def change_frog_image_back(t):
    frog.image = frog_right_image
    pyglet.clock.schedule_once(change_frog_image, 0.5)


# GAME
window = pyglet.window.Window(WIDTH, HEIGHT)

# Images load
frog_right_image = pyglet.image.load('images/frog_right.png')
frog_right_image.texture.width = FROG_WIDTH
frog_right_image.texture.height = FROG_HEIGHT
frog = pyglet.sprite.Sprite(frog_right_image)

frog_left_image = pyglet.image.load('images/frog_left.png')
frog_left_image.texture.width = FROG_WIDTH
frog_left_image.texture.height = FROG_HEIGHT

princess_image = pyglet.image.load('images/princess_right.png')
princess_image.texture.width = PRINCESS_WIDTH
princess_image.texture.height = PRINCESS_HEIGHT
princess_right = pyglet.sprite.Sprite(princess_image)

princess_image = pyglet.image.load('images/princess_left.png')
princess_image.texture.width = PRINCESS_WIDTH
princess_image.texture.height = PRINCESS_HEIGHT
princess_left = pyglet.sprite.Sprite(princess_image)

princess_image = pyglet.image.load('images/princess_frog_right.png')
princess_image.texture.width = PRINCESS_WIDTH
princess_image.texture.height = PRINCESS_HEIGHT
princess_frog_right = pyglet.sprite.Sprite(princess_image)

heart_image = pyglet.image.load('images/heart.png')
heart_image.texture.width = 40
heart_image.texture.height = 40
heart = pyglet.sprite.Sprite(heart_image)

donuts_plate_image = pyglet.image.load('images/donuts_plate.png')
donuts_plate_image.texture.width = 40
donuts_plate_image.texture.height = 40
donuts_plate = pyglet.sprite.Sprite(donuts_plate_image)

gotcha_image = pyglet.image.load('images/gotcha.png')
gotcha_image.texture.width = 400
gotcha_image.texture.height = 320
gotcha = pyglet.sprite.Sprite(gotcha_image)

menu_image = pyglet.image.load('images/menu.jpg')
menu = pyglet.sprite.Sprite(menu_image)

wedding_image = pyglet.image.load('images/wedding.png')
wedding = pyglet.sprite.Sprite(wedding_image)

game_over_image = pyglet.image.load('images/game_over.png')
game_over = pyglet.sprite.Sprite(game_over_image)

batch = pyglet.graphics.Batch()

reset()

window.push_handlers(
    on_draw=on_draw,
    on_key_press=on_key_press,
    on_key_release=on_key_release,
)

pyglet.clock.schedule_once(change_frog_image, 0.5)
pyglet.clock.schedule_interval(restore_conditions, 1/30)
pyglet.clock.schedule_interval(changing_donuts, 2)

pyglet.app.run()
