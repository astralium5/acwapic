# CatWeb API Client 2026
# by Astral

from mod import acwapicore

orca = acwapicore.orca

@orca.register("test")
def test(arg):
    print(f"test, and i got {arg} too")