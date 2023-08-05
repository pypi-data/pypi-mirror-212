def convert_figure_tag_to_shortcode(content, fixed_lines):
    """
    Converts the figure tag that has 'is-provider-youtube' class to a YouTube shortcode.
    """
    video_link = content.findNext("iframe").attrs["src"]
    video_id_part = video_link.rsplit("/")
    video_id = video_id_part[-1].split("?")[0]
    fixed_lines.append(f"{{{{< youtube {video_id} >}}}}\n")
