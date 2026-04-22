import pygame

pygame.mixer.init()

class player:
    def __init__(self,playlist):
        self.playlist=playlist
        self.index=0
        self.playing=False
    def load_music(self):
        pygame.mixer.music.load(self.playlist[self.index])
    def play(self):
        self.load_music()
        pygame.mixer.music.play()
        self.playing=True
    def stop(self):
        pygame.mixer.music.stop()
        self.playing=False
    def next_track(self):
        self.index=(self.index+1)%len(self.playlist)
        self.play()
    def previous_track(self):
        self.index=(self.index-1)%len(self.playlist)
        self.play()
    def status(self):
        return f"Playing: {self.playlist[self.index]}" if self.playing else "Stopped"
    