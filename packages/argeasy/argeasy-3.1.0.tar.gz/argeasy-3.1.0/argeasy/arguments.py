class Arguments(object):
    def __repr__(self):
        attr = [i for i in self.__dir__() if not i.startswith('__')]
        repr = 'Arguments('

        for c, a in enumerate(attr):
            value = self.__getattribute__(a)

            if isinstance(value, str):
                value = f'"{value}"'

            if c == len(attr) - 1:
                repr += f'{a}={value})'
            else:
                repr += f'{a}={value}, '

        return repr
