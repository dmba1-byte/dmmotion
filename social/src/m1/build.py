h=open('/home/claude/vox/r1/reel1_head.js').read();a=h.index("// ---------- timeline");b=h.index("// ---------- room ----------");h=h[:a]+"const SUBSDUMMY=0;\n"+h[b:]
r1=open('/home/claude/vox/r1/reel1_scenes.js').read()
wp=r1[r1.index("function wipe"):r1.index("function frameAt")]
css=open('/home/claude/vox/r1/silk.css').read();base=open('/home/claude/vox/strips.html').read()
D='/home/claude/vox/m1/'
js="\n".join(open(D+f).read() for f in ['lib5.js','fbcore.js','fx.js','m1_scenes.js'])
open(D+'m1.html','w').write('<meta charset="utf-8"><style>'+css+'html,body{margin:0;background:#000}#c{display:none}#out{display:block;width:1080px;height:1920px}</style>'+base+'<canvas id=out width=1080 height=1920></canvas><script>'+h+"\n"+wp+"\n"+js+'</script>')
