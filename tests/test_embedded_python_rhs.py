from .helpers import parse, scoped_tokens


def test_then_block_is_wrapped_and_carries_python_scopes():
    parsed = parse(
        'rule "x"\nwhen\nthen\n  insert(Score(value=95))\n  retract($s)\nend\n'
    )
    blocks = scoped_tokens(parsed, "meta.embedded.block.python.prl")
    assert len(blocks) == 1
    assert "insert" in blocks[0]


def test_end_inside_python_string_does_not_close_early():
    parsed = parse(
        'rule "x"\nwhen\nthen\n  logger.info("end of rule")\nend\n'
    )
    blocks = scoped_tokens(parsed, "meta.embedded.block.python.prl")
    assert len(blocks) == 1
    assert "end of rule" in blocks[0]
    ends = [c for c in scoped_tokens(parsed, "keyword.control.prl") if c == "end"]
    assert len(ends) == 1


def test_end_inside_python_comment_does_not_close_early():
    parsed = parse('rule "x"\nwhen\nthen\n  # end of loop\n  x = 1\nend\n')
    blocks = scoped_tokens(parsed, "meta.embedded.block.python.prl")
    assert len(blocks) == 1
    assert "end of loop" in blocks[0]


def test_empty_rhs_does_not_crash():
    parsed = parse('rule "x"\nwhen\nthen\nend\n')
    assert parsed is not None


def test_multiline_if_statement_stays_in_one_block():
    parsed = parse(
        'rule "x"\nwhen\nthen\n'
        "  if x > 1:\n"
        "    y = 2\n"
        "  else:\n"
        "    y = 3\n"
        "end\n"
    )
    blocks = scoped_tokens(parsed, "meta.embedded.block.python.prl")
    assert len(blocks) == 1
    assert "y = 2" in blocks[0] and "y = 3" in blocks[0]
