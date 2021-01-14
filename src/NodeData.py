class NodeData:

    def __init__(self, key, pos: tuple = None):
        """
        initialize the node.
        :param key: int
            The id of the node
        :param pos: tuple
            The position of the node, three coordinates are required.
        """
        self.__key = key
        self.__pos = pos
        self.__info = "W"
        self.__tag = -1
        self.__weight = 0

    def get_key(self):
        """
        :return:
        int
            The node key value.
        """
        return self.__key

    def get_pos(self):
        """
        :return:
        tuple
            The position of the node.
        """
        return self.__pos

    def set_pos(self, p: tuple):
        self.__pos = p

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
        """ set the weight of the node
        Parameters
        ----------
        t : float
            the weight
        """
        self.__weight = t

    def __repr__(self):
        ans = f'{self.get_key()}'
        return ans

    def __lt__(self, other):
        return self.get_weight() < other.get_weight()
