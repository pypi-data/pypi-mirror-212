# ExtendClass
A Python library that allows class extensions. No inheritance is needed to add methods to a class anymore.

# Installation
pip install ExtendClass

# Import
from ExtendClass import Extend
or
from ExtendClass.Extension import Extend

# Use
mod_cls = Extend(cls, method)

mod_obj = Extend(cls, method)(*args, **kwargs)

with Extend(cls, method): You can use the extended class here inside the with block
 
When you leave the with block, the method is removed. In case of overwritten methods, its returned to its original state.
