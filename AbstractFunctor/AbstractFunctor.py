# AbstractFunctor/AbstractFunctor.py

from typing import Dict, List, Optional, Set
from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractCategory.Morphism import Morphism


class AbstractFunctor:
    """
    Represents a functor between two abstract categories.
    A functor F: C → D consists of:
    - A mapping on objects: For each object X in C, F(X) is an object in D.
    - A mapping on morphisms: For each morphism f: X → Y in C, F(f): F(X) → F(Y) in D.
    Such that:
    - F(id_X) = id_{F(X)} for every object X in C.
    - F(g ∘ f) = F(g) ∘ F(f) for any composable morphisms f, g in C.
    """

    def __init__(self,
                 source_category: AbstractCategory,
                 target_category: AbstractCategory,
                 object_mapping: Dict[str, str],
                 morphism_mapping: Dict[str, str]):
        """
        Initializes the AbstractFunctor with source and target categories,
        and the mappings on objects and morphisms.

        :param source_category: The source AbstractCategory (C).
        :param target_category: The target AbstractCategory (D).
        :param object_mapping: A dictionary mapping objects in C to objects in D.
        :param morphism_mapping: A dictionary mapping morphism names in C to morphism names in D.
        """
        self.source = source_category
        self.target = target_category
        self.object_mapping = object_mapping
        self.morphism_mapping = morphism_mapping

    def apply_object(self, obj: str) -> Optional[str]:
        """
        Applies the functor to an object.

        :param obj: The object in the source category.
        :return: The corresponding object in the target category, or None if not found.
        """
        return self.object_mapping.get(obj, None)

    def apply_morphism(self, morphism: Morphism) -> Optional[Morphism]:
        """
        Applies the functor to a morphism.

        :param morphism: The morphism in the source category.
        :return: The corresponding morphism in the target category, or None if not found.
        """
        target_morphism_name = self.morphism_mapping.get(morphism.name, None)
        if target_morphism_name is None:
            print(f"Functor does not map morphism '{morphism.name}'.")
            return None

        # Retrieve the target morphism from the target category
        target_source = self.apply_object(morphism.source)
        target_target = self.apply_object(morphism.target)
        if target_source is None or target_target is None:
            print(f"Functor mapping for morphism '{morphism.name}' has invalid source or target.")
            return None

        target_morphisms = self.target.morphism_association.get(
            target_source,
            {}
        ).get(target_target, [])

        for m in target_morphisms:
            if m.name == target_morphism_name:
                return m

        print(f"Morphism '{target_morphism_name}' not found in target category.")
        return None

    def is_valid(self) -> bool:
        """
        Validates whether the functor preserves identities and composition.

        :return: True if the functor is valid, False otherwise.
        """
        # Check identity preservation
        for obj in self.source.Objects:
            source_id = self.source.get_identity(obj)
            if source_id is None:
                print(f"No identity morphism found for object '{obj}' in source category.")
                return False
            target_obj = self.apply_object(obj)
            if target_obj is None:
                print(f"Functor does not map object '{obj}'.")
                return False
            target_id = self.target.get_identity(target_obj)
            if target_id is None:
                print(f"No identity morphism found for object '{target_obj}' in target category.")
                return False
            mapped_id = self.apply_morphism(source_id)
            if mapped_id is None:
                print(f"Functor does not map identity morphism of object '{obj}'.")
                return False
            if mapped_id.name != target_id.name:
                print(f"Functor does not preserve identity morphism for object '{obj}'. "
                      f"Expected '{target_id.name}', got '{mapped_id.name}'.")
                return False

        # Check composition preservation
        for (m1_name, m2_name), comp_result_name in self.source.compositions.items():
            m1 = self.source.get_morphism(m1_name)
            m2 = self.source.get_morphism(m2_name)
            if m1 is None or m2 is None:
                print(f"Morphism '{m1_name}' or '{m2_name}' not found in source category.")
                return False

            # Apply functor to morphisms
            F_m1 = self.apply_morphism(m1)
            F_m2 = self.apply_morphism(m2)
            if F_m1 is None or F_m2 is None:
                print(f"Functor does not map morphism '{m1_name}' or '{m2_name}'.")
                return False

            # Get composition in source category
            try:
                source_composition = self.source.compose(m1, m2)
            except ValueError as e:
                print(f"Error composing morphisms '{m1_name}' and '{m2_name}': {e}")
                return False

            # Apply functor to the composition
            F_composition = self.apply_morphism(source_composition)
            if F_composition is None:
                print(f"Functor does not map composition morphism '{source_composition.name}'.")
                return False

            # Get composition in target category
            try:
                target_composition = self.target.compose(F_m1, F_m2)
            except ValueError as e:
                print(f"Error composing morphisms '{F_m1.name}' and '{F_m2.name}' in target category: {e}")
                return False

            # Compare the two compositions
            if F_composition.name != target_composition.name:
                print(f"Functor does not preserve composition for morphisms '{m1_name} ∘ {m2_name}'. "
                      f"Expected '{target_composition.name}', got '{F_composition.name}'.")
                return False

        print("Functor is valid: preserves identities and compositions.")
        return True

    def __str__(self):
        """
        Returns a string representation of the functor.
        """
        morphism_mappings = ", ".join([f"'{k}': '{v}'" for k, v in self.morphism_mapping.items()])
        object_mappings = ", ".join([f"'{k}': '{v}'" for k, v in self.object_mapping.items()])
        return (f"AbstractFunctor(\n"
                f"  Source Category: {self.source},\n"
                f"  Target Category: {self.target},\n"
                f"  Object Mapping: {{{object_mappings}}},\n"
                f"  Morphism Mapping: {{{morphism_mappings}}}\n"
                f")")

    def get_mapped_category(self) -> AbstractCategory:
        """
        Returns the image of the source category under the functor.

        :return: An AbstractCategory instance representing the image.
        """
        mapped_objects: Set[str] = set(self.object_mapping.values())
        mapped_morphisms: List[Morphism] = []
        mapped_morphism_association: Dict[str, Dict[str, List[Morphism]]] = {}

        for morphism in self.source.morphisms:
            F_morphism = self.apply_morphism(morphism)
            if F_morphism is not None:
                # Avoid duplicates
                if not any(m.name == F_morphism.name for m in mapped_morphisms):
                    mapped_morphisms.append(F_morphism)
                    if F_morphism.source not in mapped_morphism_association:
                        mapped_morphism_association[F_morphism.source] = {}
                    if F_morphism.target not in mapped_morphism_association[F_morphism.source]:
                        mapped_morphism_association[F_morphism.source][F_morphism.target] = []
                    mapped_morphism_association[F_morphism.source][F_morphism.target].append(F_morphism)

        return AbstractCategory(
            objects=list(mapped_objects),
            morphisms=mapped_morphisms,
            morphism_association=mapped_morphism_association,
            object_equivalences={},
            morphism_equivalences={}
        )

    @staticmethod
    def compose(f: 'AbstractFunctor', g: 'AbstractFunctor') -> 'AbstractFunctor':
        """
        Compose two functors g ∘ f, where f: C → D and g: D → E.

        :param f: Functor from C to D.
        :param g: Functor from D to E.
        :return: A new functor from C to E.
        """
        if f.target != g.source:
            raise ValueError("Cannot compose functors: target of first functor does not match source of second functor.")

        # Compose object mappings: obj_C -> obj_D -> obj_E
        composed_object_mapping = {}
        for obj in f.object_mapping:
            mapped_obj = f.object_mapping[obj]
            if mapped_obj in g.object_mapping:
                composed_object_mapping[obj] = g.object_mapping[mapped_obj]
            else:
                print(f"Warning: Object '{mapped_obj}' mapped by f is not mapped by g.")
                # Depending on design choice, you might skip or raise an error
                # Here, we skip unmapped objects
                continue

        # Compose morphism mappings: morphism_C -> morphism_D -> morphism_E
        composed_morphism_mapping = {}
        for morphism_name, mapped_morphism_name in f.morphism_mapping.items():
            if mapped_morphism_name in g.morphism_mapping:
                composed_morphism_mapping[morphism_name] = g.morphism_mapping[mapped_morphism_name]
            else:
                print(f"Warning: Morphism '{mapped_morphism_name}' mapped by f is not mapped by g.")
                # Depending on design choice, you might skip or raise an error
                # Here, we skip unmapped morphisms
                continue

        return AbstractFunctor(
            source_category=f.source,
            target_category=g.target,
            object_mapping=composed_object_mapping,
            morphism_mapping=composed_morphism_mapping
        )

    def equals(self, other: 'AbstractFunctor') -> bool:
        """
        Checks if two functors are equal, i.e., they have the same source, target,
        and identical object and morphism mappings.

        :param other: Another AbstractFunctor to compare with.
        :return: True if equal, False otherwise.
        """
        if self.source != other.source or self.target != other.target:
            return False
        if self.object_mapping != other.object_mapping:
            return False
        if self.morphism_mapping != other.morphism_mapping:
            return False
        return True

    def is_full(self) -> bool:
        """
        Checks if the functor is full.
        A functor F: C → D is full if for every pair of objects X, Y in C,
        the map F: Hom_C(X, Y) → Hom_D(F(X), F(Y)) is surjective.

        :return: True if the functor is full, False otherwise.
        """
        for X in self.source.Objects:
            for Y in self.source.Objects:
                # Get all morphisms in Hom_D(F(X), F(Y))
                F_X = self.apply_object(X)
                F_Y = self.apply_object(Y)
                if F_X is None or F_Y is None:
                    print(f"Functor does not map object '{X}' or '{Y}'.")
                    return False
                Hom_D = set(m.name for m in self.target.morphism_association.get(F_X, {}).get(F_Y, []))
                # Get all morphisms in Hom_C(X, Y)
                Hom_C = set(m.name for m in self.source.morphism_association.get(X, {}).get(Y, []))
                # Apply functor to Hom_C(X, Y)
                F_Hom_C = set()
                for m_name in Hom_C:
                    m = self.source.get_morphism(m_name)
                    if m:
                        F_m = self.apply_morphism(m)
                        if F_m:
                            F_Hom_C.add(F_m.name)
                # Check if Hom_D is subset of F_Hom_C
                if not Hom_D.issubset(F_Hom_C):
                    print(f"Functor is not full for Hom_D({F_X}, {F_Y}). Missing morphisms: {Hom_D - F_Hom_C}")
                    return False
        print("Functor is full.")
        return True

    def is_faithful(self) -> bool:
        """
        Checks if the functor is faithful.
        A functor F: C → D is faithful if for every pair of objects X, Y in C,
        the map F: Hom_C(X, Y) → Hom_D(F(X), F(Y)) is injective.

        :return: True if the functor is faithful, False otherwise.
        """
        for X in self.source.Objects:
            for Y in self.source.Objects:
                # Get all morphisms in Hom_C(X, Y)
                Hom_C = self.source.morphism_association.get(X, {}).get(Y, [])
                # Apply functor to Hom_C(X, Y)
                F_Hom_C = {}
                for m in Hom_C:
                    F_m = self.apply_morphism(m)
                    if F_m:
                        if F_m.name in F_Hom_C:
                            print(f"Functor is not faithful for Hom_C({X}, {Y}): "
                                  f"'{m.name}' and '{F_Hom_C[F_m.name].name}' both map to '{F_m.name}'.")
                            return False
                        F_Hom_C[F_m.name] = m
                # No duplicates found
        print("Functor is faithful.")
        return True

    def is_full_and_faithful(self) -> bool:
        """
        Checks if the functor is both full and faithful.

        :return: True if the functor is full and faithful, False otherwise.
        """
        return self.is_full() and self.is_faithful()

    def is_equivalence(self) -> bool:
        """
        Checks if the functor is an equivalence of categories.
        A functor F: C → D is an equivalence if it is full, faithful,
        and essentially surjective on objects.

        :return: True if the functor is an equivalence, False otherwise.
        """
        if not self.is_full_and_faithful():
            print("Functor is not full and faithful; cannot be an equivalence.")
            return False

        # Check essential surjectivity: For every object Y in D, there exists an object X in C such that F(X) is isomorphic to Y in D.
        for Y in self.target.Objects:
            is_isomorphic = False
            for X in self.source.Objects:
                F_X = self.apply_object(X)
                if F_X is None:
                    continue
                if self.target.are_isomorphic(F_X, Y):
                    is_isomorphic = True
                    break
            if not is_isomorphic:
                print(f"Functor is not essentially surjective: No object in C maps isomorphically to '{Y}' in D.")
                return False

        print("Functor is an equivalence of categories.")
        return True

    def is_identity_functor(self) -> bool:
        """
        Checks if the functor is an identity functor.

        :return: True if it is an identity functor, False otherwise.
        """
        if self.source != self.target:
            return False
        for obj in self.source.Objects:
            if self.apply_object(obj) != obj:
                return False
        for morphism in self.source.morphisms:
            F_morphism = self.apply_morphism(morphism)
            if F_morphism is None or F_morphism.name != morphism.name:
                return False
        return True

    def get_preimage_morphisms(self, target_morphism_name: str) -> List[Morphism]:
        """
        Retrieves all morphisms in the source category that map to a given morphism in the target category.

        :param target_morphism_name: The name of the morphism in the target category.
        :return: A list of morphisms in the source category that map to the given morphism.
        """
        preimages = []
        for morphism in self.source.morphisms:
            F_morphism = self.apply_morphism(morphism)
            if F_morphism and F_morphism.name == target_morphism_name:
                preimages.append(morphism)
        return preimages

    def get_subfunctor(self, sub_object_mapping: Dict[str, str], sub_morphism_mapping: Dict[str, str]) -> 'AbstractFunctor':
        """
        Creates a subfunctor based on the provided object and morphism mappings.

        :param sub_object_mapping: A dictionary mapping a subset of objects in C to objects in D.
        :param sub_morphism_mapping: A dictionary mapping a subset of morphism names in C to morphism names in D.
        :return: A new AbstractFunctor representing the subfunctor.
        """
        # Validate that the sub mappings are subsets of the main mappings
        for obj in sub_object_mapping:
            if obj not in self.object_mapping or sub_object_mapping[obj] != self.object_mapping[obj]:
                raise ValueError(f"Invalid object mapping for '{obj}'.")
        for morphism in sub_morphism_mapping:
            if morphism not in self.morphism_mapping or sub_morphism_mapping[morphism] != self.morphism_mapping[morphism]:
                raise ValueError(f"Invalid morphism mapping for '{morphism}'.")

        return AbstractFunctor(
            source_category=self.source,
            target_category=self.target,
            object_mapping=sub_object_mapping,
            morphism_mapping=sub_morphism_mapping
        )

    def visualize_functor(self, filename: str = "functor"):
        """
        Visualizes the functor as a mapping between source and target categories.

        :param filename: The name of the output file (without extension).
        """
        try:
            import graphviz
        except ImportError:
            print("graphviz is not installed. Install it using 'pip install graphviz' to use visualization features.")
            return

        dot = graphviz.Digraph(comment='Functor Visualization', format='png')

        
        for obj in self.source.Objects:
            dot.node(f"C_{obj}", obj, shape='circle', color='lightblue')

        
        for obj in self.target.Objects:
            dot.node(f"D_{obj}", obj, shape='circle', color='lightgreen')

        
        for morphism in self.source.morphisms:
            dot.edge(f"C_{morphism.source}", f"C_{morphism.target}", label=morphism.name, color='blue')

        
        for morphism in self.target.morphisms:
            dot.edge(f"D_{morphism.source}", f"D_{morphism.target}", label=morphism.name, color='green')

        
        for src_obj, tgt_obj in self.object_mapping.items():
            dot.edge(f"C_{src_obj}", f"D_{tgt_obj}", label=f"F({src_obj})={tgt_obj}", style='dashed', color='red')

        
        for src_morphism, tgt_morphism in self.morphism_mapping.items():
            
            src_m = self.source.get_morphism(src_morphism)
            tgt_m = self.target.get_morphism(tgt_morphism)
            if src_m and tgt_m:
                
                dot.edge(f"C_{src_m.source}", f"C_{src_m.target}",
                         label=src_m.name,
                         arrowhead='none',
                         style='dotted',
                         color='red')
                dot.edge(f"D_{tgt_m.source}", f"D_{tgt_m.target}",
                         label=tgt_m.name,
                         arrowhead='none',
                         style='dotted',
                         color='red')

        dot.render(filename, view=False)
        print(f"Functor visualization saved as {filename}.png")
