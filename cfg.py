
# 货物模板图片路径
ptdir = 'tpl/'

# 货物中心坐标,相对坐标
goods_position = [[263, 231], [417, 159], [570, 68]]

# 货物绝对坐标，在1920*1080图上的坐标
goods_abs_position = ((657,1639),(821,1555),(964,1475))

# 货物对应的建筑物编号，按需修改
# 增加物品需要将img/roi/的新的货物修改名字后放入
# tpl/文件夹下，并修改下面的映射字典
# 已包含的货物有
# bottle box chair chicken food mineral sofa vegetable wood
# laptop gear coal screw schoolbag steel
# goods_mapping ={
#     'bottle': 4,
#      'box': 2,
#      'chair': 1,
#      'chicken': 6,
#      'food': 8,
#      'mineral': 9,
#      'sofa': 3,
#      'vegetable': 5,
#      'wood': 7
# }

goods_mapping ={
    'laptop': 1,
     'box': 2,
     'sofa': 3,
     'screw': 4,
     'schoolbag': 5,
     'chicken': 6,
     'gear': 7,
     'coal': 8,
     'steel': 9
}


# 建筑物的绝对坐标
bld_positions = {
    1: (294, 1184),
    2: (551, 1061),
    3: (807, 961),
    4: (275, 935),
    5: (535, 810),
    6: (799, 687),
    7: (304, 681),
    8: (541, 568),
    9: (787, 447)
}
