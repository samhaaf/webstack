from chalicelib.orm import Session
from chalicelib.orm.objects import User, RefreshToken
from chalicelib.orm.io import dump
from pprint import pprint
from uuid import UUID

with Session() as session:
    user = session.query(User).filter(User.uid == UUID('e401c6ba-ea32-4b74-8f10-98fc3417eeff')).first()

    print('no rels')
    pprint(dump(user))

    print('get_hidden')
    pprint(dump(user, get_hidden='created_at'))

    print('all rels')
    pprint(dump(user, rels=all))

    print('rel dict 1')
    pprint(dump(user, rels={'refresh_tokens': {}}))

    print('rel dict 2')
    pprint(dump(user, rels={'refresh_tokens': {'cols': ['uid']}}))

    print('rel dict 3')
    pprint(dump(user, rels={'refresh_tokens': {'cols': 'uid'}}))

    print('rel dict 4')
    pprint(dump(user, rels={'refresh_tokens': {'cols': 'uid', 'get_hidden': 'created_at'}}))

    print('rel dict 5')
    pprint(dump(user, rels={'refresh_tokens': ['uid', 'created_at']}))

    user = session.query(RefreshToken).filter(RefreshToken.uid == UUID('4dadb6c4-f281-429e-9e02-ede77a034c51')).first()

    print('rel dict 6')
    pprint(dump(user, rels={'user': ['uid', 'created_at']}))
