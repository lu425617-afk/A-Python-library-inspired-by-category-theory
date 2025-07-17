# AbstractFunctor_Test.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractFunctor.IdentityFunctor import IdentityFunctor
from AbstractNaturalTransformation.AbstractNaturalTransformation import AbstractNaturalTransformation

def example_functor():
    # Define source category C
    objects_C = ["A", "B"]
    morphisms_C = [
        Morphism("f", "A", "B"),
        Morphism("id_A", "A", "A"),
        Morphism("id_B", "B", "B")
    ]
    morphism_association_C = {
        "A": {"A": [morphisms_C[1]], "B": [morphisms_C[0]]},
        "B": {"B": [morphisms_C[2]]}
    }
    C = AbstractCategory(
        objects=objects_C,
        morphisms=morphisms_C,
        morphism_association=morphism_association_C,
        morphism_equivalences={"id_A": "id_A", "id_B": "id_B"}  # Identity morphisms are their own inverses
    )

    # Define target category D
    objects_D = ["X", "Y"]
    morphisms_D = [
        Morphism("g", "X", "Y"),
        Morphism("id_X", "X", "X"),
        Morphism("id_Y", "Y", "Y")
    ]
    morphism_association_D = {
        "X": {"X": [morphisms_D[1]], "Y": [morphisms_D[0]]},
        "Y": {"Y": [morphisms_D[2]]}
    }
    D = AbstractCategory(
        objects=objects_D,
        morphisms=morphisms_D,
        morphism_association=morphism_association_D,
        morphism_equivalences={"g": "g", "id_X": "id_X", "id_Y": "id_Y"}  # Assume g is an isomorphism with its own inverse
    )

    # Define functor F: C → D
    object_mapping_F = {
        "A": "X",
        "B": "Y"
    }
    morphism_mapping_F = {
        "f": "g",
        "id_A": "id_X",
        "id_B": "id_Y"
    }
    F = AbstractFunctor(
        source_category=C,
        target_category=D,
        object_mapping=object_mapping_F,
        morphism_mapping=morphism_mapping_F
    )

    # Print Functor F information
    print("Functor F: C → D")
    print(F)

    # Validate if Functor F is valid
    print("\nValidating Functor F:")
    is_valid_F = F.is_valid()
    print(f"Is Functor F valid? {is_valid_F}")

    # Check the properties of the functor
    print("\nChecking Functor F Properties:")
    print(f"Is Functor F full? {F.is_full()}")
    print(f"Is Functor F faithful? {F.is_faithful()}")
    print(f"Is Functor F full and faithful? {F.is_full_and_faithful()}")

    # Create a natural transformation η: F ⇒ F (Identity Natural Transformation)
    print("\nCreating Natural Transformation η: F ⇒ F (Identity Natural Transformation)")
    components_eta = {
        "A": "id_X",
        "B": "id_Y"
    }
    eta = AbstractNaturalTransformation(F, F, components_eta)
    print(eta)

    # Validate the naturality condition of the natural transformation
    print("\nValidating Natural Transformation η:")
    is_natural = eta.is_natural()
    print(f"Is Natural Transformation η natural? {is_natural}")

    # Check if the natural transformation is a natural isomorphism
    print("\nChecking if Natural Transformation η is a natural isomorphism:")
    is_natural_iso = eta.is_natural_isomorphism()
    print(f"Is Natural Transformation η a natural isomorphism? {is_natural_iso}")

    # Try to get the inverse of the natural transformation
    if is_natural_iso:
        print("\nConstructing Inverse Natural Transformation η^{-1}: F ⇒ F")
        eta_inv = eta.inverse()
        print(eta_inv)

        # Validate the naturality of the inverse natural transformation
        print("\nValidating Inverse Natural Transformation η^{-1}:")
        is_natural_inv = eta_inv.is_natural()
        print(f"Is Inverse Natural Transformation η^{-1} natural? {is_natural_inv}")
    else:
        print("Natural Transformation η is not a natural isomorphism; inverse cannot be constructed.")

    # Visualize the natural transformation
    print("\nVisualizing Natural Transformation η:")
    eta.visualize("NaturalTransformation_eta")

if __name__ == "__main__":
    example_functor()
