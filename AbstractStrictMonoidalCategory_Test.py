# CategoryTheory/examples/strict_monoidal_category_example.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism
from AbstractStrictMonoidalCategory.AbstractStrictMonoidalCategory import AbstractStrictMonoidalCategory

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
        return Morphism(name=f"id_{tensor_objects_func(morph1.source, morph2.source)}",
                       source=tensor_objects_func(morph1.source, morph2.source),
                       target=tensor_objects_func(morph1.target, morph2.target))
    else:
        # Tensor product of non-identity morphisms
        return Morphism(name=f"{morph1.name}⊗{morph2.name}",
                       source=tensor_objects_func(morph1.source, morph2.source),
                       target=tensor_objects_func(morph1.target, morph2.target))

def main():
    # Define category C
    objects_C = ["I", "A", "B", "A⊗B"]
    morphisms_C = [
        Morphism(name="id_I", source="I", target="I"),
        Morphism(name="id_A", source="A", target="A"),
        Morphism(name="id_B", source="B", target="B"),
        Morphism(name="id_A⊗B", source="A⊗B", target="A⊗B"),
        Morphism(name="f: A→B", source="A", target="B"),
        Morphism(name="g: B→A", source="B", target="A"),
        Morphism(name="f⊗g: A⊗B→B⊗A", source="A⊗B", target="B⊗A")  # Assume B⊗A is defined elsewhere
    ]
    morphism_association_C = {
        "I": {
            "I": [morphisms_C[0]],
            "A": [morphisms_C[4]],
            "B": [morphisms_C[5]]
        },
        "A": {
            "A": [morphisms_C[1]],
            "B": [morphisms_C[4]],
            "B⊗A": [morphisms_C[6]]
        },
        "B": {
            "A": [morphisms_C[5]],
            "B": [morphisms_C[2]],
            "A⊗B": []  # To be defined if needed
        },
        "A⊗B": {
            "A⊗B": [morphisms_C[3]],
            "B⊗A": [morphisms_C[6]]
        },
        "B⊗A": {
            "B⊗A": []  # Assuming it's defined elsewhere
        }
    }
    category_C = AbstractStrictMonoidalCategory(
        objects=objects_C,
        morphisms=morphisms_C,
        morphism_association=morphism_association_C,
        unit_object="I",
        tensor_objects_func=tensor_objects_func,
        tensor_morphisms_func=tensor_morphisms_func
    )

    # Print category information
    print(category_C)

    # Compute some tensor product morphisms
    morph_f = category_C.get_morphism("f: A→B")
    morph_g = category_C.get_morphism("g: B→A")
    if morph_f and morph_g:
        tensor_morph = category_C.tensor_morphisms_pair(morph_f, morph_g)
        print(f"Tensor Morphism: {tensor_morph}")

    # Visualize the monoidal structure of the category
    category_C.visualize_monoidal_structure()

if __name__ == "__main__":
    main()
