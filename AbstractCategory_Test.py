# CategoryTheory/AbstractCategory_Test.py

from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism

def test_discrete_category():
    print("\n--- Testing Discrete Category ---")
    objects = ["X", "Y", "Z"]
    morphisms = []  # A discrete category only contains identity morphisms
    morphism_association = {
        "X": {"X": []},
        "Y": {"Y": []},
        "Z": {"Z": []}
    }
    C = AbstractCategory(
        objects=objects,
        morphisms=morphisms,
        morphism_association=morphism_association
    )
    # Add identity morphisms
    for obj in objects:
        C.identity(obj)
    
    print("Objects:", C.Objects)
    print("Morphism Count:", C.MorphismCount)
    print("Initial Objects:", C.initial_objects())
    print("Terminal Objects:", C.terminal_objects())
    print("Zero Objects:", C.zero_objects())
    morphism_tests = C.test_morphisms()
    print("Morphism Tests:", morphism_tests)
    print("Are X and Y isomorphic?", C.are_isomorphic("X", "Y"))


def test_group_as_category():
    print("\n--- Testing Group as a Category ---")
    objects = ["*"]
    morphisms = [
        Morphism("a", "*", "*"),
        Morphism("a_inv", "*", "*"),
        Morphism("id_*", "*", "*")
    ]
    morphism_association = {
        "*": {
            "*": morphisms
        }
    }
    morphism_equiv_rel = {"a": "a_inv", "a_inv": "a", "id_*": "id_*"}
    object_equivalences = {}
    
    C = AbstractCategory(
        objects=objects,
        morphisms=morphisms,
        morphism_association=morphism_association,
        object_equivalences=object_equivalences,
        morphism_equivalences=morphism_equiv_rel  # Fixed
    )
    
    # Add identity morphisms (already included in morphisms)
    
    print("Objects:", C.Objects)
    print("Morphism Count:", C.MorphismCount)
    print("Initial Objects:", C.initial_objects())
    print("Terminal Objects:", C.terminal_objects())
    print("Zero Objects:", C.zero_objects())
    morphism_tests = C.test_morphisms()
    print("Morphism Tests:", morphism_tests)
    print("Are * and * isomorphic?", C.are_isomorphic("*", "*"))
    
    # Composition of morphisms tests
    try:
        composition1 = C.compose(morphisms[0], morphisms[1])  # a ∘ a_inv
        print("Composition of a and a_inv:", composition1)
        composition2 = C.compose(morphisms[1], morphisms[0])  # a_inv ∘ a
        print("Composition of a_inv and a:", composition2)
    except ValueError as e:
        print("Composition Error:", e)

def test_poset_category():
    print("\n--- Testing Poset Category ---")
    objects = ["a", "b", "c"]
    morphisms = [
        Morphism("f", "a", "b"),
        Morphism("g", "b", "c"),
        Morphism("h", "a", "c"),
        Morphism("id_a", "a", "a"),
        Morphism("id_b", "b", "b"),
        Morphism("id_c", "c", "c")
    ]
    morphism_association = {
        "a": {"a": [morphisms[3]], "b": [morphisms[0]], "c": [morphisms[2]]},
        "b": {"b": [morphisms[4]], "c": [morphisms[1]]},
        "c": {"c": [morphisms[5]]}
    }
    object_equivalences = {}
    morphism_equiv_rel = {}
    
    C = AbstractCategory(
        objects=objects,
        morphisms=morphisms,
        morphism_association=morphism_association,
        object_equivalences=object_equivalences,  # Fixed
        morphism_equivalences=morphism_equiv_rel  # Fixed
    )
    
    print("Objects:", C.Objects)
    print("Morphism Count:", C.MorphismCount)
    print("Initial Objects:", C.initial_objects())
    print("Terminal Objects:", C.terminal_objects())
    print("Zero Objects:", C.zero_objects())
    morphism_tests = C.test_morphisms()
    print("Morphism Tests:", morphism_tests)
    print("Are a and b isomorphic?", C.are_isomorphic("a", "b"))

def test_power_set_category():
    print("\n--- Testing Power Set Category ---")
    # Define sets
    A = set()
    B = {"a"}
    C_set = {"b"}
    D = {"a", "b"}
    
    # Objects are the power set of the sets
    objects = [
        str(frozenset(A)),
        str(frozenset(B)),
        str(frozenset(C_set)),
        str(frozenset(D))
    ]
    
    # Define morphisms as inclusion relations (only non-identity morphisms)
    morphisms = [
        Morphism("f_a", str(frozenset()), str(frozenset({"a"}))),
        Morphism("f_b", str(frozenset()), str(frozenset({"b"}))),
        Morphism("f_ab", str(frozenset()), str(frozenset({"a", "b"}))),
        Morphism("g_a", str(frozenset({"a"})), str(frozenset())),
        Morphism("g_b", str(frozenset({"b"})), str(frozenset()))
    ]
    
    morphism_association = {
        str(frozenset()): {
            str(frozenset({"a"})): [morphisms[0]],
            str(frozenset({"b"})): [morphisms[1]],
            str(frozenset({"a", "b"})): [morphisms[2]]
        },
        str(frozenset({"a"})): {
            str(frozenset()): [morphisms[3]]
        },
        str(frozenset({"b"})): {
            str(frozenset()): [morphisms[4]]
        },
        str(frozenset({"a", "b"})): {
            str(frozenset({"a", "b"})): []  # Identity morphism added later via C.identity(obj)
        }
    }
    
    object_equivalences = {}
    morphism_equiv_rel = {}
    
    C = AbstractCategory(
        objects=objects,
        morphisms=morphisms,
        morphism_association=morphism_association,
        object_equivalences=object_equivalences,  # Fixed
        morphism_equivalences=morphism_equiv_rel  # Fixed
    )
    
    # Add identity morphisms
    for obj in objects:
        C.identity(obj)
    
    print("Objects:", C.Objects)
    print("Morphism Count:", C.MorphismCount)
    print("Initial Objects:", C.initial_objects())
    print("Terminal Objects:", C.terminal_objects())
    print("Zero Objects:", C.zero_objects())
    morphism_tests = C.test_morphisms()
    print("Morphism Tests:", morphism_tests)
    print("Are frozenset({'a'}) and frozenset({'b'}) isomorphic?", C.are_isomorphic(str(frozenset({"a"})), str(frozenset({"b"}))))

def test_subcategory():
    print("\n--- Testing Subcategory ---")
    objects = ["A", "B", "C"]
    morphisms = [
        Morphism("f", "A", "B"),
        Morphism("g", "B", "C"),
        Morphism("h", "A", "C"),
        Morphism("id_A", "A", "A"),
        Morphism("id_B", "B", "B"),
        Morphism("id_C", "C", "C")
    ]
    morphism_association = {
        "A": {"A": [morphisms[3]], "B": [morphisms[0]], "C": [morphisms[2]]},
        "B": {"B": [morphisms[4]], "C": [morphisms[1]]},
        "C": {"C": [morphisms[5]]}
    }
    object_equivalences = {}
    morphism_equiv_rel = {}
    
    C = AbstractCategory(
        objects=objects,
        morphisms=morphisms,
        morphism_association=morphism_association,
        object_equivalences=object_equivalences,
        morphism_equivalences=morphism_equiv_rel  # Fixed
    )
    
    # Define subcategory objects and morphisms
    sub_objects = ["A", "B", "C"]
    sub_morphisms = [morphisms[0], morphisms[1], morphisms[3], morphisms[4], morphisms[5]]
    
    sub_C = C.subcategory(sub_objects=sub_objects, sub_morphisms=sub_morphisms)
    
    print("Subcategory Objects:", sub_C.Objects)
    print("Subcategory Morphism Count:", sub_C.MorphismCount)
    morphism_tests = sub_C.test_morphisms()
    print("Subcategory Morphism Tests:", morphism_tests)
    print("Are A and B isomorphic?", sub_C.are_isomorphic("A", "B"))

def test_quotient_category():
    print("\n--- Test Quetient category（Quotient Category） ---")
    objects = ["A", "B", "C"]
    morphisms = [
        Morphism("f", "A", "B"),
        Morphism("g", "B", "C"),
        Morphism("h", "A", "C"),
        Morphism("id_A", "A", "A"),
        Morphism("id_B", "B", "B"),
        Morphism("id_C", "C", "C")
    ]
    morphism_association = {
        "A": {"A": [morphisms[3]], "B": [morphisms[0]], "C": [morphisms[2]]},
        "B": {"B": [morphisms[4]], "C": [morphisms[1]]},
        "C": {"C": [morphisms[5]]}
    }
    #define：B ≡ A
    object_equiv_rel = {"B": "A", "A": "A", "C": "C"}
    # define：f ≡ g
    morphism_equiv_rel = {"f": "g", "g": "f", "h": "h", "id_A": "id_A", "id_B": "id_A", "id_C": "id_C"}
    
    C = AbstractCategory(
        objects=objects,
        morphisms=morphisms,
        morphism_association=morphism_association,
        object_equivalences={},  
        morphism_equivalences={}  
    )
    

    

    quotient_C = C.quotient_category(object_equiv_rel=object_equiv_rel, morphism_equiv_rel=morphism_equiv_rel)
    
    print("Quotient Category Objects:", quotient_C.Objects)
    print("Quotient Category Morphism Count:", quotient_C.MorphismCount)
    morphism_tests = quotient_C.test_morphisms()
    print("Quotient Category Morphism Tests:", morphism_tests)
    print("Are A and C isomorphic in Quotient Category?", quotient_C.are_isomorphic("A", "C"))

def test_dual_category():
    print("\n--- Test Dual Category（Dual Category） ---")
    objects = ["X", "Y"]
    morphisms = [
        Morphism("f", "X", "Y"),
        Morphism("g", "Y", "X"),
        Morphism("id_X", "X", "X"),
        Morphism("id_Y", "Y", "Y")
    ]
    morphism_association = {
        "X": {"X": [morphisms[2]], "Y": [morphisms[0]]},
        "Y": {"Y": [morphisms[3]], "X": [morphisms[1]]}
    }
    morphism_equiv_rel = {"f": "g", "g": "f", "id_X": "id_X", "id_Y": "id_Y"}
    
    C = AbstractCategory(
        objects=objects,
        morphisms=morphisms,
        morphism_association=morphism_association,
        object_equivalences={},  
        morphism_equivalences=morphism_equiv_rel  
    )
    
    
    
   
    dual_C = C.dual_category()
    
    print("Dual Category Objects:", dual_C.Objects)
    print("Dual Category Morphism Count:", dual_C.MorphismCount)
    morphism_tests = dual_C.test_morphisms()
    print("Dual Category Morphism Tests:", morphism_tests)
    print("Are X and Y isomorphic in Dual Category?", dual_C.are_isomorphic("X", "Y"))
    
   
    try:
        composition1 = dual_C.compose(dual_C.morphisms[0], dual_C.morphisms[1])  # f ∘ g: Y → Y
        print("Composition of f and g:", composition1)
        composition2 = dual_C.compose(dual_C.morphisms[1], dual_C.morphisms[0])  # g ∘ f: X → X
        print("Composition of g and f:", composition2)
    except ValueError as e:
        print("Composition Error:", e)

def main():
    test_discrete_category()
    test_group_as_category()
    test_poset_category()
    test_power_set_category()
    test_subcategory()
    test_quotient_category()
    test_dual_category()

if __name__ == "__main__":
    main()
