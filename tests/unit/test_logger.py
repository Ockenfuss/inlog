import unittest as ut
from inlog.Logger import Logger
from pathlib import Path

class TestLogger(ut.TestCase):
    def setUp(self):
        self.logger = self.get_test_logger()
    def get_test_logger(self):
        return Logger({"a":1, "b": {"c": 2, "d": 3.0}, "e": {"f": "4.0", "g": "4.0, 5.0,6.0,"}}
, "1.0")

    def test_get(self):
        self.assertEqual(self.logger._get("a"),1)
        self.assertEqual(self.logger._get("b", "c"),2)
        self.assertIsInstance(self.logger._get(), dict)
        self.assertIsInstance(self.logger._get("b"), dict)
    
    def test_set(self):
        logger=self.get_test_logger()
        logger.set(4, "b", "c")
        self.assertEqual(logger.get("b", "c"),4)
        logger.set(5, "e")
        self.assertEqual(logger.get("e"),5)
        #Currently, you can also set a dict as leaf value. Unlike set_subtree, this will not generate new accessible keys
        logger.set({"h": 6}, "e")
        self.assertEqual(logger.get("e"),{"h": 6})
        self.assertRaises(KeyError, logger.get, "e", "h")
    
    def test_set_subtree(self):
        logger=self.get_test_logger()
        logger.set_subtree({"c": 5, "e":5}, "b")
        self.assertEqual(logger.get("b", "c"),5)
        self.assertEqual(logger.get("b", "e"),5)
        self.assertRaises(KeyError, logger.get, "b", "d")
    
    
    def test_get_item(self):
        logger=Logger({"a": 1, "b": {"c": {"b":2}}, "c": {"b": 3}}, "1.0")
        self.assertEqual(logger["a"],1)
        self.assertEqual(logger["b"],{"c": {"b":2}})
        self.assertEqual(logger["c"],{"b":2})
        self.assertEqual(logger["b","c"],{"b":2})
        self.assertEqual(logger["c","b"],2)
        self.assertEqual(logger["b","b"],2)
        self.assertRaises(KeyError,logger.__getitem__, ("a","b"))

    def test_set_item(self):
        logger=Logger({"a": 1, "b": {"c": {"b":2}}, "c": {"b": 3}}, "1.0")
        logger["a"]=5
        self.assertFalse(logger.is_accessed("a"))
        self.assertEqual(logger["a"],5)
        logger["c", "b"]=5
        self.assertEqual(logger["c","b"],5)
        logger["b", "c", "b"]=5
        self.assertEqual(logger["b", "c", "b"],5)
        self.assertRaises(KeyError,logger.__setitem__, ("a","b"), 5)

    def test_is_accessed(self):
        #Nothing is accessed
        self.logger._reset_access()
        self.assertFalse(self.logger.is_accessed())
        self.assertFalse(self.logger.is_accessed("a"))
        self.assertFalse(self.logger.is_accessed("b", "c"))

        #_get does not record an access
        self.logger._get("a")
        self.assertFalse(self.logger.is_accessed("a"))

        #get does record an access
        self.logger.get("a")
        self.assertTrue(self.logger.is_accessed("a"))
        self.assertFalse(self.logger.is_accessed("b"))

        #accessing an element does not access the parents
        self.logger.get("b", "c")
        self.assertFalse(self.logger.is_accessed("b"))
        self.assertTrue(self.logger.is_accessed("b", "c"))

        #accessing a parent does access the children as well
        self.logger._reset_access()
        self.logger.get("b")
        self.assertTrue(self.logger.is_accessed("b"))
        self.assertTrue(self.logger.is_accessed("b", "c"))

        #Repeated Access does not change anything
        self.logger.get("b", "c")
        self.logger.get("b")
        self.assertTrue(self.logger.is_accessed("b"))
        self.assertTrue(self.logger.is_accessed("b", "c"))
    
    def test_get_accessed_options(self):
        self.logger._reset_access()
        self.logger.get("a")
        self.assertEqual(self.logger.get_accessed_options("a"),1)
        self.assertIsNone(self.logger.get_accessed_options("b"))
        self.logger.get("b")
        self.assertEqual(self.logger.get_accessed_options("b") , {"c": 2, "d": 3.0})
        self.logger._reset_access()
        self.logger.get("a")
        self.logger.get("b", "c")
        self.assertEqual(self.logger.get_accessed_options("b") , {"c": 2})
        self.assertEqual(self.logger.get_accessed_options() , {"a":1, "b":{"c": 2}})
    
    def test_convert_type(self):
        logger=self.get_test_logger()
        #convert to str
        logger.convert_type(str, "b", "d")
        self.assertEqual(logger.get("b", "d"),"3.0")
        #convert subtree to float
        logger.convert_type(float, "b")
        self.assertEqual(logger.get("b", "d"),3.0)
        #convert to bool
        logger.set("true", "b", "d")
        logger.convert_type(bool, "b", "d")
        self.assertTrue(logger.get("b", "d"))
        logger.set(3.0, "b", "d")
    
    def test_convert_array(self):
        logger=self.get_test_logger()
        #single value
        logger.convert_array(float, "e", "f")
        self.assertEqual(logger.get("e", "f"),[4.0])
        #multiple values
        logger.convert_array(float, "e","g")
        self.assertEqual(logger.get("e", "g"),[4.0, 5.0, 6.0])
        #subtree
        logger=self.get_test_logger()
        logger.convert_array(float, "e")
        self.assertEqual(logger.get("e", "f"),[4.0])
        self.assertEqual(logger.get("e", "g"),[4.0, 5.0, 6.0])

    
    def test_create_log_dict(self):
        self.logger._reset_access()
        self.logger.get("b", "c")
        self.assertEqual(self.logger._create_log_dict()["options"]["a"],1)
        self.assertEqual(self.logger._create_log_dict(accessed_only=True)["options"]["b"],{"c": 2})
        self.assertNotIn("a" ,self.logger._create_log_dict(accessed_only=True)["options"])
    
    def test_create_log_txt(self):
        self.logger._reset_access()
        self.logger.get("b", "c")
        self.assertEqual('cd' , self.logger._create_log_txt()[0][:2])
        self.assertEqual('python' , self.logger._create_log_txt()[1][:6])
        self.assertIn('#    "a": 1,\n' , self.logger._create_log_txt())
        self.assertNotIn('#    "a": 1,\n' , self.logger._create_log_txt(accessed_only=True))
        self.assertIn('#    "b": {\n' , self.logger._create_log_txt(accessed_only=True))
    
    def test_str(self):
        self.logger._reset_access()
        self.logger.get("b", "c")
        st=str(self.logger)
        self.assertIn('    "a": 1,\n' , st)
        self.assertIn('    "b": {\n' , st)
    
    def test_repr(self):
        self.logger._reset_access()
        self.logger.get("b", "c")
        st=repr(self.logger)
        self.assertIn('    "a": 1,\n' , st)
        self.assertIn('    "b": {\n' , st)
    
    def test_create_multiple(self):
        """Test that multiple independent logger objects can be created in the same script."""
        logger1=Logger({"section1": {"name": "1"}}, "1.0")
        logger2=Logger({"section1": {"name": "2"}}, "1.0")
        self.assertEqual(logger1.get("section1", "name"), "1")
        self.assertEqual(logger2.get("section1", "name"), "2")
    
    def test_default_options(self):
        """Test that default options are used if not present in the config dict."""
        logger=Logger({"section1": {"name": "1"}}, "1.0", def_opts={"section1": {"name": "2", "age": "3"}})
        self.assertEqual(logger.get("section1", "name"), "1")
        self.assertEqual(logger.get("section1", "age"), "3")
    
    def test_get_logfile_name(self):
        # Replace
        file = "/path/to/file.txt"
        file_ext = ".log"
        change_ext = "replace"
        expected_result = [Path("/path/to/file.log")]
        result = Logger._get_logfile_name(file, file_ext, change_ext)
        self.assertEqual(result, expected_result)

        #Append
        file_ext = "log"
        change_ext = "append"
        expected_result = [Path("/path/to/file.txt.log")]
        result = Logger._get_logfile_name(file, file_ext, change_ext)
        self.assertEqual(result, expected_result)

        #no existing extension
        file = "/path/to/file"
        file_ext = "log"
        change_ext = "append"
        expected_result = [Path("/path/to/file.log")]
        result = Logger._get_logfile_name(file, file_ext, change_ext)
        self.assertEqual(result, expected_result)

        # no extension
        file = "/path/to/file.txt"
        file_ext = None
        change_ext = "append"
        expected_result = [Path("/path/to/file.txt")]
        result = Logger._get_logfile_name(file, file_ext, change_ext)
        self.assertEqual(result, expected_result)

        # no file
        file = None
        expected_result = []
        result = Logger._get_logfile_name(file, file_ext, change_ext)
        self.assertEqual(result, expected_result)

        # Test with multiple files
        files = ["/path/to/file1.csv", "/path/to/file2.txt"]
        file_ext = ".log"
        change_ext = "append"
        expected_result = [Path("/path/to/file1.csv.log"), Path("/path/to/file2.txt.log")]
        result = Logger._get_logfile_name(files, file_ext, change_ext)
        self.assertEqual(result, expected_result)

        # Test with Path objects
        files = [Path("/path/to/file1.csv"), Path("/path/to/file2.txt")]
        file_ext = "log"
        change_ext = "replace"
        expected_result = [Path("/path/to/file1.log"), Path("/path/to/file2.log")]
        result = Logger._get_logfile_name(files, file_ext, change_ext)
        self.assertEqual(result, expected_result)

        # Test with invalid change_ext value
        file = "/path/to/file.txt"
        file_ext = ".log"
        change_ext = "invalid"
        with self.assertRaises(ValueError):
            Logger._get_logfile_name(file, file_ext, change_ext)

if __name__ == '__main__':
    ut.main()