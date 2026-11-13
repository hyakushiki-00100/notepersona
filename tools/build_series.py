"""シリーズ一式を生成する。
使い方: python3 tools/build_series.py <設定.json>
生成物: note貼り付け用 / 各巻カバー / マガジンカバー / 紹介文(intros.mdに追記) / 合本md / Word合本 / 一式zip
"""
import json,sys,os,re,shutil,subprocess,tempfile,unicodedata,zipfile
sys.path.insert(0,os.path.dirname(__file__))
import covers
from make_note_paste import conv
c=json.load(open(sys.argv[1],encoding='utf-8'))
name,prefix,bg,acc=c['name'],c['prefix'],tuple(c['bg']),tuple(c['acc'])
vols=c['volumes']; tmp=tempfile.mkdtemp()
W=lambda s:sum(2 if unicodedata.east_asian_width(ch) in 'WFA' else 1 for ch in s)
cnt=lambda s:len(re.sub(r'\s','',re.sub(r'[#*>|\-]','',s)))
os.makedirs(f'note-paste/{name}',exist_ok=True)
for i,v in enumerate(vols,1):
    src=f"manuscripts/{prefix}-{v['id']}.md"
    t=conv(src); assert '**' not in t and '|' not in t
    open(f"note-paste/{name}/{i:02d}_{v['id']}.txt",'w',encoding='utf-8').write(t)
    covers.volume(f"covers/{c['short']}_{i:02d}_{v['id']}.png",name,i,v['cover'],bg,acc)
covers.magazine(f"covers-magazine/magazine_{prefix}.png",*c['magazine_title'],c['magazine_sub'],[v['step'] for v in vols],bg,acc)
# 紹介文
TAIL="価格300円/約1,400字・10分で読めます。"
L=[f"## {name}シリーズ",""]
for i,v in enumerate(vols,1):
    full=v['intro']+TAIL; xt=f"【{name} 第{i}巻】\n{v['x']}\n{c['hashtag']}\n[noteのURL]"
    xw=W(xt.replace('[noteのURL]',''))+23; assert xw<=280,(v['id'],xw)
    L+=[f"### 第{i}巻({v['id']})","",f"**note用紹介文**({len(full)}字)","",full,"",f"**X用告知文**(X換算 {xw}/280)","","```",xt,"```",""]
    print(f"第{i}巻 本文{cnt(open(f'manuscripts/{prefix}-{v['id']}.md',encoding='utf-8').read().split(chr(10),1)[1])}字 紹介{len(full)}字 X{xw}")
L+=[f"### {name}マガジン({len(c['magazine_desc'])}字)","",c['magazine_desc'],""]
p='intros/intros.md'; t=open(p,encoding='utf-8').read()
assert f"## {name}シリーズ" not in t, '紹介文は既に追記済み'
k=t.index('## マガジン説明文'); open(p,'w',encoding='utf-8').write(t[:k]+'\n'.join(L)+'\n'+t[k:])
# 合本
parts=[f"# {name}シリーズ 全{len(vols)}巻","","共通:価格300円/1,500字前後/読了10分以内"]
for i,v in enumerate(vols,1):
    body=open(f"manuscripts/{prefix}-{v['id']}.md",encoding='utf-8').read()
    parts+=["","---","",re.sub(r'^# ',f'# 【第{i}巻】',body,count=1)]
allmd='\n'.join(parts); open(f'manuscripts/{prefix}-all.md','w',encoding='utf-8').write(allmd)
shutil.copy(f'manuscripts/{prefix}-all.md',f'dist/{name}_全{len(vols)}巻.md')
pb='\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'
open(f'{tmp}/a.md','w',encoding='utf-8').write('\n'.join(pb if l.strip()=='---' else l for l in allmd.split('\n')))
subprocess.run(['pandoc',f'{tmp}/a.md','-f','markdown','-o',f'dist/{name}_全{len(vols)}巻.docx'],check=True)
# 一式zip
zp=f'dist/{name}_一式.zip'
if os.path.exists(zp): os.remove(zp)
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
    for i,v in enumerate(vols,1):
        z.write(f"manuscripts/{prefix}-{v['id']}.md",f"原稿/{i:02d}_{v['id']}.md")
        z.write(f"note-paste/{name}/{i:02d}_{v['id']}.txt",f"note貼り付け用/{i:02d}_{v['id']}.txt")
        z.write(f"covers/{c['short']}_{i:02d}_{v['id']}.png",f"カバー/{c['short']}_{i:02d}_{v['id']}.png")
    z.write(f"covers-magazine/magazine_{prefix}.png",f"カバー/magazine_{prefix}.png")
    z.write(f'dist/{name}_全{len(vols)}巻.docx',f'{name}_全{len(vols)}巻.docx')
    z.writestr('販売紹介文.md','# 販売紹介文\n\n'+'\n'.join(L))
print('zip',zp,'files',len(zipfile.ZipFile(zp).namelist()),'mag',len(c['magazine_desc']))
