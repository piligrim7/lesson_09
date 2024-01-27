import loto_classes as lc

def test_Card_init():
    card = lc.Card(player_name='test')
    assert len(card.lines) == lc.LINE_COUNT
    for line in range(lc.LINE_COUNT):
        assert len([n for n in card.lines[line] if n==0]) == lc.LINE_CELLS_COUNT-lc.LINE_NUMBERS_COUNT
        assert len([n for n in card.lines[line] if n>0]) == lc.LINE_NUMBERS_COUNT        