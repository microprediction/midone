

def test_datagen():
    from midone.datasources.streamgenerator import stream_generator
    gen = stream_generator(stream_id=0, category='train', return_float=True)  # 'train', 'test'
    value = next(gen)
    assert value is not None


def test_gen_gen():
    from midone.datasources.streamgeneratorgenerator import stream_generator_generator
    gen_gen = stream_generator_generator(category='train', return_float=True)
    for gen in gen_gen:
        value = next(gen)
        assert value is not None


if __name__=='__main__':
    test_datagen()
    test_gen_gen()