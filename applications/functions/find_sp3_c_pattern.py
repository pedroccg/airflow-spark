def find_sp3_c_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    sp3_c_patterns = []

    for class_b in soup_local.find_all('class'):
        b_id = class_b['id']
        incoming_relations = []

        for relation in soup_local.find_all('relation', {'target': b_id}):
            if relation['value'] == '1..1':
                incoming_relations.append(relation)

        if len(incoming_relations) == 2 and class_b.get('elementType') == 'AssociationClass' and class_b.get('analitycalValue', 'false') == 'true':
           
              class_a_id = incoming_relations[0]['source']
              class_c_id = incoming_relations[1]['source']

              class_a = soup_local.find('class', {'id': class_a_id})
              class_c = soup_local.find('class', {'id': class_c_id})

              if class_a and class_c:
                  sp3_c_patterns.append(class_a)
                  sp3_c_patterns.append(class_b)
                  sp3_c_patterns.append(class_c)

    return sp3_c_patterns