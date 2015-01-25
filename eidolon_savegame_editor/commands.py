import argparse

from texttable import Texttable


COMMANDS = {}
PRINTABLE_TYPES = {
    'IntProperty': lambda x: x,
    'FloatProperty': lambda x: x,
    'StringProperty': lambda x: x,
    'ArrayProperty': lambda x: '\n'.join([str(v) for v in x])
}
KNOWN_INVENTORY_ITEMS = [
    'Mushrooms',
    'Tinder',
]


def command(fn):
    COMMANDS[fn.__name__] = fn


@command
def reset_hunger(save, backup, **kwargs):
    save.set_property('hunger', 0)
    save.write(backup=backup)


@command
def add_items(save, backup, extra, **kwargs):
    parser = argparse.ArgumentParser(extra)
    parser.add_argument(
        'item', metavar='ITEM', type=str,
        choices=list(
            set(save.data['_items']['value']) |
            set(KNOWN_INVENTORY_ITEMS)
        ),
        help="Which item would you like to add to your inventory?",
    )
    parser.add_argument(
        'count', metavar='COUNT', type=int,
        help='How many would you like to add to your inventory?',
    )
    args = parser.parse_args(extra)

    did_insert = False
    items = save.data['_items']['value']
    if args.item not in items:
        did_insert = True
        items.append(args.item)
    save.set_property('_items', items)
    items = save.data['_items']['value']

    item_counts = save.data['_itemCounts']['value']
    if did_insert:
        item_counts.append(args.count)
    else:
        item_counts[items.index(args.item)] = args.count
    save.set_property('_itemCounts', item_counts)

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
