
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

##I am ssuming all filenames come directly from the commandline.  No searching of a directory. 

## I am assuming that all of my files are going to be specified in unicode  

# # #! /usr/bin/python

from __future__ import print_function

import os
import time
import glob
import sys

#I wrote an error class in case the I needed such a specification for a notifcation - this is not in the requirements
class ErrorHandler:

    def __init__(self):
        pass

    def write(self, string):

        # write error to file
        fname = " Error report (" + time.strftime("%Y-%m-%d %I-%M%p") + ").txt"
        handler = open(fname, "w")
        handler.write(string)
        handler.close()

        # write error to popup dialog.....just for fun
        dlg = wx.MessageDialog(None, string, "Crash Report", wx.ICON_HAND)
        dlg.ShowModal()
        dlg.Destroy()
        #os._exit(1) # close the program
        
    
original_stderr = sys.stderr # stored in case want to revert
sys.stderr = ErrorHandler()


path = "some/directory/path"
dirslist = os.listdir(path)


RECORD_LENGTH = 32

# Made a new function, called main(), with a loop that calls 
# validate_files(), with a sleep after each pass. Before, my present code 
# was assuming all filenames come directly from the commandline.  No searching of a directory.  
# I am assuming that this is appropriate since I moved the earlier versions of the files. 
# I let the directory name be the argument to main, and let main do a dirlist each time through the loop, 
# and pass the corresponding list to validate_files. 

def main(dirslist): 
    while True:
        for file in dirslist:
        	return validate_files(file)
        	time.sleep(5)

if __name__ == "__main__": 
    main() 


#Here this function 

##Process_data is another level for checking file length 

def process_data(f, filesize):
    f.seek(0, os.SEEK_SET)
    counter = 0

    # -- are the records text?  I assume yes, though data may differ.
    #    if a definition of a record includes the newline, then
    #    I would want to use len(record) ...
    #
    for record in f:
        print("record: %s" % ( record.strip()), file=sys.stderr)
        if RECORD_LENGTH == len(record.strip()):  # -- len(record)
            counter += 1
        else:
            return False, counter
    return True, counter

#This checks for byte size only

def validate_and_process_data(f, filesize):
    f.seek(0, os.SEEK_END)
    lastbyte = f.tell() # or check against 0  - if the files are zero length files
    if lastbyte != filesize:
        return False, 0     #This should move to a "Failure folder" How do I integrate shututil? So far, this closes and does nothing else 
        					# - should I use a try and except here?
    else:
        return process_data(f, filesize)

def validate_files(files): ## This functions job is to check all file info by name - it passes to validate_and_process_data to check for byte size only
    for file in files:
        filename, rootdir, lastmod, creation, filesize = fileinfo(file)
        f = open(filename)
        result, record_count = validate_and_process_data(f, filesize)
        if result:
            # -- Success!  Write text file with count of records
            #    recognized in record_count        	
            print('success with %s on %d records' % (filename, record_count,), file=sys.stderr)

            # How do I use shututil() to move this to a "Success" Folder print("Success! File has been read", file) 
        else: ####
            # -- Failure; need additional logic here to determine cause of the failure - OSError perhaps?
            print('Failure with %s after %d records' % (filename, record_count,), file=sys.stderr)
				

#This simply checks the file information by name
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