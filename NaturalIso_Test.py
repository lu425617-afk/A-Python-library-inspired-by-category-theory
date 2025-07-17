from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractFunctor.IdentityFunctor import IdentityFunctor
from AbstractNaturalTransformation.NaturalIsomorphism import NaturalIsomorphism


def main():
    # Define source category C
    objects_C = ["A", "B"]
    morphisms_C = [
        Morphism(name="f", source="A", target="B"),
        Morphism(name="id_A", source="A", target="A"),
        Morphism(name="id_B", source="B", target="B")
    ]
    # Define composition rules, e.g., f ∘ id_A = f, id_B ∘ f = f, id_A ∘ id_A = id_A, id_B ∘ id_B = id_B
    morphism_association_C = {
        "A": {
            "B": [morphisms_C[0]],
            "A": [morphisms_C[1]]
        },
        "B": {
            "B": [morphisms_C[2]]
        }
    }
    category_C = AbstractCategory(
        objects=objects_C,
        morphisms=morphisms_C,
        morphism_association=morphism_association_C
    )

    # Define target category D
    objects_D = ["X", "Y"]
    morphisms_D = [
        Morphism(name="g", source="X", target="Y"),
        Morphism(name="inverse_g", source="Y", target="X"),  # Inverse morphism
        Morphism(name="id_X", source="X", target="X"),
        Morphism(name="id_Y", source="Y", target="Y")
    ]
    # Define composition rules, e.g., g ∘ inverse_g = id_X, inverse_g ∘ g = id_Y, id_X ∘ id_X = id_X, id_Y ∘ id_Y = id_Y
    morphism_association_D = {
        "X": {
            "Y": [morphisms_D[0]],
            "X": [morphisms_D[2]]
        },
        "Y": {
            "X": [morphisms_D[1]],
            "Y": [morphisms_D[3]]
        }
    }
    category_D = AbstractCategory(
        objects=objects_D,
        morphisms=morphisms_D,
        morphism_association=morphism_association_D
    )

    # Define source functor F: C → D
    object_mapping_F = {
        "A": "X",
        "B": "Y"
    }
    morphism_mapping_F = {
        "f": "g",
        "id_A": "id_X",
        "id_B": "id_Y"
    }
    functor_F = AbstractFunctor(
        source_category=category_C,
        target_category=category_D,
        object_mapping=object_mapping_F,
        morphism_mapping=morphism_mapping_F
    )

    # Define target functor G: C → D (different from F, to create different mappings for this example)
    object_mapping_G = {
        "A": "X",
        "B": "Y"
    }
    morphism_mapping_G = {
        "f": "g",
        "id_A": "id_X",
        "id_B": "id_Y"
    }
    functor_G = AbstractFunctor(
        source_category=category_C,
        target_category=category_D,
        object_mapping=object_mapping_G,
        morphism_mapping=morphism_mapping_G
    )

    # Define natural isomorphism η: F ⇒ G (identity natural transformation in this case)
    components_eta = {
        "A": "id_X",
        "B": "id_Y"
    }
    natural_isomorphism_eta = NaturalIsomorphism(
        source_functor=functor_F,
        target_functor=functor_G,
        components=components_eta
    )

    # Print natural isomorphism
    print(natural_isomorphism_eta)

    # Verify naturality condition
    is_natural = natural_isomorphism_eta.is_natural()
    print(f"Natural Isomorphism η is natural: {is_natural}")

    # Check if the natural transformation is a natural isomorphism
    is_natural_iso = natural_isomorphism_eta.is_natural_isomorphism()
    print(f"Natural Isomorphism η is a natural isomorphism: {is_natural_iso}")

    # Get the inverse natural isomorphism (if it's a natural isomorphism)
    if is_natural_iso:
        inverse_eta = natural_isomorphism_eta.inverse()
        print("Inverse Natural Transformation:")
        print(inverse_eta)

    # Visualize the natural isomorphism
    natural_isomorphism_eta.visualize(filename="natural_isomorphism_eta", highlight_failures=True)


if __name__ == "__main__":
    main()
