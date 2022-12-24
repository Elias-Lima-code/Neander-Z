import pygame, datetime

from domain.services import game_controller
from domain.models.rectangle_sprite import Rectangle
from domain.models.enemy import Enemy
from pygame.math import Vector2 as vec
from domain.utils import enums
from domain.models.wave_result import WaveResult
 

class Wave():
    def __init__(self, game, **kwargs):
        self.game = game
        self.enemies_current_id = 0
        self.enemies_group = pygame.sprite.Group()
        self.max_alive_enemies = kwargs.pop("max_alive_enemies", 5)
        self.total_enemies = kwargs.pop("total_enemies", 10)
        self.wave_step = kwargs.pop("wave_step", 1)
        self.current_wave_step = kwargs.pop("current_wave_step", 0)
        self.money_multiplier = kwargs.pop("x2_multiplier", 1.8)
        self.spawn_count = 0
        self.enemies_count = 0
        self.started = False
        self.finished = False

        self.players_scores = {
            1: WaveResult(),
            2: WaveResult(),
        }


    def get_id(self):
        self.enemies_current_id += 1
        return self.enemies_current_id

    def spawn_enemy(self, enemy: Enemy):
        self.enemies_group.add(enemy)
    
        
    def start(self):
        if self.game.client_type == enums.ClientType.SINGLE:
            self.money_multiplier = 1
        self.started = True

    def end_wave(self):
        self.players_scores[1].money = (self.players_scores[1].score / 4) * self.money_multiplier
        self.players_scores[2].money = (self.players_scores[2].score / 4) * self.money_multiplier

        self.game.end_wave(self.players_scores)
        self.finished = True
        
    def kill_all(self):
        for e in self.enemies_group.sprites():
            e.kill(1)

    def handle_score(self, enemy_type: enums.Enemies, attacker):
        if attacker == 3:
            attacker = 1
        match enemy_type:
            case enums.Enemies.Z_ROGER:
                self.players_scores[attacker].score += 53
                # dinheiro dividi por 4    

        self.game.player.score = self.players_scores[1].score 

        if self.game.client_type != enums.ClientType.SINGLE:
            self.game.player2.score = self.players_scores[2].score 



    def update(self, **kwargs):
        if self.finished:
            return
        self.enemies_count = len(self.enemies_group.sprites())
        self.enemies_group.update(group_name = "enemies", game = self.game, client_type = self.game.client_type)
    
       
        # print(self.spawn_count)
    
    def draw(self, screen: pygame.Surface, offset: vec):
        for e in self.enemies_group.sprites():
            e.draw(screen, offset)
        