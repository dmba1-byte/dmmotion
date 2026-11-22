import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg=b.new_page(viewport={"width":1100,"height":508})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)[:400]));pg.on("console",lambda m:errs.append(m.text[:300]) if m.type=="error" else None)
    pg.goto("http://localhost:8765/game3d.html")
    try:pg.wait_for_function("window.DONE||window.ERR",timeout=180000)
    except Exception as e:print("timeout")
    print(pg.evaluate("window.ERR||'ok'"),errs[:4])
    def shot(n,js=None,wait=2500,key=None):
        if js:pg.evaluate(js)
        if key:pg.keyboard.down(key)
        pg.wait_for_timeout(wait)
        pg.screenshot(path=n)
        if key:pg.keyboard.up(key)
    shot("q1.png",wait=3000)
    shot("q3.png","K.x=560;K.z=70",key="d")
    shot("q5.png","K.x=-150;K.z=260;K.bike=true;K.lastH='r'",key="d",wait=1800)
    pg.evaluate("K.bike=false;K.x=60;K.z=80");pg.keyboard.press("Space");pg.wait_for_timeout(260);pg.screenshot(path="q8.png")
    pg.wait_for_timeout(800);pg.keyboard.press("f");pg.wait_for_timeout(90);pg.screenshot(path="q9.png")
    shot("q4.png","K.x=0;K.z=560;K.face='d'",wait=2500)
    print(pg.evaluate("JSON.stringify(K)"),errs[:4]);b.close()
