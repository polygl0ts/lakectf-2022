from unittest.mock import patch
import json
import subprocess

chaindle = __import__("chaindle")


def test_correct_guess():
    def guess_all_green(self, iv: bytes, ciphertext: bytes) -> str:
        return chaindle.Color.GREEN.value * len(ciphertext)

    def mock_input(*args, **kwargs) -> str:
        return json.dumps({"iv": "0" * 32, "ciphertext": "0" * 128})

    class MockPrint:
        def __init__(self):
            self.buffer = []

        def print(self, s, *args, **kwargs) -> None:
            self.buffer.append(s)

    mock_print = MockPrint()

    with patch("chaindle.Chaindle.guess", guess_all_green):
        with patch("builtins.input", mock_input):
            with patch("builtins.print", mock_print.print):
                chaindle.challenge()

    assert "EPFL" in "".join(map(str, mock_print.buffer))


def test_get_color():
    B = chaindle.Color.BLACK
    Y = chaindle.Color.YELLOW
    G = chaindle.Color.GREEN

    # Length mismatch
    try:
        chaindle.get_color(b"abc", b"de")
        assert False
    except AssertionError:
        pass

    # All green
    assert chaindle.get_color(b"abc", b"abc") == [G] * 3

    # All black
    assert chaindle.get_color(b"abc", b"def") == [B] * 3

    # Yellow
    assert chaindle.get_color(b"abc", b"acb") == [G, Y, Y]

    # Duplicate letters
    assert chaindle.get_color(b"abc", b"bdb") == [Y, B, B]
    assert chaindle.get_color(b"aabc", b"daaa") == [B, G, Y, B]


def test_solution():
    p = subprocess.run("python3 chaindle-solve.py", shell=True, capture_output=True)
    assert b"EPFL" in p.stdout, p.stdout


test_correct_guess()
test_get_color()
test_solution()
