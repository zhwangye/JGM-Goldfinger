import uiautomator2
import os
import cfg
import goods
import uuid
import cv2
import time

## 这个写得很随意，功能实现了就行

pimg = 'img/'
proi = 'img/roi/'
if not os.path.exists(pimg):
    os.makedirs(pimg)
if not os.path.exists(proi):
    os.makedirs(proi)

device_info = '127.0.0.1:7555'
for i in range(100):
    device = uiautomator2.connect(device_info)
    img = device.screenshot(format="opencv")
    cv2.imwrite(os.path.join(pimg,str(uuid.uuid1())+'.jpg'),img)
    img = img[1400:-200, 400:]
    goo = goods.Goods()
    for gidx, cpt in enumerate(cfg.goods_position):
        pts = goo.get_lt_rb(cpt)
        roi = goo.get_roi(img, pts)
        cv2.imwrite(os.path.join(proi,str(uuid.uuid1())+'.jpg'),roi)
    time.sleep(10)