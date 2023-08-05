from typing import Any

class HtmlNode:
    def __init__(self, tag:str, attrs:list[tuple[str, str | None]]) -> None:
        self.index:int = 0
        self.tag = tag
        self.attrs: dict[str, str | None] = dict()
        self.children: dict[int, Any] = dict()
        self.text: dict[int, str] = dict()
        for i in attrs:
            self.attrs[i[0]] = i[1]

    def add_child(self, child:Any):
        self.children[self.index] = child
        self.index += 1

    def add_text(self, text:str):
        self.text[self.index] = text
        self.index += 1

    def get_dom(self):
        children = []
        for i in range(self.index):
            if i in self.children:
                children.append(self.children[i].get_dom())
            else:
                children.append(self.children[i])
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "children": children
        }