"""sphinxext.revealjs.directives.incremental

The `.. incremental::` directive. This will add a transition to its children so
they appear one at a time using Reveal.js's `fragment` class.
"""

from typing import TYPE_CHECKING, List

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx.util import logging

if TYPE_CHECKING:
    from sphinx.application import Sphinx

logger = logging.getLogger(__name__)


class Incremental(Directive):
    """Incremental directive."""

    required_arguments = 1
    has_content = True
    option_spec = {"class": directives.class_option}

    _valid_arguments = ("one", "item", "nest")

    def run(self) -> List[nodes.Node]:
        self.validate_args()
        self.assert_has_content()

        text = "\n".join(self.content)
        node = nodes.container(text)
        self.state.nested_parse(self.content, self.content_offset, node)

        if self.arguments[0] == "one":
            node["classes"] += self.options.get("class", [])
            node["classes"].append("fragment")
            return [node]
        else:
            # Now we're handling the 'item' and 'nest' cases, where we need to
            # apply the 'fragment' class to nodes in node.children

            self.assert_is_incrementable(node.children[0])

            # Since we're gonna discard the parent node, copy
            # classes set by the user onto the first child node
            node.children[0]["classes"] += self.options.get("class", [])

            if isinstance(node.children[0], nodes.definition_list):
                self.contain_definition_list_items(node.children[0])

            if self.arguments[0] == "item":
                self.increment_list_items(node)
            elif self.arguments[0] == "nest":
                self.increment_nested_list_items(node)

            return node.children

    def validate_args(self) -> None:
        """Warn user if argument is invalid."""

        location = self.state_machine.get_source_and_line(self.lineno)
        if self.arguments[0] not in self._valid_arguments:
            logger.warning(
                f"Invalid argument: '{self.arguments[0]}' must be one of {', '.join(self._valid_arguments)}",
                location=location,
            )

    def assert_is_incrementable(self, node: nodes.Element) -> None:
        """Warn user if we can't apply transitions to this node."""

        location = self.state_machine.get_source_and_line(self.lineno)
        if not isinstance(node, nodes.Sequential):
            logger.warning(
                "contents of directive 'incremental' must be a list or sequence",
                location=location,
            )

    def increment_list_items(self, node: nodes.Sequential) -> None:
        """Add class 'fragment' to Sequential node's children."""

        for list_item in node.children[0].children:
            try:
                list_item["classes"] += ["fragment"]
            except TypeError:
                continue

    def increment_nested_list_items(self, node: nodes.Sequential) -> None:
        """Add class 'fragment' to a Sequential node's descendants."""

        def traverse_condition(node: nodes.Node) -> bool:
            return (
                isinstance(node, nodes.list_item)
                or isinstance(node, nodes.term)
                or isinstance(node, nodes.definition)
            )

        for list_item in node.traverse(traverse_condition):
            list_item["classes"] += ["fragment"]

    @staticmethod
    def contain_definition_list_items(dl_node: nodes.definition_list) -> None:
        """Group definitions and terms in containers."""

        dl_children = []
        for def_list_item in dl_node.children:
            container = nodes.container()
            container.children.append(def_list_item)
            dl_children.append(container)

        dl_node.children = dl_children


def setup(app: "Sphinx") -> None:
    """Setup the extension."""

    app.add_directive("incremental", Incremental)
    app.add_directive("incr", Incremental)
