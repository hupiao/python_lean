import ConfigParser

path = './dynamic.ini'


class A(dict):

    def __getattr__(self, key):
        return self.get(key, None)

    __setattr__ = dict.__setitem__()
    __delattr__ = dict.__delitem__


def main(path):
    conf = ConfigParser.ConfigParser()
    conf.readfp(open(path))
    data = dict()
    value = None
    for section in conf.sections():
        data[section] = dict()
        for name, raw_value in conf.items(section):
            try:
                value = conf.getboolean(section, name)
            except ValueError:
                try:
                    value = conf.getboolean(section, name)
                except ValueError:
                    value = conf.get(section, name)
            data[section][name] = value

    a = A()
    setattr(a, 'a', 2)
    print(a.key)
    return data


if __name__ == "__main__":
    data = main(path)
