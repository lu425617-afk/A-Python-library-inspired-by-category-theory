# CategoryTheory/examples/coequalizer_example.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractCoequalizer.AbstractCoequalizer import Coequalizer

def main():
    # Define category C
    objects_C = ["X", "Y", "CoequalizerObject"]
    morphisms_C = [
        Morphism(name="f: X→Y", source="X", target="Y"),
        Morphism(name="g: X→Y", source="X", target="Y"),
        Morphism(name="q: Y→CoequalizerObject", source="Y", target="CoequalizerObject"),
        Morphism(name="id_X", source="X", target="X"),
        Morphism(name="id_Y", source="Y", target="Y"),
        Morphism(name="id_CoequalizerObject", source="CoequalizerObject", target="CoequalizerObject")
    ]
    morphism_association_C = {
        "X": {
            "Y": [morphisms_C[0], morphisms_C[1]],
            "X": [morphisms_C[3]]
        },
        "Y": {
            "CoequalizerObject": [morphisms_C[2]],
            "Y": [morphisms_C[4]]
        },
        "CoequalizerObject": {
            "CoequalizerObject": [morphisms_C[5]]
        }
    }
    category_C = AbstractCategory(
        objects=objects_C,
        morphisms=morphisms_C,
        morphism_association=morphism_association_C
    )

    # Define functor F: C → C (Identity functor)
    object_mapping_F = {obj: obj for obj in objects_C}
    morphism_mapping_F = {morph.name: morph.name for morph in morphisms_C}
    functor_F = AbstractFunctor(
        source_category=category_C,
        target_category=category_C,
        object_mapping=object_mapping_F,
        morphism_mapping=morphism_mapping_F
    )

    # Define two parallel morphisms f: X→Y and g: X→Y
    f = category_C.get_morphism("f: X→Y")
    g = category_C.get_morphism("g: X→Y")
    if f is None or g is None:
        raise ValueError("Morphism f or g not found in the category.")

    # Define the coequalizer
    coequalizer = Coequalizer(category=category_C, morphism1=f, morphism2=g)

    # Compute the coequalizer
    coequalizer.compute_colimit()

    # Print the coequalizer
    print(coequalizer)

    # Visualize the coequalizer diagram
    coequalizer.visualize()

    # Simulate another cocone object C and its morphisms η'_X: X → C and η'_Y: Y → C
    # Since there are no specific category operations, we will simulate the verification process only
    other_cocone = {
        "Y": Morphism(name="q'_Y: Y→C", source="Y", target="C")
    }

    # Verify the universal property
    is_universal = coequalizer.verify_universal_property(other_cocone)
    print(f"Coequalizer satisfies universal property: {is_universal}")

if __name__ == "__main__":
    main()
