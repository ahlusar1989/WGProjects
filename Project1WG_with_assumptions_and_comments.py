
# # # Without data to examine here, I can only guess based on this requirement's language that 
# # fixed records are in the input.  If so, here's a slight revision to the helper functions that I wrote earlier which
# # takes the function fileinfo as a starting point and demonstrates calling a function from within a function.  
# I tested this little sample on a small set of files created with MD5 checksums.  I wrote the Python in such a way as it 
# would work with Python 2.x or 3.x (note the __future__ at the top).

# # # There are so many wonderful ways of failure, so, from a development standpoint, I would probably spend a bit 
# # more time trying to determine which failure(s) I would want to report to the user, and how (perhaps creating my own Exceptions)

# # # The only other comments I would make are about safe-file handling.

# # #   #1:  Question: After a user has created a file that has failed (in
# # #        processing),can the user create a file with the same name?
# # #        If so, then you will probably want to look at some sort
# # #        of file-naming strategy to avoid overwriting evidence of
# # #        earlier failures.

# # # File naming is a tricky thing.  I referenced the tempfile module [1] and the Maildir naming scheme to see two different 
# # types of solutions to the problem of choosing a unique filename.

# # #! /usr/bin/python

from __future__ import print_function

import os
import time

RECORD_LENGTH = 32

def process_data(f, filesize):
    f.seek(0, os.SEEK_SET)
    counter = 0

    # -- are the records text?  I assume yes, though your data may differ.
    #    if your definition of a record includes the newline, then
    #    I would want to use len(record) ...
    #
    for record in f:
        print("record: %s" % ( record.strip()), file=sys.stderr)
        if RECORD_LENGTH == len(record.strip()):  # -- len(record)
            counter += 1
        else:
            return False, counter
    return True, counter


def validate_and_process_data(f, filesize):
    f.seek(0, os.SEEK_END)
    lastbyte = f.tell()
    if lastbyte != filesize:
        return False, 0
    else:
        return process_data(f, filesize)

def validate_files(files):
    for file in files:
        filename, rootdir, lastmod, creation, filesize = fileinfo(file)
        f = open(filename)
        result, record_count = validate_and_process_data(f, filesize)
        if result:
            # -- Success!  Write text file with count of records
            #    recognized in record_count
            print('success with %s on %d records' % (filename, record_count,), file=sys.stderr)
            pass
        else:
            # -- Failure; need additional logic here to determine
            #    the cause for failure.
            print('failure with %s after %d records' % (filename, record_count,), file=sys.stderr)
            pass


def fileinfo(file):
    filename = os.path.basename(file)
    rootdir = os.path.dirname(file)
    lastmod = time.ctime(os.path.getmtime(file))
    creation = time.ctime(os.path.getctime(file))
    filesize = os.path.getsize(file)
    return filename, rootdir, lastmod, creation, filesize

if __name__ == '__main__':
   import sys
   validate_files(sys.argv[1:])

# -- end of file