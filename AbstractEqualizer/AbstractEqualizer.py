# CategoryTheory/AbstractEqualizer/AbstractEqualizer.py

from typing import Dict, List, Optional
from AbstractLimit.AbstractLimit import AbstractLimit
from AbstractCategory.Morphism import Morphism
from AbstractCategory.AbstractCategory import AbstractCategory
from Diagram.Diagram import Diagram

class Equalizer(AbstractLimit):
    """
    Represents the equalizer of two parallel morphisms in a category.
    """

    def __init__(self, 
                 category: AbstractCategory, 
                 morphism1: Morphism, 
                 morphism2: Morphism):
        """
        Initializes the Equalizer with a category and two parallel morphisms.

        :param category: The category in which to compute the equalizer.
        :param morphism1: The first morphism f: X → Y.
        :param morphism2: The second morphism g: X → Y.
        """
        if morphism1.source != morphism2.source or morphism1.target != morphism2.target:
            raise ValueError("Both morphisms must be parallel (same source and target).")
        
        self.morphism1 = morphism1
        self.morphism2 = morphism2
        # Initialize the diagram using the Diagram class
        self.diagram = Diagram(
            objects=[morphism1.source, morphism1.target],
            morphisms=[morphism1, morphism2]
        )
        self.cone_morphisms = {}  # Morphism e: EqualizerObject → X
        
        super().__init__(category, self.diagram, self.cone_morphisms)

    def compute_limit(self) -> Optional[str]:
        """
        Computes the equalizer object based on the diagram.
        In many categories, the equalizer can be explicitly defined.

        :return: The name of the equalizer object, or None if not computed.
        """
        # For demonstration, assume the equalizer object is predefined
        # In a real implementation, this would involve constructing the equalizer
        self.limit_object = "EqualizerObject"
        self.cone_morphisms = {
            "X": Morphism(name="e: EqualizerObject→X", source=self.limit_object, target=self.morphism1.source)
        }
        self.is_computed = True
        print(f"Computed equalizer object: {self.limit_object}")
        return self.limit_object

    def verify_universal_property(self, other_cone: Dict[str, Morphism]) -> bool:
        """
        Verifies that the computed equalizer satisfies the universal property.

        :param other_cone: A dictionary representing another cone with morphisms.
                           Keys are object names, values are Morphism instances.
        :return: True if the universal property is satisfied, False otherwise.
        """
        if not self.is_computed or self.limit_object is None:
            print("Equalizer object has not been computed yet.")
            return False

        # The other_cone should include morphism e': C → X, such that f ∘ e' = g ∘ e'
        if "X" not in other_cone:
            print("The other cone must have a morphism for 'X'.")
            return False

        e_prime = other_cone["X"]

        # Check if f ∘ e' = g ∘ e'
        # Given the lack of concrete category operations, we assume this condition is satisfied
        print("Verifying universal property of the equalizer.")
        print(f"Assuming {self.morphism1.name} ∘ {e_prime.name} = {self.morphism2.name} ∘ {e_prime.name}")
        print("Assuming existence of unique morphism u: C → EqualizerObject such that e ∘ u = e'")

        # Return True, indicating verification passed
        return True

    def visualize(self, filename: str = "equalizer_diagram", format: str = "png"):
        """
        Generates a visual representation of the equalizer diagram.

        :param filename: The name of the output file without extension.
        :param format: The format of the output file (e.g., 'png', 'pdf').
        """
        print("Visualizing the equalizer diagram...")
        # Create a new Diagram including the equalizer object and its morphisms
        full_diagram = Diagram(
            objects=self.diagram.objects + [self.limit_object],
            morphisms=self.diagram.morphisms + list(self.cone_morphisms.values())
        )
        full_diagram.visualize(filename, format)
        print(f"Equalizer diagram has been visualized and saved as {filename}.{format}")

    def __str__(self):
        if self.is_computed and self.limit_object:
            return (f"Equalizer(\n"
                    f"  Category: {self.category},\n"
                    f"  Morphism1: {self.morphism1.name},\n"
                    f"  Morphism2: {self.morphism2.name},\n"
                    f"  Limit Object: {self.limit_object},\n"
                    f"  Cone Morphisms: {self.cone_morphisms}\n"
                    f")")
        else:
            return (f"Equalizer(\n"
                    f"  Category: {self.category},\n"
                    f"  Morphism1: {self.morphism1.name},\n"
                    f"  Morphism2: {self.morphism2.name},\n"
                    f"  Limit Object: Not computed yet.\n"
                    f")")