from question_classifier import *
from question_parser import *
from answer_search import *
import wave
import requests
import time
import base64
from pyaudio import PyAudio, paInt16
import pyttsx3


framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = 'speech.wav'

base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
APIKey = "eBBRQNVY8r6esnCXqw46MLye"
SecretKey = "MbpDrOaNv9oobwZu611xGyKqTOcOEb7g"

HOST = base_url % (APIKey, SecretKey)


def getToken(host):
    res = requests.post(host)
    return res.json()['access_token']


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []
    # count = 0
    t = time.time()
    print('正在录音...')

    while time.time() < t + 4:  # 秒
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    stream.close()


def get_audio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


def speech2text(speech_data, token, dev_pid=1537):
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = '*******'
    SPEECH = base64.b64encode(speech_data).decode('utf-8')

    data = {
        'format': FORMAT,
        'rate': RATE,
        'channel': CHANNEL,
        'cuid': CUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }
    url = 'https://vop.baidu.com/server_api'
    headers = {'Content-Type': 'application/json'}
    # r=requests.post(url,data=json.dumps(data),headers=headers)
    print('正在识别...')
    r = requests.post(url, json=data, headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result
def yuyingbobao(x):
    # 模块初始化
    engine = pyttsx3.init()
    # 输出文件格式
    print('准备开始语音播报...')
    # 设置要播报的Unicode字符串
    engine.say(x)
    # 等待语音播报完毕
    engine.runAndWait()

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '没能理解您的问题，我数据量有限。。。能不能问的标准点'
        res_classify = self.classifier.classify(sent)#分类主函数
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)#解析主函数
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)



if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        flag = 'y'
        while flag.lower() == 'y':
            print('请输入数字选择语言：')
            devpid = input('1536：普通话(简单英文),1537:普通话(有标点),1737:英语,1637:粤语,1837:四川话\n')
            my_record()
            TOKEN = getToken(HOST)
            speech = get_audio(FILEPATH)
            result = speech2text(speech, TOKEN, int(devpid))
            print(result)
            answer = handler.chat_main(result)
            print('客服机器人:', answer)
            yuyingbobao(answer)
            flag = input('Continue?(y/n):')