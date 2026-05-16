# CatWeb API Client 2026
# by Astral

from mod.acwapicore import *

@register("Print-Log")
def test(arg):
    print(f"test, and i got {arg} too")

run()