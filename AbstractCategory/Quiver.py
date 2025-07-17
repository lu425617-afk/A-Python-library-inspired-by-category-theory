# CategoryTheory/AbstractCategory/Quiver.py

import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict
from .Morphism import Morphism

class Quiver:
    def __init__(self, objects: List[str], morphism_association: Dict[str, Dict[str, List[Morphism]]]):
        """
        Initialize a Quiver.

        :param objects: A list of objects in the category.
        :param morphism_association: The association of morphisms, in the format {source_object: {target_object: [list_of_morphisms]}}.
        """
        self.objects = objects
        self.morphism_association = morphism_association

    def visualize_graph(self, graph_type='full_labeled'):
        """
        Visualize the Quiver using networkx and matplotlib.

        :param graph_type: The type of the graph, can be 'simple', 'labeled', 'full_labeled', etc.
        """
        G = nx.DiGraph()

        # Add nodes
        for obj in self.objects:
            G.add_node(obj)

        # Add edges
        for src, targets in self.morphism_association.items():
            for tgt, morphs in targets.items():
                for morph in morphs:
                    G.add_edge(src, tgt, label=morph.name)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))

        if graph_type == 'simple':
            nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True)
        elif graph_type == 'labeled':
            nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True)
            labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        elif graph_type == 'full_labeled':
            nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True, connectionstyle='arc3, rad=0.1')
            labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        else:
            raise ValueError(f"Unknown graph type: {graph_type}")

        plt.title("Quiver Visualization")
        plt.axis('off')
        plt.show()
