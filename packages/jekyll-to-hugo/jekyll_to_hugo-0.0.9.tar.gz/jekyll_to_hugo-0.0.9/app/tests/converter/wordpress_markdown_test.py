import pytest

from app.config import ConverterOptions
from app.converter import WordpressMarkdownConverter
from app.io.reader import StringReader
from app.io.writer import MockWriter
from app.tests.utils import make_fake_configurator


@pytest.mark.parametrize(
    "author_rewrite, input_header, expected_header",
    [
        ("", {"author": "author"}, {"author": ""}),
        ("", {}, {"author": ""}),
        ("", {"a": 1}, {"a": 1, "author": ""}),
        ("NucuLabs.dev", {"author": "Denis"}, {"author": "NucuLabs.dev"}),
    ],
)
def test_header_rewrite_author(author_rewrite, input_header, expected_header):
    """
    Test the header rewrite author functionality.
    """
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(
            author_rewrite=author_rewrite,
        ),
    )
    converter = WordpressMarkdownConverter(configurator)
    assert converter.fix_header(input_header) == expected_header


@pytest.mark.parametrize(
    "header_fields_drop, input_header, expected_header",
    [
        ([], {}, {"author": ""}),
        (["a"], {"a": 1, "b": 2, "c": 3}, {"author": "", "b": 2, "c": 3}),
        (["a", "b"], {"a": 1, "b": 2, "c": 3}, {"author": "", "c": 3}),
        ([], {"a": 1, "b": 2, "c": 3}, {"author": "", "a": 1, "b": 2, "c": 3}),
    ],
)
def test_header_fields_drop(header_fields_drop, input_header, expected_header):
    """
    Test the header fields drop functionality.
    """
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(
            header_fields_drop=header_fields_drop,
        ),
    )
    converter = WordpressMarkdownConverter(configurator)
    assert converter.fix_header(input_header) == expected_header


@pytest.mark.parametrize(
    "input_lines, expected_lines",
    [
        ([], []),
        ([""], ["\n"]),
        (
            [
                '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper"><iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" height="281" loading="lazy" src="https://www.youtube.com/embed/X5865VHcGmQ?feature=oembed" title="Command Line Tools: fzf  🌸" width="500"></iframe></div></figure>Thanks!'
            ],
            ["{{< youtube X5865VHcGmQ >}}\n", "Thanks!"],
        ),
        (
            ["Hello https://youtu.be/jv40aJbRjjY?list=RDjv40aJbRjjY Done"],
            ["Hello https://youtu.be/jv40aJbRjjY?list=RDjv40aJbRjjY Done"],
        ),
    ],
)
def test_fix_html_tags_detect_youtube_links(input_lines, expected_lines):
    """
    Ensure fix_html_tags detects youtube links.
    """
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(),
    )
    converter = WordpressMarkdownConverter(configurator)
    assert converter.fix_html_tags(input_lines) == expected_lines


@pytest.mark.parametrize(
    "input_lines, expected_lines",
    [
        ([], []),
        ([""], ["\n"]),
        (["<p>Test</p>"], ["Test"]),
        (["<p>Test</p>", "<p>Test</p>"], ["Test", "Test"]),
        (["<p>Te<span>st</span></p>"], ["Test"]),
        (["<p>Te<span><span>s</span><span class='hi'>t</span></span></p>"], ["Test"]),
        (
            ["<pre>preTe<ImportantC#Tag>st</ImportantC#Tag></pre></pre>"],
            ["preTest"],
        ),
    ],
)
def test_fix_html_tags_stripe_tag(input_lines, expected_lines):
    """
    Ensure fix_html_tags removes the tag and tested tags.
    """
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(),
    )
    converter = WordpressMarkdownConverter(configurator)
    assert converter.fix_html_tags(input_lines) == expected_lines


@pytest.mark.parametrize(
    "input_lines, expected_lines",
    [
        (
            ["<pre>", "<p>Te<span>st</span></p>", "</pre>"],
            ["<pre>", "<p>Te<span>st</span></p>", "</pre>"],
        ),
        (
            [
                "```",
                '<pre class="wp-block-syntaxhighlighter-code">    <ItemGroup>',
                "```",
            ],
            ["```", "    <ItemGroup>", "```"],
        ),
        (
            [
                "```",
                '<pre class="wp-block-syntaxhighlighter-code">```    <ItemGroup>',
                "```",
            ],
            ["```", "    <ItemGroup>", "```"],
        ),
        (
            [
                "```",
                '<pre class="wp-block-syntaxhighlighter-code">',
                "<ItemGroup>",
                "```",
            ],
            ["```", "<ItemGroup>", "```"],
        ),
        (
            [
                "```",
                '<pre class="wp-block-preformatted">sudo apt-get update; sudo apt-get install --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev',
                "```",
            ],
            [
                "```",
                "sudo apt-get update; sudo apt-get install --no-install-recommends make "
                "build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev "
                "libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev "
                "libxmlsec1-dev libffi-dev liblzma-dev",
                "```",
            ],
        ),
    ],
)
def test_fix_pre_content(input_lines, expected_lines):
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(),
    )
    converter = WordpressMarkdownConverter(configurator)
    assert converter.fix_pre_content(input_lines) == expected_lines


def test_read_jekyll_post():
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(),
    )
    converter = WordpressMarkdownConverter(configurator)
    reader = StringReader("Test")
    assert converter.read_jekyll_post(reader) == "Test"


def test_write_hugo_post():
    configurator = make_fake_configurator(
        "wordpress_markdown_converter",
        ConverterOptions(),
    )
    converter = WordpressMarkdownConverter(configurator)
    writer = MockWriter()
    converter.write_hugo_post(writer, {"title": "Test"}, "Test\nLine 2")
    assert writer.content == "---\ntitle: Test\n---\nTest\nLine 2"
