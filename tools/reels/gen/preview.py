import sys, pathlib
from playwright.sync_api import sync_playwright
def sheet(svgs, out, bg='#fff', cols=4, scale=0.3):
    W,H=1080,1920
    html='<html><body style="margin:0;display:flex;flex-wrap:wrap;width:%dpx;background:#888">'%(cols*W*scale+cols*10)
    for s,b in svgs:
        html+=f'<div style="width:{W*scale}px;height:{H*scale}px;margin:5px;background:{b};overflow:hidden"><svg width="{W*scale}" height="{H*scale}" viewBox="0 0 {W} {H}">{s}</svg></div>'
    html+='</body></html>'
    p=pathlib.Path('/tmp/sheet.html'); p.write_text(html)
    rows=(len(svgs)+cols-1)//cols
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page(viewport={'width':int(cols*(W*scale+10)),'height':int(rows*(H*scale+10))})
        pg.goto(p.as_uri()); pg.screenshot(path=out,full_page=True); b.close()
