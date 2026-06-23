# ACWAPIC

ACWAPIC (Astral's CatWeb API Client, or just CWAPIC, /æk.wɑː.pɪk/) is a Python Utility to easily create APIs for the Roblox game "CatWeb".

im too lazy to type all ts crap heres an example for now 🥀

```py
import acwapic

@acwapic.register("Print-Log")
def plog(msg: str):
    acwapic.log(msg)

acwapic.run()
```