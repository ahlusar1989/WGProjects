##I am ssuming all filenames come directly from the commandline. No searching of a directory. 

## I am assuming that all of my files are going to be specified in unicode  

# # #! /usr/bin/python

from __future__ import print_function

import os
import time
import glob
import sys

def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "all.log"),"w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


#Helper Functions for the Success and Failure Folder Outcomes, respectively

    def file_len(filename):
        with open(filename) as f:
            for i, l in enumerate(f):
                pass
            return i + 1


    def copyFile(src, dest):
        try:
            shutil.copy(src, dest)
        # eg. src and dest are the same file
        except shutil.Error as e:
            print('Error: %s' % e)
        # eg. source or destination doesn't exist
        except IOError as e:
            print('Error: %s' % e.strerror)


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


path = "/Users/sahluwalia/Desktop/Projects/IntroToPython/test"
dirslist = os.listdir(path)



RECORD_LENGTH = 32

# Made a new function, called main(), with a loop that calls 
# validate_files(), with a sleep after each pass. Before, my present code 
# was assuming all filenames come directly from the commandline.  There was no actual searching of a directory.  

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


##Process_data is another level of securitization that for checks file length 

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
            return False, counter, 
    return True, counter

#This checks for byte size and 

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
            return copyFile(dirlist,"Success"), file_len(filename)

            # How do I use shututil() to move this to a "Success" Folder print("Success! File has been read", file) 
        else: ####
            # -- Failure; need additional logic here to determine cause of the failure - OSError perhaps?
            print('Failure with %s after %d records' % (filename, record_count,), file=sys.stderr)
            return copyFile(dirlist,"Failure"), file_len(filename)

#Potential Additions/Substitutions  - what are the implications/consequences for this 

def move_to_failure_folder_and_return_error_file():
    os.mkdir('Failure!')
    copyFile(filename, 'Failure')
    initialize_logger('rootdir/Failure')
    logging.error("Either this file is empty or the lines")
     
             
def move_to_success_folder_and_read(file):
    os.mkdir('Success!')
    copyFile(filename, 'Success')
    print("Success", file)
    return file_len()

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