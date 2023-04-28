def find_np3_pattern(soup):
    np3_patterns = []

    for relation in soup.find_all('relation'):
        if relation.get('elementType') == 'NonNavigableAssociation':
          
            source_class_id = relation['source']
            target_class_id = relation['target']

            source_class = soup.find('class', {'id': source_class_id})
            target_class = soup.find('class', {'id': target_class_id})

            class_label_a = source_class['label']
            class_label_b = target_class['label']

            for rel in source_class.find_all('relation'):
              rel['value'] = ':RELATED_TO'
              rel['restriction'] = f"Node {class_label_a} cannot be accessed from Node {class_label_b}"
            
            for rel in target_class.find_all('relation'):
              rel['value'] = ':RELATED_TO'
              rel['restriction'] = f"Node {class_label_a} cannot be accessed from Node {class_label_b}"

            if source_class and target_class:
                np3_patterns.append((source_class, target_class))

    return np3_patterns