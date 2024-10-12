import json

def load_map_data(self, level_name):
    # mC ~ mainConfig
    with open("data/config.json", "r") as mC:
        data = json.load(mC)
        for level in data["levels"]:
            if level["title"] == level_name:
                return level.get("map")

def calculate_start_and_block_unit(self):
    map_width = len(self.map_data[0])
    map_height = len(self.map_data)

    block_unit = min(self.width / map_width, self.height / map_height)

    start_x = (self.width - (block_unit * map_width)) / 2
    start_y = (self.height - (block_unit * map_height)) / 2

    return start_x, start_y, block_unit