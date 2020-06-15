class Torpedo:
    """
    def
    """

    def __init__(self, loc_x, loc_y,speed_x, speed_y, direction):
        self.__loc_x = loc_x
        self.__loc_y = loc_y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__direction = direction

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

    def get_direction(self):
        return self.__direction

    def set_direction(self, new_direction):
        self.__direction = new_direction