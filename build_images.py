# Gera imagens otimizadas da LP a partir dos renders (rodar da pasta earny/chale)
from PIL import Image, ImageDraw, ImageFont
import os
T='tmp/lote-v2/final/'; B='tmp/lote-v2-bloco2/final/'; O='landing/img/'
src={'fachada':T+'hero.png','vista2':T+'second.png','interior':T+'interior.png','implantacao':T+'site.png',
     'entardecer':B+'dusk.png','varanda':B+'porch.png','empena':B+'gable.png','interior2':B+'interior2.png'}
for k,f in src.items():
    im=Image.open(f).convert('RGB')
    for w in (1080,640):
        r=im if w==1080 else im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
        q=80
        while True:
            p=f'{O}{k}-{w}.webp'; r.save(p,'WEBP',quality=q,method=6)
            if os.path.getsize(p)<290_000 or q<50: break
            q-=5
# planta (recorte, fundo creme)
pl=Image.open('tmp/lote-v2/view/plan_final2.png').convert('RGB').crop((90,190,1000,1150))
pl.save(O+'planta.webp','WEBP',quality=88,method=6)
pl.resize((640,round(pl.height*640/pl.width)),Image.LANCZOS).save(O+'planta-640.webp','WEBP',quality=88,method=6)
# OG 1200x630
og=Image.new('RGB',(1200,630),'#F5F0E8')
h=Image.open(T+'hero.png').convert('RGB')
s=h.resize((760,950),Image.LANCZOS)
og.paste(s.crop((0,170,700,800)),(0,0))
d=ImageDraw.Draw(og)
FR='/usr/share/fonts/truetype/sand-box/google/Fraunces/Fraunces-VariableFont_SOFT,WONK,opsz,wght.ttf'
IN='/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf'
def font(p,sz,w):
    f=ImageFont.truetype(p,sz)
    try:
        axes=f.get_variation_axes(); vals=[]
        for a in axes:
            n=a.get('name',b'');n=n.decode() if isinstance(n,bytes) else n
            vals.append(w if 'eight' in n else (min(max(sz,a['minimum']),a['maximum']) if 'ptical' in n else a['default']))
        f.set_variation_by_axes(vals)
    except Exception as e: print('var',e)
    return f
d.text((750,90),'ninho',font=font(IN,44,500),fill='#111111')
d.line((752,150,900,150),fill='#6F0712',width=3)
y=200
for line in ['Chalé de campo,','leve de construir.']:
    d.text((750,y),line,font=font(FR,46,500),fill='#111111'); y+=58
y+=24
for line in ['Planos digitais · 42 m² · alvenaria','PDF + DWG · Santa Catarina e Sul']:
    d.text((750,y),line,font=font(IN,22,400),fill='#333333'); y+=32
d.text((750,y+28),'R$ 447',font=font(FR,52,600),fill='#6F0712')
d.text((750,575),'Render 3D ilustrativo',font=font(IN,16,400),fill='#777777')
og.save('landing/og-image.jpg','JPEG',quality=85,optimize=True,progressive=True)
# favicons
def mark(size,bg='#F5F0E8'):
    S=size*4; im=Image.new('RGBA',(S,S),bg); dd=ImageDraw.Draw(im); k=S/120
    import math
    def bez(p0,p1,p2,p3,n=40):
        return [tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*e for a,b,c,e in zip(p0,p1,p2,p3)) for t in [i/n for i in range(n+1)]]
    # zoom: content spans ~24..96 x, 32..76 y -> scale 1.45 around center (60,56)
    z=1.5; cx,cy=60,58
    def tr(pts): return [((x-cx)*z*k+S/2,(y-cy)*z*k+S/2) for x,y in pts]
    for (a,b,c,e,w) in [((28,62),(36,78),(84,78),(92,62),4.5),((34,54),(40,66),(80,66),(86,54),3.5),((42,48),(48,56),(72,56),(78,48),3)]:
        dd.line(tr(bez(a,b,c,e)),fill='#111111',width=max(1,round(w*1.3*z*k/1.3)),joint='curve')
    dd.line(tr([(52,46),(60,36),(68,46)]),fill='#6F0712',width=round(3*z*k),joint='curve')
    dd.rectangle([*tr([(54,46)])[0],*tr([(66,56)])[0]],outline='#6F0712',width=round(2.5*z*k))
    return im.resize((size,size),Image.LANCZOS).convert('RGB')
mark(32).save('landing/favicon-32.png'); mark(180).save('landing/apple-touch-icon.png'); mark(512).save('landing/icon-512.png')
mark(48).save('landing/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
