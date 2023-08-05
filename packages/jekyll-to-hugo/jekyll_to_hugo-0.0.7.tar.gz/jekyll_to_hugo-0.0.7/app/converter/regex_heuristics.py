import re
from collections import namedtuple

from app import utils

RegexCallback = namedtuple("RegexCallback", ["callback", "name"])


class RegexHeuristics:
    """
    Regex heuristics class for applying modifying a line using regex lines.
    """

    def __init__(self, configurator):
        utils.guard_against_none(configurator, "configurator")

        self.configurator = configurator
        self._regex_options = (
            self.configurator.converter_options.regex_heuristics.dict()
        )
        self._rules = {
            "^(</*pre.*?>)`{0,3}(?P<content>.*?)(<\/pre>)?$": RegexCallback(
                self._remove_pre_tag, "remove_pre_tag"
            ),
        }

    def _remove_pre_tag(self, match: re.Match) -> str:
        """
        Removes the pre tag from the match.
        """
        return match.group("content")

    def handle_regex_heuristics(self, line: str) -> str:
        """
        Manipulates a line by using regex heuristics.
        """
        if not self.configurator.converter_options.enable_regex_heuristics:
            return line

        for regex, callback in self._rules.items():
            option_enabled = self._regex_options.get(callback.name, False)
            if not option_enabled:
                continue

            match = re.match(regex, line)
            if match:
                line = callback.callback(match)
        return line
