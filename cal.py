import httplib2,json
import tkinter
http=httplib2.Http()
top = tkinter.Tk()
def drop():
    bot1("F")
def forward():
    bot1("F")
def backward():
    bot1("D")
def left():
    bot1("L")
def right():
    bot1("R")
def bot1(d):
            path = d
            pathlength = len(path)
            leftspeed = "1000"#ls
            rightspeed = "1000"#rs\
            turntime = "50"#tt
            blocktime ="100"#bt
            #ips=["http://192.168.1.12/jdrive","http://192.168.1.9/jdrive"] #home wifi
            ips = ["http://192.168.43.247/jdrive", "http://192.168.43.210/jdrive"]# phone wifi
            url_json = ips[0]
            data = {"turntime": turntime, "pathlength": pathlength, "path": path, 'leftspeed': leftspeed,
                    "rightspeed": rightspeed, "blocktime": blocktime}
            headers = {"Content-Type": "application/json; charset=UTF-8"}
            response, content = http.request(url_json, 'POST', headers=headers, body=json.dumps(data))
            print(response)
F = tkinter.Button(top, text ="forward", command =forward).pack()
B = tkinter.Button(top, text ="backward", command =backward).pack()
L = tkinter.Button(top, text ="left", command =left).pack()
R = tkinter.Button(top, text ="right", command =right).pack()
top.mainloop()