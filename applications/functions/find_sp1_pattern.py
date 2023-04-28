def find_sp1_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    sp1_patterns = []

    for relation in soup_local.find_all('relation', {'elementType': 'Aggregation'}):
        source_class_id = relation['source']
        target_class_id = relation['target']

        source_class = soup_local.find('class', {'id': source_class_id})
        target_class = soup_local.find('class', {'id': target_class_id})

        if source_class and target_class:
            # Remove all relations that are not part of the SP1 pattern
            for rel in source_class.find_all('relation'):
                if rel['target'] != target_class_id:
                    rel.decompose()
                else:
                    rel['value'] = ':HAS'

            for rel in target_class.find_all('relation'):
                if rel['target'] != source_class_id:
                    rel.decompose()
                else:
                    rel['value'] = ':HAS'

            sp1_patterns.append(source_class)
            sp1_patterns.append(target_class)

    return sp1_patterns