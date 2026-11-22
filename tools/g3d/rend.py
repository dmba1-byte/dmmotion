import sys
from playwright.sync_api import sync_playwright
shots=sys.argv[1:] or ["street:wide","street:door","lobby:top"]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    for s in shots:
        sc,cm=s.split(":");pg=b.new_page(viewport={"width":1280,"height":720})
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)[:300]));pg.on("console",lambda m:errs.append(m.text[:200]) if m.type=="error" else None)
        pg.goto(f"http://localhost:8765/scene.html?s={sc}&cam={cm}")
        try: pg.wait_for_function("window.DONE||window.ERR",timeout=120000)
        except Exception as e: print("timeout")
        print(s,pg.evaluate("window.ERR||'ok'"),errs[:3]);pg.locator("#out").screenshot(path=f"r_{sc}_{cm}.png");pg.close()
    b.close()
