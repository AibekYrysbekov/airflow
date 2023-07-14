def assert_equal(db_data, api_data):
    db_set = set(db_data)
    api_set = set(api_data.items())
    if db_set != api_set:
        raise ValueError('The data from the database does not match the data from the API. '
                         + 'Database has %s extra. ' % (db_set - api_set)
                         + 'API has %s extra.' % (api_set - db_set))
