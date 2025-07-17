from typing import Dict
from AbstractNaturalTransformation.AbstractNaturalTransformation import AbstractNaturalTransformation
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractCategory.Morphism import Morphism


class NaturalIsomorphism(AbstractNaturalTransformation):
    """
    Represents a natural isomorphism η: F ⇒ G between two functors.
    A natural isomorphism η: F ⇒ G consists of a family of isomorphisms η_X: F(X) → G(X)
    for each object X in the source category, such that for every morphism f: X → Y
    in the source category, the following diagram commutes:
    
        F(X) --F(f)--> F(Y)
         |              |
        η_X            η_Y
         |              |
         v              v
        G(X) --G(f)--> G(Y)
    """

    def __init__(self,
                 source_functor: AbstractFunctor,
                 target_functor: AbstractFunctor,
                 components: Dict[str, str]):
        """
        Initializes the natural isomorphism with source and target functors,
        and the components mapping.
    
        :param source_functor: The source functor F.
        :param target_functor: The target functor G.
        :param components: A dictionary mapping objects in the source category
                           to morphism names in the target category.
        """
        super().__init__(source_functor, target_functor, components)
        if not self.is_natural_isomorphism():
            raise ValueError("The natural transformation is not a natural isomorphism.")

    def inverse(self) -> 'NaturalIsomorphism':
        """
        Returns the inverse natural isomorphism.
    
        :return: The inverse natural isomorphism.
        :raises ValueError: If the natural transformation is not a natural isomorphism.
        """
        # Get the inverse morphism for each component morphism
        inverse_components = {}
        for obj, morph in self.components.items():
            inverse_morph = self.F.target.get_inverse_morphism(morph.name)
            if inverse_morph is None:
                raise ValueError(f"Morphism '{morph.name}' for object '{obj}' does not have an inverse.")
            inverse_components[obj] = inverse_morph.name
        
        # Create the inverse natural isomorphism, swapping the source and target functors
        return NaturalIsomorphism(
            source_functor=self.G,
            target_functor=self.F,
            components=inverse_components
        )
    
    def __str__(self):
        """
        Returns a string representation of the natural isomorphism.
        """
        components_str = ", ".join([f"{obj}: {morph.name}" for obj, morph in self.components.items()])
        return (f"NaturalIsomorphism(\n"
                f"  Source Functor: {self.F},\n"
                f"  Target Functor: {self.G},\n"
                f"  Components: {{{components_str}}}\n"
                f")")
