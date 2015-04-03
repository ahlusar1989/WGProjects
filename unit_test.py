#A simple unit test would look like this (assuming watchscript.py is the name 
of the script to be tested): 

import unittest 

from watchscript import file_len 

class FileLen(unittest.TestCase): 
    def test_five(self): 
        LEN = 5 
        FILENAME = "tmp.txt" 
        with open(FILENAME, "w") as f: 
            f.write("*" * LEN) 

        self.assertEqual(file_len(FILENAME), 5) 
        
if __name__ == "__main__": 
    unittest.main() 