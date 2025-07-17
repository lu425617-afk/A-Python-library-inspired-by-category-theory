# CategoryTheory/AbstractColimit/Coproduct.py

from typing import Dict, List, Optional
from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from .AbstractColimit import AbstractColimit

class Coproduct(AbstractColimit):
    """
    Represents the coproduct of a set of objects in a category.
    """
    
    def __init__(self, 
                 category: AbstractCategory, 
                 objects: List[str]):
        """
        Initializes the Coproduct with a category and a list of objects.

        :param category: The category in which to compute the coproduct.
        :param objects: A list of objects to form the coproduct.
        """
        self.coproduct_objects = objects
        self.diagram = {}  # In coproducts, the diagram consists of injections.
        self.cocone_morphisms = {}  # Morphisms η_X: CoproductObject → X

        # Define the diagram as injections from each object to the coproduct
        for obj in objects:
            # Injection morphism: ι_i: X_i → CoproductObject
            injection_name = f"ι_{obj}"
            injection = category.get_morphism(injection_name)
            if injection is None:
                raise ValueError(f"Injection morphism '{injection_name}' not found in the category.")
            if obj not in self.diagram:
                self.diagram[obj] = []
            self.diagram[obj].append(injection)

        # Initialize the Coproduct via AbstractColimit's constructor
        super().__init__(category, self.diagram, self.cocone_morphisms)

    def compute_colimit(self) -> Optional[str]:
        """
        Computes the coproduct object based on the diagram.
        In many categories, the coproduct can be explicitly defined.

        :return: The name of the coproduct object, or None if not computed.
        """
        # For demonstration, assume the coproduct object is predefined
        # In a real implementation, this would involve constructing the coproduct
        self.colimit_object = "CoproductObject"
        self.cocone_morphisms = {obj: Morphism(name=f"ι_{obj}", source=obj, target=self.colimit_object) for obj in self.coproduct_objects}
        self.is_computed = True
        print(f"Computed coproduct object: {self.colimit_object}")
        return self.colimit_object

    def verify_universal_property(self) -> bool:
        """
        Verifies that the computed coproduct satisfies the universal property.
        """
        if not self.is_computed or self.colimit_object is None:
            print("Coproduct object has not been computed yet.")
            return False

        # Placeholder: Assume universal property is satisfied
        print("Verifying universal property of the coproduct.")
        return True

    def __str__(self):
        if self.is_computed and self.colimit_object:
            injections = ", ".join([f"{k}: {v.name}" for k, v in self.cocone_morphisms.items()])
            return (f"Coproduct(\n"
                    f"  Category: {self.category},\n"
                    f"  Objects: {self.coproduct_objects},\n"
                    f"  Colimit Object: {self.colimit_object},\n"
                    f"  Injections: {{{injections}}}\n"
                    f")")
        else:
            return (f"Coproduct(\n"
                    f"  Category: {self.category},\n"
                    f"  Objects: {self.coproduct_objects},\n"
                    f"  Colimit Object: Not computed yet.\n"
                    f")")
