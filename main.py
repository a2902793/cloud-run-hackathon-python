
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ctypes import sizeof
import os
import logging
import random
from flask import Flask, request

#----------------------------
# from pprint import pformat
# import coloredlogs, logging
# coloredlogs.install()
# import re
#----------------------------

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
escape = ['F', 'L', 'R']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    data = request.json

    # logger.info(pformat(request.json['arena']['state']))
    my_player = data['_links']['self']['href']
    my_status = {
        'x': data['arena']['state'][my_player]['x'],
        'y': data['arena']['state'][my_player]['y'],
        'direction': data['arena']['state'][my_player]['direction']
    }
    
    columns = data['arena']['dims'][0] + 1
    rows = data['arena']['dims'][1] + 1
    arena = [[0 for _ in range(rows)] for _ in range(columns)] 
    # pattern = "\-([a-zA-Z0-9]*)\-[a-zA-Z0-9]*.a.run.app"

    for player in data['arena']['state']:
        # player_id = re.search(pattern, player).group(1)[:3]
        # print(player_id)
        player_x = data['arena']['state'][player]['x']
        player_y = data['arena']['state'][player]['y']
        # arena[player_x][player_y] = player_id
        arena[player_x][player_y] = data['arena']['state'][player]['direction']
    
    enemy_flag = False
    if my_status['direction'] == 'N':
        lower_bound = 0 if my_status['y'] < 3 else my_status['y'] - 3
        for enemy in arena[my_status['x']][lower_bound:my_status['y']]:
            if enemy == 'S':
                return 'T'
        else:
            return escape[random.randrange(len(escape))]
    elif my_status['direction'] == 'S':
        upper_bound = len(arena[0]) if my_status['y'] > len(arena[0] - 3) else my_status['y'] + 3
        for enemy in arena[my_status['x']][my_status['y']:upper_bound]:
            if enemy == 'N':
                return 'T'
        else:
            return escape[random.randrange(len(escape))]
    elif my_status['direction'] == 'W':
        lower_bound = 0 if my_status['x'] < 3 else my_status['x'] - 3
        for enemy in arena[lower_bound:my_status['x']]['y']:
            if enemy == 'E':
                return 'T'
        else:
            return escape[random.randrange(len(escape))]
    else: # 'E'
        upper_bound = len(arena) if my_status['x'] > len(arena) - 3 else my_status['x'] + 3
        for enemy in arena[my_status['x']:upper_bound]['y']:
            if enemy == 'W':
                return 'T'
        else:
            return escape[random.randrange(len(escape))]

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    # app.run(debug=True,host='127.0.0.1',port=int(os.environ.get('PORT', 8080)))

