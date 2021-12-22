from dataclasses import dataclass, field

class Person:
    name: str
    job: str
    age: int

    def __init__(self, name, job, age) -> None:
        self.name = name
        self.job = job
        self.age = age

@dataclass(order=True, frozen=True)
class PersonDataclass:
    sort_index: int = field(init=False, repr=False)
    name: str
    job: str
    age: int
    strength: int = 100

    def __post_init__(self):
        # self.sort_index = self.age
        object.__setattr__(self, 'sort_index', self.age)

    def __str__(self) -> str:
        return f"Person: {self.name}, {self.job}, {self.age}"

person1 = Person("Geralt", "Witcher", 30)
person1d = PersonDataclass("Geralt", "Witcher", 30, 99)
person2 = Person("Yennefer", "Sorceress", 25)
person2d = PersonDataclass("Yennefer", "Sorceress", 25)
person3 = Person("Yennefer", "Sorceress", 25)
person3d = PersonDataclass("Yennefer", "Sorceress", 25)

print(id(person2))
print(id(person3))
print(person1)

print(person3d == person2d)

print()
print("Dataclass")
print()

print(id(person2d))
print(id(person3d))
print(person1d)

print(person3d == person2d)
print(person1d > person2d)