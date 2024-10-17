
# Deprecated. Head to www.cruchdao.com !

def test_gen_gen():
    from midone.datasources.streamgeneratorgenerator import stream_generator_generator
    gen_gen = stream_generator_generator(category='train', return_float=True)
    for gen in gen_gen:
        value = next(gen)
        assert value is not None


if __name__=='__main__':
    test_gen_gen()