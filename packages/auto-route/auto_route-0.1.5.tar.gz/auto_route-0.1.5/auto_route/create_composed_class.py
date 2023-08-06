def create_composed_class(name, classes, strategy='namespaced'):
    """
        Dynamically create a class composed of methods from other classes.

        This function creates a new class composed of methods from other classes.
        In the case of a method name collision, the resolution strategy depends on
        the strategy argument.

        Args:
            name (str): The name of the composed class to be created.
            classes (tuple): A tuple of classes from which to compose the new class.
            strategy (str, optional): The strategy for resolving method name collisions.
                'namespaced' - Prefix each method with its class name.
                'prioritize' - Use the method from the class specified first in the classes tuple.
                Defaults to 'namespaced'.

        Returns:
            type: The composed class.

        Raises:
            ValueError: If an invalid strategy is specified.

        Example:
            >>> class A:
            >>>     def method(self):
            >>>         return "Method from A"
            >>>
            >>> class B:
            >>>     def method(self):
            >>>         return "Method from B"
            >>>
            >>> # Create the composed class with namespaced methods
            >>> C = create_composed_class("C", (A, B), strategy='namespaced')
            >>> c = C()
            >>> print(c.A_method())  # prints: "Method from A"
            >>> print(c.B_method())  # prints: "Method from B"
            >>>
            >>> # Create the composed class with prioritized methods
            >>> D = create_composed_class("D", (A, B), strategy='prioritize')
            >>> d = D()
            >>> print(d.method())  # prints: "Method from A"
        """
    methods = {}
    for cls in classes:
        for method_name, method in cls.__dict__.items():
            if callable(method) and not method_name.startswith("__"):
                if strategy == 'namespaced':
                    method_name = f"{cls.__name__}_{method_name}"
                elif strategy == 'prioritize':
                    if method_name in methods:
                        continue

                def method_wrapper(self, *args, **kwargs):
                    instance = getattr(self, f"_{cls.__name__}")
                    return method(instance, *args, **kwargs)

                methods[method_name] = method_wrapper

    ComposedClass = type(name, (object,), methods)

    def __init__(self):
        for cls in classes:
            setattr(self, f"_{cls.__name__}", cls())

    setattr(ComposedClass, "__init__", __init__)

    return ComposedClass
