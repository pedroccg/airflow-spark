def to_labeled_property_graph(final_patterns, pattern_classes):
    nodes = []
    edges = []
    for class_element in pattern_classes:
        label = class_element['label']
        class_id = class_element['id']
        properties = {}
        # Extract attributes as properties
        attributes = class_element.find_all('attribute')
        for attribute in attributes:
            properties[attribute['value']] = None
        nodes.append({"id": class_id, "label": label, "properties": properties})
        # Extract relationships as edges
        relations = class_element.find_all('relation', {'source': class_id})
        for relation in relations:
            source = relation['source']
            target = relation['target']
            value = relation['value']
            edge_id = relation['source'] + "_" + relation['target']
            restriction = relation['restriction'] if 'restriction' in relation.attrs else ''
            edges.append({"id": edge_id, "source": source, "target": target, "value": value, "restriction": restriction})


    #print(edges)
    #final_patterns["pattern"] = pattern_name

    # Append nodes if they don't already exist in final_patterns
    for node in nodes:
        if node not in final_patterns['nodes']:
            final_patterns['nodes'].append(node)

    # Append edges if they don't already exist in final_patterns
    for edge in edges:
        edge_id = edge['id']
        edge_id_reversed = "_".join(reversed(edge_id.split("_")))
        if not any(existing_edge['id'] in (edge_id, edge_id_reversed) for existing_edge in final_patterns['edges']):
            final_patterns['edges'].append(edge)


    return final_patterns