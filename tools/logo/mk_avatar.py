"""Build circle-safe Gmail / profile avatars from the DM mark."""
from PIL import Image

SRC = '/home/claude/logo/DM_logo_mark-black_1024.png'
OUT = '/home/claude/logo/'
SIZE = 1024

src = Image.open(SRC).convert('RGBA')

# The artwork is dark ink on transparent/white. Build a clean alpha mask from it.
r, g, b, a = src.split()
lum = Image.merge('RGB', (r, g, b)).convert('L')
# ink = dark pixels that are actually present
mask = lum.point(lambda v: 255 - v)
mask = Image.composite(mask, Image.new('L', src.size, 0), a.point(lambda v: 255 if v > 8 else 0))
# the ink is #1f1f1f, not pure black, so the raw mask tops out around 224.
# stretch it so solid ink is fully opaque and only the antialiased edge stays soft.
peak = max(1, mask.getextrema()[1])
mask = mask.point(lambda v: min(255, round(v * 255 / peak)))

# crop to the ink bounding box so padding is exact
bbox = mask.getbbox()
mask = mask.crop(bbox)


def avatar(fname, bg, ink, inset=0.66):
    """inset = mark width as a fraction of the full canvas.
    0.60 keeps every corner of the square mark inside Gmail's circle crop."""
    canvas = Image.new('RGBA', (SIZE, SIZE), bg)
    target = int(SIZE * inset)
    w, h = mask.size
    s = target / max(w, h)
    m = mask.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    layer = Image.new('RGBA', m.size, ink)
    layer.putalpha(m)
    canvas.alpha_composite(layer, ((SIZE - m.size[0]) // 2, (SIZE - m.size[1]) // 2))
    canvas.convert('RGB').save(OUT + fname, 'PNG')
    print('wrote', OUT + fname)


avatar('DM_avatar_white.png',     (255, 255, 255, 255), (20, 20, 20, 255))
avatar('DM_avatar_black.png',     (20, 20, 20, 255),    (255, 255, 255, 255))
avatar('DM_avatar_blueprint.png', (29, 78, 137, 255),   (255, 255, 255, 255))
avatar('DM_avatar_green.png',     (46, 155, 98, 255),   (255, 255, 255, 255))
