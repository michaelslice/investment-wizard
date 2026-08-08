from src.options.utils import parse_option_symbol


def test_parse_option_symbol() -> None:
    parsed = parse_option_symbol("AAPL260814C00130000")
    assert parsed is not None
    assert parsed.option_type == "call"
    assert parsed.strike == 130
