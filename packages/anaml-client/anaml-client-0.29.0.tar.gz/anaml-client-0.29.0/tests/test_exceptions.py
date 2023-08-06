from anaml_client.exceptions import AnamlError


def test_from_json_and_str():
    ex = AnamlError.from_json({
        'errors': [
            {
                'message': 'All my apes gone',
            },
            {
                'message': 'Must not be null',
                'field': 'name'
            },
            {
                'message': 'Must not be null',
                'field': 'description'
            },
        ]
    })
    assert str(ex) == ('The Anaml server reported an error:\n' +
                       '* All my apes gone\n' +
                       '* Must not be null (name)\n' +
                       '* Must not be null (description)')
