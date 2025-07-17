# CategoryTheory/SymmetricMonoidalCategory/SymmetricMonoidalCategory.py

from typing import Callable, Dict, List, Optional, Tuple
from AbstractMonoidalCategory.AbstractMonoidalCategory import AbstractMonoidalCategory
from AbstractCategory.Morphism import Morphism
from Diagram.Diagram import Diagram

class SymmetricMonoidalCategory(AbstractMonoidalCategory):
    """
    Represents a symmetric monoidal category.
    """
    
    def __init__(self,
                 objects: List[str],
                 morphisms: List[Morphism],
                 morphism_association: Dict[str, Dict[str, List[Morphism]]],
                 unit_object: str,
                 tensor_objects_func: Callable[[str, str], str],
                 tensor_morphisms_func: Callable[[Morphism, Morphism], Morphism],
                 associators: Dict[Tuple[str, str, str], Morphism],
                 left_unitors: Dict[str, Morphism],
                 right_unitors: Dict[str, Morphism],
                 braidings: Dict[Tuple[str, str], Morphism]):
        """
        Initializes the symmetric monoidal category.

        :param objects: List of object names in the category.
        :param morphisms: List of Morphism instances in the category.
        :param morphism_association: A nested dictionary mapping source -> target -> list of morphisms.
        :param unit_object: The unit object in the monoidal category.
        :param tensor_objects_func: Function to compute tensor product of two objects.
        :param tensor_morphisms_func: Function to compute tensor product of two morphisms.
        :param associators: Dictionary mapping object triples to their associator morphisms.
        :param left_unitors: Dictionary mapping objects to their left unitor morphisms.
        :param right_unitors: Dictionary mapping objects to their right unitor morphisms.
        :param braidings: Dictionary mapping object pairs to their braiding morphisms γ_{A,B}.
        """
        super().__init__(objects, morphisms, morphism_association, unit_object,
                         tensor_objects_func, tensor_morphisms_func,
                         associators, left_unitors, right_unitors)
        self.braidings = braidings

    def get_braiding(self, A: str, B: str) -> Morphism:
        """
        Retrieves the braiding morphism for objects A and B.

        :param A: Object A.
        :param B: Object B.
        :return: The braiding morphism γ_{A,B}.
        """
        key = (A, B)
        return self.braidings.get(key, None)

    def verify_braiding_symmetry(self) -> bool:
        """
        Verifies the symmetry condition: γ_{B,A} ∘ γ_{A,B} = id_{A⊗B}.

        :return: True if all symmetry conditions hold, False otherwise.
        """
        for (A, B), gamma_AB in self.braidings.items():
            gamma_BA = self.braidings.get((B, A), None)
            if gamma_BA is None:
                print(f"Missing braiding morphism for ({B}, {A}).")
                return False
            # Compose gamma_{B,A} ∘ gamma_{A,B}
            composed_name = f"{gamma_BA.name} ∘ {gamma_AB.name}"
            composed_morph = self.category.compose(gamma_BA, gamma_AB)
            if composed_morph is None or composed_morph.name != f"id_{self.tensor_objects(A, B)}":
                print(f"Symmetry condition failed for ({A}, {B}): {composed_name} != id_{self.tensor_objects(A, B)}")
                return False
        print("All symmetry conditions are satisfied.")
        return True

    def visualize_braiding(self, filename: str = "braiding_diagram", format: str = "png"):
        """
        Generates a visual representation of the braiding morphisms.

        :param filename: The name of the output file without extension.
        :param format: The format of the output file (e.g., 'png', 'pdf').
        """
        print("Visualizing the braiding morphisms diagram...")
        braiding_diagram = Diagram(
            objects=self.objects,
            morphisms=[]
        )
        for (A, B), gamma in self.braidings.items():
            braiding_diagram.add_morphism(gamma)
        braiding_diagram.visualize(filename, format)
        print(f"Braiding morphisms diagram has been rendered and saved as {filename}.{format}")

    def __str__(self):
        base_str = super().__str__()
        braiding_str = "\n    ".join([str(morph) for morph in self.braidings.values()])
        return (base_str + 
                f",\n  Braidings:\n    {braiding_str}\n"
                f")")
