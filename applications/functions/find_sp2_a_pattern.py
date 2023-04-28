def find_sp2_a_pattern(soup):
    sp2_patterns = []
    import copy
    soup_local = copy.copy(soup)

    for relation in soup_local.find_all('relation', {'type': 'composition'}):
        source_class_id = relation['source']
        target_class_id = relation['target']

        source_class = soup_local.find('class', {'id': source_class_id, 'elementType': 'Composition'})
        target_class = soup_local.find('class', {'id': target_class_id, 'elementType': 'Class'})

        if source_class and target_class:
          source_composition = source_class.get('elementType') == 'Composition'
          target_composition = target_class.get('elementType') == 'Class'

          if source_composition or target_composition:
              whole_class = source_class if source_composition else target_class
              part_class = target_class if source_composition else source_class

              whole_class_analytical = whole_class.get('analitycalValue', 'false') == 'true'
              part_class_analytical = part_class.get('analitycalValue', 'false') == 'true'

              whole_class_label = whole_class['label']
              part_class_label = part_class['label']

              if ((whole_class_analytical == True and part_class_analytical == True) or (whole_class_analytical == False and part_class_analytical == False)):
                  

                  # Remove all relations that are not part of the SP2 pattern
                  for rel in whole_class.find_all('relation'):
                      # Set relation value to ":IS_A"
                      rel['value'] = ":HAS"
                      rel['restriction'] = f"If class {whole_class_label} is removed, {part_class_label} must be removed"   
                      if rel['target'] != part_class['id']:
                          rel.extract()

                  for rel in part_class.find_all('relation'):
                      # Set relation value to ":IS_A"
                      rel['value'] = ":HAS"
                      rel['restriction'] = f"If class {whole_class_label} is removed, {part_class_label} must be removed"   
                      if rel['target'] != whole_class['id']:
                          rel.extract()
                  
                  sp2_patterns.append(whole_class)
                  sp2_patterns.append(part_class)

    return sp2_patterns