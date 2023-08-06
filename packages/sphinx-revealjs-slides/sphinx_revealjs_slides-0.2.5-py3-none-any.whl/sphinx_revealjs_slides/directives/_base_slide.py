"""sphinxext.revealjs.directives._base_slide

Common, slides-related stuff.
"""

from docutils.nodes import Element
from docutils.parsers.rst import Directive, directives


class BaseSlide(Directive):
    """Base for slide-related directives."""

    option_spec = {
        "class": directives.class_option,
        "background": directives.unchanged,
        # The choices below are all from Revealjs.
        # See https://revealjs.com/transitions/
        "transition": lambda arg: directives.choice(
            arg, ("none", "fade", "slide", "convex", "concave", "zoom")
        ),
        "transition-speed": lambda arg: directives.choice(
            arg, ("default", "fast", "slow")
        ),
    }

    def attach_options(self, node: Element) -> None:
        node["data-background"] = self.options.get("background")
        node["data-transition"] = self.options.get("transition")
        node["data-transition-speed"] = self.options.get("transition-speed")
        node["data-state"] = self.options.get("state")
        node["classes"] += self.options.get("class", [])
