# CategoryTheory/examples/coproduct_example.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractColimit.Coproduct import Coproduct

def main():
    # Define target category D
    objects_D = ["X", "Y", "Z", "CoproductObject"]
    morphisms_D = [
        Morphism(name="f: X→Y", source="X", target="Y"),
        Morphism(name="g: Y→Z", source="Y", target="Z"),
        Morphism(name="h: X→Z", source="X", target="Z"),
        Morphism(name="id_X", source="X", target="X"),
        Morphism(name="id_Y", source="Y", target="Y"),
        Morphism(name="id_Z", source="Z", target="Z"),
        Morphism(name="ι_X", source="X", target="CoproductObject"),
        Morphism(name="ι_Y", source="Y", target="CoproductObject"),
        Morphism(name="ι_Z", source="Z", target="CoproductObject"),
        Morphism(name="id_CoproductObject", source="CoproductObject", target="CoproductObject")
    ]
    morphism_association_D = {
        "X": {
            "Y": [morphisms_D[0]],
            "Z": [morphisms_D[2]],
            "X": [morphisms_D[3]]
        },
        "Y": {
            "Z": [morphisms_D[1]],
            "Y": [morphisms_D[4]]
        },
        "Z": {
            "Z": [morphisms_D[5]]
        },
        "CoproductObject": {
            "X": [morphisms_D[6]],
            "Y": [morphisms_D[7]],
            "Z": [morphisms_D[8]],
            "CoproductObject": [morphisms_D[9]]
        }
    }
    category_D = AbstractCategory(
        objects=objects_D,
        morphisms=morphisms_D,
        morphism_association=morphism_association_D
    )

    # Define functor G: D → D (Identity functor)
    object_mapping_G = {obj: obj for obj in objects_D}
    morphism_mapping_G = {morph.name: morph.name for morph in morphisms_D}
    functor_G = AbstractFunctor(
        source_category=category_D,
        target_category=category_D,
        object_mapping=object_mapping_G,
        morphism_mapping=morphism_mapping_G
    )

    # Define coproduct object
    coproduct = Coproduct(category=category_D, objects=["X", "Y", "Z"])

    # Compute the colimit (coproduct)
    coproduct.compute_colimit()

    # Print the coproduct
    print(coproduct)

    # Verify the universal property
    is_universal = coproduct.verify_universal_property()
    print(f"Coproduct satisfies universal property: {is_universal}")

if __name__ == "__main__":
    main()
