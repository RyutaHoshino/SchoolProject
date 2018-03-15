from xml.etree import ElementTree
import sys

def dump_node(node, indent=0):
    print("{}{} {} {}".format('    ' * indent, node.tag, node.attrib, node.text.strip()))
    for child in node:
        dump_node(child, indent + 1)

if __name__ == '__main__':
    tree = ElementTree.parse(sys.argv[1])
    dump_node(tree.getroot())
