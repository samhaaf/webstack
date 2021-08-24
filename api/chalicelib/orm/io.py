from sqlalchemy import Column
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from datetime import datetime
from pprint import pprint
from uuid import UUID


def serialize(blob):
    if isinstance(blob, dict):
        return {key: serialize(value) for key, value in blob.items()}
    if isinstance(blob, datetime):
        return blob.timestamp()
    if isinstance(blob, UUID):
        return str(blob)
    if isinstance(blob, bytes):
        return blob.decode()
    return blob


def dump(obj, cols=all, rels={}, get_hidden=None):

    ## parse cols request
    if isinstance(cols, str):
        cols = [cols]
    if cols is all:
        cols = [attr for attr in dir(obj.__class__)
            if isinstance(getattr(obj.__class__, attr), InstrumentedAttribute)
            and isinstance(getattr(obj.__class__, attr).property, ColumnProperty)
            and attr not in obj.__class__.hidden
        ]
    cols = cols or []

    ## parse get_hidden request
    _get_hidden = []
    if get_hidden is all:
        _get_hidden = obj.__class__.hidden
    if isinstance(get_hidden, (list, set, tuple)):
        _get_hidden = get_hidden
    if isinstance(get_hidden, str):
        _get_hidden = [get_hidden]

    cols += _get_hidden

    ## parse rels request
    if isinstance(rels, str):
        rels = [rels]
    if rels is all:
        rels = [attr for attr in dir(obj.__class__)
            if isinstance(getattr(obj.__class__, attr), InstrumentedAttribute)
            and isinstance(getattr(obj.__class__, attr).property, RelationshipProperty)
            and attr not in obj.__class__.hidden
        ]

    result = {}

    ## get selected columns
    for col in cols if cols else []:
        result[col] = getattr(obj, col)

    # list of rels given - accept defaults for rel dump
    if isinstance(rels, list):
        for rel in rels:
            prop = getattr(obj, rel)

            ## if the property is a list, iteratively dump
            if isinstance(prop, list):
                result[rel] = [dump(val, get_hidden=get_hidden) for val in prop]

            ## otherwise, dump once
            else:
                result[rel] = dump(prop, get_hidden=get_hidden)


    # dict of rels given - user parameters specified for rel dump
    if isinstance(rels, dict):

        ## each key in rels is property to dump
        for rel, val in rels.items():
            prop = getattr(obj, rel)

            # val is dump parameters for rel object - use
            if isinstance(val, dict):

                ## if the property is a list, iteratively dump
                if isinstance(prop, list):
                    result[rel] = [dump(
                        obj=p,
                        cols=val.get('cols', all),
                        rels=val.get('rels', {}),
                        get_hidden=val.get('get_hidden', get_hidden)
                    ) for p in prop]

                ## otherwise, dump once
                else:
                    result[rel] = dump(
                        obj=prop,
                        cols=val.get('cols', all),
                        rels=val.get('rels', {}),
                        get_hidden=val.get('get_hidden', get_hidden)
                    )


            # val is a list of columns for rel object - use
            elif isinstance(val, (list, str)):

                ## if the property is a list, iteratively dump
                if isinstance(prop, list):
                    result[rel] = [dump(
                        obj=p,
                        cols=val,
                        get_hidden=get_hidden
                    ) for p in prop]

                ## otherwise, dump once
                else:
                    result[rel] = dump(
                        obj=prop,
                        cols=val,
                        get_hidden=get_hidden
                    )

    return serialize(result)
