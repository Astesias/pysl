import uiautomation as auto
import time
import random

time.sleep(2)
t = 0
g = ['阅', '在', '活', '+1', '：', '到', ',', '.', '。']
f = ['阅  ', '在  ', '活  ', '+1  ', '：  ', '到  ', ',  ', '.  ', '。  ']
while True:
    window = auto.WindowControl(ClassName='WeChatMainWndForPC', searchDepth=1)
    meslist = window.ListControl(Name='消息')
    # for i in meslist.GetChildren():
    print(1)
    if (meslist.GetChildren() == []):
        time.sleep(1)
        continue
    elif (len(str(meslist.GetChildren()[-1].Name)) > 2):
        t += 1
        auto.SendKeys(random.sample(g, 1))
        time.sleep(0.5)
        auto.SendKeys('{enter}')


# import uiautomation as auto
# import time
# import random

# while True:
#     window = auto.WindowControl(ClassName='WeChatMainWndForPC', searchDepth=1)
#     m = window.ListControl(Name='消息')
#     print(m.get.GetChildren())
#     break

