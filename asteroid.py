import math


class Asteroid:
    """
    DES
    """
    def __init__(self, loc_x, loc_y, speed_x, speed_y):
        self.__loc_x = loc_x
        self.__loc_y = loc_y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__size = 3
        self.__radius = self.__size * 10

    def get_loc_x(self):
        return self.__loc_x

    def get_loc_y(self):
        return self.__loc_y

    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y

    def set_location(self, loc_x, loc_y):
        self.__loc_x = loc_x
        self.__loc_y = loc_y

    def draw(self, screen):
        screen.update()

    def set_speed(self, speed_x, speed_y):
        self.__speed_x = speed_x
        self.__speed_y = speed_y

    def get_radius(self):
        return self.__radius

    def has_intersection(self, obj):
        print("obj x", obj.get_loc_x())
        print("obj y", obj.get_loc_y())
        print("self x", self.__loc_x)
        print("self y", self.__loc_y)
        print(type(obj))
        d1 = obj.get_loc_x() - self.__loc_x
        d2 = obj.get_loc_y() - self.__loc_y
        distance = math.sqrt(d1 ** 2 + d2 ** 2)
        if distance <= self.__radius + obj.get_radius():
            return True
        else:
            return False

    def get_size(self):
        return self.__size
