# AbstractFunctor_Test.py

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
        morphism_association=morphism_association_C
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
        morphism_association=morphism_association_D
    )

    # Define target category E
    objects_E = ["M", "N"]
    morphisms_E = [
        Morphism("h", "M", "N"),
        Morphism("id_M", "M", "M"),
        Morphism("id_N", "N", "N")
    ]
    morphism_association_E = {
        "M": {"M": [morphisms_E[1]], "N": [morphisms_E[0]]},
        "N": {"N": [morphisms_E[2]]}
    }
    E = AbstractCategory(
        objects=objects_E,
        morphisms=morphisms_E,
        morphism_association=morphism_association_E
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

    # Define functor G: D → E
    object_mapping_G = {
        "X": "M",
        "Y": "N"
    }
    morphism_mapping_G = {
        "g": "h",
        "id_X": "id_M",
        "id_Y": "id_N"
    }
    G = AbstractFunctor(
        source_category=D,
        target_category=E,
        object_mapping=object_mapping_G,
        morphism_mapping=morphism_mapping_G
    )

    # Print functor F and G information
    print("Functor F: C → D")
    print(F)
    print("\nFunctor G: D → E")
    print(G)

    # Validate if F and G are valid
    print("\nValidating Functor F:")
    is_valid_F = F.is_valid()
    print(f"Is Functor F valid? {is_valid_F}")

    print("\nValidating Functor G:")
    is_valid_G = G.is_valid()
    print(f"Is Functor G valid? {is_valid_G}")

    # Check functor properties
    print("\nChecking Functor F Properties:")
    print(f"Is Functor F full? {F.is_full()}")
    print(f"Is Functor F faithful? {F.is_faithful()}")
    print(f"Is Functor F full and faithful? {F.is_full_and_faithful()}")

    print("\nChecking Functor G Properties:")
    print(f"Is Functor G full? {G.is_full()}")
    print(f"Is Functor G faithful? {G.is_faithful()}")
    print(f"Is Functor G full and faithful? {G.is_full_and_faithful()}")

    # Compose functors G ∘ F
    print("\nComposing Functors G ∘ F:")
    GF = AbstractFunctor.compose(F, G)
    print(GF)

    # Validate if the composed functor is valid
    print("\nValidating Functor G ∘ F:")
    is_valid_GF = GF.is_valid()
    print(f"Is Functor G ∘ F valid? {is_valid_GF}")

    # Check properties of the composed functor
    print("\nChecking Functor G ∘ F Properties:")
    print(f"Is Functor G ∘ F full? {GF.is_full()}")
    print(f"Is Functor G ∘ F faithful? {GF.is_faithful()}")
    print(f"Is Functor G ∘ F full and faithful? {GF.is_full_and_faithful()}")

    # Get the image of the composed functor
    image_GF = GF.get_mapped_category()
    print("Image of Category C under Functor G ∘ F:")
    print(image_GF)

    # Detailed print of the image category's objects and morphisms
    print("\nDetailed Image Category:")
    print(f"Objects: {image_GF.Objects}")
    print("Morphisms:")
    for morphism in image_GF.morphisms:
        print(f"  {morphism}")

    # Create identity functor
    print("\nCreating Identity Functor for Category C:")
    Id_F = IdentityFunctor(C)
    print(Id_F)

    # Validate the identity functor
    print("\nValidating Identity Functor:")
    is_valid_Id_F = Id_F.is_valid()
    print(f"Is the identity functor valid? {is_valid_Id_F}")

    # Get the image of the identity functor
    image_Id_F = Id_F.get_mapped_category()
    print("Image of Category C under Identity Functor F:")
    print(image_Id_F)

    # Check functor equivalence
    print("\nChecking Functor Equivalence:")
    another_GF = AbstractFunctor.compose(F, G)
    print(f"Are the two compositions equal? {GF.equals(another_GF)}")

    # Check if it is an equivalence functor
    print(f"\nIs Functor G ∘ F an equivalence? {GF.is_equivalence()}")

    # Check if it is an identity functor
    print(f"\nIs Functor Id_F an identity functor? {Id_F.is_identity_functor()}")

    # Get preimage morphisms
    print("\nGetting preimage morphisms for 'h' in E:")
    preimages_h = GF.get_preimage_morphisms("h")
    for pre_m in preimages_h:
        print(f"  {pre_m}")

    # Create natural transformation η: F ⇒ G ∘ F
    print("\nCreating Natural Transformation η: F ⇒ G ∘ F")
    components_eta = {
        "A": "id_M",  # η_A: F(A) = M → G(F(A)) = M
        "B": "id_N"   # η_B: F(B) = N → G(F(B)) = N
    }
    eta = AbstractNaturalTransformation(F, GF, components_eta)
    print(eta)

    # Validate naturality condition for the natural transformation
    print("\nValidating Natural Transformation η:")
    is_natural = eta.is_natural()
    print(f"Is Natural Transformation η natural? {is_natural}")

    # Try an invalid natural transformation
    print("\nCreating Invalid Natural Transformation η': F ⇒ G ∘ F")
    components_eta_invalid = {
        "A": "id_M",
        "B": "h"  # Incorrect mapping, should be "id_N"
    }
    eta_invalid = AbstractNaturalTransformation(F, GF, components_eta_invalid)
    print(eta_invalid)

    print("\nValidating Invalid Natural Transformation η':")
    is_natural_invalid = eta_invalid.is_natural()
    print(f"Is Natural Transformation η' natural? {is_natural_invalid}")

if __name__ == "__main__":
    example_functor()
