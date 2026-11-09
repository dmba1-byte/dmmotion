import base64,re
D='/home/claude/dmmotion/'
tpl=open('/home/claude/vox/site_tpl.html').read()
names=re.findall(r'\{\{([a-z_]+)\}\}',tpl)
def uri(n):
    p={'logo':D+'dm-logo.png','measure':D+'px/kit/measure.png'}.get(n,D+f'px/kit/{n}.png')
    return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
art=tpl
for n in set(names):art=art.replace('{{'+n+'}}',uri(n))
open('/home/claude/vox/kit_site.html','w').write(art)
rel=tpl
for n in set(names):
    rel=rel.replace('{{'+n+'}}','dm-logo.png' if n=='logo' else 'px/kit/measure.png' if n=='measure' else f'px/kit/{n}.png')
rel=rel.replace('<title>','<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="dm-logo.png">\n<title>',1).replace('<meta name="claude:viewport-fit-sides" content="cover">','')
rel=rel.replace('</style>','</style></head><body>',1)+'\n</body></html>'
open(D+'index.html','w').write(rel);open(D+'preview.html','w').write(rel)
open(D+'services.html','w').write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html#studio"><link rel="canonical" href="index.html#studio"><title>DM Motion</title><a href="index.html#studio">Continue</a>')
print(len(art),len(rel))
