def find_cdp2_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    cdp2_patterns = []

    for relation in soup_local.find_all('relation'):
        if relation['value'] in ('1..*', '0..*'):
            source_class_id = relation['source']
            target_class_id = relation['target']

            source_class = soup_local.find('class', {'id': source_class_id})
            target_class = soup_local.find('class', {'id': target_class_id})

            if source_class and target_class:
                # Create copies of the classes and relations
                source_class_copy = copy.copy(source_class)
                target_class_copy = copy.copy(target_class)
                relation_copy = copy.copy(relation)

                # Add restriction
                class_label_a = source_class['label']
                class_label_b = target_class_copy['label']

                # Remove all relations that are not part of the CdP2 pattern
                for rel in source_class_copy.find_all('relation'):
                    rel['value'] = ':RELATED_TO'
                    rel['restriction'] = f"Node {class_label_a} must be connected with at least one instance of Node {class_label_b}"
                    if rel['target'] != target_class_id:
                        rel.decompose()

                for rel in target_class_copy.find_all('relation'):
                    rel['value'] = ':RELATED_TO'
                    rel['restriction'] = f"Node {class_label_a} must be connected with at least one instance of Node {class_label_b}"
                    if rel['target'] != source_class_id:
                        rel.decompose()
                
                

                # Add the relevant relation to the pattern list
                cdp2_patterns.append(source_class_copy)      
                cdp2_patterns.append(target_class_copy)

    return cdp2_patterns