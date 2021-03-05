import dataclasses

def dataclass_from_dict(class_ref, data):
    try:
        fieldtypes = {f.name:f.type for f in dataclasses.fields(class_ref)}
        return class_ref(**{f:dataclass_from_dict(fieldtypes[f], data[f]) for f in data})
    except:
        return data # Not a dataclass field