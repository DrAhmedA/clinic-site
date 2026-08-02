from pathlib import Path
import re
text = Path('index.html').read_text(encoding='utf-8')
lines = text.splitlines()
voids = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
stack=[]
errors=[]
for pos,(slash,tag) in enumerate(re.findall(r'<(/?)([a-zA-Z0-9:-]+)', text),1):
    tag=tag.lower()
    if tag in voids: continue
    if slash=='':
        stack.append((tag,pos))
    else:
        if stack and stack[-1][0]==tag:
            stack.pop()
        else:
            errors.append((tag,pos, stack[-1] if stack else None))
print('unclosed', len(stack))
for tag,pos in stack[-10:]:
    print('OPEN', tag, pos)
print('errors', len(errors))
for e in errors[:20]:
    print('ERROR', e)
# report tag counts
for t in ['html','body','main','section','div']:
    opens = sum(1 for m in re.findall(r'<(/?)([a-zA-Z0-9:-]+)', text) if m[1].lower()==t and m[0]=='')
    closes = sum(1 for m in re.findall(r'<(/?)([a-zA-Z0-9:-]+)', text) if m[1].lower()==t and m[0]=='/')
    print(t, opens, closes)
# show lines around unmatched positions
for tag,pos in stack[-5:]:
    print('stack', tag, pos)
for tag,pos,_ in errors[:10]:
    print('error', tag, pos)
