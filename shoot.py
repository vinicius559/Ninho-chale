import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1] if len(sys.argv)>1 else 'file:///workspace/earny/chale/landing/index.html'
out='/workspace/earny/chale/landing/screenshots/'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for name,vp,mob in [('mobile-390',{'width':390,'height':844},True),('desktop-1440',{'width':1440,'height':900},False)]:
        pg=b.new_page(viewport=vp,device_scale_factor=2 if mob else 1,is_mobile=mob,has_touch=mob)
        errs=[];pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        pg.goto(url,wait_until='networkidle')
        # force lazy images
        pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(1200)
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(600)
        pg.add_style_tag(content=".sticky-cta{display:none!important}")
        pg.screenshot(path=out+name+'.png',full_page=True)
        print(name,pg.evaluate("document.body.scrollHeight"),'errors:',errs,
              'overflowX:',pg.evaluate("document.documentElement.scrollWidth>window.innerWidth"))
    b.close()
