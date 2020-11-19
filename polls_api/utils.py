def fields_list(Model):
    return [
        f.name
        for f in Model._meta.fields
        if f.name != 'id'
    ]
