from time import perf_counter
import os

from pybeamer.utils import EPILOGUE,create_env,mono,italic
import pybeamer.defaults as defaults
from pybeamer.nodes import Text,Node,Frame,Section,Block,Itemize

env = create_env()

class Document(Node):
    def __init__(self) -> None:
        super().__init__()
        self.title = defaults.DOCUMENT_DEFAULT_TITLE
        self.authors = None
        self.subtitle = None
        self.institute = None
        self.toc_title = defaults.TOC_DEFAULT_TITLE
        self.latex_engine = defaults.LATEX_DEFAULT_ENGINE

        self._prologue_template = env.get_template("prologue.jinja2")
        self._titlepage_template = env.get_template("titlepage.jinja2")
        self._toc_template = env.get_template("toc.jinja2")
        self._makefile_template = env.get_template("makefile.jinja2")

        self.language = defaults.DOCUMENT_DEFAULT_LANGUAGE
        self.theme = defaults.DOCUMENT_DEFAULT_THEME

    def render(self,with_titlepage : bool = True,with_toc : bool = True,return_text : bool = False,verbose_rendering_time : bool = False) -> None:
        beginning_time = perf_counter()
        
        self.text = ""
        self.text += "\n" + self._render_prologue()

        if with_titlepage:
            self.text += "\n" + self._render_titlepage()

        if with_toc:
            self.text += "\n" + self._render_toc()

        self.add(Text(EPILOGUE))
        
        self.text += self._render_nodes()

        ending_time = perf_counter()
        if verbose_rendering_time:
            print(f"Rendered in {ending_time - beginning_time}")

        if return_text:
            return self.text

    def _render_toc(self):
        return self._toc_template.render(toc_title=self.toc_title)

    def _render_titlepage(self):
        self.titlepage = self._titlepage_template.render(title=self.title,authors=self.authors,institute=self.institute)
        return self.titlepage
    
    def export(self,filepath : str):
        filename = os.path.basename(filepath)
        root,ext = os.path.splitext(filename)
        folder = os.path.dirname(filepath)
        with open(filepath,"w") as file:
            file.write(self.text)

        makefile_path = os.path.join(folder,"makefile")
        with open(makefile_path,"w") as file:
            file.write(self._makefile_template.render(latex_engine=self.latex_engine,doc_title=filename,tab="\t",root=root))

    def _render_prologue(self):
        self.prologue = self._prologue_template.render(language=self.language,theme=self.theme)
        return self.prologue
    
    def add(self,node : Node):
        self.nodes.append(node)

    def set_title(self,title : str) -> None:
        self.title = title

    def set_authors(self,authors : str) -> None:
        self.authors = authors

    def set_institute(self,institute : str) -> None:
        self.institute = institute

def main():
    d = Document()
    d.set_title("Titre du document")
    d.set_authors("Lucas and Emily")
    d.set_institute("Institut")

    frame = Frame(f"titre de la frame ({italic('en italique')})")
    frame.add(Text("texte dans la frame"))
    b = Block("titre du block")
    b.add(Text(f"texte dans le {mono('monoblock')}"))
    frame.add(b)
    d.add(frame)

    frame2 = Frame("titre de la seconde frame")
    itz = Itemize()
    itz.add(Text("item 1"))
    itz.add(Text("item 2"))

    itz2 = Itemize()
    itz2.add(Text("item 3"))
    itz.add(itz2)

    itz3 = Itemize()
    itz3.add(Text("item 4"))
    itz2.add(itz3)

    itz.add(Text("item 5"))

    frame2.add(itz)
    d.add(frame2)

    section1 = Section("section 1")
    section1.add(frame,frame2)

    d.add(Text("Texte de test"))

    frame3 = Frame("frame 3")
    block = Block("bloc de maths important","alertblock")
    block.add(Text("Du texte de maths : $A + B$"))
    frame3.add(block)

    d.add(frame3)

    d.render(verbose_rendering_time=True)
    d.export(filepath="test_tex/test.tex")