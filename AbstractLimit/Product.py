# CategoryTheory/AbstractLimit/Product.py

from typing import Dict, List, Optional
from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from .AbstractLimit import AbstractLimit

class Product(AbstractLimit):
    """
    Represents the product of a set of objects in a category.
    """

    def __init__(self, 
                 category: AbstractCategory, 
                 objects: List[str]):
        """
        Initializes the Product with a category and a list of objects.

        :param category: The category in which to compute the product.
        :param objects: A list of objects to form the product.
        """
        self.product_objects = objects
        self.diagram = {}  # In products, the diagram consists of projections.
        self.cone_morphisms = {}  # Morphisms η_X: X → ProductObject

        # Define the diagram as projections from the product to each object
        for obj in objects:
            # Projection morphism: π_i: ProductObject → X_i
            projection_name = f"π_{obj}"
            projection = category.get_morphism(projection_name)
            if projection is None:
                raise ValueError(f"Projection morphism '{projection_name}' not found in the category.")
            if obj not in self.diagram:
                self.diagram[obj] = []
            self.diagram[obj].append(projection)

        # Initialize the Product via AbstractLimit's constructor
        super().__init__(category, self.diagram, self.cone_morphisms)

    def compute_limit(self) -> Optional[str]:
        """
        Computes the product object based on the diagram.
        In many categories, the product can be explicitly defined.

        :return: The name of the product object, or None if not computed.
        """
        # For demonstration, assume the product object is predefined
        # In a real implementation, this would involve constructing the product
        self.limit_object = "ProductObject"
        self.cone_morphisms = {obj: Morphism(name=f"π_{obj}", source=self.limit_object, target=obj) for obj in self.product_objects}
        self.is_computed = True
        print(f"Computed product object: {self.limit_object}")
        return self.limit_object

    def verify_universal_property(self) -> bool:
        """
        Verifies that the computed product satisfies the universal property.
        """
        if not self.is_computed or self.limit_object is None:
            print("Product object has not been computed yet.")
            return False

        # Placeholder: Assume universal property is satisfied
        print("Verifying universal property of the product.")
        return True

    def __str__(self):
        if self.is_computed and self.limit_object:
            projections = ", ".join([f"{k}: {v.name}" for k, v in self.cone_morphisms.items()])
            return (f"Product(\n"
                    f"  Category: {self.category},\n"
                    f"  Objects: {self.product_objects},\n"
                    f"  Limit Object: {self.limit_object},\n"
                    f"  Projections: {{{projections}}}\n"
                    f")")
        else:
            return (f"Product(\n"
                    f"  Category: {self.category},\n"
                    f"  Objects: {self.product_objects},\n"
                    f"  Limit Object: Not computed yet.\n"
                    f")")
