def find_cdp3_b_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    cdp3_b_patterns = []

    for class_a in soup_local.find_all('class'):
        a_id = class_a['id']

        for relation in class_a.find_all('relation', {'source': a_id}):
            if ((relation['value'] == '1..*') or (relation['value'] == '0..*')):
                class_b_id = relation['target']
                class_b = soup_local.find('class', {'id': class_b_id})

                if class_b:
                    for relation_b in class_b.find_all('relation', {'source': class_b_id}):
                        if relation_b['value'] == '0..1' and relation_b['target'] == a_id:
                            class_label_a = class_a['label']
                            class_label_b = relation_b['label']
                            relation['value'] = ':RELATED_TO'
                            relation['restriction'] = f"Node {class_label_a} can be associated to at must one instance of Node {class_label_b}"
                            relation_b['value'] = ':RELATED_TO'
                            relation_b['restriction'] = f"Node {class_label_a} can be associated to at must one instance of Node {class_label_b}"
                            cdp3_b_patterns.append(class_a)
                            cdp3_b_patterns.append(class_b)

    return cdp3_b_patterns