class NodeData:

    def __init__(self, key, pos=(0, 0)):
        self.__key = key
        self.__pos = pos
        self.__info = "W"
        self.__tag = -1
        self.__weight = 0

    def get_key(self):
        return self.__key

    def get_pos(self):
        return self.__pos

    def get_info(self):
        return self.__info

    def get_tag(self):
        return self.__tag

    def set_tag(self, t):
        self.__tag = t

    def set_info(self, i):
        self.__info = i

    def get_weight(self):
        return self.__weight

    def set_weight(self, t):
        self.__weight = t

    def __repr__(self):
        ans = f'{self.get_key()}'  # to add more information
        return ans

    def __lt__(self, other):
        return self.get_weight() < other.get_weight()
