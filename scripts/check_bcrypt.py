import importlib
try:
    m = importlib.import_module('bcrypt')
    print('module:', m)
    print('__version__:', getattr(m, '__version__', 'MISSING'))
    print('__about__:', getattr(m, '__about__', 'MISSING'))
    print('__file__:', getattr(m, '__file__', 'MISSING'))
    print('dir contains __about__?', '__about__' in dir(m))
except Exception as e:
    print('ERROR', e)
