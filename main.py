import tkinter,threading,time,openai,socket,socks,os,sys
from tkinter import ttk #有Combobox、LabelFrame 组件时需要本语句
from tkinter import messagebox #有弹窗时需要本语句
import threading #多线程

# import time

# import openai

# import socket
# import socks

# import os
# import sys


"""

pip install tinyaes

# pyinstaller -F -w -i 1.ico --add-data "1.ico;." openai_ui.py


# 加密的
# pyinstaller -F -w -i 1.ico --add-data "1.ico;." --key '12345678' --clean openai_ui.py
# pyinstaller -F -w -i 1.ico --add-data "1.ico;." --key '12345678' --clean openai_ui.py



"""

# pyinstaller -F -w -i 1.ico --add-data "1.ico;." openai_ui.py

# **************   openai **************



last_ai_msg = '' #上一次的ai回复


def ctrl_Command_copy():
    global last_ai_msg
    # 复制
    ctrl_Entry1.clipboard_clear()
    ctrl_Entry1.clipboard_append(last_ai_msg)

def ctrl_Command_exit():
    
    # 退出
    root.destroy()
    sys.exit()

def conf():
    global mod
    global proxy
    global socks #pip install pysocks
    global socket
    global sleep
    global fontsize
    global user_fontsize
    global lineSpacing
    

    import configparser
    config = configparser.ConfigParser()
    config.read('配置.ini',encoding='utf-8')
    openai.api_key = config['配置']['api']
    mod = config['配置']['model']
    proxy = config['配置']['socks5']
    sleep = float(config['配置']['sleep'])
    fontsize = config['配置']['fontsize']
    user_fontsize = config['配置']['user_fontsize']
    api_base = config['配置']['api_base']

    

    if proxy:
        p_ip = str(proxy.split(':')[0])
        p_port = int(proxy.split(':')[1])
        socks.set_default_proxy(socks.SOCKS5, p_ip, p_port)
        socket.socket = socks.socksocket
    else:
        pass

    if api_base:
        openai.api_base = api_base



if os.path.exists('配置.ini'):
    conf() #调用 conf 函数
else:
    # 不存在 api.txt 文件,弹窗提示
    messagebox.showerror('错误','配置文件不存在')
    with open('配置.ini', 'w',encoding='utf-8') as f:
        f.write('[配置]\n;api_key\napi = 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\n; 没有就不填。 假如有 填写格式：ip:port\nsocks5 = \n; 调用的ai模型\nmodel = gpt-3.5-turbo\n;ai回复的字符之间的间隔时间，单位秒\nsleep = 0\n; ai回复内容字体大小\nfontsize = 12\n; 用户发送内容字体大小\nuser_fontsize = 12\n;api_base  没有就不填,用官方。【需专线网络】  假如有 填写\napi_base=')
    # 退出程序
    sys.exit()
    

messages = [
            {"role": "system", "content": "What can you do as an AI."},
            ]



# **************   openai **************




root=tkinter.Tk() #设定窗体变量
root.geometry('700x850+1100+60') #格式('宽x高+x+y')其中x、y为位置
root.title('OpenAi 聊天 Ver: 0.3')
# 窗体大小不可变
root.resizable(0,0)


if getattr(sys, 'frozen', None):
   basedir = sys._MEIPASS               #程序的临时目录
else:
   basedir = os.path.dirname(__file__)  #程序的根目录

icobit = os.path.join(basedir, '1.ico')   
# 设置图标 为 1.ico
#root.iconbitmap('1.ico')
root.iconbitmap(icobit)


num = 0 #问题编号,用于保存问题,每次回答结束1个问题后加1
think = 0 #标记是否网络请求中,0为否,1为是

def like_think():
    # 假装在思考
    global think

    # label 显示出来 进度条显示出来
    ctrl_Label1.place(x=27,y=675,width=150,height=18)
    ctrl_ProgressBar1.place(x=177,y=675,width=395,height=18) 

    while think:
        time.sleep(0.01)

    ctrl_Label1.place_forget() # 隐藏label
    ctrl_ProgressBar1.place_forget() # 隐藏进度条



def save_messages(num_str='0'):
    #global messages
    # 日志文件名  是此时的 年月日.txt 例如 2020-12-12.txt
    file = time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt'
    # log 文件夹不存在就创建
    if not os.path.exists('log'):
        os.mkdir('log')
    file = './log/'+file

    #with open('日志.txt', 'a',encoding='utf-8') as f:
    with open(file, 'a',encoding='utf-8') as f:
        txt = '\n---------------------\n问题: '+num_str+'已结束 \n'
        f.write(txt)

def save_messages2(i):
    file = time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt'
    # log 文件夹不存在就创建
    if not os.path.exists('log'):
        os.mkdir('log')
    file = './log/'+file
    #with open('日志.txt', 'a',encoding='utf-8') as f:
    with open(file, 'a',encoding='utf-8') as f:
        if i.get('role') == 'user':
            txt = '\n\n' + '用户：\n' + i.get('content')
        elif i.get('role') == 'assistant':
            txt = '\n\n' + 'OpenAi：\n' + i.get('content')
        
        f.write(txt)

def ctrl_Command_send_answer():
    global messages
    global num
    global think
    global mod
    global sleep
    global last_ai_msg



    
    # message = 输入框内容,去掉首尾空格,清空输入框
    #message = str_Entry1.get().strip()
    message = ctrl_Entry1.get('1.0', 'end').strip()
    
    #str_Entry1.set('')
    ctrl_Entry1.delete('1.0', 'end')

    if message == '':
        message = '继续'
    elif message == '!wq':
        save_messages(str(num))
        num = num + 1
        messages = [
            {"role": "system", "content": "What can you do as an AI."},
            ]
        
        return



    if message:
        messages.append(
                    {"role": "user", "content": message},
                    )
        try:
            think = 1
            # voice_input = 1
            # 线程调用假装在思考的函数
            t2 = threading.Thread(target=like_think)
            t2.start()


            chat = openai.ChatCompletion.create(
                #model="gpt-3.5-turbo", messages=messages
                #model="gpt-3.5-turbo", messages=messages,stream=True
                model=mod, messages=messages,stream=True
            )

            # 获取api-key的总的请求次数，每天有5000次。超过5000次就会报错
            # api-key 可以永远免费使用，但是每天只能使用5000次

            

            think = 0 #网络请求完成
            #print("ChatGPT: ",end ='')

            # 显示框内容 = 显示框内容 + 换行 + AI: + AI回复内容
            ctrl_Text1.insert('end', '\nAI: ')
            # 滚动条到最后
            ctrl_Text1.see('end')
    
            reply = ''
            for i in chat:
                #print(i)
                try:
                    i2 = i.choices[0].delta.content
                    if "<|im_end|>" == i2:
                        # 中断 for 循环
                        break

                    reply = reply + i2
                    #print(i2,end='',flush=True)
                    # 显示框显示i2,字体为紫色,刷新显示框，滚动条滚动到最后
                    ctrl_Text1.insert('end', i2)
                    ctrl_Text1.update()
                    ctrl_Text1.see('end')

                    #time.sleep(0.1)
                    time.sleep(sleep)
                except:
                    pass
                    
            #print('')
            # 显示框换行
            ctrl_Text1.insert('end', '\n')
            # 显示框滚动到最后
            ctrl_Text1.see('end')

            messages.append({"role": "assistant", "content": reply}) # 更新上下文
            save_messages2({"role": "user", "content": message}) # 保存问题
            save_messages2({"role": "assistant", "content": reply}) # 保存回答
            last_ai_msg = reply # 更新最后一次AI回复



        except Exception as e:
            # voice_input = 0
            think = 0 #网络请求完成
            if str(e).find("InvalidRequestError: This model's maximum context length is 4096 tokens.") > -1 :
                #print('联系上下文已到最大')
                #显示框换行后，显示，联系上下文已到最大。
                ctrl_Text1.insert('end', '\n联系上下文已到最大。')

            else:
                #print('错误: ',e)
                #显示框换行后，显示，错误: ,e
                ctrl_Text1.insert('end', '\n错误: '+str(e))

        
        
        


def ctrl_CommandButton1_clicked():
    global think
    think = 0 # 停止假装在思考

    # 弹窗，是否保存对话
    if messagebox.askyesno('提示','是否保存对话？'):
        # 输入框 设置为:wq
        ctrl_Entry1.delete('1.0', 'end')
        ctrl_Entry1.insert('1.0', '!wq')


        # 执行发送函数
        ctrl_Command_send()





def ctrl_Command_send():
    
    txt_tmp = ctrl_Entry1.get('1.0', 'end').strip()

    # txt_tmp 内容为空，则 txt_tmp = '继续' ，否则 txt_tmp不变
    txt_tmp = '继续' if txt_tmp == '' else txt_tmp


    # 显示框内容 = 显示框内容 + 换行 + 用户9527: + 输入框内容
    ctrl_Text1.insert('end', '\n用户9527:' + txt_tmp)
    ctrl_Text1.see('end')

    

    # 线程调用回答的函数
    t = threading.Thread(target=ctrl_Command_send_answer)
    #t.daemon(True)
    t.start()
    #t.join()





# 框架
ctrl_LabelFrame1=ttk.LabelFrame(root, text='对话框')
ctrl_LabelFrame1.place(x=27,y=17,width=639,height=650)





# 显示框
#ctrl_Text1=tkinter.Text(ctrl_LabelFrame1,font=('宋体', '16'))
ctrl_Text1=tkinter.Text(ctrl_LabelFrame1,font=('宋体', fontsize))
#ctrl_Text1.place(x=5,y=2,width=215,height=255)
ctrl_Text1.place(x=5,y=2,width=603,height=615)

# 显示框绑定滚动条
ctrl_Scrollbar1=tkinter.Scrollbar(ctrl_LabelFrame1, orient='vertical', command=ctrl_Text1.yview)
ctrl_Scrollbar1.place(x=613,y=2,width=15,height=615)
ctrl_Text1['yscrollcommand']=ctrl_Scrollbar1.set
ctrl_Scrollbar1['command']=ctrl_Text1.yview





#输入框
#str_Entry1=tkinter.StringVar() #绑定变量
#ctrl_Entry1=tkinter.Entry(root, textvariable=str_Entry1,font=('宋体', '9'))
ctrl_Entry1=tkinter.Text(root,font=('宋体', user_fontsize))
#ctrl_Entry1.place(x=7,y=305,width=173,height=29)
ctrl_Entry1.place(x=27,y=700,width=545,height=130)
# 输入框绑定回车键
root.bind('<Return>', lambda event:ctrl_Command_send())
# 输入框有边框
ctrl_Entry1['relief']='groove'



ctrl_CommandButton1=tkinter.Button(root, text='话题结束',font=('雅黑', '12'),command =ctrl_CommandButton1_clicked)#可在括号内加上调用函数部分 ,command =ctrl_CommandButton1_clicked
#ctrl_CommandButton1.place(x=194,y=305,width=43,height=29)
ctrl_CommandButton1.place(x=590,y=700,width=80,height=36)
# 设置按钮效果是有凹凸感
ctrl_CommandButton1['relief']='groove'


ctrl_CommandButton2=tkinter.Button(root, text='Copy This',font=('雅黑', '11'),command =ctrl_Command_copy)#可在括号内加上调用函数部分 ,command =ctrl_CommandButton1_clicked
ctrl_CommandButton2.place(x=590,y=747,width=80,height=36)
# 设置按钮效果是有凹凸感
ctrl_CommandButton2['relief']='groove'


ctrl_CommandButton3=tkinter.Button(root, text='退出聊天',font=('雅黑', '12'),command =ctrl_Command_exit)#可在括号内加上调用函数部分 ,command =ctrl_CommandButton1_clicked
ctrl_CommandButton3.place(x=590,y=794,width=80,height=36)
# 设置按钮效果是有凹凸感
ctrl_CommandButton3['relief']='groove'


# 添加个 进度条。 表示AI正在思考的状态。
ctrl_ProgressBar1 = ttk.Progressbar(root, orient='horizontal', length=545, mode='determinate')
ctrl_ProgressBar1.place(x=177,y=675,width=395,height=18) 
ctrl_ProgressBar1['maximum']=100        # 进度条最大值
ctrl_ProgressBar1['value']=0            # 进度条当前值
ctrl_ProgressBar1['mode']='determinate' # determinate 为确定进度条，indeterminate 为不确定进度条
ctrl_ProgressBar1['length']=395         # 进度条长度
ctrl_ProgressBar1['mode']='indeterminate'# 进度条模式
ctrl_ProgressBar1.start(2)              # 进度条开始，参数为速度，越小越快
#ctrl_ProgressBar1.stop()                # 进度条停止

# label 红字显示 ai正在思考...
ctrl_Label1 = tkinter.Label(root, text='AI正在思考...',font=('宋体', '12'), fg='red')
ctrl_Label1.place(x=27,y=675,width=150,height=18)


ctrl_Label1.place_forget() # 隐藏label
ctrl_ProgressBar1.place_forget() # 隐藏进度条







if __name__ == '__main__':
    #
    root.mainloop()
