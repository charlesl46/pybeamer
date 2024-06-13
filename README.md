# pybeamer

Create LaTeX beamers with Python.

## Installation


## Usage

### Simple example

```python
from pybeamer import Document,Text,Frame,Itemize

doc = Document()
doc.title = "My fancy document"

frame = Frame(title="my fancy first frame")
frame.add(Text("fancy text in it"))

itemize = Itemize()
itemize.add(Text("oh an item !"))
itemize.add(Text("and a second one !!"))
frame.add(itemize)

doc.add(frame)

doc.render()
doc.export("test.tex")
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
\end{frame}

\begin{frame}{my fancy first frame}
    fancy text in it
\begin{itemize}
    
        \item oh an item !
    
        \item and a second one !!
    
\end{itemize}
\end{frame}

\end{document}
```