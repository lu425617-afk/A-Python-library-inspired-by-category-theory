# CategoryTheory/AbstractStrictMonoidalCategory/AbstractStrictMonoidalCategory.py

from typing import Callable, Dict, List, Optional
from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from Diagram.Diagram import Diagram

class AbstractStrictMonoidalCategory(AbstractCategory):
    """
    Represents an abstract strict monoidal category.
    """

    def __init__(self,
                 objects: List[str],
                 morphisms: List[Morphism],
                 morphism_association: Dict[str, Dict[str, List[Morphism]]],
                 unit_object: str,
                 tensor_objects_func: Callable[[str, str], str],
                 tensor_morphisms_func: Callable[[Morphism, Morphism], Morphism]):
        """
        Initializes the strict monoidal category.

        :param objects: List of object names in the category.
        :param morphisms: List of Morphism instances in the category.
        :param morphism_association: A nested dictionary mapping source -> target -> list of morphisms.
        :param unit_object: The unit object in the monoidal category.
        :param tensor_objects_func: Function to compute tensor product of two objects.
        :param tensor_morphisms_func: Function to compute tensor product of two morphisms.
        """
        super().__init__(objects, morphisms, morphism_association)
        self.unit_object = unit_object
        self.tensor_objects = tensor_objects_func
        self.tensor_morphisms = tensor_morphisms_func

    def get_unit_object(self) -> str:
        """
        Retrieves the unit object of the monoidal category.

        :return: The name of the unit object.
        """
        return self.unit_object

    def tensor(self, obj1: str, obj2: str) -> str:
        """
        Computes the tensor product of two objects.

        :param obj1: The first object.
        :param obj2: The second object.
        :return: The tensor product object.
        """
        return self.tensor_objects(obj1, obj2)

    def tensor_morphisms_pair(self, morph1: Morphism, morph2: Morphism) -> Morphism:
        """
        Computes the tensor product of two morphisms.

        :param morph1: The first morphism.
        :param morph2: The second morphism.
        :return: The tensor product morphism.
        """
        return self.tensor_morphisms(morph1, morph2)

    def visualize_monoidal_structure(self, filename: str = "monoidal_structure_diagram", format: str = "png"):
        """
        Generates a visual representation of the monoidal structure.

        :param filename: The name of the output file without extension.
        :param format: The format of the output file (e.g., 'png', 'pdf').
        """
        print("Visualizing the monoidal structure diagram...")
        # Create a diagram that includes tensor products and unit object
        # For simplicity, we'll visualize tensor products of a few objects and morphisms

        # Example: visualize tensor products involving the unit object
        tensor_diagram = Diagram(
            objects=[self.unit_object] + self.objects,
            morphisms=[]
        )

        # Add tensor product edges
        for obj in self.objects:
            tensor_obj = self.tensor_objects(self.unit_object, obj)
            tensor_diagram.add_morphism(Morphism(name=f"I⊗{obj} → {tensor_obj}", source=self.unit_object + f"⊗{obj}", target=tensor_obj))
            tensor_diagram.add_morphism(Morphism(name=f"{obj}⊗I → {tensor_obj}", source=f"{obj}⊗{self.unit_object}", target=tensor_obj))

        # Add unit object node
        tensor_diagram.add_morphism(Morphism(name="id_I", source=self.unit_object, target=self.unit_object))

        # Render the diagram
        tensor_diagram.visualize(filename, format)
        print(f"Monoidal structure diagram has been rendered and saved as {filename}.{format}")

    def __str__(self):
        morphism_str = "\n    ".join([str(morph) for morph in self.morphisms])
        return (f"AbstractStrictMonoidalCategory(\n"
                f"  Objects: {self.objects},\n"
                f"  MorphismCount: {len(self.morphisms)},\n"
                f"  Morphisms:\n    {morphism_str},\n"
                f"  Unit Object: {self.unit_object}\n"
                f")")
