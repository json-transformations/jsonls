from jsonls.core import get_keylists, get_keystrings


def test_get_simple_keylists():
    data = {"status": "success", "message": {"affenpinscher": []}}
    expect = [
        (),
        ('message',),
        ('message', 'affenpinscher','*'),
        ('status',)
    ]
    result = sorted(get_keylists(data))
    assert result == expect


def test_get_nested_keylists():
    data = {"Solar System": {"planets": [{"name": "Mars", "moons": [{"name":
            "Phobos", "craters": [{"name": "Clustril", "diameter (km)": 3.4}, {
            "name": "D'Arrest", "diameter (km)": 2.1}]}]}]}}
    expect = [
        (),
        ('Solar System',),
        ('Solar System', 'planets', '*'),
        ('Solar System', 'planets', '*', 'moons', '*'),
        ('Solar System', 'planets', '*', 'moons', '*', 'craters', '*'),
        ('Solar System', 'planets', '*', 'moons', '*', 'craters', '*',
         'diameter (km)'),
        ('Solar System', 'planets', '*', 'moons', '*', 'craters', '*', 'name'),
        ('Solar System', 'planets', '*', 'moons', '*', 'name'),
        ('Solar System', 'planets', '*', 'name')
    ]
    result = sorted(get_keylists(data))
    for i in result:
        print(i)
    assert result == expect


def test_get_simple_keystrings():
    data = {"status": "success", "message": {"affenpinscher": []}}
    expect = [
        '.',
        '.message',
        '.message.affenpinscher.*',
        '.status'
    ]
    result = list(get_keystrings(data))
    assert result == expect


def test_get_nested_keystrings():
    data = {"Solar System": {"planets": [{"name": "Mars", "moons": [{"name":
            "Phobos", "craters": [{"name": "Clustril", "diameter (km)": 3.4},
            {"name": "D'Arrest", "diameter (km)": 2.1}]}]}]}}
    expect = [
        '.',
        '.Solar System',
        '.Solar System.planets.*',
        '.Solar System.planets.*.moons.*',
        '.Solar System.planets.*.moons.*.craters.*',
        '.Solar System.planets.*.moons.*.craters.*.diameter (km)',
        '.Solar System.planets.*.moons.*.craters.*.name',
        '.Solar System.planets.*.moons.*.name',
        '.Solar System.planets.*.name'
    ]
    result = list(get_keystrings(data))
    print(result)
    print(expect)
    assert result == expect
