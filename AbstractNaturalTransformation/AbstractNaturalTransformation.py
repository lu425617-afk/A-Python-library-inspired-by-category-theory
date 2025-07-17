# AbstractNaturalTransformation/AbstractNaturalTransformation.py

from typing import Dict
from AbstractCategory.AbstractCategory import AbstractCategory
from AbstractFunctor.AbstractFunctor import AbstractFunctor
from AbstractCategory.Morphism import Morphism


class AbstractNaturalTransformation:
    """
    Represents a natural transformation η: F ⇒ G between two functors.
    A natural transformation η: F ⇒ G consists of a family of morphisms η_X: F(X) → G(X)
    for each object X in the source category, such that for every morphism f: X → Y
    in the source category, the following diagram commutes:
    
        F(X) --F(f)--> F(Y)
         |              |
        η_X            η_Y
         |              |
         v              v
        G(X) --G(f)--> G(Y)
    """

    def __init__(self,
                 source_functor: AbstractFunctor,
                 target_functor: AbstractFunctor,
                 components: Dict[str, str]):
        """
        Initializes the natural transformation with source and target functors,
        and the components mapping.

        :param source_functor: The source functor F.
        :param target_functor: The target functor G.
        :param components: A dictionary mapping objects in the source category
                           to morphism names in the target category.
        """
        if source_functor.source != target_functor.source or source_functor.target != target_functor.target:
            raise ValueError("Source and target functors must have the same source and target categories.")
        
        self.F = source_functor
        self.G = target_functor
        self.components_names = components  # Maps object names to morphism names in target category
        self.components = self._initialize_components()  # Maps object names to Morphism instances

    def _initialize_components(self) -> Dict[str, Morphism]:
        """
        Initializes the components by converting morphism names to actual Morphism instances
        in the target category.

        :return: A dictionary mapping objects in the source category to Morphism instances.
        """
        target_category = self.F.target
        components = {}

        for obj, morph_name in self.components_names.items():
            morph = target_category.get_morphism(morph_name)
            if morph is None:
                raise ValueError(f"Morphism '{morph_name}' for object '{obj}' not found in target category.")
            components[obj] = morph

        return components

    def is_natural(self) -> bool:
        """
        Checks if the natural transformation satisfies the naturality condition.

        :return: True if the naturality condition is satisfied for all morphisms, False otherwise.
        """
        source_category = self.F.source
        target_category = self.F.target

        for morphism in source_category.morphisms:
            X, Y = morphism.source, morphism.target
            F_f = self.F.apply_morphism(morphism)
            G_f = self.G.apply_morphism(morphism)
            eta_X = self.components.get(X)
            eta_Y = self.components.get(Y)

            if eta_X is None or eta_Y is None:
                print(f"Missing components for objects '{X}' or '{Y}'.")
                return False

            # Compute G(f) ∘ η_X
            try:
                Gf_etaX = target_category.compose(G_f, eta_X)
            except ValueError as e:
                print(f"Error composing G(f) and η_X for morphism '{morphism.name}': {e}")
                return False

            # Compute η_Y ∘ F(f)
            try:
                etaY_Ff = target_category.compose(eta_Y, F_f)
            except ValueError as e:
                print(f"Error composing η_Y and F(f) for morphism '{morphism.name}': {e}")
                return False

            if Gf_etaX.name != etaY_Ff.name:
                print(f"Naturality condition failed for morphism '{morphism.name}': "
                      f"G(f) ∘ η_X = '{Gf_etaX.name}' != η_Y ∘ F(f) = '{etaY_Ff.name}'")
                return False

        print("Natural transformation satisfies all naturality conditions.")
        return True

    def is_natural_isomorphism(self) -> bool:
        """
        Checks if the natural transformation is a natural isomorphism,
        i.e., all components are isomorphisms.

        :return: True if all components are isomorphisms, False otherwise.
        """
        target_category = self.F.target

        for obj, morph in self.components.items():
            if not target_category.is_isomorphism(morph):
                print(f"Component η_{obj} = {morph.name} is not an isomorphism.")
                return False

        print("All components are isomorphisms. This is a natural isomorphism.")
        return True

    def inverse(self) -> 'AbstractNaturalTransformation':
        """
        Returns the inverse of a natural isomorphism.

        :return: The inverse natural transformation.
        :raises ValueError: If the natural transformation is not a natural isomorphism.
        """
        if not self.is_natural_isomorphism():
            raise ValueError("This natural transformation is not a natural isomorphism.")

        # Compute the inverse components
        inverse_components = {
            obj: self.F.target.get_inverse_morphism(morph.name)
            for obj, morph in self.components.items()
        }

        # Return the inverse natural transformation
        return AbstractNaturalTransformation(
            source_functor=self.G,
            target_functor=self.F,
            components={obj: inverse_components[obj].name for obj in inverse_components}
        )

    def equals(self, other: 'AbstractNaturalTransformation') -> bool:
        """
        Checks if this natural transformation is equal to another.

        :param other: The other natural transformation to compare with.
        :return: True if they are equal, False otherwise.
        """
        if self.F != other.F or self.G != other.G:
            print("The source or target functors do not match.")
            return False

        if self.components.keys() != other.components.keys():
            print("The components are defined for different sets of objects.")
            return False

        for obj, morph in self.components.items():
            other_morph = other.components.get(obj)
            if morph.name != other_morph.name:
                print(f"Component mismatch for object {obj}: "
                      f"η_{obj} = {morph.name}, other = {other_morph.name}")
                return False

        print("The two natural transformations are equal.")
        return True

    def get_component(self, obj: str) -> Morphism:
        """
        Retrieves the component of the natural transformation for a given object.

        :param obj: The object to retrieve the component for.
        :return: The corresponding morphism.
        :raises KeyError: If the object is not in the source category.
        """
        if obj not in self.components:
            raise KeyError(f"Object '{obj}' is not in the source category.")
        return self.components[obj]

    def restrict_to_subcategory(self, sub_objects: Dict[str, str]) -> 'AbstractNaturalTransformation':
        """
        Restricts the natural transformation to a subcategory.

        :param sub_objects: A subset of objects in the source category to restrict to.
        :return: A new AbstractNaturalTransformation restricted to the subcategory.
        """
        restricted_components = {
            obj: morph_name for obj, morph_name in self.components_names.items() if obj in sub_objects
        }

        return AbstractNaturalTransformation(
            source_functor=self.F,
            target_functor=self.G,
            components=restricted_components
        )

    def __str__(self):
        """
        Returns a string representation of the natural transformation.
        """
        components_str = ", ".join([f"{obj}: {morph.name}" for obj, morph in self.components.items()])
        return (f"AbstractNaturalTransformation(\n"
                f"  Source Functor: {self.F},\n"
                f"  Target Functor: {self.G},\n"
                f"  Components: {{{components_str}}}\n"
                f")")

    def compose_vertical(self, other: 'AbstractNaturalTransformation') -> 'AbstractNaturalTransformation':
        """
        Composes two natural transformations vertically.
        Requires: self.target_functor == other.source_functor.

        :param other: The second natural transformation to compose.
        :return: A new AbstractNaturalTransformation representing the composition.
        """
        # Ensure functor compatibility
        if self.G != other.F:
            raise ValueError("Target functor of the first transformation must match source functor of the second.")

        # Compose components
        composed_components = {
            obj: self.G.target.compose(
                self.components[obj],
                other.components[obj]
            ).name
            for obj in self.F.source.Objects
        }

        return AbstractNaturalTransformation(
            source_functor=self.F,
            target_functor=other.G,
            components=composed_components
        )

    def dual(self) -> 'AbstractNaturalTransformation':
        """
        Returns the dual of the natural transformation, reversing all morphisms.
        """
        dual_components = {
            obj: self.F.target.get_inverse_morphism(morph.name).name
            for obj, morph in self.components.items()
        }
        return AbstractNaturalTransformation(
            source_functor=self.G,  # Swap source and target functors
            target_functor=self.F,
            components=dual_components
        )

    def _check_naturality_condition(self, morphism: Morphism) -> bool:
        """
        Checks if the naturality condition is satisfied for a given morphism.

        :param morphism: A morphism in the source category.
        :return: True if the naturality condition is satisfied, False otherwise.
        """
        X, Y = morphism.source, morphism.target
        F_f = self.F.apply_morphism(morphism)
        G_f = self.G.apply_morphism(morphism)

        eta_X_name = self.components.get(X)
        eta_Y_name = self.components.get(Y)

        # Parse eta_X and eta_Y from target category
        eta_X = self.F.target.get_morphism(eta_X_name.name) if eta_X_name else None
        eta_Y = self.G.target.get_morphism(eta_Y_name.name) if eta_Y_name else None

        if eta_X is None or eta_Y is None:
            print(f"Components morphisms '{eta_X_name}' or '{eta_Y_name}' not found in target category.")
            return False

        # Compute G(f) ∘ η_X
        try:
            Gf_etaX = self.F.target.compose(G_f, eta_X)
        except ValueError as e:
            print(f"Error composing G(f) and η_X for morphism '{morphism.name}': {e}")
            return False

        # Compute η_Y ∘ F(f)
        try:
            etaY_Ff = self.G.target.compose(eta_Y, F_f)
        except ValueError as e:
            print(f"Error composing η_Y and F(f) for morphism '{morphism.name}': {e}")
            return False

        return Gf_etaX.name == etaY_Ff.name

    def visualize(self, filename: str = "natural_transformation", highlight_failures: bool = False):
        """
        Visualizes the natural transformation and optionally highlights failures in naturality conditions.

        :param filename: The name of the output file (without extension).
        :param highlight_failures: If True, highlights naturality condition failures in red.
        """
        try:
            import graphviz
        except ImportError:
            print("graphviz is not installed. Install it using 'pip install graphviz' to use visualization features.")
            return

        dot = graphviz.Digraph(comment="Natural Transformation Visualization", format="svg")
        dot.attr(rankdir='LR')  # 从左到右布局
        dot.attr(nodesep='1.5', ranksep='3.0')  # 调整节点间距和层级间距
        dot.attr('node', shape='circle')  # 设置默认节点形状为圆形

        # Add object nodes for functor F
        for obj in self.F.source.Objects:
            mapped_obj = self.F.apply_object(obj)
            dot.node(f"F_{obj}", f"F({obj}) = {mapped_obj}", color="lightblue")

        # Add object nodes for functor G
        for obj in self.G.source.Objects:
            mapped_obj = self.G.apply_object(obj)
            dot.node(f"G_{obj}", f"G({obj}) = {mapped_obj}", color="lightgreen")

        # Add morphism edges for functor F
        for morph in self.F.source.morphisms:
            F_m = self.F.apply_morphism(morph)
            if F_m:
                # Use the original object names to connect the nodes
                dot.edge(f"F_{morph.source}", f"F_{morph.target}", label=F_m.name, color="blue")
            else:
                print(f"Warning: Morphism '{morph.name}' not found in functor F's target category.")

        # Add morphism edges for functor G
        for morph in self.G.source.morphisms:
            G_m = self.G.apply_morphism(morph)
            if G_m:
                # Use the original object names to connect the nodes
                dot.edge(f"G_{morph.source}", f"G_{morph.target}", label=G_m.name, color="green")
            else:
                print(f"Warning: Morphism '{morph.name}' not found in functor G's target category.")

        # Add the natural transformation component (η) as a dashed edge
        for obj, morph in self.components.items():
            if morph:
                print(f"Visualizing component η_{obj}: {morph.name}")  # 调试信息
                dot.edge(f"F_{obj}", f"G_{obj}", label=f"η_{obj}: {morph.name}", color="red", style="dashed")
            else:
                print(f"Warning: Component morphism '{morph}' for object '{obj}' not found in target category.")

        # Add a legend
        with dot.subgraph(name='cluster_legend') as c:
            c.attr(label='Legend', style='dashed', color='black')
            c.node('legend_F', 'F(morphism)', shape='plaintext')
            c.node('legend_G', 'G(morphism)', shape='plaintext')
            c.node('legend_eta', 'Natural Transformation', shape='plaintext')
            c.edge('legend_F', 'legend_G', color="blue", style="solid", label='')
            c.edge('legend_G', 'legend_eta', color="green", style="solid", label='')
            c.edge('legend_F', 'legend_eta', color="red", style="dashed", label='')

        # Highlighting the failure of the naturality condition (if needed)
        if highlight_failures:
            for morphism in self.F.source.morphisms:
                if not self._check_naturality_condition(morphism):
                    src, tgt = morphism.source, morphism.target
                    eta_src = self.components.get(src)
                    eta_tgt = self.components.get(tgt)

                    if eta_src:
                        dot.edge(f"F_{src}", f"G_{src}", label=f"η_{src}: {eta_src.name}", color="red", style="dashed")
                    else:
                        print(f"Warning: Failed to find naturality component η_{src} for '{src}'.")

                    if eta_tgt:
                        dot.edge(f"F_{tgt}", f"G_{tgt}", label=f"η_{tgt}: {eta_tgt.name}", color="red", style="dashed")
                    else:
                        print(f"Warning: Failed to find naturality component η_{tgt} for '{tgt}'.")

        # Save DOT file
        with open(f"{filename}.dot", "w") as f:
            f.write(dot.source)

        
        dot.render(filename, view=False)
        print(f"Natural transformation visualization saved as {filename}.svg and {filename}.dot")
