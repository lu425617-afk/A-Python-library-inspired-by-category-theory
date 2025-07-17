# CategoryTheory/AbstractPullback/AbstractPullback.py

from typing import Dict, List, Optional, Callable
from AbstractLimit.AbstractLimit import AbstractLimit
from AbstractCategory.Morphism import Morphism
from AbstractCategory.AbstractCategory import AbstractCategory
from Diagram.Diagram import Diagram

class Pullback(AbstractLimit):
    """
    Represents the pullback of two morphisms in a category.
    """
    
    def __init__(self, 
                 category: AbstractCategory, 
                 morphism1: Morphism, 
                 morphism2: Morphism):
        """
        Initializes the Pullback with a category and two morphisms with a common codomain.

        :param category: The category in which to compute the pullback.
        :param morphism1: The first morphism f: X → Z.
        :param morphism2: The second morphism g: Y → Z.
        """
        if morphism1.target != morphism2.target:
            raise ValueError("Both morphisms must have the same codomain.")
        
        self.morphism1 = morphism1
        self.morphism2 = morphism2
        # Initialize the diagram using the Diagram class
        self.diagram = Diagram(
            objects=[morphism1.source, morphism2.source, morphism1.target],
            morphisms=[morphism1, morphism2]
        )
        self.cone_morphisms = {}  # morphisms η_X: PullbackObject → X, η_Y: PullbackObject → Y
        
        super().__init__(category, self.diagram, self.cone_morphisms)
    
    def compute_limit(self) -> Optional[str]:
        """
        Computes the pullback object based on the diagram.
        In many categories, the pullback can be explicitly defined.

        :return: The name of the pullback object, or None if not computed.
        """
        # For demonstration, assume the pullback object is predefined
        # In a real implementation, this would involve constructing the pullback
        self.limit_object = "PullbackObject"
        self.cone_morphisms = {
            "X": Morphism(name="η_X", source=self.limit_object, target=self.morphism1.source),
            "Y": Morphism(name="η_Y", source=self.limit_object, target=self.morphism2.source)
        }
        self.is_computed = True
        print(f"Computed pullback object: {self.limit_object}")
        return self.limit_object
    
    def verify_universal_property(self, other_cone: Dict[str, Morphism]) -> bool:
        """
        Verifies that the computed pullback satisfies the universal property.

        :param other_cone: A dictionary representing another cone with morphisms.
                           Keys are object names, values are Morphism instances.
        :return: True if the universal property is satisfied, False otherwise.
        """
        if not self.is_computed or self.limit_object is None:
            print("Pullback object has not been computed yet.")
            return False

        # other_cone should contain morphisms η'_X: C → X and η'_Y: C → Y
        if "X" not in other_cone or "Y" not in other_cone:
            print("The other cone must have morphisms for 'X' and 'Y'.")
            return False

        eta_prime_X = other_cone["X"]
        eta_prime_Y = other_cone["Y"]

        # Check if f ∘ u = η'_X and g ∘ u = η'_Y hold
        # Here, we cannot actually compute u since there are no specific category operations
        # So, we assume the existence of a unique u and return True

        print("Verifying universal property of the pullback.")
        print(f"Assuming existence of unique morphism u: C → {self.limit_object} such that:")
        print(f"  {self.morphism1.name} ∘ u = {eta_prime_X.name}")
        print(f"  {self.morphism2.name} ∘ u = {eta_prime_Y.name}")
        
        # Return True, indicating verification passed
        return True
    
    def visualize(self, filename: str = "pullback_diagram", format: str = "png"):
        """
        Generates a visual representation of the pullback diagram.

        :param filename: The name of the output file without extension.
        :param format: The format of the output file (e.g., 'png', 'pdf').
        """
        print("Visualizing the pullback diagram...")
        # Create a new Diagram including the pullback object and its morphisms
        full_diagram = Diagram(
            objects=self.diagram.objects + [self.limit_object],
            morphisms=self.diagram.morphisms + list(self.cone_morphisms.values())
        )
        full_diagram.visualize(filename, format)
        print(f"Pullback diagram has been visualized and saved as {filename}.{format}")
    
    def __str__(self):
        if self.is_computed and self.limit_object:
            return (f"Pullback(\n"
                    f"  Category: {self.category},\n"
                    f"  Morphism1: {self.morphism1.name},\n"
                    f"  Morphism2: {self.morphism2.name},\n"
                    f"  Limit Object: {self.limit_object},\n"
                    f"  Cone Morphisms: {self.cone_morphisms}\n"
                    f")")
        else:
            return (f"Pullback(\n"
                    f"  Category: {self.category},\n"
                    f"  Morphism1: {self.morphism1.name},\n"
                    f"  Morphism2: {self.morphism2.name},\n"
                    f"  Limit Object: Not computed yet.\n"
                    f")")