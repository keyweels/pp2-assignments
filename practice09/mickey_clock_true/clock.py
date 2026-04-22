import pygame
import math
from datetime import datetime


class MickeyClock:
    def __init__(self, screen, center, background_path, minute_hand_path, second_hand_path):
        self.screen = screen
        self.center = center

        self.background = pygame.image.load(background_path).convert_alpha()
        self.minute_hand = pygame.image.load(minute_hand_path).convert_alpha()
        self.second_hand = pygame.image.load(second_hand_path).convert_alpha()

        self.background_rect = self.background.get_rect(center=self.center)

    def get_time(self):
        now = datetime.now()
        return now.minute, now.second

    def rotate_hand(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=self.center)
        return rotated_image, rotated_rect

    def draw(self):
        minute, second = self.get_time()

        minute_angle = -minute * 6
        second_angle = -second * 6

        minute_rotated, minute_rect = self.rotate_hand(self.minute_hand, minute_angle)
        second_rotated, second_rect = self.rotate_hand(self.second_hand, second_angle)

        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(minute_rotated, minute_rect)
        self.screen.blit(second_rotated, second_rect)