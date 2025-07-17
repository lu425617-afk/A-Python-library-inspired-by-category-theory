# CategoryTheory/examples/pullback_example.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractPullback.AbstractPullback import Pullback

def main():
    # Define category C
    objects_C = ["X", "Y", "Z", "PullbackObject"]
    morphisms_C = [
        Morphism(name="f: X→Z", source="X", target="Z"),
        Morphism(name="g: Y→Z", source="Y", target="Z"),
        Morphism(name="η_X: PullbackObject→X", source="PullbackObject", target="X"),
        Morphism(name="η_Y: PullbackObject→Y", source="PullbackObject", target="Y"),
        Morphism(name="id_X", source="X", target="X"),
        Morphism(name="id_Y", source="Y", target="Y"),
        Morphism(name="id_Z", source="Z", target="Z"),
        Morphism(name="id_PullbackObject", source="PullbackObject", target="PullbackObject")
    ]
    morphism_association_C = {
        "X": {
            "Z": [morphisms_C[0]],
            "X": [morphisms_C[4]]
        },
        "Y": {
            "Z": [morphisms_C[1]],
            "Y": [morphisms_C[5]]
        },
        "Z": {
            "Z": [morphisms_C[6]]
        },
        "PullbackObject": {
            "X": [morphisms_C[2]],
            "Y": [morphisms_C[3]],
            "PullbackObject": [morphisms_C[7]]
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

    # Define two morphisms f: X→Z and g: Y→Z
    f = category_C.get_morphism("f: X→Z")
    g = category_C.get_morphism("g: Y→Z")
    if f is None or g is None:
        raise ValueError("Morphism f or g not found in the category.")

    # Define the pullback
    pullback = Pullback(category=category_C, morphism1=f, morphism2=g)

    # Compute the pullback
    pullback.compute_limit()

    # Print the pullback
    print(pullback)

    # Visualize the pullback diagram
    pullback.visualize()

    # Simulate another cone object C and its morphisms η'_X: C → X and η'_Y: C → Y
    # Since there are no specific category operations here, we will just simulate the verification process
    other_cone = {
        "X": Morphism(name="η'_X: C→X", source="C", target="X"),
        "Y": Morphism(name="η'_Y: C→Y", source="C", target="Y")
    }

    # Verify the universal property
    is_universal = pullback.verify_universal_property(other_cone)
    print(f"Pullback satisfies universal property: {is_universal}")


if __name__ == "__main__":
    main()
