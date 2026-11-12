from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
W,H=1280,670
data={
 '渡す側':dict(bg=(244,240,232),acc=(31,58,95),label='引き継ぎ・渡す側',names=['ichiran','anmoku','shiryo','setsumei','doko','saishu','toiawase'],
  c=[("業務一覧は","「1行=1回」で書く"),("一覧に載らない作業は","記録から拾う"),("引き継ぎ資料は","「辞書」として書く"),("説明は聞かせるより","「言い直してもらう」"),("同行は「やってもらって」","黙って見る"),("最終確認は","権限・連絡先・期限だけ"),("異動後の問い合わせは","「期間と窓口」を決める")]),
 '受ける側':dict(bg=(236,243,238),acc=(38,92,74),label='引き継ぎ・受ける側',names=['yomikomi','kikikata','more','fuzai','yusen','kaeru'],
  c=[("引き継ぎ資料は","「質問を作るため」に読む"),("打ち合わせでは","「いつ・誰が困るか」を聞く"),("引き継ぎ漏れは","「1週間分まとめて」聞く"),("前任者がいないなら","「頼んでいた人」から逆算"),("着任後1か月は","「期限」で並べる"),("やり方を変えるのは","「1周回してから」")]),
}
def fit(d,lines,maxw,start):
    s=start
    while True:
        f=ImageFont.truetype(F,s)
        if max(d.textlength(l,font=f) for l in lines)<=maxw: return f,s
        s-=2
for ser,cfg in data.items():
    for i,(nm,lines) in enumerate(zip(cfg['names'],cfg['c']),1):
        im=Image.new('RGB',(W,H),cfg['bg']); d=ImageDraw.Draw(im); a=cfg['acc']
        mix=lambda r:tuple(int(c*r+b*(1-r)) for c,b in zip(a,cfg['bg']))
        d.rectangle([0,0,W,18],fill=a); d.rectangle([0,H-18,W,H],fill=a)
        d.ellipse([W-260,-160,W+140,240],fill=mix(0.15)); d.ellipse([-180,H-200,180,H+160],fill=mix(0.12))
        lf=ImageFont.truetype(F,34); lab=f"{cfg['label']}  第{i}巻"
        tw=d.textlength(lab,font=lf); px,py=(W-tw)/2,110
        d.rounded_rectangle([px-28,py-14,px+tw+28,py+48],radius=31,fill=a); d.text((px,py),lab,font=lf,fill=(255,255,255))
        f,s=fit(d,list(lines),1080,84); gap=int(s*0.45); y=(H-(2*s+gap))/2+40
        for l in lines:
            w=d.textlength(l,font=f); d.text(((W-w)/2,y),l,font=f,fill=a,stroke_width=1,stroke_fill=a); y+=s+gap
        d.line([(W/2-60,y+18),(W/2+60,y+18)],fill=a,width=4)
        im.save(f'covers/{ser}_{i:02d}_{nm}.png')
