class SingletonClass:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # utwórz nową instancję tylko raz dla danej klasy
            cls._instances[cls] = super(SingletonClass, cls).__new__(cls)
        return cls._instances[cls]

    @classmethod
    def instance(cls):
        return cls()  # wywoła __new__, nie __init__ ponownie
