import numpy as np
import axelrod as axl
from axelrod import ResultSet
import randomname
from typing import List


class SimpleColorAppearance:

    def __init__(self):
        self.color = np.random.randint(0, 255, size=1, dtype=np.ubyte)


class Physics2d:

    def __init__(self, x, y, vehicle):
        self.x = x
        self.y = y
        self.vehicle = vehicle

    def move(self):
        self.vehicle.move()
        self.x = self.vehicle.x
        self.y = self.vehicle.y


class PrisonersDilemmaCompetition:

    def __init__(self, player):
        self.player = player
        self.score = 0


class Creature:

    def __init__(self, physics, appearance, competition, name):
        self.physics = physics
        self.appearance = appearance
        self.competition = competition
        self.name = name


class TheGame:
    def __init__(self, num_creatures: int, w: int, h: int):
        self.num_creatures = num_creatures
        self.w = w
        self.h = h
        self.creatures: List[Creature] = []
        self.__init_creatures()

    def get_state(self):
        matrix = np.zeros((self.w, self.h), dtype=np.ubyte)
        for creature in self.creatures:
            matrix[creature.physics.x, creature.physics.y] = creature.appearance.color
        return matrix

    def __init_creatures(self):
        count = 0
        while count < self.num_creatures:
            count += 1
            vehicle = Vehicle(self.w, self.h, np.random.randint(0, self.w), np.random.randint(0, self.h))
            physics = Physics2d(vehicle.x, vehicle.y, vehicle)
            appearance = SimpleColorAppearance()
            competition = PrisonersDilemmaCompetition(np.random.choice(axl.basic_strategies)())
            creature = Creature(physics, appearance, competition, randomname.get_name())
            self.creatures.append(creature)

    def step_forward(self):
        for creature in self.creatures:
            creature.physics.move()

    def play_tournaments(self):
        tournament_contestants = {}
        num_x_sectors = num_y_sectors = 5

        for creature in self.creatures:
            sector_x = creature.physics.x % num_x_sectors
            sector_y = creature.physics.y % num_y_sectors
            sector_number = sector_y * num_x_sectors + sector_x
            if sector_number not in tournament_contestants.keys():
                tournament_contestants[sector_number] = []
            tournament_contestants[sector_number].append(creature)

        for key, contestants in tournament_contestants.items():
            tournament = axl.Tournament([creature.competition.player for creature in contestants])
            results = tournament.play()
            self.__distribute_scores(results, contestants)

    def __distribute_scores(self, results: ResultSet, contestants: List[Creature]):
        keymap = {}
        for resultKey in range(len(results.players)):
            player_name = results.players[resultKey]
            for key in range(len(contestants)):
                creature = contestants[key]
                if player_name == creature.competition.player.name and key not in keymap.keys():
                    creature.competition.score += sum(results.scores[resultKey])
                    keymap[key] = 1


class Vehicle:
    def __init__(self, w: int, h: int, x: int, y: int):
        self.w = w
        self.h = h
        self.y = y
        self.x = x
        self.vw = np.random.randint(-3, 3)
        self.vh = np.random.randint(-3, 3)

    def move(self):
        self.y = self.y + self.vh
        if self.y < 0:
            self.y = - self.y
            self.vh = -self.vh

        if self.y >= self.h:
            self.y = self.y - 2 * (self.y - self.h + 1)
            self.vh = -self.vh

        self.x = self.x + self.vw
        if self.x < 0:
            self.x = - self.x
            self.vw = -self.vw

        if self.x >= self.w:
            self.x = self.x - 2 * (self.x - self.w + 1)
            self.vw = -self.vw

