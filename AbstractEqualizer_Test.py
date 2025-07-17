# CategoryTheory/examples/equalizer_example.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractEqualizer.AbstractEqualizer import Equalizer

def main():
    # Define category C
    objects_C = ["X", "Y", "EqualizerObject"]
    morphisms_C = [
        Morphism(name="f: X→Y", source="X", target="Y"),
        Morphism(name="g: X→Y", source="X", target="Y"),
        Morphism(name="e: EqualizerObject→X", source="EqualizerObject", target="X"),
        Morphism(name="id_X", source="X", target="X"),
        Morphism(name="id_Y", source="Y", target="Y"),
        Morphism(name="id_EqualizerObject", source="EqualizerObject", target="EqualizerObject")
    ]
    morphism_association_C = {
        "X": {
            "Y": [morphisms_C[0], morphisms_C[1]],
            "X": [morphisms_C[3]]
        },
        "Y": {
            "Y": [morphisms_C[4]]
        },
        "EqualizerObject": {
            "X": [morphisms_C[2]],
            "EqualizerObject": [morphisms_C[5]]
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

    # Define equalizer (Equalizer)
    equalizer = Equalizer(category=category_C, morphism1=f, morphism2=g)

    # Compute the equalizer
    equalizer.compute_limit()

    # Print the equalizer
    print(equalizer)

    # Visualize the equalizer diagram
    equalizer.visualize()

    # Simulate another cone object C and its morphism η'_X: C → X
    # Since there are no specific category operations, we will only simulate the verification process
    other_cone = {
        "X": Morphism(name="e'_X: C→X", source="C", target="X")
    }

    # Verify the universal property
    is_universal = equalizer.verify_universal_property(other_cone)
    print(f"Equalizer satisfies universal property: {is_universal}")

if __name__ == "__main__":
    main()
