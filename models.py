from dataclasses import  dataclass, field
from typing import Optional



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
@dataclass
class Game:
    url: str
    name: str
    year: str
    rating: str
    genres: Optional[list[Tag]] = field(default=list)
    platforms: Optional[list[Platform]] = field(default=list)