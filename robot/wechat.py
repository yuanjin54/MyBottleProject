# 导入模块
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot()
# 进入 Python 命令行、让程序保持运行
embed()

# 搜索名称含有 "游否" 的男性深圳好友
my_friend = bot.friends().search('游否', sex=MALE, city="深圳")[0]

print(my_friend)