"""sei.sphinxext.revealjs.overridenodes"""

from typing import TYPE_CHECKING, Any

from docutils import nodes
from sphinx.writers.html5 import HTML5Translator

if TYPE_CHECKING:
    from sphinx.application import Sphinx

data_attributes = {
    "state": "data-state",
}


def new_slide(html_writer: HTML5Translator, node: nodes.Element) -> str:
    return html_writer.starttag(
        node,
        "section",
        **{
            data_attributes[attr]: val
            for attr, val in node.attributes.items()
            if attr in data_attributes
        }
    )


def visit_skipnode(self, *args: Any) -> None:
    raise nodes.SkipNode


def handle_h1_slide(self, node: nodes.title) -> None:
    self.body.append("<section>")


def handle_h2_slide(self, node: nodes.title) -> None:
    self.body.append("</section>")  # close previous slide

    self.body.append("<section>")  # start horizontal slides group
    self.body.append("<section>")  # start first horizontal slide


def handle_h3_slide(self, node: nodes.title) -> None:
    self.body.append("</section>")  # close previous slide
    self.body.append("<section>")  # start next horizontal slide


def close_horizontal_slides(self, node: nodes.section) -> None:
    self.body.append("</section>")  # close last horizontal slide
    self.body.append("</section>")  # close horizontal slides group


def visit_section(self, node: nodes.section) -> None:
    self.section_level += 1


def depart_section(self, node: nodes.section) -> None:
    if self.section_level == 2:
        close_horizontal_slides(self, node)

    self.section_level -= 1


def visit_title(self, node: nodes.title) -> None:
    if isinstance(node.parent, nodes.section):
        if self.section_level == 1:
            handle_h1_slide(self, node)
        elif self.section_level == 2:
            handle_h2_slide(self, node)
        elif self.section_level == 3:
            handle_h3_slide(self, node)

    super(self.__class__, self).visit_title(node)


def depart_title(self, node: nodes.title) -> None:
    super(self.__class__, self).depart_title(node)


def visit_document(self, nodes: nodes.document) -> None:
    self.body.append('<div class="reveal">')
    self.body.append('<div class="slides">')
    super(self.__class__, self).visit_document(nodes)


def depart_document(self, nodes: nodes.document) -> None:
    super(self.__class__, self).depart_document(nodes)
    self.body.append("</div>")
    self.body.append("</div>")


def setup(app: "Sphinx") -> None:
    app.add_node(nodes.sidebar, override=True, revealjs=(visit_skipnode, None))
    app.add_node(nodes.topic, override=True, revealjs=(visit_skipnode, None))
    app.add_node(nodes.admonition, override=True, revealjs=(visit_skipnode, None))

    app.add_node(nodes.section, override=True, revealjs=(visit_section, depart_section))
    app.add_node(nodes.title, override=True, revealjs=(visit_title, depart_title))
    app.add_node(
        nodes.document, override=True, revealjs=(visit_document, depart_document)
    )
