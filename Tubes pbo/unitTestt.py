import unittest
from unittest.mock import patch
import pygame
import random

def create_pipes():
    screen_width = pygame.display.Info().current_w
    return [(screen_width + i * 300, random.randint(150, 450), False) for i in range(3)]

class TestFlappyClash(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        pygame.mixer.init()
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 36)
        self.bird_x = 50
        self.bird_y = 200
        self.bird_y_change = 0
        self.gravity = 0.6
        self.jump = -10
        self.pipe_width = 70
        self.pipe_gap = 300
        self.pipe_x_change = -6
        self.score = 0
        self.bird_hp = 100
        self.zeus_appeared = False
        self.zeus_x = self.screen_width - 310
        self.zeus_y = -350
        self.zeus_y_change = 3
        self.zeus_hp = 100
        self.zeus_lasers = []
        self.zeus_defeated_count = 0
        self.bullets = []
        self.pipes = [(self.screen_width + i * 300, random.randint(150, 450), False) for i in range(3)]
    
    def test_gravity_effect_on_bird(self):
        initial_y = self.bird_y
        self.bird_y_change += self.gravity
        self.bird_y += self.bird_y_change
        self.assertGreater(self.bird_y, initial_y)
        
    def test_jump_effect_on_bird(self):
        initial_y = self.bird_y
        self.bird_y_change = self.jump
        self.bird_y += self.bird_y_change
        self.assertLess(self.bird_y, initial_y)
        
    def test_create_pipes(self):
        pipes = create_pipes()
        self.assertEqual(len(pipes), 3)
        for pipe_x, pipe_height, passed in pipes:
            self.assertGreaterEqual(pipe_height, 150)
            self.assertLessEqual(pipe_height, 450)
            self.assertFalse(passed)

    def test_update_pipes(self):
        initial_pipe_count = len(self.pipes)
        self.pipes = [(pipe_x + self.pipe_x_change, pipe_height, passed) for pipe_x, pipe_height, passed in self.pipes]
        self.pipes = [pipe for pipe in self.pipes if pipe[0] > -self.pipe_width]
        if self.pipes[-1][0] < self.screen_width - 300:
            self.pipes.append((self.screen_width, random.randint(150, 450), False))
        self.assertEqual(len(self.pipes), initial_pipe_count)
        
    @patch('random.randint', return_value=200)
    def test_update_pipes_add_new_pipe(self, mock_randint):
        self.pipes = [(pipe_x + self.pipe_x_change, pipe_height, passed) for pipe_x, pipe_height, passed in self.pipes]
        self.pipes = [pipe for pipe in self.pipes if pipe[0] > -self.pipe_width]
        self.pipes.append((self.screen_width, 200, False))
        self.assertEqual(self.pipes[-1], (self.screen_width, 200, False))
    
    def test_update_zeus(self):
        initial_zeus_y = self.zeus_y
        self.zeus_y += self.zeus_y_change
        self.assertGreater(self.zeus_y, initial_zeus_y)
        
    def test_bird_collides_with_pipe(self):
        self.bird_y = 200
        self.pipes = [(self.bird_x + 50, 150, False)]
        collided = False
        for pipe_x, pipe_height, passed in self.pipes:
            if (self.bird_x + 50 > pipe_x and self.bird_x < pipe_x + self.pipe_width and 
                (self.bird_y < pipe_height or self.bird_y + 50 > pipe_height + self.pipe_gap)):
                collided = True
        self.assertTrue(collided)
        
    def test_bullet_hits_zeus(self):
        self.zeus_appeared = True
        self.bullets = [[self.zeus_x + 10, self.zeus_y + 10]]
        bullet = self.bullets[0]
        hit = False
        if self.zeus_appeared and bullet[0] > self.zeus_x and bullet[0] < self.zeus_x + 350 and bullet[1] > self.zeus_y and bullet[1] < self.zeus_y + 350:
            self.zeus_hp -= 10
            hit = True
        self.assertTrue(hit)
        self.assertEqual(self.zeus_hp, 90)

if __name__ == '__main__':
    unittest.main()