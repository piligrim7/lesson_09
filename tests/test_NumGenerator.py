import loto_classes as lc

def test_get_next():
    gen = lc.NumGenerator(numbers_count=lc.NUMBERS_COUNT)
    assert len(gen.numbers) == lc.NUMBERS_COUNT
    assert gen.get_next()>0
    for _ in range(lc.NUMBERS_COUNT-2):
        gen.get_next()
    assert gen.get_next()>0
    assert gen.get_next()==0