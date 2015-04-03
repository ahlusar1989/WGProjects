 
#ASSUMPTIONS

#  Without data to examine here, I can only guess based on this requirement's language that 
#  fixed records are in the input.

#  I made the assumption that the directories are in the same filesystem

# I am assuming that all of my files are going to be specified in unicode 

# "Record length" was assumed to signify line length of a file

# Addtional comments added for each function (please see below)

# # I wrote this program that takes the logic of a while loop and demonstrates calling a function from within a function.  
# I tested this little sample on a small set of files created with MD5 checksums.  I wrote the Python in such a way as it 
# would work with Python 2.x or 3.x (note the __future__ at the top).

# There are so many wonderful ways of failure, so, from a development standpoint, I would probably spend a bit 
# more time trying to determine which failure(s) I would want to report to the user, and how (perhaps creating my own Exceptions)

# The only other comments I would make are about safe-file handling.

# # #   #1:  Question: After a user has created a file that has failed (in
# # #        processing),can the user create a file with the same name?
# # #        If so, then you will probably want to look at some sort
# # #        of file-naming strategy to avoid overwriting evidence of
# # #        earlier failures.

# File naming is a tricky thing.  I referenced the tempfile module [1] and the Maildir naming scheme to see two different 
# types of solutions to the problem of choosing a unique filename. 

## Utilized Spyder's Scientific Computing IDE to debug, check for indentation errors and test function suite

from __future__ import print_function

import os.path
import time
import difflib
import logging

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


#This function's purpose is to obtain the filename, rootdir and filesize 

def fileinfo(f):
    filename = os.path.basename(f)
    rootdir = os.path.dirname(f)  
    filesize = os.path.getsize(f)
    return filename, rootdir, filesize

#This helper function returns the length of the file

def file_len(f):
    with open(f) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# If directories ARE in different file systems, I would use the following helper function:

# def move(src, dest): 
#     shutil.move(src, dest)

#This helper function attempts to copy file and move file to the respective directory
#I am assuming that the directories are in the same filesystem

def copy_and_move_file(src, dest):
    try:
        os.rename(src, dest)
        # eg. src and dest are the same file
    except IOError as e:
        print('Error: %s' % e.strerror)


path = "."


# Caveats of the "main" function is that it does not scale well 
#(although it is appropriate if one assumes that there will be few changes)

# It does not account for updated files existing in the directory - only new files "dropped" in
# (If this was included in the requirements, os.stat would be appropriate here)

 
def main(path):   
    while True:
        before = set([f for f in os.lisdir(path)])
        time.sleep(1) #time between update check
        after = set([f for f in os.listdir(path)])
        added = [f for f in after if not f in before]
        if added:
            f = ''.join(added) #assuming that one file is added
            print('Sucessfully added %s file - ready to validate') %(f)
            return validate_files(f)

    
def validate_files(f):
    #The following would could be used as an added level for security
    # creation = time.ctime(os.path.getctime(f))
    # lastmod = time.ctime(os.path.getmtime(f))
    if file_len(f) > 0 and ##### need to compare record length(line length):
        return move_to_success_folder_and_read(f)
    else:
        return move_to_failure_folder_and_return_error_file(f)


# Failure/Success Folder Functions

def move_to_failure_folder_and_return_error_file(f):
    filename, rootdir, filesize = fileinfo(f) #I am being redundant for the sake of explicitness to the compiler  
    os.mkdir('Failure')
    copy_and_move_file(rootdir, 'Failure') #file src to file destination
    initialize_logger('rootdir/Failure')
    logging.error("Either this file is empty or there are no lines") #assuming that record length is equivalent to line length
     
             
def move_to_success_folder_and_read(f):
    filename, rootdir, filesize = fileinfo(f)  
    os.mkdir('Success')
    copy_and_move_file(rootdir, 'Success') #file src to file destination
    print("Success", f)
    return file_len(f)



if __name__ == '__main__':
   main(path) 