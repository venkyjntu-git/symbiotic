#!/usr/bin/python

from utils import dbg

class ProcessWatch(object):
    """ Parse output of running process """

    def __init__(self, lines_limit = 0):
        """
        Initialize a watch. By default, do not store
        any output of the process. If \param buffer_lines
        is set to non-0 value, this watch will store
        the lines of output maximally up to \param buffer_lines,
        or will store everything when \param buffer_lines is None
        """
        self.maxlines = lines_limit

        if self.isBuffering():
            from collections import deque
            self.buff = deque(maxlen = lines_limit)

    def isBuffering(self):
        return self.maxlines is None or self.maxlines > 0

    def putLine(self, line):
        """
        Put a line from a process' output to the watch
        """
        if self.isBuffering():
            self.buff.append(line)

        self.parse(line)

    def parse(self, line):
        """
        Parse output of running process - this method
        is called always when a line is put into the watch.
        This method will be override by child class
        """
        pass

    def getLines(self):
        """
        Get buffered lines
        """
        if self.isBuffering():
            return list(self.buff)
        else:
            return []

    def ok(self):
        """
        Return True if everyithing is ok with the process,
        or False if anything went wrong (based on the process' output).
        In case that this method returns False, run() method
        will terminate the process and return -1
        """
        return True

class DbgWatch(ProcessWatch):
    """
    Watch that just prints the output as debugging messages
    with given domain. It may optionally buffer the lines
    """
    def __init__(self, dbgdom, maxlines = 0):
        ProcessWatch.__init__(self, maxlines)
        self._domain = dbgdom

    def parse(self, line):
        dbg(line, self._domain)
