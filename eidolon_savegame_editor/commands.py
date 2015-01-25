from texttable import Texttable


COMMANDS = {}
PRINTABLE_TYPES = {
    'IntProperty': lambda x: x,
    'FloatProperty': lambda x: x,
    'StringProperty': lambda x: x,
    'ArrayProperty': lambda x: '\n'.join([str(v) for v in x])
}


def command(fn):
    COMMANDS[fn.__name__] = fn


@command
def reset_hunger(save, backup, **kwargs):
    save.set_property('hunger', 0)
    save.write(backup=backup)


@command
def show_properties(save, **kwargs):
    table = Texttable()
    rows = [
        ['Name', 'Type', 'Value']
    ]

    for prop, data in save.data.items():
        value = '(not printable)'
        if data['type'] in PRINTABLE_TYPES:
            try:
                value = PRINTABLE_TYPES[data['type']](data['value'])
            except ValueError:
                value = '(error while formatting)'
        rows.append([prop, data['type'], value])
    table.add_rows(rows)

    print table.draw()
