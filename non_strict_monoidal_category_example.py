from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractMonoidalCategory.AbstractMonoidalCategory import AbstractMonoidalCategory

def tensor_objects_func(obj1: str, obj2: str) -> str:
    """
    Defines the tensor product of two objects.
    """
    if obj1 == "I":
        return obj2
    if obj2 == "I":
        return obj1
    return f"{obj1}⊗{obj2}"

def tensor_morphisms_func(morph1: Morphism, morph2: Morphism) -> Morphism:
    """
    Defines the tensor product of two morphisms.
    """
    if morph1.name.startswith("id_") and morph2.name.startswith("id_"):
        # Tensor product of two identity morphisms is an identity morphism
        return Morphism(
            name=f"id_{tensor_objects_func(morph1.source, morph2.source)}",
            source=tensor_objects_func(morph1.source, morph2.source),
            target=tensor_objects_func(morph1.target, morph2.target)
        )
    else:
        # Tensor product of non-identity morphisms
        return Morphism(
            name=f"{morph1.name}⊗{morph2.name}",
            source=tensor_objects_func(morph1.source, morph2.source),
            target=tensor_objects_func(morph1.target, morph2.target)
        )

def main():
    # Define the category C
    objects_C = ["I", "A", "B", "A⊗B", "B⊗A", "A⊗I", "I⊗A", "(A⊗B)⊗A", "A⊗(B⊗A)"]
    
    morphisms_C = {
        "id_I": Morphism(name="id_I", source="I", target="I"),
        "id_A": Morphism(name="id_A", source="A", target="A"),
        "id_B": Morphism(name="id_B", source="B", target="B"),
        "id_A⊗B": Morphism(name="id_A⊗B", source="A⊗B", target="A⊗B"),
        "id_B⊗A": Morphism(name="id_B⊗A", source="B⊗A", target="B⊗A"),
        "f: A→B": Morphism(name="f: A→B", source="A", target="B"),
        "g: B→A": Morphism(name="g: B→A", source="B", target="A"),
        "alpha_{A,B,A}": Morphism(name="alpha_{A,B,A}: (A⊗B)⊗A→A⊗(B⊗A)", source="(A⊗B)⊗A", target="A⊗(B⊗A)"),
        "alpha_{A,B,A}^{-1}": Morphism(name="alpha_{A,B,A}^{-1}: A⊗(B⊗A)→(A⊗B)⊗A", source="A⊗(B⊗A)", target="(A⊗B)⊗A"),
        "lambda_A": Morphism(name="lambda_A: I⊗A→A", source="I⊗A", target="A"),
        "lambda_A^{-1}": Morphism(name="lambda_A^{-1}: A→I⊗A", source="A", target="I⊗A"),
        "rho_A": Morphism(name="rho_A: A⊗I→A", source="A⊗I", target="A"),
        "rho_A^{-1}": Morphism(name="rho_A^{-1}: A→A⊗I", source="A", target="A⊗I"),
        "id_A⊗I": Morphism(name="id_A⊗I", source="A⊗I", target="A⊗I"),
        "id_I⊗A": Morphism(name="id_I⊗A", source="I⊗A", target="I⊗A"),
        # Removed automatically added morphisms
        # "id_(A⊗B)⊗A": Morphism(name="id_(A⊗B)⊗A: (A⊗B)⊗A → (A⊗B)⊗A", source="(A⊗B)⊗A", target="(A⊗B)⊗A"),
        # "id_A⊗(B⊗A)": Morphism(name="id_A⊗(B⊗A): A⊗(B⊗A) → A⊗(B⊗A)", source="A⊗(B⊗A)", target="A⊗(B⊗A)"),
    }

    # Print all morphism names to verify there are no duplicates
    print("All morphism names:")
    for name, morph in morphisms_C.items():
        print(f"{name}: {morph}")

    morphism_association_C = {
        "I": {
            "I": [morphisms_C["id_I"]],
            "A": [morphisms_C["lambda_A"]],
            # If there is no morphism from I to B, it can be omitted or explicitly indicated
        },
        "A": {
            "A": [morphisms_C["id_A"]],
            "B": [morphisms_C["f: A→B"]],
            "A⊗B": [morphisms_C["g: B→A"]]
        },
        "B": {
            "B": [morphisms_C["id_B"]],
            "A": [morphisms_C["g: B→A"]],
            "B⊗A": [morphisms_C["alpha_{A,B,A}"]]
        },
        "A⊗B": {
            "A⊗B": [morphisms_C["id_A⊗B"]],
            "B⊗A": [morphisms_C["alpha_{A,B,A}"]]
        },
        "B⊗A": {
            "B⊗A": [morphisms_C["id_B⊗A"]],
            "A⊗B": [morphisms_C["alpha_{A,B,A}"]]
        },
        "(A⊗B)⊗A": {
            "(A⊗B)⊗A": [morphisms_C["alpha_{A,B,A}"]],
            "A⊗(B⊗A)": [morphisms_C["alpha_{A,B,A}^{-1}"]]
        },
        "A⊗(B⊗A)": {
            "A⊗(B⊗A)": [morphisms_C["alpha_{A,B,A}^{-1}"]],
            "(A⊗B)⊗A": [morphisms_C["alpha_{A,B,A}"]]
        },
        "I⊗A": {
            "A": [morphisms_C["lambda_A"]],
            "I⊗A": [morphisms_C["id_I⊗A"]]
        },
        "A⊗I": {
            "A": [morphisms_C["rho_A"]],
            "A⊗I": [morphisms_C["id_A⊗I"]]
        },
    }

    # Print morphism associations to verify correctness
    print("\nMorphism associations:")
    for source, targets in morphism_association_C.items():
        print(f"{source}:")
        for target, morphs in targets.items():
            morph_names = [morph.name for morph in morphs]
            print(f"  {target}: {morph_names}")

    category_C = AbstractMonoidalCategory(
        objects=objects_C,
        morphisms=list(morphisms_C.values()),  # Convert dict values to list
        morphism_association=morphism_association_C,
        unit_object="I",
        tensor_objects_func=tensor_objects_func,
        tensor_morphisms_func=tensor_morphisms_func,
        associators={
            ("A", "B", "A"): morphisms_C["alpha_{A,B,A}"],               # alpha_{A,B,A}: (A⊗B)⊗A→A⊗(B⊗A)
            ("A", "B", "A_inverse"): morphisms_C["alpha_{A,B,A}^{-1}"]  # alpha_{A,B,A}^{-1}: A⊗(B⊗A)→(A⊗B)⊗A
        },
        left_unitors={
            "A": morphisms_C["lambda_A"],  # lambda_A: I⊗A→A
            "B": morphisms_C["lambda_A"],  # lambda_B: I⊗B→B (assumed to be the same as lambda_A)
            "I": morphisms_C["id_I"]        # lambda_I: I⊗I→I
        },
        right_unitors={
            "A": morphisms_C["rho_A"],      # rho_A: A⊗I→A
            "B": morphisms_C["rho_A"],      # rho_B: B⊗I→B (assumed to be the same as rho_A)
            "I": morphisms_C["id_I"]         # rho_I: I⊗I→I
        }
    )

    # Manually add inverse associators (if necessary)
    category_C.associators[("A", "B", "A_inverse")] = morphisms_C["alpha_{A,B,A}^{-1}"]  # alpha_{A,B,A}^{-1}: A⊗(B⊗A)→(A⊗B)⊗A

    # Print category information
    print("\nCategory info:")
    print(category_C)

    # Calculate some tensor product morphisms
    morph_f = category_C.get_morphism("f: A→B")
    morph_g = category_C.get_morphism("g: B→A")
    if morph_f and morph_g:
        tensor_morph = category_C.tensor_morphisms_pair(morph_f, morph_g)
        print(f"\nTensor Morphism: {tensor_morph}")

    # Visualize the monoidal structure
    category_C.visualize_monoidal_structure()

    # Verify identities (assuming they are correctly implemented)
    category_C.verify_pentagon_identity()
    category_C.verify_triangle_identity()

if __name__ == "__main__":
    main()
