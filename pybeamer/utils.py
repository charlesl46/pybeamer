from jinja2 import Environment, PackageLoader, select_autoescape,Template

EPILOGUE = r"""
\end{document}
"""

def create_env():
    env = Environment(
        loader=PackageLoader("pybeamer"),
        autoescape=select_autoescape(),
        variable_start_string='<<',
        variable_end_string='>>',
    )
    return env

utils_env = create_env()
mono_template = utils_env.from_string(r"\texttt{<<text>>}")
italic_template = utils_env.from_string(r"\textit{<<text>>}")
maths_template = utils_env.from_string(r"${<<text>>}$")

def mono(text : str) -> str:
    return mono_template.render(text=text)

def italic(text : str) -> str:
    return italic_template.render(text=text)

def math(text : str) -> str:
    return maths_template.render(text=text)

