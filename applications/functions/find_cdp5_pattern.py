def find_cdp5_pattern(soup):
    import copy
    soup_local = copy.copy(soup)
    cdp5_patterns = []

    for nary_association in soup_local.find_all('class', {'elementType': 'NAryAssociation'}):
        nary_association_id = nary_association['id']
        incoming_relations = []

        for relation in soup_local.find_all('relation', {'target': nary_association_id}):
            if relation['value'] == '1..*' or relation['value'] == '1..1':
                incoming_relations.append(relation)

        if len(incoming_relations) >= 3:
            related_classes = [soup_local.find('class', {'id': rel['source']}) for rel in incoming_relations]

            # Remove all relations that are not part of the CdP5 pattern
            for cls in related_classes:
                for rel in cls.find_all('relation'):
                    target = rel.get('target')
                    if target is not None:
                      if rel['target'] != nary_association_id:      
                          rel.extract()

            for rel in nary_association.find_all('relation'):
              source = rel.get('source')
              if source is not None:
                if rel['target'] not in [cls['id'] for cls in related_classes]:
                    rel.extract()

            cdp5_patterns.append(nary_association)
            for cls in related_classes:
              cdp5_patterns.append(cls)

    return cdp5_patterns