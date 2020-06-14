class Asteroid:
    """
    DES
    """
    def __init__(self, loc_x, loc_y):
        self.__loc_x = loc_x
        self.__loc_y = loc_y
        self.__speed_x = 0
        self.__speed_y = 0
        self.__size = 3

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

    def has_intersection(self, obj):
        return True