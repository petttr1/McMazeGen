from random import shuffle, randrange, random, choices, randint, sample
import argparse
import json
from Weapon import Weapon
from Armor import Armor
from Consumable import Consumable
from Potion import Potion


def generate_chest():
    num_items = randint(1, 24)
    selected = []
    options = [Weapon, Armor, Consumable, Potion]
    for i in range(num_items):
        o = sample(options, 1)[0]()  # toto mi je luto, pardon
        if random() < 0.2:
            o.enchant()
        selected.append(o.generate_item_string(i))
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
        x_half = x // 2
        z = len(output[0])
        z_half = z // 2

        # old maze clear
        maze_file.write(
            f"fill ~1 ~ ~1 ~{x_half} ~3 ~{z_half} air replace\n")
        maze_file.write(
            f"fill ~{x_half} ~ ~1 ~{x} ~3 ~{z_half} air replace\n")
        maze_file.write(
            f"fill ~{x_half} ~ ~{z_half} ~{x} ~3 ~{z} air replace\n")
        maze_file.write(
            f"fill ~1 ~ ~{z_half} ~{x_half} ~3 ~{z} air replace\n")

        # generate floor
        maze_file.write(
            f"fill ~1 ~-1 ~1 ~{x_half} ~-1 ~{z_half} minecraft:bedrock replace\n")
        maze_file.write(
            f"fill ~{x_half} ~-1 ~1 ~{x} ~-1 ~{z_half} minecraft:bedrock replace\n")
        maze_file.write(
            f"fill ~{x_half} ~-1 ~{z_half} ~{x} ~-1 ~{z} minecraft:bedrock replace\n")
        maze_file.write(
            f"fill ~1 ~-1 ~{z_half} ~{x_half} ~-1 ~{z} minecraft:bedrock replace\n")

        for i, row in enumerate(output):
            for j, val in enumerate(row):
                if val:
                    choice = random()
                    if choice < 0.001:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} spawner{{SpawnData:{{id:wither_skeleton,HandItems:[{{Count:1,id:golden_axe,tag:{{Enchantments:[{{id:sharpness,lvl:2}}]}}}},{{Count:1,id:shield,tag:{{Enchantments:[{{id:unbreaking,lvl:3}}]}}}}],ArmorItems:[{{Count:1,id:iron_boots}},{{Count:1,id:golden_leggings}},{{Count:1,id:golden_chestplate}},{{Count:1,id:chainmail_helmet}}],CustomName:\"BigMan\"}},SpawnRange:20,SpawnCount:5,MaxNearbyEntities:5,Delay:0,RequiredPlayerRange:20}} replace\n""")
                        maze_file.write(
                            f"fill ~{i+1} ~1 ~{j+1} ~{i+1} ~3 ~{j+1} minecraft:bedrock replace\n")
                    elif choice < 0.005:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} spawner{{SpawnData:{{id:blaze,CustomName:\"Domko\"}},SpawnRange:20,SpawnCount:5,MaxNearbyEntities:20,Delay:0,RequiredPlayerRange:20}} replace\n""")
                        maze_file.write(
                            f"fill ~{i+1} ~1 ~{j+1} ~{i+1} ~3 ~{j+1} minecraft:bedrock replace\n")
                    elif choice < 0.01:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} spawner{{SpawnData:{{id:zombie,HandItems:[{{Count:1,id:stone_sword}},{{}}],ArmorItems:[{{Count:1,id:iron_boots}},{{Count:1,id:leather_leggings}},{{Count:1,id:leather_chestplate,tag:{{display:{{color:8991416}}}}}},{{Count:1,id:creeper_head}}],CustomName:\"Denko\"}}, SpawnRange: 20, SpawnCount: 5, MaxNearbyEntities: 5, Delay: 0, RequiredPlayerRange: 20}} replace\n""")
                        maze_file.write(
                            f"fill ~{i+1} ~1 ~{j+1} ~{i+1} ~3 ~{j+1} minecraft:bedrock replace\n")
                    else:
                        maze_file.write(
                            f"fill ~{i+1} ~ ~{j+1} ~{i+1} ~3 ~{j+1} minecraft:bedrock replace\n")
                else:
                    choice = random()
                    if choice < 0.1:
                        maze_file.write(
                            f"""setblock ~{i+1} ~ ~{j+1} chest{generate_chest()} replace\n""")

        maze_file.write(
            f"fill ~1 ~ ~3 ~3 ~3 ~3 air replace\n")
        maze_file.write(
            f"fill ~{x} ~ ~{z-3} ~{x - 2} ~3 ~{z - 3} minecraft:glass replace\n")

    with open(f"{name}_clear.mcfunction", 'w', encoding='utf-8') as clear_maze_file:
        x = len(output)
        x_half = x // 2
        z = len(output[0])
        z_half = z // 2
        clear_maze_file.write(
            f"fill ~1 ~ ~1 ~{x_half} ~3 ~{z_half} air replace\n")
        clear_maze_file.write(
            f"fill ~{x_half} ~ ~1 ~{x} ~3 ~{z_half} air replace\n")
        clear_maze_file.write(
            f"fill ~{x_half} ~ ~{z_half} ~{x} ~3 ~{z} air replace\n")
        clear_maze_file.write(
            f"fill ~1 ~ ~{z_half} ~{x_half} ~3 ~{z} air replace\n")


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
