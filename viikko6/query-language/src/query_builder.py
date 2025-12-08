from matchers import All, And, HasFewerThan, PlaysIn, HasAtLeast


class QueryBuilder:
    def __init__(self, matcher=All()):
        self.matcher = matcher

    def plays_in(self, team):
        return QueryBuilder(And(self.matcher, PlaysIn(team)))

    def has_at_least(self, value, attr):
        return QueryBuilder(And(self.matcher, HasAtLeast(value, attr)))

    def has_fewer_than(self, value, attr):
        return QueryBuilder(And(self.matcher, HasFewerThan(value, attr)))

    def build(self):
        return self.matcher
