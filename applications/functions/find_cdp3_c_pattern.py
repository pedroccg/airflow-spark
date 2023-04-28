def find_cdp3_c_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    cdp3_c_patterns = []

    for class_a in soup_local.find_all('class'):
        a_id = class_a['id']
        a_analytical = class_a.get('analitycalValue', 'false') == 'true'

        for relation in soup_local.find_all('relation', {'source': a_id}):
            if ((relation['value'] == '1..*') or (relation['value'] == '0..*')):
                class_b_id = relation['target']
                class_b = soup_local.find('class', {'id': class_b_id})
                b_analytical = class_b.get('analitycalValue', 'false') == 'true'

                if class_b and (a_analytical != b_analytical):
   
                    # Merging the non-analytical class into the analytical class
                    if a_analytical == 'true':
                        merged_class = class_a
                    else:
                        merged_class = class_b
                    
                    # Check if the merged class is already in the list of patterns
                    #if not any(pattern['id'] == merged_class['id'] for pattern in cdp3_c_patterns):
                    cdp3_c_patterns.append(merged_class)
                    #
    
    return cdp3_c_patterns