class GameStates():
    """跟踪游戏的统计信息"""
    def __init__(self, ai_setttings):
        """初始化统计信息"""
        self.ai_settings = ai_setttings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
