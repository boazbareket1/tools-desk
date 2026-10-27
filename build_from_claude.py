"""Rebuild the standalone GitHub copy of the Tools Desk from the Claude artifact page + a database export.
Usage: python3 build_from_claude.py <artifact index.html (no skeleton)> <export dir with tools/ and notes/>"""
import json,glob,os,sys,datetime
art=open(sys.argv[1]).read(); exp=sys.argv[2]
old=open('index.html').read()
prefix=old[:old.index('<title>')]
shim_start=old.index('<script>\n/* Standalone storage')
shim=old[shim_start:old.index('</script>',shim_start)+len('</script>')]
def load(c):
    out={}
    for f in sorted(glob.glob(os.path.join(exp,c,'*.json'))):
        d=json.load(open(f));out[os.path.basename(f)[:-5]]=d.get('data',d)
    return out
ver=datetime.datetime.now().strftime('%Y-%m-%d-%H%M')
seed='const KEY="toolsdesk.v1",SEED='+json.dumps(load('tools'),ensure_ascii=False)+',SEED_NOTES='+json.dumps(load('notes'),ensure_ascii=False)+',SEED_VER="'+ver+'";'
import re
shim=re.sub(r'const KEY="toolsdesk\.v1",SEED=.*?SEED_VER="[^"]*";',lambda m:seed,shim,flags=re.S)
body=art
i=body.index('<script>\nconst CATS')
body=body[:i]+shim+'\n'+body[i:]
body=re.sub(r'<footer>.*?</footer>','<footer>ההערות והעריכות נשמרות בדפדפן הזה בלבד, ונשארות גם כשסוגרים את הדף.</footer>',body,count=1,flags=re.S)
open('index.html','w').write(prefix+body+('' if body.rstrip().endswith('</html>') else '</body></html>\n'))
print('built',ver)
