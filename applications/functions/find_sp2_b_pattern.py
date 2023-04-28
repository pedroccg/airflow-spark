def find_sp2_b_pattern(soup):
    from bs4 import Tag
    import copy
    soup_local = copy.copy(soup)
    sp2_patterns = []

    for relation in soup_local.find_all('relation', {'type': 'composition'}):
        source_class_id = relation['source']
        target_class_id = relation['target']

        source_class = soup_local.find('class', {'id': source_class_id, 'elementType': 'Composition'})
        target_class = soup_local.find('class', {'id': target_class_id, 'elementType': 'Class'})

        if source_class is not None and target_class is not None:

          source_composition = source_class.get('elementType') == 'Composition'
          target_composition = target_class.get('elementType') == 'Class'

          if source_composition or target_composition:
              whole_class = source_class if source_composition else target_class
              part_class = target_class if source_composition else source_class

              whole_class_analytical = whole_class.get('analitycalValue', 'false') == 'true'
              part_class_analytical = part_class.get('analitycalValue', 'false') == 'true'

              whole_class_label = whole_class['label']
              part_class_label = part_class['label']

              if whole_class_analytical or part_class_analytical:
                  # Merge the classes into the one that has the attribute analitycalValue="true"
                  analytical_class = whole_class if whole_class_analytical else part_class
                  non_analytical_class = part_class if whole_class_analytical else whole_class

                  merged_class = Tag(name='class')
                  merged_class.attrs.update({
                      'id': f"{analytical_class['id']}_{non_analytical_class['id']}",
                      'label': f"{analytical_class['label']}_{non_analytical_class['label']}",
                      'elementType': "Class",
                      'analitycalValue': 'true'
                  })

                  # erro: está a repetir a classe
                  sp2_patterns.append(merged_class)

    return sp2_patterns