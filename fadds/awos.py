""" Parser for the AWOS.txt file """
class AWOSParser(object):
    """ Parse AWOS file using iterator

    Does not parse REMARK fields

    """
    def __init__(self, awos_file):

        # TODO: Error check the awos_file file object
        self.awos_file = awos_file

    def __iter__(self):
        return self

    def next(self):

        awos = None
        while not awos:
            line = self.awos_file.readline()
            is_data = AWOS.is_data(line)
            if not line:
                raise StopIteration
            elif is_data:
                awos = AWOS(line)

        return awos

    def __next__(self):
        return self.next()


class AWOS(object):
    """ AWOS Record """

    class RecordType(object):
        DATA = 'AWOS1'
        REMARK = 'AWOS2'

    @classmethod
    def is_remark(cls, line):
        record_type = cls.__get_value(line, 1, 5)
        return record_type == cls.RecordType.REMARK

    @classmethod
    def is_data(cls, line):
        record_type = cls.__get_value(line, 1, 5)
        return record_type == cls.RecordType.DATA

    @classmethod
    def __get_value(cls, line, start, length):
        if not line:
            return ''
        start_index = start - 1
        end_index = start_index + length
        return line[start_index:end_index].strip()


    def __init__(self, line):
        self.record_type = AWOS.__get_value(line, 1, 5)
        self.identifier = AWOS.__get_value(line, 6, 4)
        self.sensor_type = AWOS.__get_value(line, 10, 10)
        self.status = AWOS.__get_value(line, 20, 1)
        self.remarks = []

    # Unused
    def add_remark(self, line):
        record_type = AWOS.__get_value(line, 1, 5)
        identifier = AWOS.__get_value(line, 6, 4)
        if record_type != self.RecordType.REMARK:
            return
        if identifier != self.identifier:
            return
        remark = AWOS.__get_value(line, 20, 236)
        self.remarks.append(remark)
