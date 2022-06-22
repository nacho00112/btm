btm (Built-ins Types Modificator for python) - Documentation
=========================================

addattr
-------

`btm.addattr(<builtin_type>, <name>, <attribute>)`

    import btm
    def _modify_int():
        btm.addattr(int, "lol", 10)

    _modify_int()
    print((1).lol)

subattr
-------

Alias for addattr, this is only a convenction,
use addattr when you are adding attributes, and
btm.subattr when you are substituting attributes.

    import btm
    print(btm.addattr is btm.subattr) # Output: True

addmeth
-------

    @btm.addmeth(<builtin_type>, <name (optional)>)
    def method(self, ...):
        ...

`<name>` is optional and by default btm.addmeth use `method.__name__` as the name.

    import btm
    def _modify_str():
        @btm.addmeth(str)
        def print(self):
            print(self)

    _modify_str()
    "Hello World!".print() # Output: Hello World!

submeth
-------

as subattr but for addmeth.

subclass
--------

`btm.subclass(<builtin_type>, <subclass (optional)>)`
`<subclass>` is optional and by default btm.subclass
return a decorator taking the subclass.

    @btm.subclass(list)
    class list:
        decoration = "-" * 10 + "\n%s\n" + "-" * 10 
        def pretty_print(self):
            for each in self:
                print(self.decoration % each)
    ["Hello World!", "Eggs", "Spam"].pretty_print()
    try:
        # unfortunately attributes are immutable, but the next lesson have a trick for solve this
        [].decoration = "+" * 10 + "\n%s\n" + "+" * 10
    except AttributeError:
        print("built-in types attributes are immutable")

mutable attributes
----------

    def _list_mutable_attrs():
        """
        Doing something like:
        from types import SimpleNamespace
        btm.addattr(list, "attrs", SimpleMamespace())
        mylist = []
        mylist.attrs.something = 1
        works but the attributes are shared in all lists:
        mylist_2 = []
        mylist_2.attrs.something_2 = 2
        print(hasattr(mylist_2.attrs, "something")) # Output: True
        print(hssattr(mylist_2.attrs, "something_2")) # Output: True
        and substituting __init__ or __new__
        not works because magic methods not are called for some reason,
        then for a individual attrs attribute for each list
        the unique solution are the methods,
        in each instance a new method is created:
        print([].append is [].append) # Output: False
        and python allow to set attributes to the methods!
        """
        @btm.addmeth(list)
        def attrs(self): pass

    _list_mutable_attrs()

    mylist = []
    mylist.attrs.something = 1
    mylist_2 = []
    mylist_2.attrs.something_2 = 2
    print(hasattr(mylist_2.attrs, "something")) # Output: False
    print(hssattr(mylist_2.attrs, "something_2")) # Output: True

Its all! now you can modify absolutely all the Python Built-in types, with this limitations:

1) attributes are immutable, you need to set the attributes to a method.
2) new magic methods not are called for some reason.
3) Some modifications can cause a fatal "Segmentation fault" error,
if you get this error, try with different implementations of your modification.

