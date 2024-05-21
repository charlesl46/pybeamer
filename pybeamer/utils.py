from jinja2 import Environment, PackageLoader, select_autoescape

EPILOGUE = r"""
\end{document}
"""

def create_env():
    env = Environment(
        loader=PackageLoader("pybeamer"),
        autoescape=select_autoescape()
    )
    return env