import base64,os,sys
from playwright.sync_api import sync_playwright
out='/home/claude/dmmotion/px/kit/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.on('pageerror',lambda e:print('ERR',e));pg.on('console',lambda m:print('LOG',m.text) if m.type=='error' else None);pg.goto('file:///home/claude/vox/strips.html');pg.wait_for_timeout(300)
    for k in pg.evaluate('Object.keys(STRIPS)'):
        try:
            d=pg.evaluate(f'STRIPS["{k}"]()');open(f'{out}s_{k}.png','wb').write(base64.b64decode(d.split(',')[1]))
        except Exception as e:print('FAIL',k,str(e)[:120])
    print('ok')
