from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag, Doctype


def get_parents_recursively(tree, parentless_classes):
    if not tree:
        return parentless_classes
    else:
        if "childGenerator" in dir(tree):
            for child in tree.childGenerator():
                if isinstance(child, Tag):
                    child_class = child.get("class", [])
                    if child_class:
                        direct_parent = tuple(child.parent.get('class',())) if child.parent else None
                        if not direct_parent:
                            parentless_classes.append(tuple(child_class))
                else:
                    continue
                get_parents_recursively(child, parentless_classes)
        else:
            if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                pass
    return parentless_classes

def get_children_recursively(tree, childless_classes):
    if not tree:
        return childless_classes
    else:
        if "childGenerator" in dir(tree):
            for child in tree.childGenerator():
                if isinstance(child, Tag):
                    child_class = child.get("class", [])
                    if child_class:
                        found_tag = False
                        for element in child.children:
                            if isinstance(element, Tag):
                                found_tag = True
                                direct_child = tuple(element.get('class',()))
                                if not direct_child:
                                    childless_classes.append(tuple(child_class))
                                break
                        if not found_tag:
                            childless_classes.append(tuple(child_class))
                else:
                    continue
                get_children_recursively(child, childless_classes)
        else:
            if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                pass
    return childless_classes

def get_parentless_classes(source_code_file):
    '''
        This function is responsible for identifying CSS classes that have no DIRECT parents.
        That is a good indication that those classes belong to the "wildcard" category.
    '''
    with open(source_code_file, 'r') as source_code:
        parsed_code = BeautifulSoup(source_code, 'html.parser')
        for child in parsed_code.childGenerator():
            if isinstance(child, Tag):
                parentless_classes = get_parents_recursively(child, parentless_classes=[])
                return parentless_classes

def get_childless_classes(source_code_file):
    '''
        This function is responsible for identifying CSS classes that have no DIRECT children.
        That is a good indication that those classes belong to the "wildcard" category.
    '''
    with open(source_code_file, 'r') as source_code:
        parsed_code = BeautifulSoup(source_code, 'html.parser')
        for child in parsed_code.childGenerator():
            if isinstance(child, Tag):
                childless_classes = get_children_recursively(child, childless_classes=[])
                return childless_classes


def get_parents_of_child(tree, child_parents_dict):
    if not tree:
        return child_parents_dict
    else:
        if "childGenerator" in dir(tree):
            for child in tree.childGenerator():
                if isinstance(child, Tag):
                    child_class = tuple(sorted(child.get('class', []))) if child.get('class', []) else ()
                    if child_class:
                        if child_class not in child_parents_dict:
                            if child.parent and child.parent.get('class', ()):
                                parent_class = tuple(sorted(child.parent.get('class', [])))
                                child_parents_dict[child_class] = [parent_class]
                        else:
                            if child.parent and child.parent.get('class', ()):
                                parent_class = tuple(sorted(child.parent.get('class', [])))
                                if parent_class not in child_parents_dict[child_class]:
                                    child_parents_dict[child_class].append(parent_class)
                else:
                    continue
                get_parents_of_child(child, child_parents_dict)
        else:
            if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                pass
    return child_parents_dict

def get_parents_of_each_class(source_code_file):
    '''
        This function is responsible for identifying CSS classes' DIRECT parent.
    '''
    child_parents_dict = {}
    with open(source_code_file, 'r') as source_code:
        parsed_code = BeautifulSoup(source_code, 'html.parser')
        for child in parsed_code.childGenerator():
            if isinstance(child, Tag):
                child_parents_dict = get_parents_of_child(child, child_parents_dict={})
    return child_parents_dict


def get_wildcard_classes(source_code_file, threshold=3):
    wildcard_classes = []
    child_parents_dict = get_parents_of_each_class(source_code_file)
    for child_cls, parents in child_parents_dict.items():
        if len(parents) >= threshold:
            wildcard_classes.append(child_cls)
    return wildcard_classes
                

print(get_wildcard_classes('test_cases/case1.html'))