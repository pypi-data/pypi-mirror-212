"""sphinx_revealjs_slides.builder"""

from sphinx.builders.html import StandaloneHTMLBuilder


class RevealjsBuilder(StandaloneHTMLBuilder):
    name = "revealjs"
    search = False

    def get_theme_config(self) -> tuple[str, dict]:
        return self.config.revealjs_html_theme, self.config.revealjs_html_theme_options
