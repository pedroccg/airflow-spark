def group_classes_by_attributes(soup):
    from bs4 import BeautifulSoup
    c1_classes = BeautifulSoup('<root></root>', 'xml')
    c2_classes = BeautifulSoup('<root></root>', 'xml')
    c3_classes = BeautifulSoup('<root></root>', 'xml')
    other_classes = BeautifulSoup('<root></root>', 'xml')

    for class_element in soup.find_all('class'):
        c1 = class_element.get('C1', 'false') == 'true'
        c2 = class_element.get('C2', 'false') == 'true'
        c3 = class_element.get('C3', 'false') == 'true'

        if c1:
            c1_classes.root.append(class_element.extract())
        elif c2:
            c2_classes.root.append(class_element.extract())
        elif c3:
            c3_classes.root.append(class_element.extract())
        else:
            other_classes.root.append(class_element.extract())

    # Combine the groups as per the given conditions
    c2_classes.root.extend(c1_classes.root.contents)
    c3_classes.root.extend(c1_classes.root.contents)
    c3_classes.root.extend(c2_classes.root.contents)
    other_classes.root.extend(c1_classes.root.contents)
    other_classes.root.extend(c2_classes.root.contents)
    other_classes.root.extend(c3_classes.root.contents)

    return c1_classes, c2_classes, c3_classes, other_classes