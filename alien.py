import pygame
from pygame.sprite import Sprite


class Alien(Sprite):


    def __init__(self,ai_settings, screen):
        #初始化外星人及起始位置
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        #初始位置在左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #准确位置
        self.x = float(self.rect.x)

    def blime(self):

        self.screen.bilt(self.image, self.rect)

    def check_edgs(self):#查看是不是走到了屏幕边缘，决定转向
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        #右移
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x