def find_cdp3_a_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    cdp3_a_patterns = []

    for class_a in soup_local.find_all('class'):
        a_id = class_a['id']
        a_analytical = class_a.get('analitycalValue', 'false') == 'true'
        for relation in class_a.find_all('relation', {'source': a_id}):
            if ((relation['value'] == '1..*') or (relation['value'] == '0..*')):
                class_b_id = relation['target']
                class_b = soup_local.find('class', {'id': class_b_id})
                b_analytical = class_b.get('analitycalValue', 'false') == 'true'

                if class_b:
                    for relation_b in class_b.find_all('relation', {'source': class_b_id}):
                      
                        if relation_b['value'] == '1..1' and relation_b['target'] == a_id and ((b_analytical == 'false' and a_analytical == 'false') or (b_analytical == 'true' and a_analytical == 'true')):

                            # Add restriction
                            class_label_a = class_a['label']
                            class_label_b = class_b['label']
                            
                            # Remove all relations that are not part of the pattern
                            for rel in class_b.find_all('relation'):
                                rel['value'] = ':RELATED_TO'
                                rel['restriction'] = f"Node {class_label_a} must be associated to only one instance of Node {class_label_b}"
                                if 'target' in rel.attrs:
                                    if rel['target'] != class_b_id:
                                        rel.extract()

                            for rel in relation_b.find_all('relation'):
                                rel['value'] = ':RELATED_TO'
                                rel['restriction'] = f"Node {class_label_a} must be associated to only one instance of Node {class_label_b}"
                                if 'target' in rel.attrs:
                                    if rel['target'] != a_id:
                                        rel.extract()
                            
                            cdp3_a_patterns.append(class_a)
                            cdp3_a_patterns.append(class_b)

    return cdp3_a_patterns