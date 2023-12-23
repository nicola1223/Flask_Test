from flask import current_app

def add_to_index(model):
    if not current_app.solr:
        return
    payload = {
        'id': model.id
    }
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.solr.add([payload])
    current_app.solr.commit()

def remove_from_index(model):
    if not current_app.solr:
        return
    current_app.solr.delete_by_id(model.id)
    current_app.solr.commit()

def query_index(query, page, per_page):
    # if not current_app.solr:
    #     return [], 0
    params = {
        'q': query,
        'defType': 'edismax',
        'qf': 'body^2',
        'pf': 'body^2',
        'mm': '1<-1 3<80%',
        'fuzzy': 'true',
        'start': (page - 1) * per_page,
        'rows': per_page
    }
    search_results = current_app.solr.search(**params)
    ids = [int(result['id']) for result in search_results.docs]
    total_results = search_results.hits

    return ids, total_results