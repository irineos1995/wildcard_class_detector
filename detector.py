from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag, Doctype


# Base case
def get_parents_recursively(tree, wildcard_classes):
    if not tree:
        return wildcard_classes
    else:
        if "childGenerator" in dir(tree):
            for child in tree.childGenerator():
                if isinstance(child, Tag):
                    child_class = child.get("class", [])
                    if child_class:
                        # parents = [tuple(parent.get('class', ())) for parent in child.parents]
                        direct_parent = tuple(child.parent.get('class',())) if child.parent else None
                        # print(f'{tuple(child_class)} has DIRECT parent {direct_parent}')
                        if not direct_parent:
                            wildcard_classes.append(tuple(child_class))
                else:
                    continue
                get_parents_recursively(child, wildcard_classes)
        else:
            if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                pass
    return wildcard_classes

def orphan_classes(source_code_file):
    '''
        This function is responsible for identifying CSS classes that have no DIRECT parents.
        That is a good indication that those classes belong to the "wildcard" category.
    '''
    with open(source_code_file, 'r') as source_code:
        parsed_code = BeautifulSoup(source_code, 'html.parser')
        for child in parsed_code.childGenerator():
            if isinstance(child, Tag):
                wildcard_classes = get_parents_recursively(child, wildcard_classes=[])
                print(wildcard_classes)

orphan_classes('test_cases/case1.html')