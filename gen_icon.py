from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random

SIZE = 512
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

cx, cy, R = SIZE // 2, SIZE // 2, 230

# ── Deep shadow ring ─────────────────────────────────────────────────────────
shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([cx - R - 12, cy - R - 12, cx + R + 12, cy + R + 12], fill=(20, 10, 0, 160))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, shadow)
draw = ImageDraw.Draw(img)

# ── Outer bevel ring ─────────────────────────────────────────────────────────
BEVEL = 14
for i in range(BEVEL, 0, -1):
    t = i / BEVEL
    r_val = int(180 + t * 60)
    g_val = int(110 + t * 50)
    b_val = int(10 + t * 10)
    draw.ellipse([cx - R - i, cy - R - i, cx + R + i, cy + R + i],
                 outline=(r_val, g_val, b_val, 255), width=1)

# ── Main coin body — radial gold gradient ────────────────────────────────────
coin_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
cd = ImageDraw.Draw(coin_layer)

steps = 200
for i in range(steps, 0, -1):
    t = i / steps
    r_val = int(80 + t * 155)
    g_val = int(45 + t * 100)
    b_val = int(0 + t * 15)
    alpha = 255
    ri = int(R * (i / steps))
    cd.ellipse([cx - ri, cy - ri, cx + ri, cy + ri],
               fill=(r_val, g_val, b_val, alpha))

img = Image.alpha_composite(img, coin_layer)
draw = ImageDraw.Draw(img)

# ── Specular highlight (top-left arc) ────────────────────────────────────────
hi_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
hd = ImageDraw.Draw(hi_layer)
hd.ellipse([cx - R + 10, cy - R + 10, cx + R - 80, cy + R - 180],
           fill=(255, 240, 160, 60))
hi_layer = hi_layer.filter(ImageFilter.GaussianBlur(22))
img = Image.alpha_composite(img, hi_layer)
draw = ImageDraw.Draw(img)

# ── Dalmatian spots (irregular, scattered, clipped to coin) ──────────────────
rng = random.Random(42)
spot_mask = Image.new("L", (SIZE, SIZE), 0)
sm = ImageDraw.Draw(spot_mask)
sm.ellipse([cx - R + 4, cy - R + 4, cx + R - 4, cy + R - 4], fill=255)

spot_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
spd = ImageDraw.Draw(spot_layer)

spots = [
    (cx - 95,  cy - 60,  22, 18),
    (cx + 75,  cy - 85,  18, 14),
    (cx - 50,  cy + 100, 28, 20),
    (cx + 100, cy + 55,  16, 13),
    (cx - 130, cy + 30,  14, 11),
    (cx + 50,  cy - 130, 12, 16),
    (cx + 130, cy - 30,  10,  8),
    (cx - 80,  cy - 130, 20, 15),
    (cx + 60,  cy + 115, 14, 11),
    (cx - 140, cy - 70,  10,  8),
    (cx + 150, cy + 10,  9,   7),
    (cx - 20,  cy + 155, 11,  9),
    (cx - 170, cy + 80,  8,   6),
    (cx + 30,  cy - 165, 9,   7),
]

for (sx, sy, rw, rh) in spots:
    angle = rng.uniform(0, 360)
    # Slightly irregular ellipse
    col = (40 + rng.randint(-15, 15),
           22 + rng.randint(-8, 8),
           0,
           int(rng.uniform(0.42, 0.62) * 255))
    spd.ellipse([sx - rw, sy - rh, sx + rw, sy + rh], fill=col)

# Soften spots slightly then clip
spot_layer = spot_layer.filter(ImageFilter.GaussianBlur(2))
spot_layer.putalpha(Image.fromarray(
    __import__("numpy").minimum(
        __import__("numpy").array(spot_layer.split()[3]),
        __import__("numpy").array(spot_mask)
    ).astype("uint8")
))
img = Image.alpha_composite(img, spot_layer)
draw = ImageDraw.Draw(img)

# ── Rim / edge detail ─────────────────────────────────────────────────────────
draw.ellipse([cx - R + 2, cy - R + 2, cx + R - 2, cy + R - 2],
             outline=(240, 195, 80, 220), width=3)
draw.ellipse([cx - R + 6, cy - R + 6, cx + R - 6, cy + R - 6],
             outline=(100, 55, 5, 130), width=2)

# ── Inner embossed ring ───────────────────────────────────────────────────────
IR = R - 28
draw.ellipse([cx - IR, cy - IR, cx + IR, cy + IR],
             outline=(200, 150, 40, 90), width=2)
draw.ellipse([cx - IR + 3, cy - IR + 3, cx + IR - 3, cy + IR - 3],
             outline=(255, 220, 100, 50), width=1)

# ── "STC" lettering ────────────────────────────────────────────────────────────
font_path = r"C:\Users\User\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\f02a2201-c42f-4ecd-a20e-e4fb275696f1\9fafb072-e792-44b0-a678-96c03e5398b8\skills\canvas-design\canvas-fonts\BigShoulders-Bold.ttf"
try:
    font_main = ImageFont.truetype(font_path, 130)
except Exception as e:
    print("Font error:", e)
    font_main = ImageFont.load_default()

text = "STC"
bbox = draw.textbbox((0, 0), text, font=font_main)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
tx = cx - tw // 2 - bbox[0]
ty = cy - th // 2 - bbox[1] - 8

# Engraved shadow layer
for dx, dy, alpha in [(-3, 3, 80), (-2, 2, 100), (3, -3, 120), (2, -2, 100)]:
    draw.text((tx + dx, ty + dy), text, font=font_main,
              fill=(30, 15, 0, alpha))

# Main text — deep amber base
draw.text((tx, ty), text, font=font_main, fill=(180, 95, 10, 255))

# Highlight pass
hi_font_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
hfd = ImageDraw.Draw(hi_font_layer)
hfd.text((tx - 1, ty - 2), text, font=font_main, fill=(255, 235, 140, 180))
hi_font_layer = hi_font_layer.filter(ImageFilter.GaussianBlur(2))
img = Image.alpha_composite(img, hi_font_layer)
draw = ImageDraw.Draw(img)

# Crisp top highlight
draw.text((tx, ty), text, font=font_main, fill=(255, 220, 100, 200))

# ── "SpottyCoin" subtitle ─────────────────────────────────────────────────────
font_path2 = r"C:\Users\User\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\f02a2201-c42f-4ecd-a20e-e4fb275696f1\9fafb072-e792-44b0-a678-96c03e5398b8\skills\canvas-design\canvas-fonts\Jura-Light.ttf"
try:
    font_sub = ImageFont.truetype(font_path2, 28)
except:
    font_sub = ImageFont.load_default()

sub = "SpottyCoin"
sbbox = draw.textbbox((0, 0), sub, font=font_sub)
sw = sbbox[2] - sbbox[0]
sx2 = cx - sw // 2 - sbbox[0]
sy2 = cy + 68

draw.text((sx2, sy2), sub, font=font_sub, fill=(80, 40, 5, 160))
draw.text((sx2 - 1, sy2 - 1), sub, font=font_sub, fill=(220, 170, 60, 200))

# ── Final clip to circle ──────────────────────────────────────────────────────
mask = Image.new("L", (SIZE, SIZE), 0)
md = ImageDraw.Draw(mask)
md.ellipse([cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14], fill=255)
img.putalpha(mask)

out_path = r"E:\Work\my-token\spottycoin_icon.png"
img.save(out_path, "PNG")
print(f"Saved: {out_path}")
