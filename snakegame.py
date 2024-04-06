import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

BLOCK_SIZE = 20
SPEED = 10


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.eat_sound = pygame.mixer.Sound("gooble.mp3")
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.apple_image = pygame.image.load('apple.jpg')
        self.apple_image = pygame.transform.scale(self.apple_image, (BLOCK_SIZE, BLOCK_SIZE))
        self.lives = 3
        self.cumulative_score = 0
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (self.w, self.h))
        self.arrow_images = {
            pygame.K_LEFT: pygame.transform.scale(pygame.image.load('left_arrow.png'), (60, 60)),
            pygame.K_RIGHT: pygame.transform.scale(pygame.image.load('right_arrow.png'), (60, 60)),
            pygame.K_UP: pygame.transform.scale(pygame.image.load('up_arrow.png'), (60, 60)),
            pygame.K_DOWN: pygame.transform.scale(pygame.image.load('down_arrow.png'), (60, 60))
        }
        self.key_positions = {
            pygame.K_LEFT: (self.w - 210, self.h - 110),
            pygame.K_RIGHT: (self.w - 120, self.h - 110),
            pygame.K_UP: (self.w - 165, self.h - 165),
            pygame.K_DOWN: (self.w - 165, self.h - 55)
        }
        self.start_time = pygame.time.get_ticks()
        self.blink_timer = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
        self._move(self.direction)
        self.snake.insert(0, self.head)
        game_over = False
        if self._is_collision():
            self.lives -= 1
            self.cumulative_score += self.score
            if (self.lives == 0):
                game_over = True
                return game_over, self.cumulative_score
            else:
                self.direction = Direction.RIGHT
                self.head = Point(self.w / 2, self.h / 2)
                self.snake = [self.head,
                              Point(self.head.x - BLOCK_SIZE, self.head.y),
                              Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
                self.score = 0
                self._place_food()
                self.start_time = pygame.time.get_ticks()
                return False, self.cumulative_score
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self.eat_sound.play(maxtime=1000, fade_ms=100)
        else:
            self.snake.pop()
        self._update_ui()
        self.clock.tick(SPEED)
        return game_over, self.score



    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        return False



    def _update_ui(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.apple_image, (self.food.x, self.food.y))
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, WHITE, (0, 0, self.w, 100))
        lives_text = font.render("Lives: " + str(self.lives), True, BLACK)
        cumulative_score_text = font.render("Cumulative Score: " + str(self.cumulative_score), True, BLACK)
        score_text = font.render("Score: " + str(self.score), True, BLACK)
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000
        timer_text = font.render("Time: " + str(elapsed_time) + "s", True, BLACK)
        self.display.blit(lives_text, [10, 10])
        self.display.blit(cumulative_score_text, [10, 40])
        self.display.blit(score_text, [10, 70])
        self.display.blit(timer_text, [self.w-100, 10])
        keys = pygame.key.get_pressed()
        for key in self.arrow_images:
            if keys[key]:
                self.blink_timer += 1
                if (self.blink_timer % 20) < 10:
                    pygame.draw.rect(self.display, YELLOW,
                                     (self.key_positions[key][0] - 5, self.key_positions[key][1] - 5, 70, 70), 3)
                self.display.blit(self.arrow_images[key], self.key_positions[key])

        pygame.display.flip()



    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)




if __name__ == '__main__':
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
