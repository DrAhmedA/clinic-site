from pathlib import Path
from html.parser import HTMLParser
text = Path('index.html').read_text(encoding='utf-8')
class TagChecker(HTMLParser):
    void_tags = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.void_tags:
            self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            self.errors.append((tag, self.getpos(), self.stack[-1] if self.stack else None))
    def handle_startendtag(self, tag, attrs):
        pass
    def close(self):
        super().close()
        return self.stack, self.errors
checker = TagChecker();
checker.feed(text)
stack, errors = checker.close()
print('unclosed=', len(stack))
for tag,pos in stack[-20:]:
    print('OPEN', tag, pos)
print('errors=', len(errors))
for e in errors[:50]:
    print('ERROR', e)
