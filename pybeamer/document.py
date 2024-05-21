from pybeamer.utils import EPILOGUE,create_env
import pybeamer.defaults as defaults
from pybeamer.nodes import Text,Node,Frame,Section

env = create_env()

class Document(Node):
    def __init__(self) -> None:
        super().__init__()
        self.title = defaults.DOCUMENT_DEFAULT_TITLE
        self.authors = None
        self.subtitle = None
        self.institute = None
        self.toc_title = defaults.TOC_DEFAULT_TITLE

        self._prologue_template = env.get_template("prologue.jinja2")
        self._titlepage_template = env.get_template("titlepage.jinja2")
        self._toc_template = env.get_template("toc.jinja2")

        self.language = defaults.DOCUMENT_DEFAULT_LANGUAGE

    def render(self,with_titlepage : bool = True,with_toc : bool = True) -> None:
        self.text = ""
        self.text += "\n" + self._render_prologue()

        if with_titlepage:
            self.text += "\n" + self._render_titlepage()

        if with_toc:
            self.text += "\n" + self._render_toc()

        self.add(Text(EPILOGUE))
        
        self.text += self._render_nodes()

    def _render_toc(self):
        return self._toc_template.render(toc_title=self.toc_title)

    def _render_titlepage(self):
        self.titlepage = self._titlepage_template.render(title=self.title)
        return self.titlepage
    
    def export(self,filepath : str):
        with open(filepath,"w") as file:
            file.write(self.text)

    def _render_prologue(self):
        self.prologue = self._prologue_template.render(language=self.language)
        return self.prologue
    
    def add(self,node : Node):
        self.nodes.append(node)

    def set_title(self,title : str) -> None:
        self.title = title

def main():
    d = Document()

    frame = Frame("titre de la frame")
    frame.add(Text("texte dans la frame"))
    d.add(frame)

    frame2 = Frame("titre de la seconde frame")
    d.add(frame2)

    section1 = Section("section 1")
    section1.add(frame,frame2)

    d.add(Text("Texte de test"))
    d.render()
    d.export(filepath="test.tex")