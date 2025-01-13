from pybeamer.utils import create_env
from typing import Literal
from pybeamer.exceptions import WrongNodeTypeError

env = create_env()

class Node:
    def __init__(self) -> None:
        if self.__class__ == Node:
            raise Exception("A node can't be instanciated")
        self.nodes : list = []

    def _render_nodes(self):
        return "\n".join([node.to_text() for node in self.nodes])

    def to_text(self) -> str:
        pass

    def add(self,*nodes):
        for node in nodes:
            if self.check_authorized(node):
                self.nodes.append(node)
            else:
                raise WrongNodeTypeError(f"Node type {node.__class__.__name__} can't be added to node type {self.__class__.__name__}")

    @classmethod
    def check_authorized(cls,node):
        if cls.__authorized_direct_children__ is None:
            return False
        else:
            return node.__class__.__name__ in cls.__authorized_direct_children__

class Section(Node):
    __authorized_direct_children__ = ["Frame"]

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
    __authorized_direct_children__ = None

    def __init__(self,text : str) -> None:
        super().__init__()
        self.text = text
    
    def to_text(self) -> str:
        return self.text
    
class Frame(Node):
    __authorized_direct_children__ = ["Block","Text","Itemize"]
    template = env.get_template("frame.jinja2")

    def __init__(self,title : str = None) -> None:
        super().__init__()
        self.title = title
        
    
    def to_text(self) -> str:
        content = self._render_nodes()
        return Frame.template.render(title=self.title,content=content)
    
class Block(Node):
    __authorized_direct_children__ = ["Text","Itemize"]
    template = env.get_template("block.jinja2")

    def __init__(self,title : str = None,block_type : Literal["block","alertblock","examples"] = "block") -> None:
        super().__init__()
        self.title = title
        self.type = block_type
        
    def to_text(self) -> str:
        content = self._render_nodes()
        return Block.template.render(title=self.title,content=content,block_type=self.type)

class Itemize(Node):
    __authorized_direct_children__ = ["Text","Itemize","Enumerate"]
    template = env.get_template("itemize.jinja2")

    def __init__(self) -> None:
        super().__init__()

    def _render_nodes(self):
        for node in self.nodes:
            text = node.to_text()
            if node.__class__ == Text:
                text = f"\item {text}"
            yield text
       
    def to_text(self) -> str:
        items = self._render_nodes()
        return Itemize.template.render(items=items)

class Enumerate(Node):
    __authorized_direct_children__ = ["Text","Itemize","Enumerate"]
    template = env.get_template("enumerate.jinja2")

    def __init__(self) -> None:
        super().__init__()

    def _render_nodes(self):
        for node in self.nodes:
            text = node.to_text()
            if node.__class__ == Text:
                text = f"\item {text}"
            yield text
       
    def to_text(self) -> str:
        items = self._render_nodes()
        return Itemize.template.render(items=items)
    