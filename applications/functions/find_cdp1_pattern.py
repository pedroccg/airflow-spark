def find_cdp1_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    cdp1_patterns = []

    for class_a in soup_local.find_all('class'):
        a_id = class_a['id']

        for relation in soup_local.find_all('relation', {'target': a_id}):
            if ((relation['value'] == '1..*') or (relation['value'] == '0..*')):
                class_b_id = relation['target']
                class_b = soup_local.find('class', {'id': class_b_id})

                if class_b:
                    for relation_b in class_b.find_all('relation', {'source': class_b_id}):
                        if ((relation_b['value'] == '1..*') or relation_b['value'] == '0..*') and relation_b['target'] == a_id:
                            relation['value'] = ':RELATED_TO'
                            cdp1_patterns.append(class_a)
                            cdp1_patterns.append(class_b)

    return cdp1_patterns