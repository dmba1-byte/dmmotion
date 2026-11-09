import sys,os,subprocess
from playwright.sync_api import sync_playwright
sets=[int(x) for x in sys.argv[1].split(',')];fr=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1008,'height':1080});pg.on('pageerror',lambda e:print('ERR',e));pg.goto('file:///home/claude/vox/fbview.html');pg.wait_for_timeout(300)
    for s in sets:
        d=f'ff_{s}';os.makedirs(d,exist_ok=True)
        idx=range(32) if fr=='all' else [int(x) for x in fr.split(',')]
        for i in idx:
            pg.evaluate(f'drawFB({i},{s})');pg.screenshot(path=f'{d}/{i:03d}.png',clip={'x':0,'y':0,'width':1008,'height':1080})
        if fr=='all':subprocess.run(f'ffmpeg -y -loglevel error -stream_loop 3 -framerate 24 -i {d}/%03d.png -pix_fmt yuv420p -crf 16 -c:v libx264 views{s+1}.mp4',shell=True)
