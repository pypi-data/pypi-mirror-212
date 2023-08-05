from .html import HtmlNode
from html.parser import HTMLParser

class Parser(HTMLParser):
    void_tags = [
        'area', 'base', 'br', 'col',
        'embred', 'hr', 'img', 'input',
        'link', 'meta', 'source', 'track',
        'wbr'
        ]

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack:list[HtmlNode] = []
        self.roots:list[HtmlNode] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in Parser.void_tags:
            return self.handle_startendtag(tag, attrs)
        node = HtmlNode(tag, attrs)
        self.stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        if tag == self.stack[-1].tag:
            node = self.stack.pop()
            if self.stack:
                self.stack[-1].add_child(node)
            else:
                self.roots.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = HtmlNode(tag, attrs)
        if len(self.stack) > 0:
            self.stack[-1].add_child(node)
        else:
            self.roots.append(node)

    def handle_data(self, data: str) -> None:
        if data.strip() != '' and self.stack:
            self.stack[-1].add_text(data)

    def parse(self, data:str) -> list[HtmlNode]:
        self.stack.clear()
        self.roots.clear()
        self.feed(data)
        return [i for i in self.roots]