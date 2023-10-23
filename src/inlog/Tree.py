class TreeNode(object):
    def __init__(self, value=None, children=None) -> None:
        self.value=value
        if children is None:
            children={}
        self.children=children
        
    
    @classmethod
    def from_leafdict(cls, leafs: dict, other=None):
        children={}
        for k,v in leafs.items():
            if isinstance(v, dict):
                children[k]=cls.from_leafdict(v, other)
            else:
                children[k]=TreeNode(v)
        return cls(value=other, children=children)
    
    def to_leafdict(self) -> dict:
        if len(self.children)==0:
            return self.value
        d={}
        for k,v in self.children.items():
            d[k]=v.to_leafdict()
        return d
    
    def get(self, *keys):
        if len(keys)==0:
            return self
        return self.get(*keys[:-1]).children[keys[-1]]
    
    def set(self, tree_node, *keys):
        self.get(*keys[:-1]).children[keys[-1]]=tree_node
    
    def to_prettystr(self, depth=0) -> str:
        offset="  "*depth+"|-"
        pretty=f"TreeNode({self.value})\n"
        for k,v in self.children.items():
            pretty+=f"{offset}{k}: {v.to_prettystr(depth+1)}"
        return pretty
    
    def __repr__(self) -> str:
        return self.to_prettystr()
    
    def update(self, tree_node, *keys):
        subtree=self.get(*keys)
        subtree.value=tree_node.value
        for k,v in tree_node.children.items():
            if k in subtree.children:
                subtree.children[k].update(v)
            else:
                subtree.children[k]=v

    def copy(self):
        copy=TreeNode(self.value)
        for k,v in self.children.items():
            copy.children[k]=v.copy()
        return copy
    
    def set_all(self, value, *keys):
        if len(keys)==0:
            self.value=value
            for k,v in self.children.items():
                v.set_all(value)
        else:
            self.children[keys[0]].set_all(value, *keys[1:])
    
    def make_leaf(self, *keys):
        self.get(*keys).children={}
    
    def map(self, function):
        self.value=function(self.value)
        for k,v in self.children.items():
            v.map(function)
    
    def match_depth_first(self, *keys):
        if len(keys)==0:
            return self
        for k,v in self.children.items():
            result=None
            if k==keys[0]:
                result=v.match_depth_first(*keys[1:])
            else:
                result=v.match_depth_first(*keys)
            if result is not None:
                return result
        return None
    
    def filter_any(self, filter_func=lambda x: bool(x.value)):
        """Return the smallest possible subtree which contains all nodes for which filter_func returns True

        Parameters
        ----------
        filter_func : function, optional
            Function which takes a TreeNode as input and returns True or False. The default is lambda x: bool(x.value).

        Returns
        -------
        TreeNode or None
            The filtered subtree or None if no node matches the filter.
        """
        filtered_children={}
        for k,v in self.children.items():
            filtered=v.filter_any(filter_func)
            if filtered is not None:
                filtered_children[k]=filtered
        if len(filtered_children)>0:
            return TreeNode(self.value, filtered_children)
        elif filter_func(self):
            return TreeNode(self.value)
        else:
            return None
        
    def select(self, selection_tree):
        """Return a subtree which contains all nodes which are in selection_tree

        Parameters
        ----------
        selection_tree : TreeNode
            The tree which specifies which nodes to select

        Returns
        -------
        TreeNode
            The selected subtree
        """
        selected_children={}
        for k,v in self.children.items():
            if k in selection_tree.children:
                selected_children[k]=v.select(selection_tree.children[k])
        return TreeNode(self.value, selected_children)


