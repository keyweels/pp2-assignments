import pygame
from datetime import datetime


def crop_transparent(image):
    rect = image.get_bounding_rect()
    return image.subsurface(rect).copy()


def blit_rotate_pivot(screen, image, pivot_world, pivot_image, angle):
    image_rect = image.get_rect(topleft=(pivot_world[0] - pivot_image[0], pivot_world[1] - pivot_image[1]))
    offset_center_to_pivot = pygame.math.Vector2(pivot_world) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(angle)
    rotated_center = (pivot_world[0] - rotated_offset.x, pivot_world[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotozoom(image, -angle, 1)
    rotated_rect = rotated_image.get_rect(center=rotated_center)

    screen.blit(rotated_image, rotated_rect)


class MickeyClock:
    def __init__(self, screen, center, background, right_hand, left_hand):
        self.screen = screen
        self.center = center

        self.background = pygame.transform.smoothscale(background, (700, 700))
        self.bg_rect = self.background.get_rect(center=self.center)

        self.right_hand = crop_transparent(right_hand)
        self.left_hand = crop_transparent(left_hand)

        self.right_hand = pygame.transform.smoothscale(
            self.right_hand,
            (
                max(1, int(self.right_hand.get_width() * 0.55)),
                max(1, int(self.right_hand.get_height() * 0.55))
            )
        )
        self.left_hand = pygame.transform.smoothscale(
            self.left_hand,
            (
                max(1, int(self.left_hand.get_width() * 0.50)),
                max(1, int(self.left_hand.get_height() * 0.50))
            )
        )

        self.pivot_world = (self.center[0], self.center[1] - 8)

        self.right_pivot_image = (self.right_hand.get_width() - 12, self.right_hand.get_height() - 12)
        self.left_pivot_image = (self.left_hand.get_width() // 2, self.left_hand.get_height() - 12)

    def draw(self):
        now = datetime.now()
        minute = now.minute
        second = now.second

        minute_angle = minute * 6
        second_angle = second * 6

        self.screen.blit(self.background, self.bg_rect)

        blit_rotate_pivot(
            self.screen,
            self.right_hand,
            self.pivot_world,
            self.right_pivot_image,
            minute_angle
        )

        blit_rotate_pivot(
            self.screen,
            self.left_hand,
            self.pivot_world,
            self.left_pivot_image,
            second_angle
        )