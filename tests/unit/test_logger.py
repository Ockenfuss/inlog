import unittest as ut
from inlog.Logger import Logger

class TestLogger(ut.TestCase):
    def setUp(self):
        self.logger = self.get_test_logger()
    def get_test_logger(self):
        return Logger({"a":1, "b": {"c": 2, "d": 3.0}, "e": {"f": "4.0", "g": "4.0, 5.0,6.0,"}}
, "1.0")

    def test_get(self):
        assert(self.logger.get("a")==1)
        assert(self.logger.get("b", "c")==2)
        assert(isinstance(self.logger.get(), dict))
        assert(isinstance(self.logger.get("b"), dict))
    
    def test_set(self):
        self.logger.set(4, "b", "c")
        assert(self.logger.get("b", "c")==4)
        self.logger.set(5, "e")
        assert(self.logger.get("e")==5)
    
    def test_find_depth_first(self):
        logger=self.get_test_logger()
        logger.options={"a": 1, "b": {"c": 2}, "c": {"d": 3}}
        assert(logger._find_depth_first("a")==["a"])
        assert(logger._find_depth_first("b")==["b"])
        assert(logger._find_depth_first("c")==["b","c"])
        assert(logger._find_depth_first("d")==["c","d"])
        assert(logger._find_depth_first("e")==None)
    
    def test_get_item(self):
        logger=self.get_test_logger()
        logger.options={"a": 1, "b": {"c": {"b":2}}, "c": {"b": 3}}
        self.assertEqual(logger["a"],1)
        self.assertEqual(logger["b"],{"c": {"b":2}})
        self.assertEqual(logger["c"],{"b":2})
        self.assertEqual(logger["b","c"],{"b":2})
        self.assertEqual(logger["c","b"],2)
        self.assertEqual(logger["b","b"],2)
        self.assertRaises(KeyError,logger.__getitem__, ("a","b"))

    def test_set_item(self):
        logger=self.get_test_logger()
        logger.options={"a": 1, "b": {"c": {"b":2}}, "c": {"b": 3}}
        logger["a"]=5
        self.assertEqual(logger["a"],5)
        logger["c", "b"]=5
        self.assertEqual(logger["c","b"],5)
        logger["b", "c", "b"]=5
        self.assertEqual(logger["b", "c", "b"],5)
        self.assertRaises(KeyError,logger.__setitem__, ("a","b"), 5)

    def test_match_depth_first(self):
        logger=self.get_test_logger()
        logger.options={"a": 1, "b": {"c": {"b":2}}, "c": {"b": 3}}
        self.assertEqual(logger._match_depth_first("a"),["a"])
        self.assertEqual(logger._match_depth_first("b"),["b"])
        self.assertEqual(logger._match_depth_first("c"),["b", "c"])
        self.assertEqual(logger._match_depth_first("b","c"),["b", "c"])
        self.assertEqual(logger._match_depth_first("c","b"),["b", "c", "b"])
        self.assertIsNone(logger._match_depth_first("a","b"))


    
    def test_is_accessed(self):
        #Nothing is accessed
        self.logger._reset_access()
        assert(not self.logger.is_accessed())
        assert(not self.logger.is_accessed("a"))
        assert(not self.logger.is_accessed("b", "c"))

        #_get does not record an access
        self.logger._get("a")
        assert(not self.logger.is_accessed("a"))

        #get does record an access
        self.logger.get("a")
        assert(self.logger.is_accessed("a"))
        assert(not self.logger.is_accessed("b"))

        #accessing an element does access the parents as well
        self.logger.get("b", "c")
        assert(self.logger.is_accessed("b"))
        assert(self.logger.is_accessed("b", "c"))
        #Repeated Access does not change anything
        self.logger.get("b")
        assert(self.logger.is_accessed("b"))
        assert(self.logger.is_accessed("b", "c"))
    
    def test_get_accessed_options(self):
        self.logger._reset_access()
        self.logger.get("a")
        assert(self.logger.get_accessed_options("a")==1)
        assert(self.logger.get_accessed_options("b") is None)
        self.logger.get("b")
        assert(self.logger.get_accessed_options("b") == {})
        self.logger.get("b", "c")
        assert(self.logger.get_accessed_options("b") == {"c": 2})
        assert(self.logger.get_accessed_options() == {"a":1, "b":{"c": 2}})
    
    def test_convert_type(self):
        #convert to str
        self.logger.convert_type(str, "b", "d")
        assert(self.logger.get("b", "d")=="3.0")
        #convert subtree to float
        self.logger.convert_type(float, "b")
        assert(self.logger.get("b", "d")==3.0)
        #convert to bool
        self.logger.set("true", "b", "d")
        self.logger.convert_type(bool, "b", "d")
        assert(self.logger.get("b", "d"))
        self.logger.set(3.0, "b", "d")
    
    def test_convert_array(self):
        #single value
        self.logger.convert_array(float, "e", "f")
        assert(self.logger.get("e", "f")==[4.0])
        #multiple values
        self.logger.convert_array(float, "e","g")
        assert(self.logger.get("e", "g")==[4.0, 5.0, 6.0])
        #subtree
        self.logger=self.get_test_logger()
        self.logger.convert_array(float, "e")
        assert(self.logger.get("e", "f")==[4.0])
        assert(self.logger.get("e", "g")==[4.0, 5.0, 6.0])

    
    def test_create_log_dict(self):
        self.logger._reset_access()
        self.logger.get("b", "c")
        assert(self.logger._create_log_dict()["options"]["a"]==1)
        assert(self.logger._create_log_dict(accessed_only=True)["options"]["b"]=={"c": 2})
        assert("a" not in self.logger._create_log_dict(accessed_only=True)["options"])
    
    def test_create_log_txt(self):
        self.logger._reset_access()
        self.logger.get("b", "c")
        assert('#    "a": 1,\n' in self.logger._create_log_txt())
        assert('#    "a": 1,\n' not in self.logger._create_log_txt(accessed_only=True))
        assert('#    "b": {\n' in self.logger._create_log_txt(accessed_only=True))




if __name__ == '__main__':
    unittest.main()