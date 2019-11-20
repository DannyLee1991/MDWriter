import os
from typing import List

__all__ = ["MDWriter", "MDTitle", "MDTextArea", "MDHyperlink", "MDText", "MDList", "MDLine", "MDCode", "MDQuote",
           "MDImage", "MDTable"]


class MDElement:
    md_str = ''

    def __init__(self):
        self.md_str = self._to_md()

    def _to_md(self) -> str:
        """
        构造markdown语法文本
        :return:
        """
        pass


class MDBlock:
    pass


class MDText(MDElement):
    def __init__(self, text, type=""):
        self.mdtext = text
        self.type = type if type in ["", "*", "**", "***", "~~", "`"] else ""
        super(MDText, self).__init__()

    def _to_md(self) -> str:
        return "{type}{text}{type}".format(text=self.mdtext, type=self.type)


class MDHyperlink(MDText):
    def __init__(self, mdtext: (MDText, str), link, title=""):
        self.mdtext = auto_cvt_mdtext(mdtext)
        self.link = link
        self.title = title
        super().__init__(self)

    def _to_md(self) -> str:
        return '[{mdtext}]({link} "{title}")'.format(mdtext=self.mdtext.md_str, link=self.link, title=self.title)


class MDTextArea(MDElement, MDBlock):
    def __init__(self, mdtext_list: List[MDText] = []):
        self.mdtext_list = []
        for mdtext in mdtext_list:
            if type(mdtext) == str:
                self.mdtext_list.append(MDText(mdtext))
            else:
                self.mdtext_list.append(mdtext)
        super().__init__()

    def _to_md(self) -> str:
        return "".join([mdtext.md_str for mdtext in self.mdtext_list])


class MDTitle(MDElement, MDBlock):
    def __init__(self, mdtext: (MDText, str), level: int = 1):
        self.mdtext = auto_cvt_mdtext(mdtext)
        self.level = level
        super().__init__()

    def _to_md(self) -> str:
        return "{mk} {title}".format(mk="#" * self.level, title=self.mdtext.md_str)


class MDImage(MDElement, MDBlock):
    def __init__(self, img_url, img_title="", img_alt=""):
        self.img_url = img_url
        self.img_title = img_title
        self.img_alt = img_alt
        super().__init__()

    def _to_md(self) -> str:
        return '![{img_alt}]({img_url} "{img_title}")' \
            .format(img_alt=self.img_alt,
                    img_url=self.img_url,
                    img_title=self.img_title)


class MDLine(MDElement, MDBlock):
    def __init__(self):
        super().__init__()

    def _to_md(self) -> str:
        return '---'


class MDQuote(MDElement, MDBlock):
    def __init__(self, mdtext: (MDText, str), level=1):
        self.mdtext = auto_cvt_mdtext(mdtext)
        self.level = level
        super().__init__()

    def _to_md(self) -> str:
        return "{mk} {text}".format(mk=">" * self.level, text=self.mdtext.md_str)


class MDList(MDElement, MDBlock):
    def __init__(self, items: List[MDElement] = [], level=0):
        self.items = [auto_cvt_mdtext(item) for item in items]
        self.level = level
        super().__init__()

    def _to_md(self) -> str:
        md_str = ""
        for item in self.items:
            if isinstance(item, list):
                md_str += MDList(item, level=self.level + 1).md_str
            else:
                md_str += (
                    "{level}- {text}{newline}".format(level="   " * self.level, text=item.md_str, newline=os.linesep))
        return md_str


class MDCode(MDElement, MDBlock):
    def __init__(self, code, code_type=''):
        self.code = code
        self.code_type = code_type
        super().__init__()

    def _to_md(self) -> str:
        return "```{code_type}{new_line}{code}{new_line}```" \
            .format(code_type=self.code_type,
                    new_line=os.linesep,
                    code=self.code)


class MDTable(MDElement, MDBlock):
    def __init__(self, headers: List[MDElement] = [], rows: List[List[MDElement]] = []):
        self.headers = headers
        self.rows = rows
        super().__init__()

    def _to_md(self) -> str:
        header_str = "|"
        divider = "|"
        for header in self.headers:
            header = auto_cvt_mdtext(header)
            header_str += " {header} |".format(header=header.md_str)
            divider += ":-:|"
        md_str = header_str + os.linesep + divider + os.linesep

        for row in self.rows:
            row_str = "| {row} |{new_line}" \
                .format(row=" | ".join([auto_cvt_mdtext(item).md_str for item in row]),
                        new_line=os.linesep)
            md_str += row_str
        return md_str


def auto_cvt_mdtext(element: (MDElement, str)):
    return MDText(element) if type(element) == str else element


class MarkDownBuilder:

    def __init__(self):
        self.elements = []

    def append(self, element: MDBlock):
        self.elements.append(element)
        return self

    def build(self):
        md_str = ""
        for element in self.elements:
            md_str += element.md_str
            md_str += os.linesep
            md_str += os.linesep
        return md_str


# ------------------------

class MDWriter:
    def __init__(self, path: str):
        self.dir = os.sep.join(path.split(os.sep)[:-1])
        self.path = path
        self.name = path.split(os.sep)[-1]

        os.makedirs(self.dir, exist_ok=True)

        self.file = open(self.path, 'w')
        self.builder = MarkDownBuilder()

    def write_element(self, element: MDBlock):
        self.builder.append(element)

    def write_elements(self, element_list: List[MDBlock]):
        for element in element_list:
            self.builder.append(element)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        md_str = self.builder.build()
        with open(self.path, 'w') as f:
            f.write(md_str)
