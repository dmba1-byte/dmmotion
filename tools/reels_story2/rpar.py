import asyncio, sys, os
from playwright.async_api import async_playwright
N=int(58.6*30); W=3
async def worker(p,w):
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
    await pg.goto('file:///home/claude/reels/story2/full2_run.html')
    for i in range(w,N,W):
        await pg.evaluate(f'setT({i/30})'); await pg.screenshot(path=f'ff2/{i:05d}.png')
    await b.close()
async def main():
    os.makedirs("ff2",exist_ok=True)
    async with async_playwright() as p:
        await asyncio.gather(*[worker(p,w) for w in range(W)])
asyncio.run(main())
