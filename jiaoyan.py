content=[]
with open('./data/man_can.txt','rt',encoding='utf-8') as f1:
    for l in f1:
        content.append(l.split(',',4)[3][2:-1])
    data=set(content)
    print(data)