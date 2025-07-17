# CategoryTheory/examples/limit_example.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractLimit.Product import Product

def main():
    # Define category C
    objects_C = ["A", "B", "C"]
    morphisms_C = [
        Morphism(name="f: A→B", source="A", target="B"),
        Morphism(name="g: A→C", source="A", target="C"),
        Morphism(name="h: B→C", source="B", target="C"),
        Morphism(name="id_A", source="A", target="A"),
        Morphism(name="id_B", source="B", target="B"),
        Morphism(name="id_C", source="C", target="C"),
        Morphism(name="π_A", source="ProductObject", target="A"),
        Morphism(name="π_B", source="ProductObject", target="B"),
        Morphism(name="π_C", source="ProductObject", target="C")
    ]
    morphism_association_C = {
        "A": {
            "B": [morphisms_C[0]],
            "C": [morphisms_C[1]],
            "A": [morphisms_C[3]]
        },
        "B": {
            "C": [morphisms_C[2]],
            "B": [morphisms_C[4]]
        },
        "C": {
            "C": [morphisms_C[5]]
        },
        "ProductObject": {
            "A": [morphisms_C[6]],
            "B": [morphisms_C[7]],
            "C": [morphisms_C[8]]
        }
    }
    category_C = AbstractCategory(
        objects=objects_C + ["ProductObject"],
        morphisms=morphisms_C,
        morphism_association=morphism_association_C
    )

    # Define functor F: C → C (identity functor)
    object_mapping_F = {obj: obj for obj in objects_C + ["ProductObject"]}
    morphism_mapping_F = {morph.name: morph.name for morph in morphisms_C}
    functor_F = AbstractFunctor(
        source_category=category_C,
        target_category=category_C,
        object_mapping=object_mapping_F,
        morphism_mapping=morphism_mapping_F
    )

    # Define product object
    product = Product(category=category_C, objects=["A", "B", "C"])

    # Compute limit (product)
    product.compute_limit()

    # Print the product
    print(product)

    # Verify universal property
    is_universal = product.verify_universal_property()
    print(f"Product satisfies universal property: {is_universal}")

if __name__ == "__main__":
    main()
