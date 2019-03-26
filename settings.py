class Settings():
    """"存储《外星人入侵》的所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        """飞船设置"""
        self.ship_limit = 3

        """子弹设置"""
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60,60)
        self.bullet_allowed = 10

        """外星人设置"""
        self.fleet_drop_speed = 50
        self.fleet_direction = 1
        self.initialize_settings()

        """以什么样的速度加快节奏"""
        self.speedup_scale =1.0
        self.score_scale = 1.5

    def initialize_settings(self):
        self.ship_speed_factor = 1.0
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5
        self.alien_point = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_point = int(self.score_scale * self.alien_point)