import pygame.font
class Scoreboard():
    """显示得分信息"""
    def __init__(self,ai_settings, screen,stats):
        """初始化得分涉及的属性"""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        """设置显示得分字体"""
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        """初始得分图像"""
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """将得分渲染为图像"""
        score_str = str(self.stats.score)
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        """将得分显示在右上角"""
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """显示得分"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)

    def prep_high_score(self):
        """将最高得分渲染为图像"""
        high_score = self.stats.high_score
        high_score_str = "{:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)

        """将最高得分显示在屏幕中央"""
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
