import random

from tests.test_case import PyBeamerTestCase
from pybeamer.nodes import Node,Section,Frame,Itemize,Enumerate,Text,Block
from pybeamer.exceptions import WrongNodeTypeError

class TestNodes(PyBeamerTestCase):
    def setUp(self) -> None:
        self.node_classes_objs = [Section("title"),Frame(),Itemize(),Enumerate(),Text("text"),Block()]

    def test_node(self):
        with self.assertRaises(Exception): # a node can't be directly instanciated
            Node()

    def test_section(self):
        title = "title"
        section = Section(title)
        self.assertEqual(section.title,title)
        self.assertEqual(section._render_nodes(),"")
        section.add(Frame())
    
    def test_frame(self):
        title = random.choice([None,"title"])
        frame = Frame(title)
        self.assertEqual(frame.title,title)

    def test_children(self):
        for obj in [Section("title"),Frame(),Itemize(),Enumerate(),Text("text"),Block()]:
            for node_obj in self.node_classes_objs:
                if (not obj.__class__.__authorized_direct_children__) or (not node_obj.__class__.__name__ in obj.__class__.__authorized_direct_children__):
                    with self.assertRaises(WrongNodeTypeError):
                        obj.add(node_obj)
                else:
                    obj.add(node_obj)

        



        
