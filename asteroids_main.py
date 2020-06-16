import asteroid
from screen import Screen
import sys

from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import randint
import math

DEFAULT_ASTEROIDS_NUM = 5
DEFAULT_TORPEDOS_NUM = 10
SIZE_ASTEROIDS = 3
RIGHT = "right"
LEFT = "left"
LOST_LIFE_MSG = "You have lost a life."
LOST_LIFE_TITLE = "Lost life."
MIN_ASTEROID_SPEED = 1
MAX_ASTEROID_SPEED = 4


def calc_speed_of_tor_from_obj(obj, alpha):
    obj_speed_x = obj.get_speed_x() + \
                  math.cos(math.radians(obj.get_direction())) * alpha
    obj_speed_y = obj.get_speed_y() + \
                  math.sin(math.radians(obj.get_direction())) * alpha
    return obj_speed_x, obj_speed_y


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
        self.__torpedos_lst = []
        self.__score = 0

    def run(self):
        self.__generate_asteroids()

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
        self.__all_obj_updates()
        self.__check_intersections()

    def __all_obj_updates(self):
        self.__update_ship_location()
        self.__update_ship_speed()
        self.__update_ship_direction()
        self.__update_asteroid_location()
        self.__update_torpedo_location()
        self.__shoot_torpedo()

    def __draw_all(self, __asteroid=None):
        self.__screen.draw_ship(self.__ship.get_loc_x(),
                                self.__ship.get_loc_y(),
                                self.__ship.get_direction())
        for ast in self.__asteroids_lst:
            self.__screen.draw_asteroid(ast,
                                        ast.get_loc_x(),
                                        ast.get_loc_y())
        torp_to_remove = []
        for i in range(len(self.__torpedos_lst)):
            torp = self.__torpedos_lst[i]
            time_alive = torp.get_time_alive()
            if time_alive < 200:
                torp.set_time_alive(time_alive + 1)
                self.__screen.draw_torpedo(torp, torp.get_loc_x(),
                                           torp.get_loc_y(),
                                           torp.get_direction())
            else:
                torp_to_remove.append(torp)

        for torp in torp_to_remove:
            self.__screen.unregister_torpedo(torp)
            self.__torpedos_lst.remove(torp)


    def __update_ship_direction(self):
        direction = self.__ship.get_direction()
        if self.__screen.is_right_pressed():
            direction -= 7
        elif self.__screen.is_left_pressed():
            direction += 7
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

        new_x = min_x + ((obj.get_loc_x() + obj.get_speed_x() - min_x) % (max_x - min_x))
        new_y = min_y + ((obj.get_loc_y() + obj.get_speed_y() - min_y) % (max_y - min_y))
        return new_x, new_y


    def __update_ship_speed(self):
        while self.__screen.is_up_pressed():
            new_speed_x, new_speed_y = calc_speed_of_tor_from_obj(self.__ship, 1)  # ship is 1
            self.__ship.set_speed(new_speed_x, new_speed_y)


    def __solve_torpedoes_intersections(self):
        length = len(self.__torpedos_lst)
        torp_to_remove = []
        ast_to_remove = set()
        for i in range(length):
            torp = self.__torpedos_lst[i]
            asteroid_intersected = self.__get_intersected_astroid(torp)
            if self.__get_intersected_astroid(torp) is not None:
                self.__generate_baby_asteroids(asteroid_intersected, torp)
                torp_to_remove.append(self.__torpedos_lst[i])
                ast_to_remove.add(asteroid_intersected)
        for torp in torp_to_remove:
            self.__screen.unregister_torpedo(torp)
            self.__torpedos_lst.remove(torp)

        for ast in ast_to_remove:
            self.__screen.unregister_asteroid(ast)
            self.__asteroids_lst.remove(ast)


    def __get_intersected_astroid(self, obj):
        length = len(self.__asteroids_lst)
        for i in range(length):
            ast = self.__asteroids_lst[i]
            if ast.has_intersection(obj):
                return ast


    def __solve_ship_intersections(self):
        asteroid_intersected = self.__get_intersected_astroid(self.__ship)
        if asteroid_intersected is not None:
            self.__screen.unregister_asteroid(asteroid_intersected)
            self.__asteroids_lst.remove(asteroid_intersected)
            self.__screen.show_message(LOST_LIFE_TITLE, LOST_LIFE_MSG)
            self.__screen.remove_life()


    def __check_intersections(self):
        self.__solve_ship_intersections()
        self.__solve_torpedoes_intersections()


#########################################################################
    # part 3
    def __generate_asteroids(self):
        for i in range(DEFAULT_ASTEROIDS_NUM):
            # TODO: edit asteroid speeds
            now_asteroid = Asteroid(randint(self.__screen_min_x, self.__screen_max_x),
                                    randint(self.__screen_min_y, self.__screen_max_y),
                                    randint(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED),
                                    randint(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED))
            if not now_asteroid.has_intersection(self.__ship):
                self.__asteroids_lst.append(now_asteroid)
                self.__screen.register_asteroid(now_asteroid, SIZE_ASTEROIDS)


    def __calc_baby_ast_speed(self, ast, torp):
        torp_speed_x, torp_speed_y = torp.get_speed_x(), torp.get_speed_y()
        ast_speed_x, ast_speed_y = ast.get_speed_x(), ast.get_speed_y()
        new_speed_x = (torp_speed_x + ast_speed_x) \
                      / math.sqrt(ast_speed_x ** 2 + ast_speed_y ** 2)
        new_speed_y = -(torp_speed_y + ast_speed_y) \
                      / math.sqrt(ast_speed_x ** 2 + ast_speed_y ** 2)
        return new_speed_x, new_speed_y


    def __generate_baby_asteroids(self, ast, torp):
        size = ast.get_size()
        x, y = ast.get_loc_x(), ast.get_loc_y()
        new_speeds = self.__calc_baby_ast_speed(ast, torp)
        baby_speed_x, baby_speed_y = new_speeds[0], new_speeds[1]
        if size != 1:
            if size == 3:
                baby_size = 2
            elif size == 2:
                baby_size = 1
            baby_asteroid_1 = Asteroid(x, y, baby_speed_x, baby_speed_y)
            baby_asteroid_2 = Asteroid(x, y, -baby_speed_x, -baby_speed_y)
            self.__asteroids_lst.append(baby_asteroid_1)
            self.__asteroids_lst.append(baby_asteroid_2)
            self.__screen.register_asteroid(baby_asteroid_1, baby_size)
            self.__screen.register_asteroid(baby_asteroid_2, baby_size)


    #########################################################################
    # part 4

    def __shoot_torpedo(self):
        if len(self.__torpedos_lst) < DEFAULT_TORPEDOS_NUM:
            if self.__screen.is_space_pressed():
                tor_speed_x, tor_speed_y = calc_speed_of_tor_from_obj(self.__ship, 2)
                torpedo = Torpedo(self.__ship.get_loc_x(), self.__ship.get_loc_y(), tor_speed_x, tor_speed_y,
                                  self.__ship.get_direction())
                self.__torpedos_lst.append(torpedo)
                self.__screen.register_torpedo(torpedo)


    def __update_torpedo_location(self):
        for tor in self.__torpedos_lst:
            new_x, new_y = self.__calc_new_location(tor)
            print("new x", new_x, "new_y", new_y)
            tor.set_location(new_x, new_y)


    def __add_score(self, asteroid_size):
        if asteroid_size == 3:
            self.__score += 20
        elif asteroid_size == 2:
            self.__score += 50
        elif asteroid_size == 3:
            self.__score += 100
        self.__screen.set_score(self.__score)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
