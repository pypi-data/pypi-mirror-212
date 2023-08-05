# Jekyll to Hugo Converter

Jekyll to Hugo Converter is a simple tool to convert Jekyll posts to Hugo posts.

I've used this tool to convert [my blog](https://blog.nuculabs.dev) from WordPress to Jekyll and finally to Hugo.

The tool has the following features:
- Batch conversion.
- Post header fields drop/ignore.
- Links rewrite. (Search and Replace)
- Author name rewrite.

It was written in a way that is easy to extend, while I wrote it for my own personal use, I hope you'll find some use for it as well.

Note: This tool is not perfect, it will not convert everything. If you find a bug, please open a PR.

## Table of Contents

* [Usage](#usage)
  * [PiPy](#pipy)
  * [Python From Source](#python-from-source)
  * [Docker](#docker)
* [Configuration](#configuration)
  * [Example Configuration](#example-configuration)
* [License](#license)

## Usage

### PiPy or Pipx

If you have Python installed, you can use the following commands:

```bash
pip install jekyll-to-hugo
jekyll-to-hugo
```

You will need to create a `config.yaml` file in the current directory. See example [here](./config.yaml).

_`pipx` is a tool to install Python CLI tools in isolated environments_

### Python From Source

If you have Python installed, you can use the following commands:

```bash
pip install -r requirements.txt
python3 jekyll-to-hugo.py <jekyll_post_path> <hugo_post_path>
```

To change the config, edit `config.yaml`.

The configuration file path can be configured with the `CONFIG_PATH` environment variable.

### Docker

If you don't have Python installed, you can use Docker:

1. Build the image.

```bash
docker build -t jekyll-to-hugo -f ./docker/Dockerfile .
```

2. Run the image. You will need to mount the following directories: config file, Jekyll posts directory, Hugo posts directory.

```bash
docker run -it --rm -v $(pwd):/app jekyll-to-hugo
```

## Configuration

The configuration file is a YAML file. See example [here](./config.yaml).
The configuration file path can be configured with the `CONFIG_PATH` environment variable.

### Example Configuration

```yaml
logging_level: "INFO"
source_path: "/Users/dnutiu/PycharmProjects/jekyll-to-hugo/my_test_data/_posts"
output_path: "/Users/dnutiu/NucuLabsProjects/NucuLabsDevBlog/content/posts"
converter: "wordpress_markdown_converter"
converter_options:
  enable_regex_heuristics: true
  author_rewrite: "Denis Nuțiu"
  links_rewrite:
    - source: "http://localhost/"
      target: "/"
    - source: "https://nuculabs.wordpress.com/"
      target: "https://nuculabs.dev/posts/"
    - source: "https://twitter.com/metonymyqt"
      target: "https://twitter.com/nuculabs"
  header_fields_drop:
    - restapi_import_id
    - original_post_id
    - timeline_notification
    - wordads_ufa
    - spay_email
    - amp_status
    - advanced_seo_description
    - publicize_twitter_user
```

## License

This project is licensed under the GPL-3.0 license - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ by [NucuLabs.dev](https://blog.nuculabs.dev)