# CategoryTheory/examples/pushout_example.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractPushout.AbstractPushout import Pushout

def main():
    # Define category C
    objects_C = ["Z", "X", "Y", "PushoutObject"]
    morphisms_C = [
        Morphism(name="f: Z→X", source="Z", target="X"),
        Morphism(name="g: Z→Y", source="Z", target="Y"),
        Morphism(name="η_X: PushoutObject→X", source="PushoutObject", target="X"),
        Morphism(name="η_Y: PushoutObject→Y", source="PushoutObject", target="Y"),
        Morphism(name="id_Z", source="Z", target="Z"),
        Morphism(name="id_X", source="X", target="X"),
        Morphism(name="id_Y", source="Y", target="Y"),
        Morphism(name="id_PushoutObject", source="PushoutObject", target="PushoutObject")
    ]
    morphism_association_C = {
        "Z": {
            "X": [morphisms_C[0]],
            "Y": [morphisms_C[1]],
            "Z": [morphisms_C[4]]
        },
        "X": {
            "PushoutObject": [morphisms_C[2]],
            "X": [morphisms_C[5]]
        },
        "Y": {
            "PushoutObject": [morphisms_C[3]],
            "Y": [morphisms_C[6]]
        },
        "PushoutObject": {
            "PushoutObject": [morphisms_C[7]]
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

    # Define two morphisms f: Z→X and g: Z→Y
    f = category_C.get_morphism("f: Z→X")
    g = category_C.get_morphism("g: Z→Y")
    if f is None or g is None:
        raise ValueError("Morphism f or g not found in the category.")

    # Define the pushout
    pushout = Pushout(category=category_C, morphism1=f, morphism2=g)

    # Compute the pushout
    pushout.compute_colimit()

    # Print the pushout
    print(pushout)

    # Visualize the pushout diagram
    pushout.visualize()

    # Simulate another cocone object C and its morphisms η'_X: X → C and η'_Y: Y → C
    # Since there are no specific category operations here, we will just simulate the verification process
    other_cocone = {
        "X": Morphism(name="η'_X: X→C", source="X", target="C"),
        "Y": Morphism(name="η'_Y: Y→C", source="Y", target="C")
    }

    # Verify the universal property
    is_universal = pushout.verify_universal_property(other_cocone)
    print(f"Pushout satisfies universal property: {is_universal}")

if __name__ == "__main__":
    main()
