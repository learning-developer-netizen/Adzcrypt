def get_next_id(db_dict):
    """Get the next available ID for a dictionary-based database."""
    if not db_dict:
        return 1
    return max(db_dict.keys()) + 1

def filter_data(data_dict, filters):
    """Filter a dictionary of data based on the provided filters."""
    if not filters:
        return data_dict
    
    result = {}
    for key, item in data_dict.items():
        matches = True
        for filter_key, filter_value in filters.items():
            if filter_key not in item or item[filter_key] != filter_value:
                matches = False
                break
        if matches:
            result[key] = item
    return result 