import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
#import time

CHUNK = 1024  # 每个缓冲区的帧数
FORMAT = pyaudio.paInt16  # 采样位数
CHANNELS = 1  # 单声道
RATE = 44100  # 采样频率
def play_audio(wave_input_path):
    p = pyaudio.PyAudio()  # 实例化
    wf = wave.open(wave_input_path, 'rb')  # 读 wav 文件
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)  # 读数据
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()  # 关闭资源
    stream.close()
    p.terminate()
    
def record_audio(wave_out_path, record_second):
    """ 录音功能 """
    p = pyaudio.PyAudio()  # 实例化对象
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # 打开流，传入响应参数
    wf = wave.open(wave_out_path, 'wb')  # 打开 wav 文件。
    wf.setnchannels(CHANNELS)  # 声道设置
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
    wf.setframerate(RATE)  # 采样频率设置

    for _ in range(0, int(RATE * record_second / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)  # 写入数据
    stream.stop_stream()  # 关闭流
    stream.close()
    p.terminate()
    wf.close()
 


def wavread(path):
    wavfile =  wave.open(path,"rb")
    params = wavfile.getparams()
    framesra,frameswav= params[2],params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.short)
    datause.shape = -1,2
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0/framesra)
    return datause,time

def main():
    #path = input()
    wavdata,wavtime = wavread('original sound.wav')
    plt.title('************')
    plt.subplot(211)
    plt.plot(wavtime, wavdata[0],color = 'green')
    plt.subplot(212)
    plt.plot(wavtime, wavdata[1])
    plt.show()
    
main()


 
# 
#t=10 
#print('开始录音')
#record_audio("sound recording.wav",t)
#time.sleep(1)
#print('开始播放')
#play_audio('original sound.wav')

