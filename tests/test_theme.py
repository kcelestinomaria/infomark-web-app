import theme

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_dark_theme():
    result = theme.dark_theme()
    assert result['config']['background'] == '#000'
    assert result['config']['title']['color'] == '#0f0'
