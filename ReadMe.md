本家国梦自动化脚本主要思想来自于[Jiahonzheng/JGM-Automator](https://github.com/Jiahonzheng/JGM-Automator) 环境配置请参照左侧链接。

功能：

- 自动收金币
- 自动移动货物

改进：

- 获取货物的绝对位置，截取60*60px 的货物图片，与货物模板**计算相似度**（颜色直方图），从而判断货物类别，接着移动到对应建筑


注意：

- 需要自己在cfg.py中**修改货物和建筑物的映射关系**

