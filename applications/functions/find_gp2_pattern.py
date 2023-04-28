def find_gp2_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    gp2_patterns = []
    merged_classes = []

    for class_b in soup_local.find_all('class'):
        b_id = class_b['id']
        incoming_generalizations = []

        for relation in soup_local.find_all('relation', {'target': b_id, 'type': 'generalization'}):
            source_class_id = relation['source']
            source_class = soup_local.find('class', {'id': source_class_id, 'elementType': 'Generalization'})

            if source_class:
                incoming_generalizations.append(relation)

        if len(incoming_generalizations) >= 2 and incoming_generalizations[0]['value'] == 'Complete, Overlapping' and incoming_generalizations[1]['value'] == 'Complete, Overlapping':
            class_a_id = incoming_generalizations[0]['source']
            class_c_id = incoming_generalizations[1]['source']

            class_a = soup_local.find('class', {'id': class_a_id})
            class_c = soup_local.find('class', {'id': class_c_id})

            if class_a and class_b and class_c:

              # Merge the classes into a single class with no relations
              merged_class = soup_local.new_tag('class', attrs={'id': f"{class_a_id}_{b_id}_{class_c_id}", 'label': f"{class_a['label']}_{class_b['label']}_{class_c['label']}", 'elementType': "Class"})
              
 
              merged_classes.append(merged_class)

    return merged_classes