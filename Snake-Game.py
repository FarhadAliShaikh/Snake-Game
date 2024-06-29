# Add background image and music

import pygame
from pygame.locals import *
import time
import random

SIZE = 40


class Apple:
    def __init__(self, paren_screen):
        self.parent_screen = paren_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 14) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = "right"

        self.length = 1
        self.block_x = [SIZE]
        self.block_y = [SIZE]

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.block_x[i] = self.block_x[i - 1]
            self.block_y[i] = self.block_y[i - 1]

        if self.direction == "left":
            self.block_x[0] -= SIZE

        if self.direction == "right":
            self.block_x[0] += SIZE

        if self.direction == "up":
            self.block_y[0] -= SIZE

        if self.direction == "down":
            self.block_y[0] += SIZE

        self.draw()

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()

        self.screen = pygame.display.set_mode((1000, 600))
        self.snake = Snake(self.screen)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.screen.blit(score, (850, 10))

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "ding":
            sound = pygame.mixer.Sound("resources/ding.mp3")
        elif sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.screen.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i],
                                 self.snake.block_y[i]):
                self.play_sound("crash")
                raise "Collision Occured"

        # snake hit walls
        if not (0 <= self.snake.block_x[0] <= 1000 and 0 <= self.snake.block_y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.screen.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.screen.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def restart_game(self):
        self.snake = Snake(self.screen)
        self.apple = Apple(self.screen)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.restart_game()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
