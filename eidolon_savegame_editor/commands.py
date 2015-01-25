import json

from prettytable import PrettyTable


COMMANDS = {}


def command(fn):
    COMMANDS[fn.__name__] = fn


@command
def reset_hunger(save, backup, **kwargs):
    save.set_property('hunger', 0)
    save.write(backup=backup)


@command
def show_properties(save, **kwargs):
    table = PrettyTable(['Name', 'Type', 'Value'])

    for prop, data in save.data.items():
        value = '(not printable)'
        if data['type'] in ['IntProperty', 'FloatProperty', 'StringProperty']:
            try:
                value = json.dumps(data['value'])
            except ValueError:
                pass
        table.add_row([prop, data['type'], value])

    print table
