import json
from threading import Timer


def debounce(func, delay=3):
    def debounced(*args, **kwargs):
        def call_it():
            func(*args, **kwargs)
        debounced.t.cancel()
        debounced.t = Timer(delay, call_it)
        debounced.t.start()
    debounced.t = Timer(0, lambda: None)
    return debounced


def readFiled(filename="text.txt", encoding="utf-8"):
    f = open(filename, 'r')
    d = f.read().encode(f.encoding).decode(encoding)
    f.close()
    return d


def writeFiled(strins, filename="text.txt", encoding="utf-8"):
    d = readFiled(filename)
    try:

        f = open(filename, 'w')
        f.write(strins.encode(encoding).decode(f.encoding))
        f.close()
        return True

    except Exception as e:
        print(e)
        f = open(filename, 'w')
        f.write(d.encode(encoding).decode(f.encoding))
        f.close()
        return False


def readJson(filename="text.txt"):
    return json.loads(readFiled(filename))


def writeJson(data, filename="text.txt"):
    return writeFiled(json.dumps(data), filename)
