"""sphinxext.revealjs.directives.newslide

Use this to create a new slide. Content will resume after a slide break.

Pass in an argument to give the new slide a title::

    .. newslide:: Title

With no arguments, the new slide will have the same title as its
parent slide.
"""

from typing import TYPE_CHECKING, List
from docutils import nodes

from ._base_slide import BaseSlide

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class newslide(nodes.General, nodes.Element):
    """Newslide node."""


class Newslide(BaseSlide):
    """Newslide directive."""

    optional_arguments = 1
    final_argument_whitespace = True

    def run(self) -> List[nodes.Element]:
        local_title = self.arguments[0] if self.arguments else ""

        slide_node = newslide("", localtitle=local_title)
        self.attach_options(slide_node)

        return [slide_node]


def visit_newslide(self, node: newslide) -> None:
    title = node["localtitle"]
    if not title and node.parent:
        title = node.parent.next_node(nodes.title).astext().strip()

    self.body.append("</section>")
    self.body.append(
        self.starttag(
            node,
            "section",
            **{att: val for att, val in node.attributes.items() if val is not None},
        )
    )
    self.body.append(f"<h{self.section_level}>{title}</h{self.section_level}>")


def depart_newslide(self, node: newslide) -> None:
    pass


def ignore_newslide(self, node: newslide) -> None:
    raise nodes.SkipNode


def setup(app: "Sphinx") -> None:
    app.add_node(
        newslide,
        revealjs=(visit_newslide, depart_newslide),
        html=(ignore_newslide, None),
    )
    app.add_directive("newslide", Newslide)
