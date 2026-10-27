# Guide

```mermaid
C4Context
    Person(user, "User", $link="people/user.md")
    System(shop, "Shop")
    Rel(user, shop, "Uses", $link="people/user.md")
```

```mermaid
pie title Users
    "people/user.md" : 1
    "Others" : 2
```
