from pybeamer.utils import create_env
from typing import Self

env = create_env()

class Node:
    def __init__(self) -> None:
        self.nodes : list[Self] = []

    def _render_nodes(self):
        return "\n".join([node.to_text() for node in self.nodes])

    def to_text(self) -> str:
        pass

    def add(self,*nodes):
        for node in nodes:
            self.nodes.append(node)

class Section(Node):
    def __init__(self,title : str) -> None:
        super().__init__()
        self.title = title
    
    def to_text(self):
        content = ""
        intro = "\section{{title}}".format(title=self.title)
        content += intro
        content += self._render_nodes()
        return content

class Text(Node):
    def __init__(self,text : str) -> None:
        super().__init__()
        self.text = text
    
    def to_text(self) -> str:
        return self.text
    
class Frame(Node):
    def __init__(self,title : str = None) -> None:
        super().__init__()
        self.title = title
        self.template = env.get_template("frame.jinja2")
    
    def to_text(self) -> str:
        content = self._render_nodes()
        return self.template.render(title=self.title,content=content)
    
class Block(Node):
    def __init__(self,title : str = None) -> None:
        super().__init__()
        self.title = title
        self.template = env.get_template("block.jinja2")

    def to_text(self) -> str:
        content = self._render_nodes()
        return self.template.render(title=self.title,content=content)

class Itemize(Node):
    def __init__(self) -> None:
        super().__init__()
        self.template = env.get_template("itemize.jinja2")

    def _render_nodes(self):
        for node in self.nodes:
            if node.__class__ == Text:
                typ = "text"
            elif node.__class__ == Itemize:
                typ = "itemize"
            
            yield (typ,node.to_text())
       

    def to_text(self) -> str:
        items = self._render_nodes()
        return self.template.render(items=items)


    