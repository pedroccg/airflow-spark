def find_cdp4_b_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    cdp4_b_patterns = []

    for relation in soup_local.find_all('relation'):
        if relation['value'] == '1..1':
            source_class_id = relation['source']
            target_class_id = relation['target']

            source_class = soup_local.find('class', {'id': source_class_id})
            target_class = soup_local.find('class', {'id': target_class_id})

            reverse_relation = soup_local.find('relation', {'source': target_class_id, 'target': source_class_id})
            if reverse_relation is not None and reverse_relation['value'] != '1..1':
              continue

            if source_class is not None and target_class is not None:
              source_analytical = source_class.get('analitycalValue', 'false') == 'true'
              target_analytical = target_class.get('analitycalValue', 'false') == 'true'

              if source_class and target_class and (source_analytical != target_analytical):
                  # Remove all relations that are not part of the CdP4-B pattern
                  for rel in source_class.find_all('relation'):
                      if rel['target'] != target_class_id:
                          rel.extract()

                  for rel in target_class.find_all('relation'):
                      if rel['target'] != source_class_id:
                          rel.extract()

                  # Merging the non-analytical class into the analytical class
                  if source_analytical:
                      merged_class = source_class
                  else:
                      merged_class = target_class

                  cdp4_b_patterns.append(merged_class)

    return cdp4_b_patterns