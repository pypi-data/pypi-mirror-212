from __future__ import annotations

class list(list):
    def __new__(cls, iterable = None):
        if iterable is not None:
            return super().__new__(list, iterable)
        return super().__new__(list)
    
    def __mod__(self, other):
        if isinstance(other, list) and len(self) == len(other):
            new_list = list()
            for i in range(len(self)):
                new_list.append(self[i] % other[i])
            return new_list