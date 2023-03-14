import tkinter,threading,time,openai,socket,socks,os,sys
from tkinter import ttk 
from tkinter import messagebox 
import threading 
"""

"""
last_ai_msg = '' 
new_entry = 0 
def ctrl_Command_copy():
    global last_ai_msg
    ctrl_Entry1.clipboard_clear()
    ctrl_Entry1.clipboard_append(last_ai_msg)
def ctrl_Command_exit():
    
    root.destroy()
    sys.exit()
def conf():
    global mod
    global proxy
    global socks 
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
    conf() 
else:
    messagebox.showerror('错误','配置文件不存在')
    with open('配置.ini', 'w',encoding='utf-8') as f:
        f.write('[配置]\n;api_key\napi = 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\n; 没有就不填。 假如有 填写格式：ip:port\nsocks5 = \n; 调用的ai模型\nmodel = gpt-3.5-turbo\n;ai回复的字符之间的间隔时间，单位秒\nsleep = 0\n; ai回复内容字体大小\nfontsize = 12\n; 用户发送内容字体大小\nuser_fontsize = 12\n;api_base  没有就不填,用官方。【需专线网络】  假如有 填写\napi_base=')
    sys.exit()
    
messages = [
            {"role": "system", "content": "What can you do as an AI."},
            ]
root=tkinter.Tk() 
root.geometry('700x850+1100+60') 
root.title('OpenAi 聊天 Ver: 0.5')
root.resizable(0,0)
if getattr(sys, 'frozen', None):
   basedir = sys._MEIPASS               
else:
   basedir = os.path.dirname(__file__)  
icobit = os.path.join(basedir, '1.ico')   
root.iconbitmap(icobit)
num = 0 
think = 0 
def like_think():
    global think
    ctrl_Label1.place(x=27,y=675,width=150,height=18)
    ctrl_ProgressBar1.place(x=177,y=675,width=395,height=18) 
    while think:
        time.sleep(0.01)
    ctrl_Label1.place_forget() 
    ctrl_ProgressBar1.place_forget() 
def save_messages():
    file = time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt'
    if not os.path.exists('log'):
        os.mkdir('log')
    file = './log/'+file
    with open(file, 'a',encoding='utf-8') as f:
        txt = '\n---------------------\n问题已结束 \n'
        f.write(txt)
def save_messages2(i):
    file = time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt'
    if not os.path.exists('log'):
        os.mkdir('log')
    file = './log/'+file
    with open(file, 'a',encoding='utf-8') as f:
        if i.get('role') == 'user':
            txt = '\n\n' + i.get('content')
        elif i.get('role') == 'assistant':
            txt = '\n\n' + i.get('content')
        
        f.write(txt)
def ctrl_Command_send_answer(txt_tmp,send_txt):
    global messages
    global num
    global think
    global mod
    global sleep
    global last_ai_msg
    global new_entry
    
    
    message = txt_tmp
    if message == '':
        message = '继续'
    elif message == '!wq':
        save_messages()
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
            t2 = threading.Thread(target=like_think)
            t2.start()
            chat = openai.ChatCompletion.create(
                model=mod, messages=messages,stream=True
            )
            
            think = 0 
            new_entry = 0 
    
            reply = ''
            reply_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            reply_show = reply_time + ' AI: \n'
            ctrl_Text1.insert('end', reply_show)
            ctrl_Text1.see('end')
            for i in chat:
                try:
                    i2 = i.choices[0].delta.content
                    if "<|im_end|>" == i2:
                        break
                    reply = reply + i2
                    reply_show = reply_show + i2
                    if new_entry:
                        break
                    ctrl_Text1.insert('end', i2)
                    ctrl_Text1.update()
                    ctrl_Text1.see('end')
                    time.sleep(sleep)
                except:
                    pass
                    
            ctrl_Text1.insert('end', '\n')
            ctrl_Text1.see('end')
            messages.append({"role": "assistant", "content": reply}) 
            save_messages2({"role": "user", "content":send_txt}) 
            save_messages2({"role": "assistant", "content": reply_show}) 
            last_ai_msg = reply 
        except Exception as e:
            think = 0 
            if str(e).find("InvalidRequestError: This model's maximum context length is 4096 tokens.") > -1 :
                ctrl_Text1.insert('end', '\n联系上下文已到最大。')
            else:
                ctrl_Text1.insert('end', '\n错误: '+str(e))
        
        
        
def ctrl_CommandButton1_clicked():
    global think
    think = 0 
    if messagebox.askyesno('提示','是否保存对话？'):
        ctrl_Entry1.delete('1.0', 'end')
        ctrl_Entry1.insert('1.0', '!wq')
        ctrl_Command_send()
def ctrl_Command_send():
    global new_entry
    
    txt_tmp = ctrl_Entry1.get('1.0', 'end').strip()
    txt_tmp = '继续' if txt_tmp == '' else txt_tmp
    send_txt = '\n'+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' 用户9527: \n' +txt_tmp + '\n\n'
    ctrl_Text1.insert('end', send_txt)
    ctrl_Text1.see('end')
    new_entry = 1 
    ctrl_Entry1.delete('1.0', 'end')
    
    t = threading.Thread(target=ctrl_Command_send_answer,args=(txt_tmp,send_txt))
    t.start()
ctrl_LabelFrame1=ttk.LabelFrame(root, text='对话框')
ctrl_LabelFrame1.place(x=27,y=17,width=639,height=650)
ctrl_Text1=tkinter.Text(ctrl_LabelFrame1,font=('宋体', fontsize))
ctrl_Text1.place(x=5,y=2,width=603,height=615)
ctrl_Scrollbar1=tkinter.Scrollbar(ctrl_LabelFrame1, orient='vertical', command=ctrl_Text1.yview)
ctrl_Scrollbar1.place(x=613,y=2,width=15,height=615)
ctrl_Text1['yscrollcommand']=ctrl_Scrollbar1.set
ctrl_Scrollbar1['command']=ctrl_Text1.yview
ctrl_Entry1=tkinter.Text(root,font=('宋体', user_fontsize))
ctrl_Entry1.place(x=27,y=700,width=545,height=130)
root.bind('<Return>', lambda event:ctrl_Command_send())
ctrl_Entry1['relief']='groove'
ctrl_CommandButton1=tkinter.Button(root, text='话题结束',font=('雅黑', '12'),command =ctrl_CommandButton1_clicked)
ctrl_CommandButton1.place(x=590,y=700,width=80,height=36)
ctrl_CommandButton1['relief']='groove'
ctrl_CommandButton2=tkinter.Button(root, text='Copy This',font=('雅黑', '11'),command =ctrl_Command_copy)
ctrl_CommandButton2.place(x=590,y=747,width=80,height=36)
ctrl_CommandButton2['relief']='groove'
ctrl_CommandButton3=tkinter.Button(root, text='退出聊天',font=('雅黑', '12'),command =ctrl_Command_exit)
ctrl_CommandButton3.place(x=590,y=794,width=80,height=36)
ctrl_CommandButton3['relief']='groove'
ctrl_ProgressBar1 = ttk.Progressbar(root, orient='horizontal', length=545, mode='determinate')
ctrl_ProgressBar1.place(x=177,y=675,width=395,height=18) 
ctrl_ProgressBar1['maximum']=100        
ctrl_ProgressBar1['value']=0            
ctrl_ProgressBar1['mode']='determinate' 
ctrl_ProgressBar1['length']=395         
ctrl_ProgressBar1['mode']='indeterminate'
ctrl_ProgressBar1.start(2)              
ctrl_Label1 = tkinter.Label(root, text='AI正在思考...',font=('宋体', '12'), fg='red')
ctrl_Label1.place(x=27,y=675,width=150,height=18)
ctrl_Label1.place_forget() 
ctrl_ProgressBar1.place_forget() 
if __name__ == '__main__':
    root.mainloop()
