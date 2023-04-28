def find_np2_pattern(soup):
    np2_patterns = []

    for relation in soup.find_all('relation'):
        if relation['value'] == '*..*':
            class_a_id = relation['source']
            class_b_id = relation['target']

            class_a = soup.find('class', {'id': class_a_id})
            class_b = soup.find('class', {'id': class_b_id})

            if class_a and class_b:
                # Check if the pair already exists in the list in any order
                if not any([(class_a, class_b) in np2_patterns or (class_b, class_a) in np2_patterns]):
                    np2_patterns.append((class_a, class_b))

    return np2_patterns