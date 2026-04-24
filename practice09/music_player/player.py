import pygame
import os


class Music:
    def __init__(self):
        self.playlist = [
            "music/Caliente.mp3",
            "music/Planovaia.mp3"
        ]
        self.current_track = 0
        pygame.mixer.music.load(self.playlist[self.current_track])

    def play(self):
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.current_track += 1

        if self.current_track >= len(self.playlist):
            self.current_track = 0

        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play()

    def back(self):
        self.current_track -= 1

        if self.current_track < 0:
            self.current_track = len(self.playlist) - 1

        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play()

    def get_current_track_name(self):
        return os.path.basename(self.playlist[self.current_track])