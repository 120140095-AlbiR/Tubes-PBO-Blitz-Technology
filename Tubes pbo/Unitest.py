import unittest
from unittest.mock import patch, Mock
import pygame


pygame.init = Mock()
pygame.display = Mock()
pygame.font = Mock()
pygame.mixer = Mock()


import FlapyClash  

class TestFlappyClash(unittest.TestCase):
    def setUp(self):
        # Persiapan yang dibutuhkan sebelum setiap test
        FlapyClash.screen_width = 800
        FlapyClash.screen_height = 600
        FlapyClash.bird_x = 50
        FlapyClash.bird_y = 300
        FlapyClash.bird_y_change = 0
        FlapyClash.gravity = 0.6
        FlapyClash.jump = -10
        FlapyClash.pipe_width = 70
        FlapyClash.pipe_gap = 250
        FlapyClash.pipe_x_change = -6
        FlapyClash.bird_hp = 100
        FlapyClash.zeus_hp = 100
        FlapyClash.zeus_appeared = False
        FlapyClash.zeus_appearance_scores = [10, 60, 120, 180]
        FlapyClash.score = 0
        FlapyClash.pipes = [(FlapyClash.screen_width, 300, False)]
        FlapyClash.bullets = []

    def test_create_pipes(self):
        pipes = FlapyClash.create_pipes()
        self.assertEqual(len(pipes), 3)
        for pipe in pipes:
            self.assertTrue(150 <= pipe[1] <= 450)
            self.assertEqual(pipe[2], False)

    def test_update_bird(self):
        FlapyClash.bird_y = 10
        FlapyClash.bird_y_change = 0
        FlapyClash.update_bird()
        self.assertGreater(FlapyClash.bird_y, 10)
        FlapyClash.bird_y = FlapyClash.screen_height - 1
        FlapyClash.update_bird()
        self.assertFalse(FlapyClash.running)

    def test_update_pipes(self):
        initial_score = FlapyClash.score
        FlapyClash.pipes = [(FlapyClash.bird_x + 100, 300, False)]
        FlapyClash.update_pipes()
        self.assertEqual(FlapyClash.score, initial_score + 1)

    def test_update_zeus_appearance(self):
        FlapyClash.score = 10
        FlapyClash.update_zeus()
        self.assertTrue(FlapyClash.zeus_appeared)

    def test_update_bullets(self):
        FlapyClash.bullets = [[FlapyClash.bird_x + 10, FlapyClash.bird_y + 25]]
        FlapyClash.zeus_appeared = True
        FlapyClash.zeus_x = FlapyClash.bird_x + 20
        FlapyClash.zeus_y = FlapyClash.bird_y
        FlapyClash.update_bullets()
        self.assertEqual(FlapyClash.zeus_hp, 90)

if __name__ == '__main__':
    unittest.main()
