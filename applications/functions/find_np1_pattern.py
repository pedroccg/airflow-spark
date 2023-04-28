def find_np1_pattern(soup):
    np1_patterns = []

    for class_a in soup.find_all('class'):
        a_id = class_a['id']

        for relation in soup.find_all('relation', {'source': a_id}):
            if relation['value'] == '1..*':
                class_b_id = relation['target']
                class_b = soup.find('class', {'id': class_b_id})

                if class_b:
                    np1_patterns.append((class_a, class_b))

    return np1_patterns