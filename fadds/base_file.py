# -*- coding: utf-8 -*-
"""
Author: @sposs
Date: 19.08.16
"""


class BaseFile(object):
    def __init__(self, file_obj):
        self.file = file_obj
        self.object = None
        self.last_obj = None

    def __iter__(self):
        return self

    def next(self):
        last_obj = None
        while 1:
            last_pos = self.file.tell()
            line = self.file.readline()
            if not line:
                if last_obj:
                    self.file.seek(last_pos)
                    return last_obj
                raise StopIteration
            if self.object.is_new(line):
                if last_obj:
                    self.file.seek(last_pos)
                    return last_obj
                last_obj = self.object()
                last_obj.add_record(line)
            else:
                last_obj.add_record(line)


class BaseData(object):
    key_length = 4
    NEW = ""

    def __init__(self):
        self.record_type = ""
        self.identifier = ""

    @classmethod
    def get_value(cls, line, start, length):
        if not line:
            return ''
        start_index = start - 1
        end_index = start_index + length
        return line[start_index:end_index].strip()

    @classmethod
    def is_new(cls, line):
        record_type = cls.get_value(line, 1, cls.key_length)
        return record_type == cls.NEW

    @classmethod
    def get_record_type(cls, line):
        record_type = cls.get_value(line, 1, cls.key_length)
        return record_type

    def __eq__(self, other):
        return self.identifier == other.identifier and self.__class__ == other.__class__

    def add_record(self, line):
        record_type = self.get_record_type(line)
        if record_type == self.NEW:
            self.record_type = self.__class__.get_value(line, 1, self.key_length)
            self.identifier = self.__class__.get_value(line, self.key_length+1, 4)
        self.special_data(record_type, line)

    def special_data(self, record_type, line):
        raise NotImplementedError

    def __repr__(self):
        return "%s" % self.identifier
