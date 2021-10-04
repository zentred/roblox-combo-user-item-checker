import glob
import requests
from threading import Thread

threadc = 25

type = 'asset'
assetids = open('ids.txt','r').read().splitlines()

hits = open('hits.txt','r').read().splitlines()

def divide(stuff):
    return [stuff[i::threadc] for i in range(threadc)]

def cpm():
    import ctypes
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f'Done: {done}/{len(hits)} | ID: {assetids.index(gg)}/{len(assetids)}')

def check(combos):
    global done
    for combo in combos:
        try: username,password,cookie = combo.split(':',2)
        except:
            try:
                username,password = combo.split(':')
            except: continue
        try:
            r = requests.get(f'http://api.roblox.com/users/get-by-username?username={username}')
            if 'User not found' in r.text: continue
            id = r.json()['Id']
            r = requests.get(f'https://inventory.roblox.com/v1/users/{id}/items/{type}/{gg}')
            if 'The specified user does not exist!' in r.text: continue
            if r.json()['data'] != []:
                print(username+':'+password,gg)
                hasitem.append(username+':'+password+'\n')
            done += 1
        except Exception as e: print(e); combos.append(combo)

gg = 0
Thread(target=cpm).start()
for assetid in assetids:
    done = 0
    gg = assetid
    print('Checking',gg)
    hasitem = []
    threads = []
    for i in range(threadc):
        threads.append(Thread(target=check,args=[divide(hits)[i]]))
        threads[i].start()
    for thread in threads:
        thread.join()
    try:
        fname = requests.get(f'https://api.roblox.com/Marketplace/ProductInfo?assetId={assetid}').json()['Name']
        for char in fname:
            if char.lower() not in list('abcdefghijklmnopqrstuvwxyz1234567890 '):
                fname = fname.replace(char,'')
    except:
        fname = f'{assetid}'
    with open(f'./checked/{fname}.txt','w') as f:
        f.writelines(hasitem)

input('FINISHED')
