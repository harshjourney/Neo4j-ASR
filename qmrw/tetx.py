import pyttsx3
import win32.com.client
def yuyingbobao(xx):
    # 模块初始化
    engine = pyttsx3.init()
    # 输出文件格式
    print('准备开始语音播报...')
    # 设置要播报的Unicode字符串
    engine.say(xx)
    # 等待语音播报完毕
    engine.runAndWait()
if __name__ == '__main__':
    x = '520'
    yuyingbobao(x)
