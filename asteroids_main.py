import asteroid
from screen import Screen
import sys

from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import randint
import math

DEFAULT_ASTEROIDS_NUM = 5
SIZE_ASTEROIDS = 3
RIGHT = "right"
LEFT = "left"
LOST_LIFE_MSG = "You have lost a life."
LOST_LIFE_TITLE = "Lost life."
MIN_ASTEROID_SPEED = 1
MAX_ASTEROID_SPEED = 4


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship(randint(self.__screen_min_x, self.__screen_max_x),
                           randint(self.__screen_min_y, self.__screen_max_y))
        self.__asteroids_lst = []

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        # TODO: Your code goes here
        self.__generate_draw_asteroids()
        self.__draw_all()
        self.__all_obj_updates()
        self.__check_intersections()

    def __all_obj_updates(self):
        self.__update_ship_location()
        self.__update_ship_speed()
        self.__update_ship_direction()
        self.__update_asteroid_location()


    def __draw_all(self, __asteroid=None):
        self.__screen.draw_ship(self.__ship.get_loc_x(),
                                self.__ship.get_loc_y(),
                                self.__ship.get_direction())
        for ast in self.__asteroids_lst:
            self.__screen.draw_asteroid(ast,
                                        ast.get_loc_x(),
                                        ast.get_loc_y())

    def __update_ship_direction(self):
        direction = self.__ship.get_direction()
        if self.__screen.is_right_pressed():
            direction += math.degrees(7)
        elif self.__screen.is_left_pressed():
            direction -= math.degrees(7)
        self.__ship.set_direction(direction)

    def __update_ship_location(self):
        new_x, new_y = self.__calc_new_location(self.__ship)
        self.__ship.set_location(new_x, new_y)

    def __update_asteroid_location(self):
        for ast in self.__asteroids_lst:
            new_x, new_y = self.__calc_new_location(ast)
            ast.set_location(new_x, new_y)

    def __calc_new_location(self, obj):
        min_x, max_x = self.__screen_min_x, self.__screen_max_x
        min_y, max_y = self.__screen_min_y, self.__screen_max_y

        new_x = min_x + (obj.get_loc_x() + obj.get_speed_x() - min_x) \
                % (max_x - min_x)
        new_y = min_y + (obj.get_loc_y() + obj.get_speed_y() - min_y) \
                % (max_y - min_y)
        return new_x, new_y


    def __update_ship_speed(self):
        up_pressed = False
        if self.__screen.is_up_pressed():
            up_pressed = True
        ship = self.__ship
        while up_pressed:
            new_speed_x = ship.get_speed_x() + \
                          math.cos(math.radians(ship.get_direction()))
            new_speed_y = ship.get_speed_y() + \
                          math.sin(math.radians(ship.get_direction()))
            if not self.__screen.is_up_pressed():
                ship.set_speed(new_speed_x, new_speed_y)
                up_pressed = False

    def __check_intersections(self):
        for ast in self.__asteroids_lst:
            if ast.has_intersection(self.__ship):
                self.__screen.show_message(LOST_LIFE_TITLE, LOST_LIFE_MSG)
                self.__asteroids_lst.remove(ast)
                self.__screen.unregister_asteroid(ast)
                self.__screen.remove_life()


    #########################################################################
    # part 3
    def __generate_draw_asteroids(self):
        while len(self.__asteroids_lst) < DEFAULT_ASTEROIDS_NUM:
            now_asteroid = Asteroid(randint(self.__screen_min_x, self.__screen_max_x),
                                    randint(self.__screen_min_y, self.__screen_max_y),
                                    randint(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED),
                                    randint(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED))
            if not now_asteroid.has_intersection(self.__ship):
                self.__asteroids_lst.append(now_asteroid)
                self.__screen.register_asteroid(now_asteroid, SIZE_ASTEROIDS)

    #########################################################################
    # part 4
    torpedo = Torpedo(__shi)
    def disparar_torpedo(self):
        self.__screen.draw_torpedo()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
