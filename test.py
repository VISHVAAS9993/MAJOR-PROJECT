import httplib2,json
import tkinter
http=httplib2.Http()
def forward(x):
    bot1("F",x,1000,1000)
    print('F')
def drop(x):
    bot1("D",x,0,0)
    print('d')
def left(x):
    bot1("L",x,500,500)
    print('l')
def right(x):
    print('r')
    bot1("R",x,500,500)
def bot1(d,x,rs,ls):
        path = d
        pathlength = len(path)
        leftspeed = str(ls)
        rightspeed = str(rs)
        turntime = "10"#tt
        blocktime ="50"#bt
        # ips=["http://192.168.1.12/jdrive","http://192.168.1.9/jdrive"] #home wifi
        ips = ["http://192.168.43.247/jdrive", "http://192.168.43.210/jdrive"]  # phone wifi
        url_json = ips[x]
        data = {"turntime": turntime, "pathlength": pathlength, "path": path, 'leftspeed': leftspeed,
                "rightspeed": rightspeed, "blocktime": blocktime}
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        response, content = http.request(url_json, 'POST', headers=headers, body=json.dumps(data))
        print(x)