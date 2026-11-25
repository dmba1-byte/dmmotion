import sys,base64,os,subprocess
from playwright.sync_api import sync_playwright
args=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    for a in args:
        v,_,n=a.partition(':');n=int(n or 0)
        pg=b.new_page(viewport={"width":1280,"height":720});errs=[]
        pg.on("pageerror",lambda e:errs.append(str(e)[:400]));pg.on("console",lambda m:errs.append(m.text[:300]) if m.type=="error" else None)
        pg.goto(f"http://localhost:8765/v4.html?v={v}")
        try:pg.wait_for_function("window.DONE||window.ERR",timeout=300000)
        except Exception:print("timeout")
        print(v,(pg.evaluate("window.ERR||'ok'"))[:500],errs[:2],flush=True)
        if n==0: pg.locator("#out").screenshot(path=f"w_{v}.png")
        else:
            os.makedirs(f"fr_{v}",exist_ok=True)
            for i in range(n):
                d=pg.evaluate(f"step({i})");open(f"fr_{v}/{i:03d}.jpg","wb").write(base64.b64decode(d.split(',')[1]))
            print(v,"frames",n,errs[:2],flush=True)
        pg.close()
    b.close()
