#Various integrations tests for inlog, including file IO
import unittest as ut
from inlog.Logger import Logger
from pathlib import Path
import tempfile

class TestLogger(ut.TestCase):
    def setUp(self):
        self.logger = self.get_test_logger()
    def get_test_logger(self):
        return Logger({"a":1, "b": {"c": 2, "d": 3.0}, "e": {"f": "4.0", "g": "4.0, 5.0,6.0,"}}, "1.0")

    def test_write_log(self):
        with tempfile.TemporaryDirectory() as tempdir:
            datafile=Path(tempdir)/"data.txt"
            logfile=Path(tempdir)/"data.txt.log"
            logger=self.get_test_logger()
            logger.get("a")
            logger.write_log(datafile)
            with open(logfile, "r") as file:
                lines=file.readlines()
                self.assertTrue('    "dependencies": {}\n'in lines)
                self.assertTrue('    "output_files": [],\n'in lines)
                self.assertTrue('        "a": 1\n' in lines)
    
    def test_write_log_deprecation(self):
        #Test if a deprecation warning is raised if only a file with replaced extension exists
        #This was the default before version 2.2.0
        with tempfile.TemporaryDirectory() as tempdir:
            datafile=Path(tempdir)/"data.txt"
            datafile2=Path(tempdir)/"data2.txt"
            logfile=Path(tempdir)/"data2.txt.log"
            logger=self.get_test_logger()
            logger.get("a")
            logger.write_log(datafile, ext_modification_mode='replace') #create an old-style log file
            #assert that a deprecation warning is raised
            with self.assertWarns(DeprecationWarning):
                logger.write_log(datafile2, old_logs=datafile) #create a new-style log file
            #assert that the new log file is created
            self.assertTrue(logfile.exists())



if __name__ == '__main__':
    ut.main()
        