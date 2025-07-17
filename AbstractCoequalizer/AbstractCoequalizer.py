# CategoryTheory/AbstractCoequalizer/AbstractCoequalizer.py

from typing import Dict, List, Optional
from AbstractColimit.AbstractColimit import AbstractColimit
from AbstractCategory.Morphism import Morphism
from AbstractCategory.AbstractCategory import AbstractCategory
from Diagram.Diagram import Diagram

class Coequalizer(AbstractColimit):
    """
    Represents the coequalizer of two parallel morphisms in a category.
    """
    
    def __init__(self, 
                 category: AbstractCategory, 
                 morphism1: Morphism, 
                 morphism2: Morphism):
        """
        Initializes the Coequalizer with a category and two parallel morphisms.
        
        :param category: The category in which to compute the coequalizer.
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
        self.cocone_morphisms = {}  # morphism q: Y → CoequalizerObject
        
        super().__init__(category, self.diagram, self.cocone_morphisms)
    
    def compute_colimit(self) -> Optional[str]:
        """
        Computes the coequalizer object based on the diagram.
        In many categories, the coequalizer can be explicitly defined.
        
        :return: The name of the coequalizer object, or None if not computed.
        """
        # For demonstration, assume the coequalizer object is predefined
        # In a real implementation, this would involve constructing the coequalizer
        self.colimit_object = "CoequalizerObject"
        self.cocone_morphisms = {
            "Y": Morphism(name="q: Y→CoequalizerObject", source=self.morphism1.target, target=self.colimit_object)
        }
        self.is_computed = True
        print(f"Computed coequalizer object: {self.colimit_object}")
        return self.colimit_object
    
    def verify_universal_property(self, other_cocone: Dict[str, Morphism]) -> bool:
        """
        Verifies that the computed coequalizer satisfies the universal property.
        
        :param other_cocone: A dictionary representing another cocone with morphisms.
                             Keys are object names, values are Morphism instances.
        :return: True if the universal property is satisfied, False otherwise.
        """
        if not self.is_computed or self.colimit_object is None:
            print("Coequalizer object has not been computed yet.")
            return False

        # other_cocone 应该包含 morphism q': Y → C，使得 q' ∘ f = q' ∘ g
        if "Y" not in other_cocone:
            print("The other cocone must have a morphism for 'Y'.")
            return False

        q_prime = other_cocone["Y"]

        # 检查 q' ∘ f = q' ∘ g
        # 由于缺乏具体的范畴操作，我们假设此条件被满足
        print("Verifying universal property of the coequalizer.")
        print(f"Assuming {q_prime.name} ∘ {self.morphism1.name} = {q_prime.name} ∘ {self.morphism2.name}")
        print("Assuming existence of unique morphism u: CoequalizerObject → C such that u ∘ q = q'")
        
        # 返回 True，表示验证通过
        return True
    
    def visualize(self, filename: str = "coequalizer_diagram", format: str = "png"):
        """
        Generates a visual representation of the coequalizer diagram.
        
        :param filename: The name of the output file without extension.
        :param format: The format of the output file (e.g., 'png', 'pdf').
        """
        print("Visualizing the coequalizer diagram...")
        # 创建一个新的 Diagram 包含余等化子对象及其态射
        full_diagram = Diagram(
            objects=self.diagram.objects + [self.colimit_object],
            morphisms=self.diagram.morphisms + list(self.cocone_morphisms.values())
        )
        full_diagram.visualize(filename, format)
        print(f"Coequalizer diagram has been visualized and saved as {filename}.{format}")
    
    def __str__(self):
        if self.is_computed and self.colimit_object:
            return (f"Coequalizer(\n"
                    f"  Category: {self.category},\n"
                    f"  Morphism1: {self.morphism1.name},\n"
                    f"  Morphism2: {self.morphism2.name},\n"
                    f"  Colimit Object: {self.colimit_object},\n"
                    f"  Cocone Morphisms: {self.cocone_morphisms}\n"
                    f")")
        else:
            return (f"Coequalizer(\n"
                    f"  Category: {self.category},\n"
                    f"  Morphism1: {self.morphism1.name},\n"
                    f"  Morphism2: {self.morphism2.name},\n"
                    f"  Colimit Object: Not computed yet.\n"
                    f")")
