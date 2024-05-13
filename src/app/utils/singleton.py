class Singleton:
    def __init__(self, cls) -> None:
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError("Singleton Class Instance() Please call it in the method")

    def __instancecheck__(self, __instance) -> bool:
        return isinstance(__instance, self._cls)
