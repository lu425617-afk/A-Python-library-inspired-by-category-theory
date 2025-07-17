# CategoryTheory/Diagram/Diagram.py

from typing import List, Dict
from AbstractCategory.Morphism import Morphism
from graphviz import Digraph

class Diagram:
    """
    Represents a diagram in a category, consisting of objects and morphisms.
    """

    def __init__(self, objects: List[str], morphisms: List[Morphism]):
        """
        Initializes the Diagram with a list of objects and morphisms.

        :param objects: List of object names in the diagram.
        :param morphisms: List of Morphism instances in the diagram.
        """
        self.objects = objects
        self.morphisms = morphisms
        self.morphism_association = self._build_morphism_association()

    def _build_morphism_association(self) -> Dict[str, Dict[str, List[Morphism]]]:
        """
        Builds a mapping from source objects to target objects to morphisms.

        :return: A nested dictionary mapping source -> target -> list of morphisms.
        """
        association = {obj: {} for obj in self.objects}
        for morphism in self.morphisms:
            src = morphism.source
            tgt = morphism.target
            if src not in association:
                association[src] = {}
            if tgt not in association[src]:
                association[src][tgt] = []
            association[src][tgt].append(morphism)
        return association

    def add_morphism(self, morphism: Morphism):
        """
        Adds a morphism to the diagram.

        :param morphism: The Morphism instance to add.
        """
        if morphism.source not in self.objects:
            self.objects.append(morphism.source)
        if morphism.target not in self.objects:
            self.objects.append(morphism.target)
        self.morphisms.append(morphism)
        # Update association
        if morphism.source not in self.morphism_association:
            self.morphism_association[morphism.source] = {}
        if morphism.target not in self.morphism_association[morphism.source]:
            self.morphism_association[morphism.source][morphism.target] = []
        self.morphism_association[morphism.source][morphism.target].append(morphism)

    def get_morphisms_from(self, source: str, target: str) -> List[Morphism]:
        """
        Retrieves all morphisms from a source object to a target object.

        :param source: The source object name.
        :param target: The target object name.
        :return: List of Morphism instances.
        """
        return self.morphism_association.get(source, {}).get(target, [])

    def visualize(self, filename: str = "diagram", format: str = "png"):
        """
        Generates a visual representation of the diagram using graphviz.

        :param filename: The name of the output file without extension.
        :param format: The format of the output file (e.g., 'png', 'pdf').
        """
        dot = Digraph(comment="Category Diagram", format=format)
        # Add nodes
        for obj in self.objects:
            dot.node(obj, obj)
        # Add edges
        for morphism in self.morphisms:
            label = morphism.name
            dot.edge(morphism.source, morphism.target, label=label)
        # Render the graph
        dot.render(filename, view=True)
        print(f"Diagram has been rendered and saved as {filename}.{format}")

    def __str__(self):
        morphism_str = "\n    ".join([str(morph) for morph in self.morphisms])
        return (f"Diagram(\n"
                f"  Objects: {self.objects},\n"
                f"  Morphisms:\n    {morphism_str}\n"
                f")")
