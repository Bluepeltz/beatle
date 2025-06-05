import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_import_framework():
    import beatle
    assert hasattr(beatle, "BeatleBot")
