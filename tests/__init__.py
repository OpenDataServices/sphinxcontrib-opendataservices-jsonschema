import os.path


def path(*args):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples', *args))
