# -*- coding: utf-8 -*-
"""生成 4 张交付配图 -> /workspace"""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode

WS = "/workspace"
os.makedirs(WS, exist_ok=True)

REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def F(sz, bold=False): return ImageFont.truetype(BOLD if bold else REG, sz, index=2)

# 配色：深玫瑰夜空
C_BG1=(21,10,31); C_BG2=(46,20,48); C_BG3=(74,31,62)
C_GOLD=(247,178,201); C_GOLD2=(201,167,235)
C_TEXT=(245,236,243); C_MUTED=(189,164,182)
C_BEIGE=(244,237,227); C_INK=(58,38,52); C_ROSE=(176,84,116)

URL = "https://xiaochuan2026.github.io/tianming-attachment/"

def gradient(size):
    w,h=size
    img=np.zeros((h,w,3),dtype=np.uint8)
    for y in range(h):
        t=y/(h-1)
        if t<0.5:
            a=t/0.5; c=tuple(int(C_BG1[i]+(C_BG2[i]-C_BG1[i])*a) for i in range(3))
        else:
            a=(t-0.5)/0.5; c=tuple(int(C_BG2[i]+(C_BG3[i]-C_BG2[i])*a) for i in range(3))
        img[y,:]=c
    return Image.fromarray(img).convert("RGB")

def glow(base, cx, cy, r, color, alpha=120):
    lay=Image.new("RGBA", base.size, (0,0,0,0))
    d=ImageDraw.Draw(lay)
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=color+(255,))
    lay=lay.filter(ImageFilter.GaussianBlur(r*0.8))
    lay.putalpha(alpha)
    return Image.alpha_composite(base.convert("RGBA"), lay).convert("RGB")

def wrap(text, font, maxw):
    lines=[]; cur=""
    for ch in text:
        if ch=="\n": lines.append(cur); cur=""; continue
        test=cur+ch
        if font.getlength(test)>maxw and cur: lines.append(cur); cur=ch
        else: cur=test
    if cur: lines.append(cur)
    return lines

def draw_text(d, xy, text, font, fill, anchor="mm", align="center"):
    d.text(xy, text, font=font, fill=fill, anchor=anchor, align=align)

def rr(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def make_qr():
    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
    qr.add_data(URL); qr.make(fit=True)
    return qr.make_image(fill_color="#2a0f24", back_color="white").convert("RGB")

# ============ POSTER 1080x1440 ============
def poster():
    W,H=1080,1440
    img=gradient((W,H))
    img=glow(img, 200, 230, 300, C_GOLD, 90)
    img=glow(img, 920, 1150, 320, C_GOLD2, 80)
    img=glow(img, 980, 260, 220, C_GOLD2, 50)
    d=ImageDraw.Draw(img)
    pill="依恋风格 · 心理测评"
    pf=F(30,True); pw=pf.getlength(pill)+60
    rr(d,(W/2-pw/2,90,W/2+pw/2,90+64),32,fill=(255,255,255,22),outline=C_GOLD,width=2)
    draw_text(d,(W/2,122),pill,pf,fill=C_GOLD)
    tf=F(78,True)
    draw_text(d,(W/2,250),"你是哪种依恋类型？",tf,fill=C_TEXT)
    sf=F(33)
    for i,line in enumerate(wrap("恋爱里你是哪一种？看清自己的相处模式，把关系处得更舒服。", sf, 880)):
        draw_text(d,(W/2,360+i*46),line,sf,fill=C_MUTED)
    tf2=F(40,True)
    draw_text(d,(W/2,500),"4 大依恋 · 8 种细分",tf2,fill=C_GOLD2)
    qr=make_qr().resize((300,300))
    card_x,card_y,cw,ch=W/2-210,620,420,470
    rr(d,(card_x,card_y,card_x+cw,card_y+ch),28,fill=(255,255,255,235))
    img.paste(qr,(int(W/2-150),int(card_y+40)))
    qf=F(30,True)
    draw_text(d,(W/2,card_y+ch-46),"扫码测一测你的依恋类型",qf,fill=C_INK)
    cf=F(30,True)
    draw_text(d,(W/2,H-70),"原创出品 © 小船",cf,fill=C_GOLD)
    img.save(os.path.join(WS,"tianming_attachment_poster.png"))
    print("poster saved")

# ============ COVER 1080x1440（作品封面：带「依恋」圆圈 + 卖点小字，无二维码） ============
def cover():
    W,H=1080,1440
    img=gradient((W,H))
    img=glow(img, 200, 250, 320, C_GOLD, 70)
    img=glow(img, 920, 1180, 340, C_GOLD2, 60)
    d=ImageDraw.Draw(img)
    # pill
    pill="依恋风格 · 心理测评"
    pf=F(30,True); pw=pf.getlength(pill)+60
    rr(d,(W/2-pw/2,150,W/2+pw/2,150+64),32,fill=(255,255,255,22),outline=C_GOLD,width=2)
    draw_text(d,(W/2,182),pill,pf,fill=C_GOLD)
    # title
    tf=F(76,True)
    draw_text(d,(W/2,330),"你是哪种依恋类型？",tf,fill=C_TEXT)
    # 卖点小字
    sf=F(32)
    draw_text(d,(W/2,410),"看清你的相处模式，把关系处得更舒服",sf,fill=C_MUTED)
    # 「依恋」圆圈
    cx,cy=540,640
    d.ellipse([cx-180,cy-180,cx+180,cy+180], outline=C_GOLD, width=5)
    d.ellipse([cx-150,cy-150,cx+150,cy+150], outline=C_GOLD2, width=2)
    ef=F(120,True)
    draw_text(d,(cx,cy),"依恋",ef,fill=C_TEXT)
    # 类型小字
    tf2=F(34,True)
    draw_text(d,(W/2,860),"4 大依恋类型 · 8 种细分风格",tf2,fill=C_GOLD2)
    # 底部卖点
    hf=F(28,True)
    draw_text(d,(W/2,940),"心理测评 · 单主结果 · 丰富解读",hf,fill=C_GOLD)
    # copyright
    cf=F(30,True)
    draw_text(d,(W/2,H-70),"原创出品 © 小船",cf,fill=C_GOLD)
    img.save(os.path.join(WS,"tianming_attachment_cover.png"))
    print("cover saved")

# ============ DETAIL 1080 x auto ============
TYPES=[
 ("安全型","安全自在型","松弛 · 信任 · 边界","自带安全感，爱得从容，也放得下。"),
 ("安全型","温暖滋养型","主动 · 共情 · 稳定","关系里的小太阳，擅长把爱说出口。"),
 ("焦虑型","焦虑粘人型","焦虑 · 索取确认 · 敏感","爱得用力，越在乎越怕抓不住。"),
 ("焦虑型","试探博弈型","试探 · 内耗 · 患得患失","不敢直接要爱，用推开测试爱。"),
 ("回避型","回避疏离型","回避 · 独立 · 隔离","不是不爱，是不知道怎么靠太近。"),
 ("回避型","高冷抽离型","抽离 · 自我 · 压抑","心门锁得很死，亲密对你像危险。"),
 ("恐惧型","恐惧纠结型","恐惧 · 推拉 · 矛盾","又想靠近又怕被伤，于是边爱边逃。"),
 ("恐惧型","崩塌逃离型","逃离 · 自我保护 · 崩塌","关系一认真，就想先跑为敬。"),
]
def detail():
    W=1080
    head=300; card_h=196; gap=22; foot=90
    H=head+len(TYPES)*(card_h+gap)+foot
    img=gradient((W,H))
    img=glow(img,180,160,260,C_GOLD,70)
    img=glow(img,920,H-260,300,C_GOLD2,60)
    d=ImageDraw.Draw(img)
    hf=F(46,True); draw_text(d,(W/2,90),"8 种依恋细分类型",hf,fill=C_GOLD)
    sf=F(30); draw_text(d,(W/2,150),"从安全 / 焦虑 / 回避 / 恐惧，再细到你的专属相处模式",sf,fill=C_MUTED)
    draw_text(d,(W/2,200),"测完你会拿到：组合词拆解 · 典型表现 · 对恋人影响 · 怎么调整",sf,fill=C_MUTED)
    y=head
    for cat,name,chips,one in TYPES:
        x0,x1=60,W-60
        rr(d,(x0,y,x1,y+card_h),22,fill=(55,25,50),outline=C_GOLD,width=2)
        cf=F(26,True); draw_text(d,(x0+150,y+44),cat,cf,fill=C_GOLD2,anchor="mm")
        nf=F(42,True); draw_text(d,(x0+150,y+96),name,nf,fill=C_TEXT,anchor="mm")
        chf=F(27); draw_text(d,(x0+150,y+150),chips,chf,fill=C_GOLD,anchor="mm")
        olf=F(28)
        lines=wrap(one, olf, 360)
        ty=y+card_h/2-(len(lines)-1)*20
        for ln in lines:
            draw_text(d,(x1-30,ty),ln,olf,fill=C_MUTED,anchor="rm")
            ty+=40
        y+=card_h+gap
    cf=F(30,True); draw_text(d,(W/2,H-46),"原创出品 © 小船",cf,fill=C_GOLD)
    img.save(os.path.join(WS,"tianming_attachment_detail.png"))
    print("detail saved", H)

# ============ DISCLAIMER 1280x720 ============
def disclaimer():
    W,H=1280,720
    img=Image.new("RGB",(W,H),C_BEIGE)
    d=ImageDraw.Draw(img)
    img=glow(img,80,80,260,C_GOLD,40)
    img=glow(img,W-60,H-60,260,C_GOLD2,35)
    d=ImageDraw.Draw(img)
    tf=F(50,True); draw_text(d,(W/2,90),"产品说明",tf,fill=C_ROSE)
    items=[
      "本商品为虚拟电子资料，内容为「依恋类型」在线心理测评。",
      "不邮寄实物，下单后自动发送测试链接，凭链接即可进入。",
      "虚拟资料一经售出，不退不换，请确认需求后再下单。",
      "结果仅供娱乐与自我觉察参考，不构成任何专业心理诊断。",
    ]
    bf=F(33)
    y=200
    for it in items:
        draw_text(d,(120,y),"▪",F(34,True),fill=C_ROSE,anchor="lm")
        ln=wrap(it,bf,W-300)
        draw_text(d,(170,y),ln[0],bf,fill=C_INK,anchor="lm")
        yy=y+50
        for extra in ln[1:]:
            draw_text(d,(170,yy),extra,bf,fill=C_INK,anchor="lm"); yy+=50
        y+=max(50,50*len(ln))+34
    cf=F(30,True); draw_text(d,(W/2,H-54),"原创出品 © 小船",cf,fill=C_ROSE)
    img.save(os.path.join(WS,"tianming_attachment_disclaimer.png"))
    print("disclaimer saved")

poster(); cover(); detail(); disclaimer()
print("ALL IMAGES DONE")
