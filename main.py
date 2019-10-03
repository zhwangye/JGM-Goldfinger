import cfg
import time
from random import randint
import uiautomator2 as u2
from goods import Goods

class Simulator():
    def __init__(self,decvice_info):
        # self.coins_step = 5    # 收取金币时间
        self.start_time = 0
        self.upgrade_step = 10   # 升级时间
        self.level_num = 20     # 等级提升数量
        self.goods = Goods()
        self.device =u2.connect(decvice_info)
        self.bld_positions = cfg.bld_positions
        self.goods_mapping = cfg.goods_mapping

    def fmt_seconds(self,seconds):
        """格式化时间，秒 -> h:m:s"""
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        print("[*] start:","%d:%02d:%02d" % (h, m, s))

    def start(self):
        """启动模拟器"""
        print('[*] starting...')
        self.start_time = time.time()
        cnt_loop = 0    # 记录迭代次数
        bld_index = 1   # 建筑编号，用于建筑升级
        postcar_index = 0    # 记录邮车的次数
        while True:
            print('[*] index:',str(bld_index))
            print('[*] loops:',str(cnt_loop))
            started_time = time.time()-self.start_time
            if started_time // 3600 == postcar_index:   # 每隔1h领取一次
                self.postcar()
                self.shop()
                postcar_index += 1
            self.fmt_seconds(started_time)

            # 每次都先点击“建设”菜单，增加鲁棒性
            for i in range(5):
                bld_menu_btn_x, bld_menu_btn_y = self.rd_offset((63, 1880), 10)
                self.device.click(bld_menu_btn_x,bld_menu_btn_y)
                time.sleep(0.01)
            # 处理xx之光
            x, y = self.rd_offset((550, 1650), 10)
            self.device.click(x, y)
            self.move_goods()
            self.get_coins()
            cnt_loop += 1
            if cnt_loop % self.upgrade_step == 0:     # 每收集x轮金币升级一次
                self.upgrade_building(bld_index)
                bld_index += 1
                if bld_index==10:
                    bld_index = 1
            time.sleep(randint(1,3))

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
        game_shot = self.device.screenshot(format="opencv")
        goods_pts,bld_pts = self.goods.match_goods(game_shot)
        if len(goods_pts) > 0 and len(bld_pts) > 0 and len(goods_pts)==len(bld_pts):
            for i in range(len(goods_pts)):
                if len(goods_pts[i]) != 0 and len(bld_pts[i]) != 0:
                    sx,sy = self.rd_offset(goods_pts[i])
                    ex,ey = self.rd_offset(bld_pts[i])
                    for i in range(5):
                        self.device.swipe(sx,sy,ex,ey)
                        time.sleep(0.15)

    def upgrade_building(self,index):
        """自动升级建筑"""
        upgrade_ui_btn = (963,1153)
        upgrade_btn = (851,1741)
        self.device.click(upgrade_ui_btn[0],upgrade_ui_btn[1])  # 进入升级界面
        time.sleep(0.5)
        bld_x,bld_y = self.bld_positions.get(index)
        self.device.click(bld_x,bld_y)  # 选择建筑
        time.sleep(0.5)
        for i in range(self.level_num):    # 点x下，即升x级
            self.device.click(upgrade_btn[0], upgrade_btn[1])
            time.sleep(0.1)
        self.device.click(upgrade_ui_btn[0], upgrade_ui_btn[1])     # 返回建设界面

    def postcar(self):
        """签到领奖励"""
        post_car_btn = [163,337]
        confirm_btn = [541,1185]
        self.device.click(post_car_btn[0], post_car_btn[1])
        time.sleep(0.5)
        self.device.click(confirm_btn[0], confirm_btn[1])

    def shop(self):
        """
        商店打开红包，收集相片。暴力拆解，满福->福气
        一共点击10轮，每个红包点击6次；在点击相册
        """
        shop_btn = (423,1859)
        # 满福->福气
        pkts_btn = ((873,701),(535,711),(207,675))
        album_btn = (509,1415)
        confirm_btn = (311,1115)
        self.device.click(shop_btn[0],shop_btn[1])
        for i in range(10):
            for pts in pkts_btn:
                x,y = self.rd_offset(pts)
                for i in range(6):
                    self.device.click(x,y)
                    time.sleep(0.1)
        for _ in range(10):
            x,y = self.rd_offset(album_btn)
            self.device.click(x,y)
            time.sleep(0.5)
        self.device.click(confirm_btn[0],confirm_btn[1])

if __name__ == '__main__':
    device_info = '127.0.0.1:7555'
    sim = Simulator(device_info)
    sim.start()

