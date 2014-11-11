#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementation fabric and abstract fabric design pattern
and test OOP opportunities of language
"""

from abc import ABCMeta, abstractmethod


class Race(object):
    """docstring for Race"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def buff():
        pass


class Human(Race):
    """docstring for Human"""

    def __init__(self):
        super(Human, self).__init__()
        self.hp = 50
        self.int = 9
        self.str = 6
        self.agi = 5

    def buff(self):
        self.int += int(self.int * 0.16)


class Orc(Race):
    """docstring for Orc"""

    def __init__(self):
        super(Orc, self).__init__()
        self.hp = 70
        self.int = 3
        self.str = 9
        self.agi = 8

    def buff(self):
        self.str += int(self.str * 0.16)


class Elf(Race):
    """docstring for Elf"""

    def __init__(self):
        super(Elf, self).__init__()
        self.hp = 30
        self.int = 8
        self.str = 3
        self.agi = 9

    def buff(self):
        self.agi += int(self.agi * 0.08)
        self.int += int(self.int * 0.08)


class Hero(object):
    """docstring for Hero"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def name(self):
        pass

    def show(self):
        return "class:%s, hp:%d, int:%d, str:%d, agi:%d, ad:%d, md:%d" % \
            (self.name(), self.hp, self.int, self.str, self.agi, self.ad, self.md)


class Warrior(Hero):
    """docstring for Warrior"""

    def __init__(self):
        super(Warrior, self).__init__()

    def blink(self):
        self.hp += 20
        return 30


class Paladin(Warrior, Human):
    """docstring for Paladin"""
    def __init__(self):
        super(Paladin, self).__init__()
        self.hp += int(self.hp * 0.3)
        self.ad = int(self.str * 1.5)
        self.md = int(self.int * 0.5)

    def attack(self):
        return int((self.ad + self.md) * 0.7)

    def holy_light(self):
        self.hp += int(self.hp * 0.5)

    def name(self):
        return "Paladin"


class Berserker(Warrior, Orc):
    """docstring for Berserker"""

    def __init__(self):
        super(Berserker, self).__init__()
        self.hp += int(self.hp * 0.2)
        self.ad = int(self.str * 2.0)
        self.md = 0

    def attack(self):
        return int(self.ad * 1.2)

    def rage(self):
        self.hp -= int(self.hp * 0.2)
        self.ad += int(self.ad * 0.5)

    def name(self):
        return "Berserker"


class Rogue(Warrior, Elf):
    """docstring for Rogue"""

    def __init__(self):
        super(Rogue, self).__init__()
        self.hp += int(self.hp * 0.1)
        self.ad = int(self.str * 3.0)
        self.md = int(self.int * 0.5)

    def attack(self):
        return int((self.ad * 1) / (self.hp * 0.1)) + self.md * 2

    def shadow(self):
        self.ad += int(self.ad * 0.3)
        self.md += int(self.ad * 0.5)

    def name(self):
        return "Rogue"


class WarriorFabric(object):
    """docstring for WarriorFabric"""

    @staticmethod
    def get_instance(race):
        return {Human.__name__: Paladin(),
                Orc.__name__: Berserker(),
                Elf.__name__: Rogue()}[race]


class AbstractSide(object):
    """docstring for AbstractSquad"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def side_buff(self):
        pass


class Alliance(AbstractSide):
    """docstring for Alliance"""

    def __init__(self):
        super(Alliance, self).__init__()

    def side_buff(self, hero):
        hero.md += int(hero.md * 0.05)
        hero.hp += int(hero.md * 0.30)
        return hero


class Horde(AbstractSide):
    """docstring for Alliance"""

    def __init__(self):
        super(Horde, self).__init__()

    def side_buff(self, hero):
        hero.ad += int(hero.md * 0.10)
        hero.hp += int(hero.md * 0.20)
        return hero


class AbstractSquad(object):
    """docstring for AbstractSquad"""

    __metaclass__ = ABCMeta

    def __init__(self, fabric):
        super(AbstractSquad, self).__init__()
        self.party = []
        self.fabric = fabric

    @abstractmethod
    def create_squad(self, side):
        pass

    def prepare(self):
        for hero in self.party:
            hero = self.side_buff(hero)
            hero.buff()
        return self.party


class AllianceSquad(AbstractSquad, Alliance):
    """docstring for AllianceSquad"""

    def __init__(self, fabric):
        super(AllianceSquad, self).__init__(fabric)

    def create_squad(self):
        self.party.append(self.fabric.get_instance(Human.__name__))
        self.party.append(self.fabric.get_instance(Human.__name__))
        self.party.append(self.fabric.get_instance(Elf.__name__))
        return self.prepare()


class HordeSquad(AbstractSquad, Horde):
    """docstring for AllianceSquad"""

    def __init__(self, fabric):
        super(HordeSquad, self).__init__(fabric)

    def create_squad(self):
        self.party.append(self.fabric.get_instance(Orc.__name__))
        self.party.append(self.fabric.get_instance(Orc.__name__))
        self.party.append(self.fabric.get_instance(Elf.__name__))
        return self.prepare()


###========================================================================
###========================================================================
###========================================================================


if __name__ == "__main__":
    horde = HordeSquad(WarriorFabric)
    hordeParty = horde.create_squad()
    alliance = AllianceSquad(WarriorFabric)
    allyParty = alliance.create_squad()

    for hero in hordeParty:
        print hero.show()

    for hero in allyParty:
        print hero.show()
