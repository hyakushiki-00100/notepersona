"""カバー画像の共通関数(1280x670)。シリーズ追加時はこれを使う。"""
from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
W,H=1280,670
def _base(bg,acc):
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    mix=lambda r:tuple(int(x*r+b*(1-r)) for x,b in zip(acc,bg))
    d.rectangle([0,0,W,18],fill=acc); d.rectangle([0,H-18,W,H],fill=acc)
    d.ellipse([W-260,-160,W+140,240],fill=mix(0.15)); d.ellipse([-180,H-200,180,H+160],fill=mix(0.12))
    return im,d
def _pill(d,text,y,size,acc):
    f=ImageFont.truetype(F,size); tw=d.textlength(text,font=f); px=(W-tw)/2
    d.rounded_rectangle([px-28,y-14,px+tw+28,y+size+14],radius=(size+28)//2,fill=acc); d.text((px,y),text,font=f,fill=(255,255,255))
def volume(path,label,n,lines,bg,acc):
    im,d=_base(bg,acc); _pill(d,f"{label}  第{n}巻",110,34,acc)
    s=84
    while max(d.textlength(l,font=ImageFont.truetype(F,s)) for l in lines)>1080: s-=2
    f=ImageFont.truetype(F,s); gap=int(s*0.45); y=(H-(2*s+gap))/2+40
    for l in lines:
        w=d.textlength(l,font=f); d.text(((W-w)/2,y),l,font=f,fill=acc,stroke_width=1,stroke_fill=acc); y+=s+gap
    d.line([(W/2-60,y+18),(W/2+60,y+18)],fill=acc,width=4); im.save(path)
def magazine(path,top,main,sub,steps,bg,acc):
    im,d=_base(bg,acc); _pill(d,f"マガジン  全{len(steps)}巻",78,32,acc)
    y=165
    for size,l in [(64,top),(96,main)]:
        f=ImageFont.truetype(F,size)
        while d.textlength(l,font=f)>1100: size-=4; f=ImageFont.truetype(F,size)
        w=d.textlength(l,font=f); d.text(((W-w)/2,y),l,font=f,fill=acc,stroke_width=1,stroke_fill=acc); y+=size+22
    fs=ImageFont.truetype(F,32); w=d.textlength(sub,font=fs); d.text(((W-w)/2,y+6),sub,font=fs,fill=acc)
    cf=ImageFont.truetype(F,26); pad,gap=18,14
    ws=[d.textlength(s,font=cf)+pad*2 for s in steps]; x=(W-sum(ws)-gap*(len(ws)-1))/2
    for s,wd in zip(steps,ws):
        d.rounded_rectangle([x,520,x+wd,570],radius=25,outline=acc,width=3,fill=bg); d.text((x+pad,531),s,font=cf,fill=acc); x+=wd+gap
    im.save(path)
