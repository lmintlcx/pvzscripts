# coding=utf-8

from pvz import ReadMemory
from pvz.core import seeds_string
from pvz.core import zombies_string

sun = ReadMemory("int", 0x6A9EC0, 0x768, 0x5560)
print("当前阳光数: " + str(sun))

zombies_count_max = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x94)
zombies_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x90)
for i in range(zombies_count_max):
    zombie_dead = ReadMemory("bool", zombies_offset + 0xec + i * 0x15c)
    if not zombie_dead:
        zombie_type = ReadMemory("int", zombies_offset + 0x24 + i * 0x15c)
        zombie_row = ReadMemory("int", zombies_offset + 0x1c + i * 0x15c)
        zombie_x = ReadMemory("int", zombies_offset + 0x8 + i * 0x15c)
        zombie_hp = ReadMemory("int", zombies_offset + 0xc8 + i * 0x15c)
        print("%s僵尸 位于 %d 路 横坐标 %d 本体血量 %d"
              % (zombies_string[zombie_type][1], zombie_row + 1, zombie_x, zombie_hp))

plants_count_max = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
plants_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
for i in range(plants_count_max):
    plant_dead = ReadMemory("bool", plants_offset + 0x141 + i * 0x14c)
    plant_squished = ReadMemory("bool", plants_offset + 0x142 + i * 0x14c)
    if not plant_dead and not plant_squished:
        plant_type = ReadMemory("int", plants_offset + 0x24 + i * 0x14c)
        plant_row = ReadMemory("int", plants_offset + 0x1c + i * 0x14c)
        plant_col = ReadMemory("int", plants_offset + 0x28 + i * 0x14c)
        plant_hp = ReadMemory("int", plants_offset + 0x40 + i * 0x14c)
        plant_hp_max = ReadMemory("int", plants_offset + 0x44 + i * 0x14c)
        print("植物序号 %d 位于 %d 路 %d 列 血量 %d/%d 类型 %s"
              % (i, plant_row + 1, plant_col + 1, plant_hp, plant_hp_max, seeds_string[plant_type][1]))
