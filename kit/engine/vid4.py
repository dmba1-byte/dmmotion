import subprocess,os,sys
from playwright.sync_api import sync_playwright
sets=[int(x) for x in sys.argv[1].split(',')];frames=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 and sys.argv[2]!='all' else list(range(96))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1920,'height':1080});pg.on('pageerror',lambda e:print('ERR',e));pg.goto('file:///home/claude/vox/kit4.html');pg.wait_for_timeout(300)
    for s in sets:
        d=f'f4_{s}';os.makedirs(d,exist_ok=True)
        pg.evaluate(f'window.SET={s}')
        for i in frames:
            pg.evaluate(f'draw({i})');pg.screenshot(path=f'{d}/{i:03d}.png',clip={'x':0,'y':0,'width':1920,'height':1080})
        if len(frames)==96:
            subprocess.run(f'ffmpeg -y -loglevel error -framerate 24 -i {d}/%03d.png -pix_fmt yuv420p -crf 16 -c:v libx264 k4set{s+1}.mp4',shell=True)
    b.close()
