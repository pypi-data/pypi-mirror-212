import uuid
from blue_object import Object

class GameObject(Object):
    def __init__(self, parent=None) -> None:
        self.id = uuid.uuid1().int
        self.name = "GameObject"
        self.children = {}
        if parent == None:
            self.parent = 'scene'
        else:
            self.parent = parent 

    def add_child(self, object):
        self.children[object.id] = object
        object.parent = self

    def get_children(self):
        return self.children

    def get_object_tree(self):
        for i in self.children:
            self.children.get_object_tree()

    def __str__(self) -> str:
        return self.name
