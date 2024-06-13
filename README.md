# pybeamer

Create LaTeX beamers with Python.

## Installation


## Usage

### Simple example

```python
from pybeamer import Document,Text,Frame,Itemize
from pybeamer.utils import italic,mono

doc = Document()
doc.title = "My fancy document"

frame = Frame(title="my fancy first frame")
frame.add(Text("fancy text in it"))
frame.add(Text(italic("and italic text too")))

itemize = Itemize()
itemize.add(Text("oh an item !"))
itemize.add(Text("and a second one !!"))
itemize.add(Text(f"and a third with {mono('mono text')}"))
frame.add(itemize)

doc.add(frame)

doc.render()
doc.export("test_tex/test.tex")
```

This outputs a LaTeX document in `test.tex` and a `makefile` to help you start playing with it.

```latex
\documentclass{beamer}
\usepackage[english]{babel}
\usetheme{Madrid}
\begin{document}
\title{ My fancy document }

\frame{\titlepage}
\begin{frame}{Table of contents}
    \tableofcontents
\end{frame}\begin{frame}{my fancy first frame}
    fancy text in it
\textit{and italic text too}
\begin{itemize}
    
        \item oh an item !
    
        \item and a second one !!
    
        \item and a third with \texttt{mono text}
    
\end{itemize}
\end{frame}

\end{document}
```