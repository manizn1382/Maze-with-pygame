import string

import self as self


class Cell_status:
    def __init__(self, flags: string):
        self.right, self.left, self.up, self.down, self.teleport, self.portal, self.mist = int(flags[0]), int(flags[1]), int(flags[2]), int(flags[3]), int(flags[4]), int(flags[5]), int(flags[6])
        self.leftPuzzle = False
        self.rightPuzzle = False
        self.upPuzzle = False
        self.downPuzzle = False
