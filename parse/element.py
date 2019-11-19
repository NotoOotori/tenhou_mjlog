from enum import IntEnum

class Element():
    """
        Base class for all elements.
    """
    def __init__(self, element):
        self.tag, self.attrib = element.tag, element.attrib
        self._check_tag()

    def __getattr__(self, name):
        # if name == 'tag':
        #     return type(self).__name__.upper()
        raise AttributeError('Attribute {} not found.'.format(name))

    def _check_tag(self):
        pass
        # if self.tag != 'ELEMENT':
        #     if tag.upper() != self.tag:
        #         raise Exception('Please check the tag.')

    def to_string(self):
        raise NotImplementedError('Subclasses must define to_string method.')

class Shuffle(Element):
    def __init__(self, element):
        super().__init__(element)

    def to_string(self):
        return '{}: {}'.format(self.tag, 'We do not care about the shuffle.')

class Go(Element):
    def __init__(self, element):
        super().__init__(element)

    def to_string(self):
        return '{}: {}'.format(self.tag, 'We do not care about the lobby.')

class Un(Element):
    def __init__(self, element):
        super().__init__(element)

    def to_string(self):
        return '{}: {}'.format(self.tag, 'We do not care about the players.')

class PlayerDraw(IntEnum):
    D = 0
    E = 1
    F = 2
    G = 3

class Tile():
    def __init__(self, number):
        self.number = number

    def to_string(self):
        return '{}{}-{}'.format(
            'mpsz'[self.number // 36],
            (self.number % 36) // 4 + 1,
            (self.number % 36) % 4
        )

class Draw(Element):
    def __init__(self, element):
        super().__init__(element)

    def __getattr__(self, name):
        if name == 'player':
            return PlayerDraw[self.tag[0]]
        if name == 'tile':
            return Tile(int(self.tag[1:])).to_string()
        return super().__getattr__(name)

    def _check_tag(self):
        pass

    def to_string(self):
        return '{}: Player {} draws the tile {}.'.format(self.tag, self.player, self.tile)
