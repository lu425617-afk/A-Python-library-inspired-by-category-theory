# CategoryTheory/AbstractCategory/Morphism.py

class Morphism:
    def __init__(self, name: str, source: str, target: str):
        """
        Initialize a morphism.

        :param name: The name of the morphism.
        :param source: The source object of the morphism.
        :param target: The target object of the morphism.
        """
        self.name = name
        self.source = source
        self.target = target

    def __repr__(self):
        return f"Morphism({self.name}: {self.source} → {self.target})"

    def __eq__(self, other):
        return (
            isinstance(other, Morphism) and
            self.name == other.name and
            self.source == other.source and
            self.target == other.target
        )

    def __hash__(self):
        return hash((self.name, self.source, self.target))
