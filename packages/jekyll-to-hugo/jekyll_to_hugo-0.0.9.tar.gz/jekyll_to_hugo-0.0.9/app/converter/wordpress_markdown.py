import yaml
from bs4 import BeautifulSoup, Tag

from app import utils
from app.config import Configurator
from app.converter.regex_heuristics import RegexHeuristics
from app.converter.tags_heuristics import convert_figure_tag_to_shortcode
from app.io.reader import IoReader
from app.io.writer import IoWriter
from app.utils import key_error_silence


class WordpressMarkdownConverter:
    """
    Markdown converter that converts jekyll posts to hugo posts.
    """

    def __init__(self, configurator: Configurator):
        """
        Initializes the WordpressMarkdownConverter

        Parameters
        ----------
        configurator : Configurator
            The configurator instance.
        """
        utils.guard_against_none(configurator, "configurator")
        self.configurator = configurator
        self.regex_heuristics = RegexHeuristics(configurator)

    def fix_header(self, header: dict) -> dict:
        """
        Fix the Hugo header

        Parameters
        ----------
        header : dict
            The header to fix

        Returns
        -------
        dict
            The fixed header
        """
        for field in self.configurator.converter_options.header_fields_drop:
            with key_error_silence():
                del header[field]
        # rewrite header fields
        with key_error_silence():
            header["guid"] = header["guid"].replace("http://localhost", "")
        with key_error_silence():
            header["author"] = self.configurator.converter_options.author_rewrite
        return header

    def fix_pre_content(self, post_lines: list[str]) -> list[str]:
        """
        Fixes the pre content from the post lines when enclosed in backticks code blocks.
        """
        fixed_lines = []
        index = 0
        while index < len(post_lines):
            line = post_lines[index]
            if line == "```":
                found_enclosing = False
                search_index = index + 1
                while search_index < len(post_lines):
                    if post_lines[search_index] == "```":
                        found_enclosing = True
                        break
                    search_index += 1
                if found_enclosing:
                    for line_index, line in enumerate(
                        post_lines[index : search_index + 1]
                    ):
                        if line_index == 1:
                            regex_line = self.regex_heuristics.handle_regex_heuristics(
                                str(line)
                            )
                            if regex_line:
                                fixed_lines.append(regex_line)
                        else:
                            fixed_lines.append(line)
                    index = search_index + 1
                    continue
            index += 1
            fixed_lines.append(line)
        return fixed_lines

    def fix_html_tags(self, post_lines):
        """
        Fixes the html tags from the post lines.
        """
        fixed_lines = []
        is_in_code_block = False
        for line in post_lines:
            # Enter code block mode when detecting a line that starts with ```
            # and exit when detecting a line that starts with ```.
            if line.startswith("```"):
                if is_in_code_block:
                    is_in_code_block = False
                else:
                    is_in_code_block = True
                fixed_lines.append(line)
                continue

            # Skip modifying the line if it is in code block mode.
            if is_in_code_block:
                fixed_lines.append(line)
                continue

            # Treat empty string as a new line.
            if line == "":
                fixed_lines.append("\n")
                continue

            # Parse the line as html and remove the HTML tags from it.
            soup = BeautifulSoup(line, features="html.parser")
            for content in soup.contents:
                if isinstance(content, Tag):
                    # found html tag
                    self._fix_html_tag(content, fixed_lines)
                else:
                    # found text, add it to the fixed lines
                    fixed_lines.append(
                        self.regex_heuristics.handle_regex_heuristics(str(content))
                    )
        return fixed_lines

    def _fix_html_tag(self, content: Tag, fixed_lines: list):
        """
        Fixes the html tag.
        """
        # Check if tag is a YouTube video and add it as a shortcode.
        if "is-provider-youtube" in content.attrs.get("class", []):
            convert_figure_tag_to_shortcode(content, fixed_lines)
        # Fix unknown tags by removing the tag and only add inner content.
        # content.contents is a list of all the inner content of the tag.
        else:
            tags = list(map(str, content.contents))
            if tags:
                # recursively fix the inner content of the tag.
                fixed_tags = self.fix_html_tags(tags)
                if fixed_tags:
                    fixed_lines.append("".join(fixed_tags))

    def convert_post_content(self, post_content: str) -> str:
        """
        Converts the post content

        Parameters
        ----------
        post_content : str
            The post content

        Returns
        -------
        str
            The converted post content
        """
        # fix links inside post content with simple replace
        for task in self.configurator.converter_options.links_rewrite:
            source_link = task.get("source")
            target_link = task.get("target")
            if not source_link or not target_link:
                continue
            post_content = post_content.replace(source_link, target_link)

        # fix unknown tags
        post_lines = post_content.split("\n")
        fixed_lines = self.fix_pre_content(post_lines)
        fixed_lines = self.fix_html_tags(fixed_lines)

        return "\n".join(fixed_lines)

    def read_jekyll_post(self, reader: IoReader):
        """
        Read a Jekyll post from the reader.

        Parameters
        ----------
        reader : IoReader
            The IoReader instance for reading.
        """
        # read source
        return reader.read()

    def write_hugo_post(self, writer: IoWriter, post_header: dict, post_content: str):
        """
        Write a Hugo post to the specified writer.

        Parameters
        ----------
        writer : IoWriter
            The IoWriter instance for writing.
        post_header : dict
            The post header
        post_content : str
            The post content
        """
        data = ["---\n", yaml.dump(post_header), "---\n", post_content]
        writer.write("".join(data))

    def convert_jekyll_to_hugo(self, reader: IoReader, writer: IoWriter):
        """
        Convert a Jekyll post to a Hugo post

        Parameters
        ----------
        reader : IoReader
            The IoReader instance for reading.
        writer : IoWriter
            The IoWriter instance for writing.
        """
        contents = self.read_jekyll_post(reader)

        # fix header
        header = yaml.safe_load(contents.split("---")[1])
        fixed_header = self.fix_header(header)
        # fix content
        post_content = contents.split("---", 2)[2].lstrip()
        fixed_post_content = self.convert_post_content(post_content)

        self.write_hugo_post(
            writer,
            fixed_header,
            fixed_post_content,
        )
