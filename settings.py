class Settings():
    def __init__(self):
        """初始化游戏静态设置"""
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (0, 230, 230)
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        #子弹
        self.bullet_speed_factor = 1
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 3

        self.alien_speed_factor = 1
        self.fleet_drop_speed = 5
        #1为向右,-1向左
        self.fleet_direction = 1

        #记分
        self.alien_points = 1
        #游戏节奏的加速度
        self.speed_scale = 1.1
        """提高一个外星人的分数"""
        self.score_scale = 1.5
        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        """初始化各个因素的速度"""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度"""
        self.ship_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.alien_speed_factor *= self.speed_scale
        self.alien_points = int(self.alien_points * self.score_scale)