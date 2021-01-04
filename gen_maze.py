from Spawners.NonEquippableMob import NonEquippableMob
from Spawners.EquippableMob import EquippableMob
from Spawners.Spawner import Spawner
from Chestitems.TippedArrow import TippedArrow
from Chestitems.Shield import Shield
from Chestitems.Bow import Bow
from Chestitems.Potion import Potion
from Chestitems.Consumable import Consumable
from Chestitems.Armor import Armor
from Chestitems.Weapon import Weapon
from random import shuffle, randrange, random, choices, randint, sample
import argparse
import json

import sys
import os
sys.path.append('/Chestitems')
sys.path.append('/Spawners')


def generate_chest():
    num_items = randint(1, 24)
    selected = []
    options = [Weapon, Armor, Consumable, Potion, Bow, Shield, TippedArrow]
    for i in range(num_items):
        o = sample(options, 1)[0]()
        if random() < 0.2 or type(o) == Potion:
            o.enchant()
        selected.append(o.generate_item_string(i))
    slots = sample([i for i in range(24)], num_items)
    for item, slot in zip(selected, slots):
        item['Slot'] = slot
    chest = {'Items': selected}
    return json.dumps(chest).replace('\"', '').replace('\'', '\"')


def make_maze(w=16, h=8):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s


def parse_maze(maze: [str], name: str):
    o = []
    for row in maze.split('\n')[:-2]:
        a = [1]
        for i in range(0, len(row)):
            if row[i] == ' ' or random() < 0.05:
                a.append(0)
                continue
            a.append(1)
        a.append(1)
        o.append(a)
    o.append([1 for _ in range(len(o[0]))])
    output = [[1 for _ in range(len(o[0]))]]
    for oo in o:
        output.append(oo)

    with open(f"{name}.mcfunction", 'w', encoding='utf-8') as maze_file:

        x = len(output)
        z = len(output[0])

        x_segments = x//20
        z_segments = z//20

        for x_seg in range(x_segments):
            for z_seg in range(z_segments):
                # old maze clear
                maze_file.write(
                    f"fill ~{x_seg * 20} ~ ~{z_seg * 20} ~{(x_seg + 1) * 20} ~4 ~{(z_seg + 1) * 20} air replace\n")
                # generate floor
                maze_file.write(
                    f"fill ~{x_seg * 20} ~-1 ~{z_seg * 20} ~{(x_seg + 1) * 20} ~-1 ~{(z_seg + 1) * 20} bedrock replace\n")
                # generate ceiling
                maze_file.write(
                    f"fill ~{x_seg * 20} ~4 ~{z_seg * 20} ~{(x_seg + 1) * 20} ~4 ~{(z_seg + 1) * 20} bedrock replace\n")

                if (x_seg == 0):
                    maze_file.write(
                        f"fill ~{x_segments * 20} ~ ~{z_seg * 20} ~{x} ~4 ~{(z_seg + 1) * 20} air replace\n")
                    # generate floor
                    maze_file.write(
                        f"fill ~{x_segments * 20} ~-1 ~{z_seg * 20} ~{x} ~-1 ~{(z_seg + 1) * 20} bedrock replace\n")
                    # generate ceiling
                    maze_file.write(
                        f"fill ~{x_segments * 20} ~4 ~{z_seg * 20} ~{x} ~4 ~{(z_seg + 1) * 20} bedrock replace\n")

            maze_file.write(
                f"fill ~{x_seg * 20} ~ ~{z_segments * 20} ~{(x_seg + 1) * 20} ~4 ~{z} air replace\n")
            # generate floor
            maze_file.write(
                f"fill ~{x_seg * 20} ~-1 ~{z_segments * 20} ~{(x_seg + 1) * 20} ~-1 ~{z} bedrock replace\n")
            # generate ceiling
            maze_file.write(
                f"fill ~{x_seg * 20} ~4 ~{z_segments * 20} ~{(x_seg + 1) * 20} ~4 ~{z} bedrock replace\n")

        # old maze clear
        maze_file.write(
            f"fill ~{x_segments * 20} ~ ~{z_segments * 20} ~{x} ~4 ~{z} air replace\n")
        # generate floor
        maze_file.write(
            f"fill ~{x_segments * 20} ~-1 ~{z_segments * 20} ~{x} ~-1 ~{z} bedrock replace\n")
        # generate ceiling
        maze_file.write(
            f"fill ~{x_segments * 20} ~4 ~{z_segments * 20} ~{x} ~4 ~{z} bedrock replace\n")

        for i, row in enumerate(output):
            for j, val in enumerate(row):
                if val:
                    choice = random()
                    if choice < 0.01:
                        spawner = Spawner()
                        mob = sample(
                            [EquippableMob, NonEquippableMob], 1)[0]()
                    if choice < 0.001:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} spawner{spawner.generate_spawner_string(mob)} replace\n""")
                        maze_file.write(
                            f"fill ~{i+1} ~1 ~{j+1} ~{i+1} ~3 ~{j+1} minecraft:obsidian replace\n")
                    elif choice < 0.005:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} spawner{spawner.generate_spawner_string(mob)} replace\n""")
                        maze_file.write(
                            f"fill ~{i+1} ~1 ~{j+1} ~{i+1} ~3 ~{j+1} minecraft:obsidian replace\n")
                    elif choice < 0.01:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} spawner{spawner.generate_spawner_string(mob)} replace\n""")
                        maze_file.write(
                            f"fill ~{i+1} ~1 ~{j+1} ~{i+1} ~3 ~{j+1} minecraft:obsidian replace\n")
                    else:
                        maze_file.write(
                            f"fill ~{i+1} ~ ~{j+1} ~{i+1} ~3 ~{j+1} minecraft:obsidian replace\n")
                else:
                    choice = random()
                    if choice < 0.01:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} chest{generate_chest()} replace\n""")
                    elif choice < 0.05:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} torch replace\n""")

        maze_file.write(
            f"fill ~1 ~ ~3 ~3 ~3 ~3 air replace\n")
        maze_file.write(
            f"fill ~{x} ~ ~{z-3} ~{x-1} ~3 ~{z - 3} minecraft:glass replace\n")

    with open(f"{name}_clear.mcfunction", 'w', encoding='utf-8') as clear_maze_file:
        x = len(output)
        z = len(output[0])

        x_segments = x//20
        z_segments = z//20

        for x_seg in range(x_segments):
            for z_seg in range(z_segments):
                clear_maze_file.write(
                    f"fill ~{x_seg * 20} ~-1 ~{z_seg * 20} ~{(x_seg + 1) * 20} ~4 ~{(z_seg + 1) * 20} air replace\n")
                if (x_seg == 0):
                    clear_maze_file.write(
                        f"fill ~{x_segments * 20} ~-1 ~{z_seg * 20} ~{x} ~4 ~{(z_seg + 1) * 20} air replace\n")
            clear_maze_file.write(
                f"fill ~{x_seg * 20} ~-1 ~{z_segments * 20} ~{(x_seg + 1) * 20} ~4 ~{z} air replace\n")
        clear_maze_file.write(
            f"fill ~{x_segments * 20} ~-1 ~{z_segments * 20} ~{x} ~4 ~{z} air replace\n")


if __name__ == '__main__':
    width = 10
    height = 10
    name = "maze"
    pars = argparse.ArgumentParser(description='Generate a maze.',
                                   epilog='Enjoy the program! :)',
                                   prefix_chars='/')
    pars.add_argument("width", help="Width of the maze",
                      type=int, default=width)
    pars.add_argument("height", help="Height of the maze",
                      type=int, default=height)
    pars.add_argument("name", help="Name of the file the maze is stored within",
                      type=str, default=name)
    args = pars.parse_args()

    maze = make_maze(args.width, args.height)
    parse_maze(maze, args.name)
