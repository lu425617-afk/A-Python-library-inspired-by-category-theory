# CategoryTheory/AbstractCategory/AbstractCategory.py

from typing import List, Dict, Tuple, Optional, Set, Union
from .Quiver import Quiver
from .Morphism import Morphism

def count_elements(collection: Union[List, Tuple, Dict]) -> int:
    """Calculate the number of elements in a collection """
    if isinstance(collection, (list, tuple)):
        return len(collection)
    elif isinstance(collection, dict):
        return len(collection.keys())
    return 0

class AbstractCategory:
    """Represents an abstract category, including objects, morphisms, and their relationships"""

    def __init__(self,
                 objects: List[str],
                 morphisms: List[Morphism],
                 morphism_association: Dict[str, Dict[str, List[Morphism]]],
                 object_equivalences: Optional[Dict[str, str]] = None,
                 morphism_equivalences: Optional[Dict[str, str]] = None,
                 compositions: Optional[Dict[Tuple[str, str], str]] = None):
                
        """
        
        Initialize an AbstractCategory instance.

        :param objects: List of objects in the category.
        :param morphisms: List of morphisms in the category (excluding identity morphisms).
        :param morphism_association: Morphism association, indicating the mapping of morphisms from source objects to target objects.
        :param object_equivalences: Equivalence relations of objects.
        :param morphism_equivalences: Equivalence relations of morphisms.
        :param compositions: User-defined morphism compositions.
        """
        self.quiver = Quiver(objects, morphism_association)
        self.objects = objects.copy()  # Copy the list to avoid modifying the original list
        self.morphisms = morphisms.copy()  # Copy the list to avoid modifying the original list
        self.morphism_association = {src: {tgt: morphs.copy() for tgt, morphs in targets.items()} 
                                     for src, targets in morphism_association.items()}
        self.object_equivalences = object_equivalences.copy() if object_equivalences else {}
        self.morphism_equivalences = morphism_equivalences.copy() if morphism_equivalences else {}
        self.identity_morphisms = {obj: Morphism(f"id_{obj}", obj, obj) for obj in self.objects}
        self.compositions = compositions.copy() if compositions else {}

        # Add identity morphisms to the association and append them to the morphisms list (to avoid duplicates)
        for obj in self.objects:
            if obj not in self.morphism_association:
                self.morphism_association[obj] = {}
            if obj not in self.morphism_association[obj]:
                self.morphism_association[obj][obj] = []
            identity = self.identity_morphisms[obj]
            # Check if the identity morphism already exists
            if not any(morph.name == identity.name for morph in self.morphism_association[obj][obj]):
                self.morphism_association[obj][obj].append(identity)
                self.morphisms.append(identity)  # Only add it if not already added
            # Ensure the identity morphism maps to itself
            # Ensure the identity morphism maps to itself
            self.morphism_equivalences[identity.name] = identity.name

    def are_equivalent(self, element1: str, element2: str, equivalence_type: str = 'morphism') -> bool:
        """
        Check if two elements (objects or morphisms) are equivalent.

        :param element1: The first element (object or morphism).
        :param element2: The second element (object or morphism).
        :param equivalence_type: "object" or "morphism", to specify the type to check.
        :return: True if equivalent, False otherwise.
        """
        if element1 == element2:
            return True

        equivalences = (
            self.object_equivalences if equivalence_type == 'object' else self.morphism_equivalences
        )

        return (element2 in equivalences.get(element1, [])) or (element1 in equivalences.get(element2, []))

    @property
    def Objects(self) -> List[str]:
        """Return the list of objects in the category."""
        return self.quiver.objects

    @property
    def ObjectCount(self) -> int:
        """Return the number of objects."""
        return count_elements(self.quiver.objects)

    @property
    def MorphismAssociation(self) -> Set[str]:
        """Return all morphism associations, formatted as 'morphism: source → target'."""
        return {f"{morph.name}: {morph.source} → {morph.target}"
                for src, targets in self.quiver.morphism_association.items()
                for tgt, morphs in targets.items()
                for morph in morphs}

    @property
    def MorphismNames(self) -> List[str]:
        """Return the names of all morphisms."""
        return [morph.name for morph in self.morphisms]

    @property
    def MorphismCount(self) -> int:
        """Return the number of morphisms."""
        return count_elements(self.morphisms)

    @property
    def IdentityMorphisms(self) -> Dict[str, Morphism]:
        """Return all identity morphisms for the objects."""
       
        return self.identity_morphisms

    @property
    def ObjectEquivalenceCount(self) -> int:
        """Count the number of object equivalence relations."""
        return len(self.object_equivalences)

    @property
    def MorphismEquivalenceCount(self) -> int:
        """Count the number of morphism equivalence relations."""
        return len(self.morphism_equivalences)

    def Hom(self, obj1: str, obj2: str) -> List[Morphism]:
        """
        Return all morphisms from object obj1 to obj2.

        :param obj1: Source object.
        :param obj2: Target object.
        :return: List of morphisms.
        """
        return self.morphism_association.get(obj1, {}).get(obj2, [])

    def identity(self, obj: str) -> Morphism:
        """返回给定对象的恒等态射。"""
        return self.identity_morphisms[obj]

    def get_identity(self, obj: str) -> Optional[Morphism]:
        """
        Retrieve the identity morphism for the given object.
        
        :param obj: The object whose identity morphism is to be retrieved.
        :return: The identity morphism if found, else None.
        """
        identity_name = f"id_{obj}"
        for morphism in self.morphisms:
            if morphism.name == identity_name and morphism.source == obj and morphism.target == obj:
                return morphism
        print(f"No identity morphism found for object {obj}.")
        return None

    def get_morphism(self, name: str) -> Optional[Morphism]:
        """
        Retrieve a morphism by its name.
        
        :param name: The name of the morphism.
        :return: The morphism if found, else None.
        """
        for morphism in self.morphisms:
            if morphism.name == name:
                return morphism
        print(f"Morphism {name} not found in category.")
        return None

    def identity(self, obj: str) -> Morphism:
        """Return the identity morphism for the given object."""
        return self.identity_morphisms[obj]

    def get_identity(self, obj: str) -> Optional[Morphism]:
        """
        Retrieve the identity morphism for the given object.
        
        :param obj: The object whose identity morphism is to be retrieved.
        :return: The identity morphism if found, else None.
        """
        identity_name = f"id_{obj}"
        for morphism in self.morphisms:
            if morphism.name == identity_name and morphism.source == obj and morphism.target == obj:
                return morphism
        print(f"No identity morphism found for object {obj}.")
        return None

    def get_morphism(self, name: str) -> Optional[Morphism]:
        """
        Retrieve a morphism by its name.
        
        :param name: The name of the morphism.
        :return: The morphism if found, else None.
        """
        for morphism in self.morphisms:
            if morphism.name == name:
                return morphism
        print(f"Morphism {name} not found in category.")
        return None

    def has_path(self, start: str, end: str, visited: Optional[Set[str]] = None) -> bool:
        """Check if there is a path from start to end."""
        if visited is None:
            visited = set()
        if start == end:
            return True
        if start in visited:
            return False
        visited.add(start)
        for morph in self.Hom(start, end):
            if self.has_path(morph.target, end, visited):
                return True
        for morph in self.morphisms:
            if morph.source == start and morph.target not in visited:
                if self.has_path(morph.target, end, visited):
                    return True
        return False

    def initial_objects(self) -> List[str]:
        """Return all initial objects."""
        initial_objs = []
        for obj in self.objects:
            # Initial objects do not have any morphisms coming into them
            incoming = any(
                morph.target == obj for src, targets in self.morphism_association.items()
                for morphs in targets.values() for morph in morphs if morph.source != obj
            )
            if not incoming:
                initial_objs.append(obj)
        return initial_objs

    def terminal_objects(self) -> List[str]:
        """Return all terminal objects."""
        terminal_objs = []
        for obj in self.objects:
            # Terminal objects do not have any morphisms going out of them
            outgoing = any(
                morph.source == obj for morphs in self.morphism_association.get(obj, {}).values()
                for morph in morphs if morph.target != obj
            )
            if not outgoing:
                terminal_objs.append(obj)
        return terminal_objs


    def zero_objects(self) -> List[str]:
        """Return all zero objects."""
        initial_objs = self.initial_objects()
        terminal_objs = self.terminal_objects()
        zero_objs = [obj for obj in initial_objs if obj in terminal_objs]
        return zero_objs

    def __str__(self):
        morphism_details = "\n  Morphisms:"
        for morphism in self.morphisms:
            morphism_details += f"\n    {morphism}"
        return f"AbstractCategory(\n  Objects: {self.Objects},\n  MorphismCount: {self.MorphismCount}{morphism_details}\n)"

    def Hom_cached(self, obj1: str, obj2: str) -> Tuple[str, ...]:
        """
        Cache the result of the Hom set to improve performance.

        :param obj1: Source object.
        :param obj2: Target object.
        :return: Tuple of morphism names.
        """
        print(f"Fetching Hom({obj1}, {obj2})")
        morphs = self.morphism_association.get(obj1, {}).get(obj2, [])
        return tuple(morph.name for morph in morphs)

    def Hom_names(self, obj1: str, obj2: str) -> Tuple[str, ...]:
        """
        Return the names of the morphisms in the Hom set.

        :param obj1: Source object.
        :param obj2: Target object.
        :return: Tuple of morphism names.
        """
        return self.Hom_cached(obj1, obj2)

    def is_isomorphism(self, morph: Morphism) -> bool:
        """Check if the morphism is an isomorphism (bijective)."""
        print(f"Checking if morphism {morph.name} is an isomorphism")
        inverse_name = self.morphism_equivalences.get(morph.name)
        if not inverse_name:
            print(f"Morphism {morph.name} has no inverse.")
            return False
        inverse = next((m for m in self.morphisms if m.name == inverse_name), None)
        if not inverse:
            print(f"Inverse morphism {inverse_name} for {morph.name} not found.")
            return False
        # Check if they are mutual inverses
        if self.morphism_equivalences.get(inverse.name) == morph.name:
            print(f"Morphisms {morph.name} and {inverse.name} are inverses.")
            return True
        else:
            print(f"Morphisms {morph.name} and {inverse.name} are not inverses.")
            return False

    def is_monomorphism(self, morph: Morphism) -> bool:
        """Check if the morphism is a monomorphism (injective)."""
        # The actual implementation depends on the definition of the category
        # Here we provide a simple placeholder implementation
        print(f"Checking if morphism {morph.name} is a monomorphism")
        return True

    def is_epimorphism(self, morph: Morphism) -> bool:
        """Check if the morphism is an epimorphism (surjective)."""
        # The actual implementation depends on the definition of the category
        # Here we provide a simple placeholder implementation
        print(f"Checking if morphism {morph.name} is an epimorphism")
        return True

    def is_bimorphism(self, morph: Morphism) -> bool:
        """Check if the morphism is a bimorphism (both monomorphism and epimorphism)."""
        print(f"Checking if morphism {morph.name} is a bimorphism")
        return self.is_monomorphism(morph) and self.is_epimorphism(morph)

    def compose_morphisms(self, morphism_sequence: List[Tuple[Morphism, str, str]]) -> Optional[Tuple[str, str, str]]:
        """
        Compose a sequence of morphisms and return the result of the composition.

        :param morphism_sequence: A sequence of morphisms in the format [(morph1, X, Y), (morph2, Y, Z)].
        :return: A tuple (composed name, source object, target object) or None.
        """
        try:
            if not morphism_sequence:
                raise ValueError("The morphism sequence cannot be empty.")

            composed_name = []
            src_object = morphism_sequence[0][1]
            tgt_object = morphism_sequence[-1][2]

            for i in range(len(morphism_sequence) - 1):
                current_morph, _, current_target = morphism_sequence[i]
                next_morph, next_source, _ = morphism_sequence[i + 1]

                if current_target != next_source:
                    raise ValueError(f"Cannot compose: the target of {current_morph.name} is not equal to the source of {next_morph.name}")

                composed_name.append(current_morph.name)

            composed_name.append(morphism_sequence[-1][0].name)

            predefined_composition = self.compositions.get((src_object, tgt_object))
            if predefined_composition:
                combined_name = predefined_composition
            else:
                combined_name = " ∘ ".join(composed_name)

            return (combined_name, src_object, tgt_object)

        except Exception as e:
            raise ValueError(f"Composition error: {e}")

    def compose(self, morph1: Morphism, morph2: Morphism, add_if_missing: bool = True) -> Morphism:
        """
        Compose two morphisms.

        :param morph1: The first morphism.
        :param morph2: The second morphism.
        :param add_if_missing: Whether to add the new composition morphism if it doesn't already exist.
        :return: The composed morphism.
        """
        print(f"Attempting to compose {morph1.name} and {morph2.name}")

        # Get identity morphisms
        id_morph1 = self.identity(morph1.source)
        id_morph2 = self.identity(morph2.target)

        # If morph1 is the identity morphism for morph2's source, return morph2
        if morph1.name == id_morph1.name:
            print(f"{morph1.name} is the identity on {morph1.source}, returning {morph2.name}")
            return morph2

        # If morph2 is the identity morphism for morph1's target, return morph1
        if morph2.name == id_morph2.name:
            print(f"{morph2.name} is the identity on {morph2.target}, returning {morph1.name}")
            return morph1

        # Check if the source and target match
        if morph1.target != morph2.source:
            print(f"Cannot compose {morph1.name} with {morph2.name}: target of {morph1.name} != source of {morph2.name}")
            raise ValueError(f"Cannot compose morphism {morph1.name} with {morph2.name}")

        # Find existing composition morphisms
        possible_morphisms = self.morphism_association.get(morph1.source, {}).get(morph2.target, [])
        for morph in possible_morphisms:
            if morph.name == f"{morph1.name} ∘ {morph2.name}":
                print(f"Found existing composition: {morph.name}")
                return morph

        if add_if_missing:
            # If no explicit composition is found, define a new composition morphism
            composed_name = f"{morph1.name} ∘ {morph2.name}"
            print(f"Creating new composition morphism: {composed_name}")
            new_morph = Morphism(composed_name, morph1.source, morph2.target)
            self.morphism_association[morph1.source][morph2.target].append(new_morph)
            self.morphisms.append(new_morph)
            return new_morph
        else:
            print(f"No composition found for {morph1.name} ∘ {morph2.name} and not adding new morphism.")
            raise ValueError(f"No composition found for {morph1.name} ∘ {morph2.name}")
    
    def is_inverse(self, morph1: Morphism, morph2: Morphism) -> bool:
        """
        Check if two morphisms are inverses of each other.

        :param morph1: The first morphism.
        :param morph2: The second morphism.
        :return: True if they are inverses, False otherwise.
        """
        return (morph1.source == morph2.target and
                morph1.target == morph2.source and
                self.morphism_equivalences.get(morph1.name) == morph2.name and
                self.morphism_equivalences.get(morph2.name) == morph1.name)

    def test_morphisms(self) -> List[Dict[str, Union[str, bool]]]:
        """Test the properties (monomorphism, epimorphism, isomorphism, bimorphism) of all morphisms."""
        results = []
        for morph in self.morphisms:
            results.append({
                "morphism": morph.name,
                "is_monomorphism": self.is_monomorphism(morph),
                "is_epimorphism": self.is_epimorphism(morph),
                "is_isomorphism": self.is_isomorphism(morph),
                "is_bimorphism": self.is_bimorphism(morph)
            })
        return results

    def are_isomorphic(self, obj1: str, obj2: str) -> bool:
        """
        Check if two objects are isomorphic, including identity isomorphisms.

        :param obj1: The first object.
        :param obj2: The second object.
        :return: True if they are isomorphic, False otherwise.
        """
        print(f"Checking if objects {obj1} and {obj2} are isomorphic.")
        morphisms1 = self.morphism_association.get(obj1, {}).get(obj2, [])
        morphisms2 = self.morphism_association.get(obj2, {}).get(obj1, [])

        for morph1 in morphisms1:
            for morph2 in morphisms2:
                print(f"Trying morphism pair: {morph1.name}, {morph2.name}")
                try:
                    # Check if morph1 ∘ morph2 is id_obj2
                    comp1 = self.compose(morph2, morph1, add_if_missing=False)
                    print(f"Composition {morph2.name} ∘ {morph1.name} = {comp1.name}")
                    # Check if morph2 ∘ morph1 is id_obj1
                    comp2 = self.compose(morph1, morph2, add_if_missing=False)
                    print(f"Composition {morph1.name} ∘ {morph2.name} = {comp2.name}")
                    if comp1.name == f"id_{obj2}" and comp2.name == f"id_{obj1}":
                        print(f"Objects {obj1} and {obj2} are isomorphic via {morph1.name} and {morph2.name}.")
                        return True
                except ValueError as e:
                    print(f"Composition failed: {e}")
                    continue
        print(f"Objects {obj1} and {obj2} are not isomorphic.")
        return False

    def dual_category(self) -> 'AbstractCategory':
        """
        Create the dual category of the current category.

        :return: An AbstractCategory instance representing the dual category.
        """
        dual_morphism_association = {}
        dual_morphisms = []
        dual_morphism_equivalences = {}

        for morph in self.morphisms:
            dual_morph = Morphism(morph.name, morph.target, morph.source)
            dual_morphisms.append(dual_morph)
            if dual_morph.target not in dual_morphism_association:
                dual_morphism_association[dual_morph.target] = {}
            if dual_morph.source not in dual_morphism_association[dual_morph.target]:
                dual_morphism_association[dual_morph.target][dual_morph.source] = []
            dual_morphism_association[dual_morph.target][dual_morph.source].append(dual_morph)
            dual_morphism_equivalences[dual_morph.name] = dual_morph.name

        dual_category = AbstractCategory(
            objects=self.objects.copy(),
            morphisms=dual_morphisms.copy(),
            morphism_association=dual_morphism_association.copy(),
            object_equivalences=self.object_equivalences.copy(),
            morphism_equivalences=dual_morphism_equivalences.copy(),
            compositions=self.compositions.copy()
        )
        return dual_category

    def subcategory(self, sub_objects: List[str], sub_morphisms: List[Morphism]) -> 'AbstractCategory':
        """
        Create a subcategory consisting of the specified objects and morphisms.

        :param sub_objects: List of objects in the subcategory.
        :param sub_morphisms: List of morphisms in the subcategory.
        :return: An AbstractCategory instance representing the subcategory.
        """
        sub_morphism_association = {}
        for morph in sub_morphisms:
            src, dst = morph.source, morph.target
            if src in sub_objects and dst in sub_objects:
                if src not in sub_morphism_association:
                    sub_morphism_association[src] = {}
                if dst not in sub_morphism_association[src]:
                    sub_morphism_association[src][dst] = []
                sub_morphism_association[src][dst].append(morph)

        # Add identity morphisms
        for obj in sub_objects:
            identity = Morphism(f"id_{obj}", obj, obj)
            if obj not in sub_morphism_association:
                sub_morphism_association[obj] = {}
            if obj not in sub_morphism_association[obj]:
                sub_morphism_association[obj][obj] = []
            if not any(m.name == identity.name for m in sub_morphism_association[obj][obj]):
                sub_morphism_association[obj][obj].append(identity)

        # Subcategory morphism list includes the specified morphisms and identity morphisms
        sub_morphisms_with_id = sub_morphisms.copy()
        for obj in sub_objects:
            identity = self.identity(obj)
            if identity not in sub_morphisms_with_id:
                sub_morphisms_with_id.append(identity)

        return AbstractCategory(
            objects=sub_objects.copy(),
            morphisms=sub_morphisms_with_id.copy(),
            morphism_association=sub_morphism_association.copy(),
            object_equivalences=self.object_equivalences.copy(),
            morphism_equivalences=self.morphism_equivalences.copy(),
            compositions=self.compositions.copy()
        )

    def _reduce_equivalences(self, elements: List[str], equivalences: Dict[str, str]) -> List[str]:
        """
        Simplify a set of objects or morphisms by removing duplicates based on equivalence relations.

        :param elements: A list of elements.
        :param equivalences: A dictionary of equivalence relations.
        :return: A simplified list of elements.
        """
        reduced_elements = []
        seen = set()
        for elem in elements:
            rep = self.find_equivalent_object(elem, equivalences) if equivalences else elem
            if rep not in seen:
                seen.add(rep)
                reduced_elements.append(rep)
        return reduced_elements

    def find_equivalent_object(self, obj: str, equiv_rel: Optional[Dict[str, str]] = None) -> str:
        """
        Find the representative of an object in its equivalence relation.

        :param obj: The object to find.
        :param equiv_rel: The equivalence relation dictionary.
        :return: The representative element.
        """
        if equiv_rel is None:
            equiv_rel = self.object_equivalences
        while obj in equiv_rel:
            obj = equiv_rel[obj]
        return obj

    def find_equivalent_morphism(self, morph: Morphism, equiv_rel: Optional[Dict[str, str]] = None) -> str:
        """
        Find the representative of a morphism in its equivalence relation.

        :param morph: The morphism to find.
        :param equiv_rel: The equivalence relation dictionary.
        :return: The name of the representative morphism.
        """
        if equiv_rel is None:
            equiv_rel = self.morphism_equivalences
        while morph.name in equiv_rel:
            inverse_name = equiv_rel[morph.name]
            # Find the morphism with that name
            morph = next((m for m in self.morphisms if m.name == inverse_name), morph)
        return morph.name

    def quotient_category(self, object_equiv_rel: Dict[str, str], morphism_equiv_rel: Dict[str, str]) -> 'AbstractCategory':
        print("Starting to create the quotient category")
        
        # 1. Handle object equivalence relations
        print("Handling object equivalence relations")
        new_objects_set = set(object_equiv_rel.values())
        new_objects = list(new_objects_set)
        print(f"New object set: {new_objects}")
        
        # 2. Handle morphism equivalence relations
        print("Handling morphism equivalence relations")
        equiv_morphisms = {}
        for morphism in self.morphisms:
            equiv_name = morphism_equiv_rel.get(morphism.name, morphism.name)
            if equiv_name not in equiv_morphisms:
                equiv_morphisms[equiv_name] = Morphism(
                    equiv_name,
                    object_equiv_rel.get(morphism.source, morphism.source),
                    object_equiv_rel.get(morphism.target, morphism.target)
                )
        
        new_morphisms = list(equiv_morphisms.values())
        print(f"New morphism set: {[m.name for m in new_morphisms]}")
        
        # 3. Construct the new morphism association
        print("Constructing the new morphism association")
        new_morphism_association = {}
        for morphism in new_morphisms:
            if morphism.source not in new_morphism_association:
                new_morphism_association[morphism.source] = {}
            if morphism.target not in new_morphism_association[morphism.source]:
                new_morphism_association[morphism.source][morphism.target] = []
            new_morphism_association[morphism.source][morphism.target].append(morphism)
        
        print("New morphism association construction completed")
        
        # 4. Instantiate the quotient category
        print("Instantiating the quotient category")
        quotient_category = AbstractCategory(
            objects=new_objects,
            morphisms=new_morphisms,
            morphism_association=new_morphism_association,
            object_equivalences={},  # The objects in the quotient category are already reduced, so no equivalence relations are needed
            morphism_equivalences={}  # Same for morphisms
        )
        
        print("Quotient category instantiation completed")
        return quotient_category

    def visualize(self, graph_type: str = "full_labeled", show_compositions: bool = False):
        """
        Visualize the Quiver graph structure of the category.

        :param graph_type: The type of the graph, optional values include 'full_labeled', 'simple', 'labeled', etc.
        :param show_compositions: Whether to display composition morphisms.
        :param backend: Visualization backend, such as 'matplotlib', 'graphviz'.
        :param kwargs: Other optional parameters, like 'layout', 'node_color', 'node_size', etc.
        """
        self.quiver.visualize_graph(graph_type=graph_type)

    def _build_simple_reduced_association(self) -> Dict[str, Dict[str, Optional[Morphism]]]:
        """
        Build a simplified and reduced morphism association (for the ReducedSimple series).

        :return: The simplified morphism association dictionary.
        """
        simple_reduced_association = {}
        for src, targets in self.morphism_association.items():
            simple_reduced_association[src] = {}
            for dst, morphs in targets.items():
                simple_reduced_association[src][dst] = morphs[0] if morphs else None
        return simple_reduced_association

    @property
    def ReducedSimpleMorphismAssociation(self) -> Dict[str, Dict[str, Optional[Morphism]]]:
        """Return the simplified and reduced morphism association."""
        return self._build_simple_reduced_association()

    @property
    def ReducedSimpleMorphismNames(self) -> List[str]:
        """Return the set of simplified and reduced morphism names."""
        simple_names = set()
        for src, targets in self.ReducedSimpleMorphismAssociation.items():
            for morph in targets.values():
                if morph:
                    simple_names.add(morph.name)
        return list(simple_names)

    @property
    def ReducedSimpleMorphismEdges(self) -> List[str]:
        """Return the set of simplified and reduced morphism edges."""
        simple_edges = []
        for src, targets in self.ReducedSimpleMorphismAssociation.items():
            for morph in targets.values():
                if morph:
                    simple_edges.append(f"{morph.name}: {morph.source} → {morph.target}")
        return simple_edges

    @property
    def ReducedMonomorphisms(self) -> List[Morphism]:
        """Return the simplified monomorphisms."""
        return [morph for morph in self.morphisms if morph.name in self.ReducedSimpleMorphismNames and self.is_monomorphism(morph)]

    @property
    def ReducedEpimorphisms(self) -> List[Morphism]:
        """Return the simplified epimorphisms."""
        return [morph for morph in self.morphisms if morph.name in self.ReducedSimpleMorphismNames and self.is_epimorphism(morph)]

    @property
    def ReducedBimorphisms(self) -> List[Morphism]:
        """Return the simplified bimorphisms."""
        return [morph for morph in self.morphisms if morph.name in self.ReducedSimpleMorphismNames and self.is_bimorphism(morph)]

    @property
    def ReducedRetractions(self) -> List[Morphism]:
        """Return the simplified retraction morphisms."""
        return [morph for morph in self.morphisms if morph.name in self.ReducedSimpleMorphismNames and self.is_retraction(morph)]

    @property
    def ReducedSections(self) -> List[Morphism]:
        """Return the simplified section morphisms."""
        return [morph for morph in self.morphisms if morph.name in self.ReducedSimpleMorphismNames and self.is_section(morph)]

    def has_all_small_limits(self) -> bool:
        """Check if the category supports all small limits (completeness)."""
        # The implementation here is just an example. A more complex logic might be needed based on the actual category definition.
        # Check if finite pullbacks are supported
        supports_finite_pullbacks = all(
            self.pullback(f, g) is not None
            for f in self.morphisms
            for g in self.morphisms
            if f != g and f.target == g.target
        )
        # Check if there are initial objects
        has_initial_object = len(self.initial_objects()) > 0
        return supports_finite_pullbacks and has_initial_object

    def is_complete_category(self) -> bool:
        """
        Check if the category is complete, meaning it has all small limits.

        :return: True if complete, False otherwise.
        """
        return self.has_all_small_limits()

    def has_all_small_colimits(self) -> bool:
        """Check if the category supports all small colimits (cocompleteness)."""
        # The implementation here is just an example. A more complex logic might be needed based on the actual category definition.
        # Check if finite pushouts are supported
        supports_finite_pushouts = all(
            self.pushout(f, g) is not None
            for f in self.morphisms
            for g in self.morphisms
            if f != g and f.source == g.source
        )
        # Check if there are terminal objects
        has_terminal_object = len(self.terminal_objects()) > 0
        return supports_finite_pushouts and has_terminal_object

    def is_cocomplete_category(self) -> bool:
        """
        Check if the category is cocomplete, meaning it has all small colimits.

        :return: True if cocomplete, False otherwise.
        """
        return self.has_all_small_colimits()

    def pullback(self, f: Morphism, g: Morphism) -> Optional[str]:
        """
        Calculate the pullback of two morphisms, if it exists.

        :param f: The first morphism.
        :param g: The second morphism.
        :return: The name of the pullback object or None if it doesn't exist.
        """
        if f.target != g.target:
            return None
        pullback_obj = f"{f.name}×{g.name}"
        return pullback_obj

    def pushout(self, f: Morphism, g: Morphism) -> Optional[str]:
        """
        Calculate the pushout of two morphisms, if it exists.

        :param f: The first morphism.
        :param g: The second morphism.
        :return: The name of the pushout object or None if it doesn't exist.
        """
        if f.source != g.source:
            return None
        pushout_obj = f"{f.name}∪{g.name}"
        return pushout_obj

    def product(self, obj1: str, obj2: str) -> Optional[str]:
        """
        Calculate the product of two objects, if it exists.

        :param obj1: The first object.
        :param obj2: The second object.
        :return: The name of the product object or None if it doesn't exist.
        """
        product_obj = f"{obj1}×{obj2}"
        return product_obj

    def exponential(self, obj1: str, obj2: str) -> Optional[str]:
        """
        Calculate the exponential object of two objects, if it exists.

        :param obj1: The base object of the exponential.
        :param obj2: The exponent object of the exponential.
        :return: The name of the exponential object or None if it doesn't exist.
        """
        exponential_obj = f"{obj2}^{obj1}"
        return exponential_obj

    def has_cartesian_closed_structure(self) -> bool:
        """Check if the category has a Cartesian closed structure."""
        # Check if all object pairs have products
        supports_products = all(self.product(a, b) for a in self.objects for b in self.objects)

        # Check if all exponentials exist
        supports_exponentials = all(
            self.exponential(b, a) for a in self.objects for b in self.objects
        )

        return supports_products and supports_exponentials

    def is_cartesian_closed_category(self) -> bool:
        """
        Determine if the category is Cartesian closed.

        :return: True if it is Cartesian closed, False otherwise.
        """
        return self.has_cartesian_closed_structure()

    def get_associativity_equations(self) -> List[str]:
        """
        Return the list of associativity equations: (g ∘ f) ∘ h = g ∘ (f ∘ h).

        :return: A list of equation strings.
        """
        equations = []
        for morph1 in self.morphisms:
            for morph2 in self.morphisms:
                for morph3 in self.morphisms:
                    if morph1.target == morph2.source and morph2.target == morph3.source:
                        eq_left = f"({morph2.name} ∘ {morph1.name}) ∘ {morph3.name}"
                        eq_right = f"{morph2.name} ∘ ({morph1.name} ∘ {morph3.name})"
                        equations.append(f"{eq_left} = {eq_right}")
        return equations

    def get_identity_equations(self) -> List[str]:
        """
        Return the list of identity equations: id_X ∘ f = f and f ∘ id_Y = f.

        :return: A list of equation strings.
        """
        equations = []
        for obj in self.objects:
            identity = self.identity(obj)
            for morph in self.morphisms:
                if morph.source == obj:
                    equations.append(f"{identity.name} ∘ {morph.name} = {morph.name}")
                if morph.target == obj:
                    equations.append(f"{morph.name} ∘ {identity.name} = {morph.name}")
        return equations

    def get_commutativity_equations(self) -> List[str]:
        """
        Return the list of commutativity equations, for all paths that should commute.

        :return: A list of equation strings.
        """
        equations = []
        for src in self.objects:
            for dst in self.objects:
                if src == dst:
                    continue
                paths = self._find_paths(src, dst)
                if len(paths) > 1:
                    # Generate the morphism combinations for all paths
                    morphism_combinations = []
                    for path in paths:
                        if len(path) < 2:
                            continue
                        morphs = []
                        for i in range(len(path) - 1):
                            morph = next((m for m in self.Hom(path[i], path[i+1]) if m.target == path[i+1]), None)
                            if morph:
                                morphs.append(morph.name)
                        if morphs:
                            morphism_combinations.append(" ∘ ".join(morphs))
                    # Generate the equations
                    for i in range(len(morphism_combinations) - 1):
                        equations.append(f"{morphism_combinations[i]} = {morphism_combinations[i + 1]}")
        return equations

    @property
    def AssociativityEquations(self) -> List[str]:
        """Generate the list of associativity equations for the category."""
        return self.get_associativity_equations()

    @property
    def IdentityEquations(self) -> List[str]:
        """Generate the list of identity equations for the category."""
        return self.get_identity_equations()

    @property
    def CommutativityEquations(self) -> List[str]:
        """Generate the list of commutativity equations for the category."""
        return self.get_commutativity_equations()

    def _find_paths(self, start: str, end: str, path: Optional[List[str]] = None) -> List[List[str]]:
        """
        Recursively find all paths from start to end.

        :param start: The starting object.
        :param end: The target object.
        :param path: The current path.
        :return: A list of all paths.
        """
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.morphism_association:
            return []
        paths = []
        for morph in self.morphisms:
            if morph.source == start and morph.target not in path:
                new_paths = self._find_paths(morph.target, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def has_limits(self) -> bool:
        """Simple check if the category supports limits."""
        # Assume all categories support limits, but the actual logic can be more complex depending on the category definition
        return True

    def limit(self, diagram: str) -> str:
        """
        Return the limit object (in this example, the first object).

        :param diagram: A description of the limit diagram.
        :return: The name of the limit object.
        """
        if not self.has_limits():
            raise ValueError("This category does not support limits")
        return self.objects[0]

    def power_set(self, obj: str) -> List[Tuple[str, ...]]:
        """
        Calculate the power set of an object, returning all subsets.

        :param obj: The object for which to calculate the power set.
        :return: A list of subsets represented as tuples.
        """
        from itertools import chain, combinations
        return list(chain.from_iterable(combinations([obj], r) for r in range(len([obj]) + 1)))

    # Placeholder methods for further implementation
    def dual_space(self, vector_space: str) -> str:
        """Return the dual space of the given vector space."""
        return f"{vector_space}*"

    def fundamental_group(self, space: str, base_point: str) -> str:
        """Return the fundamental group based on base_point as a placeholder."""
        return f"π1({space}, {base_point})"

    def continuous_function_algebra(self, space: str) -> str:
        """Return a placeholder string representing the continuous function algebra of the space."""
        return f"C({space})"

    def pullback_map(self, arrow: str) -> str:
        """Return a placeholder string representing the pullback map."""
        return f"pullback({arrow})"

    def tangent_bundle(self, manifold: str) -> str:
        """Return a string representing the tangent bundle of a manifold."""
        return f"T({manifold})"

    def differential_map(self, morphism: Morphism) -> str:
        """Return a string representing the differential map of a morphism."""
        return f"d({morphism.name})"

    def group_action(self, group_element: str) -> str:
        """Simulate a group action: return a string describing the group action."""
        return f"Action({group_element})"

    def lie_algebra(self, group: str) -> str:
        """Simulate a Lie algebra map: return a string describing the Lie algebra."""
        return f"LieAlgebra({group})"

    def tensor_product(self, v: str, w: str) -> str:
        """Simulate the tensor product operation: return a string describing the tensor product."""
        return f"Tensor({v}, {w})"

    def get_inverse_morphism(self, morphism_name: str) -> Morphism:
        """
        Retrieves the inverse of a given morphism, if it exists.

        :param morphism_name: The name of the morphism whose inverse is to be found.
        :return: The inverse morphism.
        :raises ValueError: If no inverse is found for the given morphism.
        """
        # Check the equivalence relation dictionary
        inverse_name = self.morphism_equivalences.get(morphism_name, None)
        if inverse_name is None:
            raise ValueError(f"No inverse morphism found for {morphism_name} in equivalence relations.")

        # Find the corresponding morphism instance
        for morphism in self.morphisms:
            if morphism.name == inverse_name:
                return morphism

        # If the corresponding instance is not found, raise an exception
        raise ValueError(f"Inverse morphism '{inverse_name}' not found in the category.")
