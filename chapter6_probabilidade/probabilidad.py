import enum, random

# um Enum é um conjuto tipado de valores enumerados que deixa
# o código mais descritivo e legível.
class kid(enum.Enum):
    BOY = 0
    GIRL = 1

def random_kid() -> kid:
    return random.choice([kid.BOY, kid.GIRL])

both_girls=0
older_girls=0
either_girl=0

random.seed(0)

for _ in range(10000):
    younger = random_kid()

    older = random_kid()
    if older == kid.GIRL:
        older_girls+=1
    if older == kid.GIRL and younger == kid.GIRL:
        both_girls+=1
    if older == kid.GIRL or younger == kid.GIRL:
        either_girl+=1

print(f"(Both | older): {both_girls / older_girls}") # 0.514 - 1/2
print(f"(Both | either): {both_girls / either_girl}") # 0.342 - 1/3
