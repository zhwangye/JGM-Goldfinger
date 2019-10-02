import cfg
import time
from random import randint
import uiautomator2 as u2
from goods import Goods

class Simulator():
    def __init__(self,decvice_info):
        # self.coins_step = 5    # 收取金币时间
        self.goods_step = 5     # 检测货物到达时间
        self.upgrade_step = 15*60   # 升级时间
        self.shop_step = 20     # 商店时间
        self.goods = Goods()
        self.device =u2.connect(decvice_info)
        self.bld_positions = cfg.bld_positions
        self.goods_mapping = cfg.goods_mapping

    def start(self):
        """启动模拟器"""
        print('[*] starting...')
        while True:
            self.device.click(self.rd_offset((550, 1650),10))
            self.move_goods()
            self.get_coins()
            time.sleep(randint(5,10))

    def rd_offset(self,pt,offset=5):
        """每个坐标随机偏移"""
        return (pt[0]+randint(0-offset,offset),pt[1]+randint(0-offset,offset))

    def get_coins(self):
        """获取金币"""
        for i in range(3):
            sx, sy = self.rd_offset(self.bld_positions.get(i * 3 + 1))
            ex, ey = self.rd_offset(self.bld_positions.get(i * 3 + 3))
            self.device.swipe(sx, sy, ex, ey)

    def move_goods(self):
        """移动货物至相应建筑"""
        print('[*] screenshotting...')
        game_shot = self.device.screenshot(format="opencv")
        goods_pts,bld_pts = self.goods.match_goods(game_shot)
        for i in range(len(goods_pts)):
            if len(goods_pts[i]) != 0 and len(bld_pts[i]) != 0:
                sx,sy = self.rd_offset(goods_pts[i])
                ex,ey = self.rd_offset(bld_pts[i])
                for i in range(5):
                    self.device.swipe(sx,sy,ex,ey)
                    time.sleep(0.15)
        return True if len(goods_pts) > 0 else False


if __name__ == '__main__':
    device_info = '127.0.0.1:7555'
    sim = Simulator(device_info)
    sim.start()

