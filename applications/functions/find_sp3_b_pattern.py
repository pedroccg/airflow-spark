def find_sp3_b_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    sp3_b_patterns = []

    for class_b in soup_local.find_all('class'):
        b_id = class_b['id']
        incoming_relations = []
        for relation in soup_local.find_all('relation', {'target': b_id}):
            if relation['value'] == '1..1':
                incoming_relations.append(relation)
        
        if len(incoming_relations) == 2 and class_b.get('elementType') == 'AssociationClass':
            # Check for the third relationship with a D class with a 1..* relationship
            d_class_relation = soup_local.find('relation', {'target': b_id, 'value': '1..*'})

            class_a_id = incoming_relations[0]['source']
            class_c_id = incoming_relations[1]['source']

            class_a = soup_local.find('class', {'id': class_a_id})
            class_c = soup_local.find('class', {'id': class_c_id})

            if class_a and class_c:
                sp3_b_patterns.append(class_a)
                sp3_b_patterns.append(class_b)
                sp3_b_patterns.append(class_c)
                if d_class_relation:
                  d_class_id = d_class_relation['target']
                  d_class = soup_local.find('class', {'id': d_class_id})
                  sp3_b_patterns.append(d_class)

    return sp3_b_patterns