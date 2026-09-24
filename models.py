from dataclasses import  dataclass

@dataclass
class Game:
    url: str
    name: str
    year: str
    rating: str

@dataclass
class Tag:
    slug: str
    name: str
    def matches(self, user_input: str) -> bool:
        user_input = user_input.strip().lower()
        names = [self.slug, self.name]
        names = [name.strip().lower() for name in names]
        return user_input in names

@dataclass
class Platform:
    code: str
    title: str
    def matches(self, user_input: str) -> bool:
        user_input = user_input.strip().lower()
        names = [self.code, self.title]
        names = [name.strip().lower() for name in names]
        return user_input in names

if __name__ == "__main__":
    from dataclasses import asdict
    g = Game(1,2,3,4)
    print(asdict(g))
