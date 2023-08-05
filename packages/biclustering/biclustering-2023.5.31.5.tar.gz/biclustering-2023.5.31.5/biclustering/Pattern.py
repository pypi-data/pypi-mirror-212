import copy

class Pattern:
    def __init__(self, itemset: set, object: list):
        self.itemset = set(itemset)
        self.object = copy.deepcopy(object)
    
    def __eq__(self, __o) -> bool:
        if len(__o.itemset) != len(self.itemset):
            return False
        if self.itemset != __o.itemset:
            return False
        return self.has_same_object(__o)

    def add_item(self, item):
        self.itemset.add(item)
    
    def get_object(self) -> list:
        return copy.deepcopy(self.object)
    
    def get_itemset(self) -> set:
        return self.itemset
    
    def get_copy(self):
        return Pattern(self.itemset, self.object)
    
    def size(self) -> int:
        return len(self.itemset)
    
    def is_closed(self, pattern_list) -> bool:
        """Checks whether the pattern is closed within pattern_list"""
        search_space = [pat for pat in pattern_list if pat.size() > self.size() and self.has_same_object(pat)]
    
        for pat in search_space:
            if self.get_itemset().issubset(pat.get_itemset()):
                return False
                
        return True
    
    def intersection(self, other):
        """Returns the interesction with the given pattern"""
        itemset = self.get_itemset().intersection(other.get_itemset())
        new_object = list(set(self.get_object()).union(set(other.get_object())))
        return Pattern(itemset, new_object)

    def merge_leaf(self, leaf: list):
        self.object = list(set(self.get_object()).union(set(leaf)))
    
    def is_object_subset(self, object1, object2):
        """Returns whether object1 is a subset of object2"""
        return set(object1).issubset(set(object2))

    def has_same_object(self, other):
        return self.is_object_subset(self.object, other.get_object()) and self.is_object_subset(other.get_object(), self.object)

    def __str__(self): 
        return "Pattern(\n\titemset: "+str(self.itemset)+"\n\tobject: "+str(self.object)+"\n)"
    
    def support_count(self):
        return len(self.object)
    
    def get_object_as_line(self):
        return str(self.get_object())
        
    def toJSON(self, include_object = False) ->dict:
        JSON = {
            "itemset": list(self.itemset),
            "support": len(self.object)
        }

        if(include_object):
            JSON["object"] = self.object
        
        return JSON
