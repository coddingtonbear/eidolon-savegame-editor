import datetime
import logging
import os
import shutil
import struct


INTEGER_ARRAY_NAMES = [
    '_itemCounts',
]


logger = logging.getLogger(__name__)


class Savegame(object):
    NAME_SIZE = 1
    NAME = 2
    TYPE_SIZE = 8
    TYPE = 3

    def __init__(self, filename):
        self._cursor = 0
        self.data = {}

        self.filename = filename
        self.contents = self.read()
        self.process_contents()

    def read(self):
        with open(os.path.expanduser(self.filename), 'rb') as handle:
            return handle.read()

    def write(self, backup=True):
        if backup:
            self.backup()
        with open(os.path.expanduser(self.filename), 'wb') as handle:
            handle.write(self.contents)

    def backup(self):
        original_path = os.path.expanduser(self.filename)
        final_path = '%s.%s' % (
            original_path,
            datetime.datetime.strftime(
                datetime.datetime.utcnow(),
                '%Y%m%dT%H%M%SZ'
            )
        )
        shutil.copy(original_path, final_path)

    def _pack_string(self, string):
        return ''.join([
            struct.pack('i', len(string) + 1),
            string,
            '\x00',
        ])

    def set_content_range(self, start, end, value):
        self.contents = (
            self.contents[0:start] +
            value +
            self.contents[end:]
        )

    def set_float_property(self, name, value):
        data = self.data[name]
        self.set_content_range(
            data['end'] - 4,
            data['end'],
            struct.pack('f', value)
        )

    def set_array_property_string(self, name, value):
        data = self.data[name]

        packed_strings = ''.join([
            self._pack_string(v) for v in value
        ])
        packed_array = ''.join([
            struct.pack('i', len(value)),
            packed_strings,
        ])
        output = ''.join([
            struct.pack('i', len(packed_array)),
            struct.pack('i', 0),
            packed_array,
        ])
        self.set_content_range(
            data['value_start'],
            data['end'],
            output,
        )

    def set_array_property_integer(self, name, value):
        data = self.data[name]

        packed_integers = ''.join([
            struct.pack('i', v) for v in value
        ])
        packed_array = ''.join([
            struct.pack('i', len(value)),
            packed_integers
        ])
        output = ''.join([
            struct.pack('i', len(packed_array)),
            struct.pack('i', 0),
            packed_array
        ])
        self.set_content_range(
            data['value_start'],
            data['end'],
            output
        )

    def set_property(self, name, value):
        property_type = self.data[name]['type']
        if property_type == 'FloatProperty':
            self.set_float_property(name, value)
        elif property_type == 'ArrayProperty':
            if name in INTEGER_ARRAY_NAMES:
                self.set_array_property_integer(name, value)
            else:
                self.set_array_property_string(name, value)
        else:
            raise NotImplemented()

        # Reload contents since they might've shifted during flight
        self.process_contents()

    def read_string(self, size):
        end = self.cursor + size
        value = self.contents[self.cursor:end-1]
        logger.debug('Read string: "%s"', value)
        # Strings are null-terminated
        self.cursor = end
        return value

    def read_integer(self):
        end = self.cursor + 4
        value = struct.unpack('i', self.contents[self.cursor:end])[0]
        logger.debug('Read integer: %s', value)
        self.cursor = end
        return value

    def read_array_property_string(self):
        # Size -- we don't need to read this
        self.read_integer()
        # This appears to always be '0'
        self.read_integer()
        count = self.read_integer()
        logger.debug('Beginning to read array.')

        value = []
        for idx in range(count):
            length = self.read_integer()
            string = self.read_string(length)
            logger.debug('Found array element %s (%s)', string, length)
            value.append(string)

        end = self.cursor
        logger.debug('Read array value: %s', value)
        self.cursor = end
        return value

    def read_array_property_integer(self):
        # Size -- we don't need to read this
        self.read_integer()
        # This appears to always be '0'
        self.read_integer()
        count = self.read_integer()
        logger.debug('Beginning to read array.')

        value = []
        for idx in range(count):
            data = self.read_integer()
            logger.debug('Found array element %s', data)
            value.append(data)

        end = self.cursor
        logger.debug('Read array value: %s', value)
        self.cursor = end
        return value

    def read_struct_property(self):
        first_part = self.read_integer()
        self.read_integer()
        second_part = self.read_integer()
        end = self.cursor + first_part + second_part
        value = self.contents[self.cursor:end]
        logger.debug('Read struct value: %s', value)
        self.cursor = end
        return value

    def read_float_property(self):
        data_length = self.read_integer()
        self.read_integer()
        end = self.cursor + data_length
        value = struct.unpack('f', self.contents[self.cursor:end])[0]
        logger.debug('Read float value: %s', value)
        self.cursor = end
        return value

    def read_int_property(self):
        # This would be the length -- but we already know it
        self.read_integer()
        self.read_integer()
        value = self.read_integer()
        logger.debug('Read integer value: %s', value)
        return value

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        logger.debug(
            'Advancing cursor from %s to %s.',
            self._cursor,
            value
        )
        self._cursor = value

    def process_contents(self):
        # Skip preamble
        self.cursor = 8
        state = self.NAME_SIZE
        meta = {}

        while True:
            if self.cursor >= len(self.contents):
                break
            if state == self.NAME_SIZE:
                meta['_size'] = self.read_integer()
                meta['start'] = self.cursor
                logger.debug(
                    'Found size "%s", entering NAME state',
                    meta['_size']
                )
                state = self.NAME
                continue
            elif state == self.NAME:
                meta['name'] = self.read_string(meta['_size'])
                logger.debug(
                    'Found name "%s", entering TYPE_SIZE state',
                    meta['name'],
                )
                state = self.TYPE_SIZE
                continue
            elif state == self.TYPE_SIZE:
                meta['_size'] = self.read_integer()
                logger.debug(
                    'Found type size "%s", entering TYPE state',
                    meta['_size'],
                )
                state = self.TYPE
                continue
            elif state == self.TYPE:
                meta['type'] = self.read_string(meta['_size'])
                logger.debug('Found type "%s", reading value', meta['type'])
                meta['value_start'] = self.cursor
                if meta['type'] == 'ArrayProperty':
                    if meta['name'] in INTEGER_ARRAY_NAMES:
                        meta['value'] = self.read_array_property_integer()
                    else:
                        meta['value'] = self.read_array_property_string()
                if meta['type'] == 'StructProperty':
                    meta['value'] = self.read_struct_property()
                if meta['type'] == 'FloatProperty':
                    meta['value'] = self.read_float_property()
                if meta['type'] == 'IntProperty':
                    meta['value'] = self.read_int_property()
                meta['end'] = self.cursor
                self.data[meta['name']] = meta
                meta = {}
                state = self.NAME_SIZE
                continue
