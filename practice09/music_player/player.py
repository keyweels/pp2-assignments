import os
import pygame


class Player:
    def __init__(self, playlist):
        self.playlist = playlist
        self.index = 0
        self.is_playing = False

    def load_current_track(self):
        if not self.playlist:
            raise ValueError("No tracks found")
        track = self.playlist[self.index]
        if not os.path.exists(track):
            raise FileNotFoundError(f"Track not found: {track}")
        pygame.mixer.music.load(track)

    def play(self):
        self.load_current_track()
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.playlist:
            return
        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return
        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No tracks"
        return os.path.basename(self.playlist[self.index])

    def get_position_seconds(self):
        pos = pygame.mixer.music.get_pos()
        if pos < 0:
            return 0
        return pos // 1000