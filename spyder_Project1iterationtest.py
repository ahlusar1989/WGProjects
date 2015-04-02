 

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

## I am assuming that all of my files are going to be specified in unicode  

## Utilized Spyder's Scientific Computing IDE to debug, check for identation errors and test function suite

from __future__ import print_function

import os.path
import time
import logging
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


#Returns filename, rootdir and filesize 

def fileinfo(f):
    filename = os.path.basename(f)
    rootdir = os.path.dirname(f)  
    filesize = os.path.getsize(f)
    return filename, rootdir, filesize

#returns length of file
def file_len(f):
    with open(f) as f:
        for i, l in enumerate(f):
            pass
            return i + 1
#attempts to copy file and move file to it's directory
def copy_and_move_file(src, dest):
    try:
        os.rename(src, dest)
        # eg. src and dest are the same file
    except IOError as e:
        print('Error: %s' % e.strerror)

    
#def main(rootdir):      
#    while True:
#        time.sleep(1) #time between update check   
#    if added:
#        print('Sucessfully added new file! We are ready to validate: ' + f)
#        return validate_files(f)
#    else:
#        return move_to_failure_folder_and_return_error_file(f)

path = "."
dirlist = os.listdir(path)
 
def main(dirlist):   
    before = dict([(f, 0) for f in dirlist])
    while True:
        time.sleep(1) #time between update check
    after = dict([(f, None) for f in dirlist])
    added = [f for f in after if not f in before]
    if added:
        f = ''.join(added)
        print('Sucessfully added %s file - ready to validate') %()
        return validate_files(f)
    else:
        return move_to_failure_folder_and_return_error_file(f)


    
def validate_files(f):
    creation = time.ctime(os.path.getctime(f))
    lastmod = time.ctime(os.path.getmtime(f))
    if creation == lastmod and file_len(f) > 0:
        return move_to_success_folder_and_read(f)
    if file_len < 0 and creation != lastmod:
        return move_to_success_folder_and_read(f)
    else:
        return move_to_failure_folder_and_return_error_file(f)


#Potential Additions/Substitutions

def move_to_failure_folder_and_return_error_file():
    filename, rootdir, lastmod, creation, filesize = fileinfo(file)  
    os.mkdir('Failure')
    copy_and_move_file( 'Failure')
    initialize_logger('rootdir/Failure')
    logging.error("Either this file is empty or there are no lines")
     
             
def move_to_success_folder_and_read():
    filename, rootdir, lastmod, creation, filesize = fileinfo(file)  
    os.mkdir('Success')
    copy_and_move_file(rootdir, 'Success') #file name
    print("Success", file)
    return file_len(file)



if __name__ == '__main__':
   main(dirlist) 