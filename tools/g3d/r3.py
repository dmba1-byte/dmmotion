import sys
from playwright.sync_api import sync_playwright
vs=sys.argv[1:] or ["street","lobby","drive","moto","dog","tailor","site"]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    for v in vs:
        pg=b.new_page(viewport={"width":1280,"height":720});errs=[]
        pg.on("pageerror",lambda e:errs.append(str(e)[:300]));pg.on("console",lambda m:errs.append(m.text[:200]) if m.type=="error" else None)
        pg.goto(f"http://localhost:8765/v3.html?v={v}")
        try:pg.wait_for_function("window.DONE||window.ERR",timeout=240000)
        except Exception:print("timeout")
        print(v,(pg.evaluate("window.ERR||'ok'"))[:400],errs[:2]);pg.locator("#out").screenshot(path=f"v_{v}.png");pg.close()
    b.close()
