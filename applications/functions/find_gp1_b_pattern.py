def find_gp1_b_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    gp1_patterns = []
    merged_classes = []

    for class_b in soup_local.find_all('class'):
        b_id = class_b['id']
        incoming_generalizations = []

        for relation in soup_local.find_all('relation', {'target': b_id, 'type': 'generalization'}):
            source_class_id = relation['source']
            source_class = soup_local.find('class', {'id': source_class_id, 'elementType': 'Generalization'})

            if source_class:
                incoming_generalizations.append(relation)

        if len(incoming_generalizations) >= 2 and incoming_generalizations[0]['value'] == 'Incomplete, Disjoint, Overlapping' and incoming_generalizations[1]['value'] == 'Incomplete, Disjoint, Overlapping':
            class_a_id = incoming_generalizations[0]['source']
            class_c_id = incoming_generalizations[1]['source']

            class_a = soup_local.find('class', {'id': class_a_id})
            class_c = soup_local.find('class', {'id': class_c_id})

            # Remove all relations that are not part of the GP1 pattern
            for rel in class_a.find_all('relation'):
                if rel['target'] != b_id:
                    rel.decompose()

            for rel in class_b.find_all('relation'):
                if rel['source'] not in [class_a_id, class_c_id]:
                    rel.decompose()

            for rel in class_c.find_all('relation'):
                if rel['target'] != b_id:
                    rel.decompose()

            # Set relation value to ":IS_A"
            for rel in incoming_generalizations:
                rel['value'] = ":IS_A"

            if class_a and class_b and class_c:
              gp1_patterns.append(class_a)
              gp1_patterns.append(class_b)
              gp1_patterns.append(class_c)

    return gp1_patterns