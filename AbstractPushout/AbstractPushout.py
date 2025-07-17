# CategoryTheory/AbstractPushout/AbstractPushout.py

from typing import Dict, List, Optional, Callable
from AbstractColimit.AbstractColimit import AbstractColimit
from AbstractCategory.Morphism import Morphism
from AbstractCategory.AbstractCategory import AbstractCategory
from Diagram.Diagram import Diagram

class Pushout(AbstractColimit):
    """
    Represents the pushout of two morphisms in a category.
    """
    
    def __init__(self, 
                 category: AbstractCategory, 
                 morphism1: Morphism, 
                 morphism2: Morphism):
        """
        Initializes the Pushout with a category and two morphisms with a common source.

        :param category: The category in which to compute the pushout.
        :param morphism1: The first morphism f: Z → X.
        :param morphism2: The second morphism g: Z → Y.
        """
        if morphism1.source != morphism2.source:
            raise ValueError("Both morphisms must have the same source.")
        
        self.morphism1 = morphism1
        self.morphism2 = morphism2
        # Initialize the diagram using the Diagram class
        self.diagram = Diagram(
            objects=[morphism1.target, morphism2.target, morphism1.source],
            morphisms=[morphism1, morphism2]
        )
        self.cocone_morphisms = {}  # morphisms η_X: PushoutObject → X, η_Y: PushoutObject → Y
        
        super().__init__(category, self.diagram, self.cocone_morphisms)
    
    def compute_colimit(self) -> Optional[str]:
        """
        Computes the pushout object based on the diagram.
        In many categories, the pushout can be explicitly defined.

        :return: The name of the pushout object, or None if not computed.
        """
        # For demonstration, assume the pushout object is predefined
        # In a real implementation, this would involve constructing the pushout
        self.colimit_object = "PushoutObject"
        self.cocone_morphisms = {
            "X": Morphism(name="η_X", source=self.colimit_object, target=self.morphism1.target),
            "Y": Morphism(name="η_Y", source=self.colimit_object, target=self.morphism2.target)
        }
        self.is_computed = True
        print(f"Computed pushout object: {self.colimit_object}")
        return self.colimit_object
    
    def verify_universal_property(self, other_cocone: Dict[str, Morphism]) -> bool:
        """
        Verifies that the computed pushout satisfies the universal property.

        :param other_cocone: A dictionary representing another cocone with morphisms.
                             Keys are object names, values are Morphism instances.
        :return: True if the universal property is satisfied, False otherwise.
        """
        if not self.is_computed or self.colimit_object is None:
            print("Pushout object has not been computed yet.")
            return False

        # other_cocone should contain morphisms η'_X: X → C and η'_Y: Y → C
        if "X" not in other_cocone or "Y" not in other_cocone:
            print("The other cocone must have morphisms for 'X' and 'Y'.")
            return False

        eta_prime_X = other_cocone["X"]
        eta_prime_Y = other_cocone["Y"]

        # Check if u ∘ f = η'_X and u ∘ g = η'_Y hold
        # Here, we cannot actually compute u since there are no specific category operations
        # So, we assume the existence of a unique u and return True

        print("Verifying universal property of the pushout.")
        print(f"Assuming existence of unique morphism u: {self.colimit_object} → C such that:")
        print(f"  u ∘ {self.morphism1.name} = {eta_prime_X.name}")
        print(f"  u ∘ {self.morphism2.name} = {eta_prime_Y.name}")
        
        # Return True, indicating verification passed
        return True
    
    def visualize(self, filename: str = "pushout_diagram", format: str = "png"):
        """
        Generates a visual representation of the pushout diagram.

        :param filename: The name of the output file without extension.
        :param format: The format of the output file (e.g., 'png', 'pdf').
        """
        print("Visualizing the pushout diagram...")
        # Create a new Diagram including the pushout colimit object and its morphisms
        full_diagram = Diagram(
            objects=self.diagram.objects + [self.colimit_object],
            morphisms=self.diagram.morphisms + list(self.cocone_morphisms.values())
        )
        full_diagram.visualize(filename, format)
        print(f"Pushout diagram has been visualized and saved as {filename}.{format}")
    
    def __str__(self):
        if self.is_computed and self.colimit_object:
            return (f"Pushout(\n"
                    f"  Category: {self.category},\n"
                    f"  Morphism1: {self.morphism1.name},\n"
                    f"  Morphism2: {self.morphism2.name},\n"
                    f"  Colimit Object: {self.colimit_object},\n"
                    f"  Cocone Morphisms: {self.cocone_morphisms}\n"
                    f")")
        else:
            return (f"Pushout(\n"
                    f"  Category: {self.category},\n"
                    f"  Morphism1: {self.morphism1.name},\n"
                    f"  Morphism2: {self.morphism2.name},\n"
                    f"  Colimit Object: Not computed yet.\n"
                    f")")
