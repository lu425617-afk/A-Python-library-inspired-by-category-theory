# CategoryTheory/examples/test_symmetric_monoidal_category.py

from AbstractCategory.Morphism import Morphism
from SymmetricMonoidalCategory.SymmetricMonoidalCategory import SymmetricMonoidalCategory

def tensor_objects_func(obj1: str, obj2: str) -> str:
    """
    Defines the tensor product of two objects with proper parentheses.
    """
    if obj1 == "I":
        return obj2
    if obj2 == "I":
        return obj1
    return f"({obj1}⊗{obj2})"

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
    try:
        # Define objects of category C
        objects_C = ["I", "A", "B", "(A⊗B)", "B⊗A", "((A⊗B)⊗C)", "(A⊗(B⊗C))"]
        
        # Define morphisms of category C
        morphisms_C = [
            Morphism(name="id_I", source="I", target="I"),
            Morphism(name="id_A", source="A", target="A"),
            Morphism(name="id_B", source="B", target="B"),
            Morphism(name="id_(A⊗B)", source="(A⊗B)", target="(A⊗B)"),
            Morphism(name="id_B⊗A", source="B⊗A", target="B⊗A"),
            Morphism(name="f: A→B", source="A", target="B"),
            Morphism(name="g: B→A", source="B", target="A"),
            Morphism(name="gamma_AB: (A⊗B)→B⊗A", source="(A⊗B)", target="B⊗A"),
            Morphism(name="gamma_BA: B⊗A→(A⊗B)", source="B⊗A", target="(A⊗B)"),
            Morphism(name="alpha_A,B,C: ((A⊗B)⊗C)→(A⊗(B⊗C))", source="((A⊗B)⊗C)", target="(A⊗(B⊗C))"),
            Morphism(name="lambda_A: (I⊗A)→A", source="(I⊗A)", target="A"),
            Morphism(name="rho_A: (A⊗I)→A", source="(A⊗I)", target="A")
        ]
        
        # Define morphism associations of category C
        morphism_association_C = {
            "I": {
                "I": [morphisms_C[0]],
                "(I⊗A)": [morphisms_C[10]],
                "(I⊗B)": [morphisms_C[11]]  # Assuming the same lambda and rho for both
            },
            "A": {
                "A": [morphisms_C[1]],
                "B": [morphisms_C[5]],    # f: A→B
                "B⊗A": [morphisms_C[7]]    # gamma_AB: (A⊗B)→B⊗A
            },
            "B": {
                "A": [morphisms_C[6]],    # g: B→A
                "B": [morphisms_C[2]],
                "(A⊗B)": [morphisms_C[8]]  # gamma_BA: B⊗A→(A⊗B)
            },
            "(A⊗B)": {
                "(A⊗B)": [morphisms_C[3]],  # id_(A⊗B): (A⊗B)→(A⊗B)
                "B⊗A": [morphisms_C[7]]      # gamma_AB: (A⊗B)→B⊗A
            },
            "B⊗A": {
                "B⊗A": [morphisms_C[4]],      # id_B⊗A: B⊗A→B⊗A
                "(A⊗B)": [morphisms_C[8]]    # gamma_BA: B⊗A→(A⊗B)
            },
            "((A⊗B)⊗C)": {
                "((A⊗B)⊗C)": [morphisms_C[9]]  # alpha_A,B,C: ((A⊗B)⊗C)→(A⊗(B⊗C))
            },
            "(A⊗(B⊗C))": {
                "(A⊗(B⊗C))": [morphisms_C[9]]  # alpha_A,B,C: ((A⊗B)⊗C)→(A⊗(B⊗C))
            }
        }
        
        # Define associators
        associators = {
            ('A', 'B', 'C'): morphisms_C[9]  # alpha_A,B,C: ((A⊗B)⊗C)→(A⊗(B⊗C))
        }
        
        # Define left unitors
        left_unitors = {
            'A': morphisms_C[10],  # lambda_A: (I⊗A)→A
            'B': morphisms_C[10]   # lambda_B: (I⊗B)→B (assuming the same lambda_A used for B)
        }
        
        # Define right unitors
        right_unitors = {
            'A': morphisms_C[11],  # rho_A: (A⊗I)→A
            'B': morphisms_C[11]   # rho_B: (B⊗I)→B (assuming the same rho_A used for B)
        }
        
        # Define braidings
        braidings = {
            ('A', 'B'): morphisms_C[7],  # gamma_AB: (A⊗B)→B⊗A
            ('B', 'A'): morphisms_C[8]   # gamma_BA: B⊗A→(A⊗B)
        }
        
        # Create an instance of SymmetricMonoidalCategory
        category_C = SymmetricMonoidalCategory(
            objects=objects_C,
            morphisms=morphisms_C,
            morphism_association=morphism_association_C,
            unit_object="I",
            tensor_objects_func=tensor_objects_func,
            tensor_morphisms_func=tensor_morphisms_func,
            associators=associators,
            left_unitors=left_unitors,
            right_unitors=right_unitors,
            braidings=braidings
        )
        
        # Print category information
        print(category_C)
        
        # Compute some tensor product morphisms
        morph_f = category_C.get_morphism("f: A→B")
        morph_g = category_C.get_morphism("g: B→A")
        if morph_f and morph_g:
            tensor_morph = category_C.tensor_morphisms_pair(morph_f, morph_g)
            print(f"Tensor Morphism: {tensor_morph}")
        
        # Visualize monoidal structure
        category_C.visualize_monoidal_structure(
            filename='monoidal_structure_diagram',
            format='png'
        )
        
        # Visualize braiding morphisms
        category_C.visualize_braiding(
            filename='braiding_diagram',
            format='png'
        )
        
        # Verify identities (assuming implementation exists)
        pentagon = category_C.verify_pentagon_identity()
        triangle = category_C.verify_triangle_identity()
        print(f"Pentagon identity holds: {pentagon}")
        print(f"Triangle identity holds: {triangle}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
