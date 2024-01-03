import unittest as ut
import inlog
from io import StringIO

class TestLogger(ut.TestCase):
    def test_load_ini(self):
        f_ini=StringIO("""
                [section1]
                start=1
                intermediate=abc.dat
                [section2]
                foo=2
                """)
        logger=inlog.load_ini(f_ini, "1.0")
        self.assertEqual(logger.get("section1", "start"), "1")
        self.assertEqual(logger.get("section1", "intermediate"), "abc.dat")
        self.assertEqual(logger.get("section2", "foo"), "2")
        self.assertRaises(FileNotFoundError, inlog.load_ini, "does/not/exist.ini", "1.0")
    
    def test_load_yaml(self):
        f_yaml=StringIO("""
                section1:
                    start: 1
                    intermediate: abc.dat
                section2:
                    foo: 2
                """)
        logger=inlog.load_yaml(f_yaml, "1.0")
        self.assertEqual(logger.get("section1", "start"), 1)
        self.assertEqual(logger.get("section1", "intermediate"), "abc.dat")
        self.assertEqual(logger.get("section2", "foo"), 2)
        self.assertRaises(FileNotFoundError, inlog.load_yaml, "does/not/exist.ini", "1.0")
    
    def test_load_json(self):
        f_json=StringIO("""
                {
                    "section1": {
                        "start": 1,
                        "intermediate": "abc.dat"
                    },
                    "section2": {
                        "foo": 2
                    }
                }
                """)
        logger=inlog.load_json(f_json, "1.0")
        self.assertEqual(logger.get("section1", "start"), 1)
        self.assertEqual(logger.get("section1", "intermediate"), "abc.dat")
        self.assertEqual(logger.get("section2", "foo"), 2)
        self.assertRaises(FileNotFoundError, inlog.load_json, "does/not/exist.ini", "1.0")
    
    def test_default_ini(self):
        """Test that default values are used if not present in the config file"""
        f_ini=StringIO("""
                [section1]
                start=1
                intermediate=abc.dat
                """)
        logger=inlog.load_ini(f_ini, "1.0", def_opts={"section1": {"start": "2", "stop": "3"}})
        self.assertEqual(logger.get("section1", "start"), "1")
        self.assertEqual(logger.get("section1", "intermediate"), "abc.dat")
        self.assertEqual(logger.get("section1", "stop"), "3")

