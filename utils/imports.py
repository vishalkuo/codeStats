def module_exists(name):
    try:
        __import__(str(name))
    except ImportError:
        return False
    else:
        return True