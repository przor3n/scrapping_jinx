import os
import importlib.util


from .wykop

p = os.path.abspath(os.path.dirname(__file__))

np = os.path.join(p, 'wykop' + '.py')

print(p)
print(np)

spec = importlib.util.spec_from_file_location("wykoppl.pages." + "wykop", np)
_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_mod)
c = getattr(_mod, 'Wykop')()
print(c)