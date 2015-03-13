import curses
class InvalidTransition(Exception):
    pass

class PathExist(Exception):
    pass
    
class TrieFSA(object):
    """
    Trie implementation using dictionary

    >>> t = TrieFSA()
    >>> t.add_paths(['bar', 'baz', 'barz'], last_value_func = lambda o: "_end_")
    >>> t.add_paths(['bar'], last_value_func = lambda o: "_end_")# doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    PathExist: Path 'bar' exist
    >>> t.valid_input()
    ['b']
    >>> t.add_paths(['foo'], last_value_func = lambda o: "_end_")
    >>> t.valid_input()
    ['b', 'f']
    >>> t.take('b')
    >>> t.take('a')
    >>> t.take('r')
    >>> t.matching_paths()
    [(['b', 'a', 'r'], '_end_'), (['b', 'a', 'r', 'z'], '_end_')]
    >>> t.take('a') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    InvalidTransition: "Invalid input 'a'. Valid are ['z']"
    >>> t.reset()
    >>> t.take('f')
    >>> t.matching_paths()
    [(['f', 'o', 'o'], '_end_')]
    >>> t.has_path('bar')
    True
    >>> t.has_path('ba')
    False
    >>> t.has_path('blah')
    False
    """
    
    def __init__(self, last_key = None):
        root = {}
        self.root = root
        self.last_key = last_key
        self.state = root
        self.path = []
        
    def add_paths(self, iter_list, last_value_func = None):
        assert callable(last_value_func)
        
        for iterable in iter_list:
            if self.has_path(iterable):
                raise PathExist("Path %r exist" %(iterable))

            cur_dict = self.root
            for o in iterable:
                cur_dict = cur_dict.setdefault(o, {})
            cur_dict[self.last_key] = last_value_func(iterable)

    def valid_input(self):
        return [k for k in self.state if k is not self.last_key]
        
    def take(self, key):
        if key in self.state:
            self.path.append(key)
            self.state = self.state[key]
        else:
            raise InvalidTransition("\"Invalid input %r. Valid are %r\"" %(key, self.valid_input()))
        
    def matching_paths(self):
        """
        Return the matching paths of the current state
        """
        def aux(state, path):
            paths = []
            for key in state:
                if key == self.last_key:
                    paths.append((path, state[key]))
                else:
                    paths += aux(state[key], path + [key])
            return paths
                
        return aux(self.state, self.path)
    
    def reset(self):
        self.state = self.root
        self.path = []

    def has_path(self, iterable):
        current = self.root
        for i in iterable:
            try:
                current = current[i]
            except KeyError:
                return False

        return self.last_key in current
