import factory.fuzzy

from fastzero.models import Todo, TodoState, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"text{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.username}password")


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker("text")
    description = factory.Faker("text")
    state = factory.fuzzy.FuzzyChoice(TodoState)
