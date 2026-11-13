"""Check authored data before a generator overwrites any pages."""


def validate_data(data, taxonomy, content, micro, glossary, timeline, master_starts):
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    units = {row[0] for row in data}
    require(len(data) == len(units) == 14, 'Expected 14 distinct course units')
    for name, collection in (
        ('taxonomy', taxonomy), ('content', content), ('glossary', glossary),
        ('timeline', timeline), ('master_starts', master_starts),
    ):
        require(set(collection) == units, f'{name}: unit keys do not match the course')
    groups = {(num, group) for num in units for group in taxonomy[num]}
    require(set(micro) == groups, f'Micro-lessons do not match taxonomy groups: {set(micro) ^ groups}')
    for num, name, subs, goal, kind, lessons in data:
        require(len(lessons) == 3, f'{num}: expected 3 introductory lessons')
        require(all(len(row) == 8 and all(row) for row in lessons), f'{num}: malformed introductory lesson')
        rows = [line.split('｜') for line in content[num].strip().splitlines()]
        require(len(rows) == 6 and all(len(row) == 5 and all(row) for row in rows),
                f'{num}: expected 6 extended lessons with 5 nonempty fields each')
        require(bool(taxonomy[num]) and all(taxonomy[num].values()), f'{num}: empty taxonomy group')
        require(bool(glossary[num]) and all(len(row) == 2 and all(row) for row in glossary[num]), f'{num}: malformed glossary')
        terms = [row[0] for row in glossary[num]]
        require(len(terms) == len(set(terms)), f'{num}: duplicate glossary term')
        require(bool(timeline[num]) and all(len(row) == 5 for row in timeline[num]), f'{num}: malformed timeline')
        require(len(master_starts[num]) == 6 and all(master_starts[num]), f'{num}: malformed masterwork starting point')
    for key, row in micro.items():
        require(len(row) == 9 and all(row), f'{key}: malformed micro-lesson')
        require(all(len(hook) == 2 and all(hook) for hook in row[2]), f'{key}: malformed observation hook')
