# -*- coding: utf-8 -*-
import time
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')


#是否允许使用!!back
back = 1

#中英切换(中=1, 英=0)
EN_CN = 0

death_player = {}
dim_tran = {
    0: '§a主世界',
    -1: '§c地狱',
    1: '§6末地',
    'minecraft:overworld': '§a主世界',
    'minecraft:the_nether': '§c地狱',
    'minecraft:the_end': '§6末地'
}
tp_tran = {
    0: 'minecraft:overworld',
    -1: 'minecraft:the_nether',
    1: 'minecraft:overworld',
    'minecraft:overworld': 'minecraft:overworld',
    'minecraft:the_nether': 'minecraft:the_nether',
    'minecraft:the_end': 'minecraft:the_end'
}

def on_death_message(server, death_message):
    player = death_message.split( )[0]
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    pos = PlayerInfoAPI.getPlayerInfo(server, player, path='Pos')
    xyz = str(int(pos[0])) + ' ' + str(int(pos[1])) + ' ' + str(int(pos[2]))
    dim = PlayerInfoAPI.getPlayerInfo(server, player, path='Dimension')
    if back == 1:
        death_player[player] = [xyz, dim]
        if EN_CN ==0:
            msg = (death_message.replace(player, 'You'), ' at ', tp_tran[dim], ' ', xyz, '. Sent "!!back" to back there')
        else:
            msg = ('您刚刚在',dim_tran[dim] , ' ', xyz, ' 处死亡。发送 "!!back" 回到死亡点')
    else:
        if EN_CN ==0:
            msg = (death_message.replace(player, 'You'), ' at ', xyz)
        else:
            msg = ('您刚刚在',dim_tran[dim] , ' ', xyz, ' 处死亡。')
    server.tell(player, msg)

def  on_user_info(server, info):
    if info.content == '!!back':
        if info.player in death_player.keys():
            server.tell(info.player, '将在3秒后传送，请不要移动')
            time.sleep(3)
            server.execute('execute in {} run tp {} {}'.format(tp_tran[death_player[info.player][1]], info.player, death_player[info.player][0]))
            del death_player[info.player]
        else:
            server.tell(info.player, '未查询到死亡记录')

def on_player_left(server, player):
    if player in death_player.keys():
        del death_player[player]

def on_load(server, old_module):
    server.add_help_message('!!back', '显示与返回死亡点')