# AbstractFunctor/IdentityFunctor.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractFunctor.AbstractFunctor import AbstractFunctor


class IdentityFunctor(AbstractFunctor):
    """
    Represents the identity functor F: C → C,
    where F maps each object and morphism to itself.
    """

    def __init__(self, category: AbstractCategory):
        """
        Initializes the IdentityFunctor with the given category.

        :param category: The category to map to itself.
        """
        object_mapping = {obj: obj for obj in category.Objects}
        morphism_mapping = {morphism.name: morphism.name for morphism in category.morphisms}
        super().__init__(
            source_category=category,
            target_category=category,
            object_mapping=object_mapping,
            morphism_mapping=morphism_mapping
        )
