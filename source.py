import re

class Source(object):    
    # The class Source is an alternative File object. 
    # It can read a well-structured text file (such as csv or excel txt output). 
    # It reads lines in block (readblock function) whenever the block_key has been changed
    def __init__(self, file_path, pattern, block_key, has_header=True):
        self.pattern = re.compile(pattern)
        self.block_key = block_key
        self.the_file = open(file_path, 'r')
        if has_header:
            self.the_file.readline()
        self.buffer_line = self.the_file.readline()
        m = self.pattern.match(self.buffer_line)
        if m is not None:
            self.block_flag = m.group(self.block_key)
        else: 
            self.block_flag = ''
    
    def close(self):
        self.the_file.close()
    
    def readblock(self):
        block = self.buffer_line
        if self.buffer_line:
            while self.buffer_line:
                this_line = self.the_file.readline()
                m = self.pattern.match(this_line)
                if (m is not None) and (m.group(self.block_key) != self.block_flag):
                    self.buffer_line = None
                    self.block_flag = m.group(self.block_key)
                elif m is not None:
                    block = block + "\n" + this_line
                    self.block_flag = m.group(self.block_key)
                else:
                    self.buffer_line = None
                    block = block + "\n" + this_line
            self.buffer_line = this_line
        return block
        
