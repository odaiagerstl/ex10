from screen import Screen
import sys

from ship import Ship
from random import randint
import math

DEFAULT_ASTEROIDS_NUM = 5
RIGHT = "right"
LEFT = "left"


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship(randint(self.__screen_min_x, self.__screen_max_x),
                           randint(self.__screen_min_y, self.__screen_max_y))

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
        self.__draw_all()
        self.__all_ship_updates()

    def __all_ship_updates(self):
        self.__update_ship_location()
        self.__update_ship_speed()
        self.__update_ship_direction()

    def __draw_all(self):
        self.__screen.draw_ship(self.__ship.get_loc_x(),
                                self.__ship.get_loc_y(),
                                self.__ship.get_direction())

    def __update_ship_direction(self):
        direction = self.__ship.get_direction()
        if self.__screen.is_right_pressed():
            direction += math.degrees(7)
        elif self.__screen.is_left_pressed():
            direction -= math.degrees(7)
        self.__ship.set_direction(direction)

    def __update_ship_location(self):
        min_x, max_x = self.__screen_min_x, self.__screen_max_x
        min_y, max_y = self.__screen_min_y, self.__screen_max_y

        new_x = min_x + (self.__ship.get_loc_x() + self.__ship.get_speed_x() - min_x) \
                % (max_x - min_x)
        new_y = min_y + (self.__ship.get_loc_y() + self.__ship.get_speed_y() - min_y) \
                % (max_y - min_y)
        self.__ship.set_location(new_x, new_y)

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


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
