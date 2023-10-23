import unittest as ut
from inlog.Tree import TreeNode

class TestTree(ut.TestCase):
    # def setUp(self):

    def test_init(self):
        tn=TreeNode(1)
        self.assertEqual(tn.value,1)
        self.assertEqual(tn.children,{})
    
    def test_get(self):
        tn=TreeNode(1, {"a":TreeNode(2)})
        self.assertEqual(tn.get("a").value,2)

    def test_from_dict(self):
        d={"a":1, "b":{"c":2}}
        tree=TreeNode.from_leafdict(d)
        print(tree)
        self.assertEqual(len(tree.children),2)
        self.assertEqual(len(tree.children["b"].children),1)
        self.assertEqual(tree.get("a").value,1)
        self.assertEqual(tree.get("b","c").value,2)
    
    def test_to_dict(self):
        d={"a":1, "b":{"c":2}}
        tree=TreeNode.from_leafdict(d)
        self.assertEqual(tree.to_leafdict(),d)

    def test_update(self):
        tree=TreeNode.from_leafdict({"section1": {"name": "1"}})
        #Update a subsection
        tree_update=TreeNode.from_leafdict({"age": "2", "parents":{"mother":"mia"}})
        tree.update(tree_update, "section1")
        self.assertEqual(tree.get("section1", "name").value, "1")
        self.assertEqual(tree.get("section1", "age").value, "2")
        self.assertEqual(tree.get("section1", "parents","mother").value, "mia")
        #Update without specifying a section. Note how this is different from set(), which would not keep the old options.
        tree_update=TreeNode.from_leafdict({"section1": {"name": "2"}})
        tree.update(tree_update)
        self.assertEqual(tree.get("section1", "name").value, "2")
        self.assertEqual(tree.get("section1", "age").value, "2")
        #Update an item which has no children yet. This is equivalent to set().
        tree.update(tree_update, "section1", "name")
    
    def test_copy(self):
        tree=TreeNode.from_leafdict({"section1": {"name": "1"}})
        tree_copy=tree.copy()
        self.assertEqual(tree.to_leafdict(), tree_copy.to_leafdict())
        tree_copy.update(TreeNode.from_leafdict({"section1": {"name": "2"}}))
        self.assertNotEqual(tree.to_leafdict(), tree_copy.to_leafdict())
    
    def test_make_leaf(self):
        tree=TreeNode.from_leafdict({"a": {"b": {"c": 1}}})
        tree.make_leaf("a", "b")
        self.assertRaises(KeyError, tree.get, "a", "b", "c")
    
    def test_map(self):
        tree=TreeNode.from_leafdict({"a1": {"b1": {"c": 1}, "b2": 1}, "a2": 1}, other=0)
        print(tree)
        tree.map(lambda x: x+1)
        self.assertEqual(tree.get("a1", "b1", "c").value, 2)
        self.assertEqual(tree.get("a1", "b2").value, 2)
        self.assertEqual(tree.get("a2").value, 2)


    
    def test_set_all(self):
        tree=TreeNode.from_leafdict({"section1": {"name": 1}})
        tree.set_all(2)
        self.assertEqual(tree.value, 2)
        self.assertEqual(tree.get("section1").value, 2)
        self.assertEqual(tree.get("section1", "name").value, 2)
        tree.set_all(3, "section1", "name")
        self.assertEqual(tree.get("section1").value, 2)
        self.assertEqual(tree.get("section1", "name").value, 3)
    
    def test_match_depth_first(self):
        d={"a": 1, "b": {"c": {"b":2}}, "c": {"b": 3}}
        tree=TreeNode.from_leafdict(d)
        self.assertIs(tree.match_depth_first("a"), tree.get("a"))
        self.assertIs(tree.match_depth_first("b"),tree.get("b"))
        self.assertIs(tree.match_depth_first("c"),tree.get("b", "c"))
        self.assertIs(tree.match_depth_first("b","c"),tree.get("b", "c"))
        self.assertIs(tree.match_depth_first("c","b"),tree.get("b", "c", "b"))
        self.assertIsNone(tree.match_depth_first("a","b"))
    
    def test_filter_any(self):
        d={"a":0, "b": {"c": {"d":1}, "g": {"h":2}}, "e": {"f": 3}}
        tree=TreeNode.from_leafdict(d)
        def filter_func(x):
            if x.value is None:
                return False
            if x.value<=1:
                return True
        tree_filtered=tree.filter_any(filter_func=filter_func)
        self.assertEqual(tree_filtered.get("a").value, 0)
        self.assertEqual(tree_filtered.get("b","c","d").value, 1)
        self.assertRaises(KeyError, tree_filtered.get, "b", "g", "h")
        self.assertRaises(KeyError, tree_filtered.get, "e", "f")

        def filter_func(x):
            if x.value is None:
                return False
            if x.value<=2:
                return True
        tree_filtered=tree.filter_any(filter_func=filter_func)
        self.assertEqual(tree_filtered.get("a").value, 0)
        self.assertEqual(tree_filtered.get("b","c","d").value, 1)
        self.assertEqual(tree_filtered.get("b", "g", "h").value, 2)
        self.assertRaises(KeyError, tree_filtered.get, "e", "f")
    
    def test_select(self):
        d={"a":0, "b": {"c": {"d":1}, "g": {"h":2}}, "e": {"f": 3}}
        selection={"a":0, "b": {"c": {"d":0}}, "e": 0}
        tree=TreeNode.from_leafdict(d)
        tree_selection=TreeNode.from_leafdict(selection)
        tree_selected=tree.select(tree_selection)
        self.assertEqual(tree_selected.get("a").value, 0)
        self.assertEqual(tree_selected.get("b","c","d").value, 1)
        self.assertEqual(tree_selected.get("e").value, None)
        self.assertRaises(KeyError, tree_selected.get, "b", "g", "h")
        self.assertRaises(KeyError, tree_selected.get, "e", "f")

    #From Logger. Unused now. Might be a useful testcase if implemented.
    # def test_find_depth_first(self):
    #     logger=self.get_test_logger()
    #     logger.options={"a": 1, "b": {"c": 2}, "c": {"d": 3}}
    #     self.assertEqual(logger._find_depth_first("a"),["a"])
    #     self.assertEqual(logger._find_depth_first("b"),["b"])
    #     self.assertEqual(logger._find_depth_first("c"),["b","c"])
    #     self.assertEqual(logger._find_depth_first("d"),["c","d"])
    #     self.assertEqual(logger._find_depth_first("e"),None)