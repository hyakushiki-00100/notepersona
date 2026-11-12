"""manuscripts/*.md を note貼り付け用テキストに変換する。
使い方: python3 tools/make_note_paste.py <入力.md> <出力.txt>
変換: 表→箇条書き / ## →■ / 引用→全角字下げ / 太字記号除去 / 有料ライン→目印行
"""
import re,sys
def conv(src):
    L=open(src,encoding='utf-8').read().split('\n'); out=[]; i=0
    while i<len(L):
        l=L[i]
        if l.startswith('|'):
            rows=[]
            while i<len(L) and L[i].startswith('|'):
                c=[x.strip() for x in L[i].strip('|').split('|')]
                if not all(re.fullmatch(r'-+',x) for x in c): rows.append(c)
                i+=1
            h=rows[0]
            for r in rows[1:]:
                out.append('・'+r[0])
                for hh,v in zip(h[1:],r[1:]): out.append(f'　{hh}:{v}')
            continue
        if l.startswith('# '): out+=['【タイトル】'+l[2:],'(↑noteのタイトル欄に入力。本文には貼らない)']
        elif l.startswith('## '): out.append('■'+l[3:])
        elif 'ここから有料' in l: out.append('▼▼▼ ここに有料ラインを設定 ▼▼▼')
        elif l.startswith('> '): out.append('　'+l[2:])
        elif l.startswith('- '): out.append('・'+l[2:])
        else: out.append(l)
        i+=1
    return '\n'.join(out).replace('**','')
if __name__=='__main__':
    open(sys.argv[2],'w',encoding='utf-8').write(conv(sys.argv[1]))
