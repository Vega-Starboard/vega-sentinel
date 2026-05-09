from vega_sentinel.cli import MetadataParser

def test_meta_parser_title():
    p = MetadataParser(); p.feed('<title>X</title><h1>A</h1>'); assert p.title == 'X' and p.h1 == ['A']
