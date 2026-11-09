import base64,os
from playwright.sync_api import sync_playwright
os.makedirs('/home/claude/dmmotion/px/kit',exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.on('pageerror',lambda e:print('ERR',e));pg.goto('file:///home/claude/vox/sprites.html');pg.wait_for_timeout(300)
    for k in pg.evaluate('Object.keys(SP)'):
        d=pg.evaluate(f'SP["{k}"]()')
        open(f'/home/claude/dmmotion/px/kit/{k}.png','wb').write(base64.b64decode(d.split(',')[1]))
    print('done')
