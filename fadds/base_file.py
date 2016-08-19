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
        last_obj = None  # when we start, we have no object in memory
        while 1:
            last_pos = self.file.tell()  # store where in the file we are
            line = self.file.readline()  # get a line
            if not line:
                if last_obj:  # there is an object in memory, we need to return it
                    self.file.seek(last_pos)  # still rewind
                    return last_obj
                raise StopIteration  # here is nothing else in the file, stop iterating
            if self.object.is_new(line):  # there is a 'new' object
                if last_obj:  # this new object replaces a previous, so we need to return the previous
                    self.file.seek(last_pos)  # rewind to before the new object line so that next call we start by
                    # creating the object
                    return last_obj  # return the last object in memory
                last_obj = self.object()  # create the object
            last_obj.add_record(line)  # store object properties


class BaseData(object):
    key_length = 4
    NEW = ""

    def __init__(self):
        self.record_type = ""  # all objects have a record type
        self.identifier = ""  # as well as a unique ID

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
        """
        Can be useful to compare 2 objects, just in case
        :param BaseData other:
        :return: bool
        """
        return self.identifier == other.identifier and self.__class__ == other.__class__

    def add_record(self, line):
        """
        Add the object record
        :param str line: a line
        :return: None
        """
        record_type = self.get_record_type(line)
        if record_type == self.NEW:
            self.record_type = self.__class__.get_value(line, 1, self.key_length)
            self.identifier = self.__class__.get_value(line, self.key_length+1, 4)  # assume identifier length is 4
        self.special_data(record_type, line)  # for each object, we have a special data handling (template pattern)

    def special_data(self, record_type, line):
        """
        Must be implemented by sub classes
        :param str record_type: a type of record, to know what to fill in
        :param str line: a line
        :return: None
        """
        raise NotImplementedError

    def __repr__(self):
        return "%s" % self.identifier
