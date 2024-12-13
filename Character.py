import pygame
import self

from config import yellow_cost, red_cost, black_cost, player_score, left_side_arrow


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.player_x = x
        self.player_y = y
        self.score = player_score
        self.won = False
        self.mist_cell = False
        self.mist_track = 0
        self.out_mist = 0

    def __getitem__(self):
        return self.player_x, self.player_y

    def up_handler(self, up_cs):

        if up_cs.track == 0:
            self.player_x -= 1
            up_cs.track += 1
            self.score -= black_cost
        elif up_cs.track == 1:
            self.player_x -= 1
            up_cs.track += 1
            self.score -= yellow_cost
        elif up_cs.track == 2:
            self.player_x -= 1
            up_cs.track += 1
            self.score -= red_cost

    def down_handler(self, down_cs):

        if down_cs.track == 0:
            self.player_x += 1
            down_cs.track += 1
            self.score -= black_cost
        elif down_cs.track == 1:
            self.player_x += 1
            down_cs.track += 1
            self.score -= yellow_cost
        elif down_cs.track == 2:
            self.player_x += 1
            down_cs.track += 1
            self.score -= red_cost

    def left_handler(self, left_cs):

        if left_cs.track == 0:
            self.player_y -= 1
            left_cs.track += 1
            self.score -= black_cost
        elif left_cs.track == 1:
            self.player_y -= 1
            left_cs.track += 1
            self.score -= yellow_cost
        elif left_cs.track == 2:
            self.player_y -= 1
            left_cs.track += 1
            self.score -= red_cost

    def right_handler(self, right_cs):

        if right_cs.track == 0:
            self.player_y += 1
            right_cs.track += 1
            self.score -= black_cost
        elif right_cs.track == 1:
            self.player_y += 1
            right_cs.track += 1
            self.score -= yellow_cost
        elif right_cs.track == 2:
            self.player_y += 1
            right_cs.track += 1
            self.score -= red_cost

    def teleport_check(self, key):
        if self.player_x == 1 and self.player_y == 7 and key[pygame.K_UP]:
            # place player in downside teleport
            self.player_x = 9
            self.player_y = 2
            return True
        if self.player_x == 9 and self.player_y == 2 and key[pygame.K_DOWN]:  # downside_teleport_position
            # place player in upside teleport
            self.player_x = 1
            self.player_y = 7
            return True
        return False

    def move(self, key, maze_status):

        cs = maze_status[self.player_x][self.player_y]

        if key[pygame.K_RETURN]:
            if self.player_x == 6 and self.player_y == 7:
                self.player_x = 1
                self.player_y = 4
            elif self.player_x == 1 and self.player_y == 4:
                self.player_x = 6
                self.player_y = 7

        elif key[pygame.K_UP]:
            res = self.teleport_check(key)
            if not res:
                up_cs = maze_status[self.player_x - 1][self.player_y] if self.player_x - 1 >= 0 else None
                if up_cs:
                    if up_cs.downPuzzle == 1 or cs.upPuzzle == 1:
                        pass  # Update logic for puzzles here

                    if up_cs.down == 1 or cs.up == 1:
                        pass
                    elif cs.mist != 1:
                        if up_cs.mist != 1:
                            self.up_handler(up_cs)
                        elif up_cs.mist == 1:
                            self.out_mist = (self.player_x, self.player_y)
                            self.score -= black_cost
                            self.player_x -= 1
                            self.mist_cell = True
                    elif cs.mist == 1:
                        if up_cs.mist != 1:
                            self.player_x -= 1
                            self.mist_cell = False
                            self.mist_track = 0
                        elif up_cs.mist == 1:
                            self.player_x -= 1
                            self.mist_track += 1
                            if self.mist_track >= 2 and not (self.player_x == 6 and self.player_y == 7):
                                self.player_x, self.player_y = self.out_mist[0], self.out_mist[1]
                                self.mist_track = 0
                                self.mist_cell = False

        elif key[pygame.K_DOWN]:
            res = self.teleport_check(key)

            if not res:
                down_cs = maze_status[self.player_x + 1][self.player_y] if self.player_x + 1 < len(
                    maze_status) else None
                if down_cs:
                    if down_cs.upPuzzle == 1 or cs.downPuzzle == 1:
                        pass  # Update logic for puzzles here

                    if down_cs.up == 1 or cs.down == 1:
                        pass
                    elif cs.mist != 1:
                        if down_cs.mist != 1:
                            self.down_handler(down_cs)
                        elif down_cs.mist == 1:
                            self.out_mist = (self.player_x, self.player_y)
                            self.score -= black_cost
                            self.player_x += 1
                            self.mist_cell = True
                    elif cs.mist == 1:
                        if down_cs.mist != 1:
                            self.player_x += 1
                            self.mist_cell = False
                            self.mist_track = 0
                        elif down_cs.mist == 1:
                            self.player_x += 1
                            self.mist_track += 1
                            if self.mist_track >= 2 and not (self.player_x == 6 and self.player_y == 7):
                                self.player_x, self.player_y = self.out_mist[0], self.out_mist[1]
                                self.mist_track = 0
                                self.mist_cell = False

        elif key[pygame.K_LEFT]:
            if self.player_x == left_side_arrow[0] and self.player_y == left_side_arrow[1] + 1:  # bound-check
                pass
            else:
                left_cs = maze_status[self.player_x][self.player_y - 1] if self.player_y - 1 >= 0 else None
                if left_cs:
                    if left_cs.rightPuzzle == 1 or cs.leftPuzzle == 1:
                        pass  # Update logic for puzzles here

                    if left_cs.right == 1 or cs.left == 1:
                        pass
                    elif cs.mist != 1:
                        if left_cs.mist != 1:
                            self.left_handler(left_cs)
                        elif left_cs.mist == 1:
                            self.out_mist = (self.player_x, self.player_y)
                            self.score -= black_cost
                            self.player_y -= 1
                            self.mist_cell = True
                    elif cs.mist == 1:
                        if left_cs.mist != 1:
                            self.player_y -= 1
                            self.mist_cell = False
                            self.mist_track = 0
                        elif left_cs.mist == 1:
                            self.player_y -= 1
                            self.mist_track += 1
                            if self.mist_track >= 2 and not (self.player_x == 6 and self.player_y == 7):
                                self.player_x, self.player_y = self.out_mist[0], self.out_mist[1]
                                self.mist_track = 0
                                self.mist_cell = False

        elif key[pygame.K_RIGHT]:
            right_cs = maze_status[self.player_x][self.player_y + 1] if self.player_y + 1 < len(
                maze_status[0]) else None
            if right_cs:
                if right_cs.leftPuzzle == 1 or cs.rightPuzzle == 1:
                    pass  # Update logic for puzzles here

                if right_cs.left == 1 or cs.right == 1:
                    pass
                elif cs.mist != 1:
                    if right_cs.mist != 1:
                        self.right_handler(right_cs)
                    elif right_cs.mist == 1:
                        self.out_mist = (self.player_x, self.player_y)
                        self.score -= black_cost
                        self.player_y += 1
                        self.mist_cell = True
                elif cs.mist == 1:
                    if right_cs.mist != 1:
                        self.player_y += 1
                        self.mist_cell = False
                        self.mist_track = 0
                    elif right_cs.mist == 1:
                        self.player_y += 1
                        self.mist_track += 1
                        if self.mist_track >= 2 and not (self.player_x == 6 and self.player_y == 7):
                            self.player_x, self.player_y = self.out_mist[0], self.out_mist[1]
                            self.mist_track = 0
                            self.mist_cell = False
