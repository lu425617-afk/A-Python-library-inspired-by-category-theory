       
        #The catpy visualization tools can help users draw pictures.
        #  And these pictures can show objects,morphisms and categories.
        #  It support different layouts like spring, circular, shell and dot. 
        # And the users can also change the color, 
        # shapes, size of node to make the graph clearer

import matplotlib.pyplot as plt
import networkx as nx
from typing import List
from AbstractCategory.Quiver import Quiver

class Visualizer:
    @staticmethod
    def visualize_quiver(quiver: Quiver,
                         filename: str = 'quiver_diagram',
                         format: str = 'png',
                         layout: str = 'dot',  
                         node_color: str = 'lightblue',
                         edge_color: str = 'black',
                         node_shape: str = 'o',
                         font_size: int = 12,
                         font_color: str = 'black',
                         arrowstyle: str = '-|>',
                         arrowsize: int = 15,
                         node_size: int = 1500,
                         linewidths: float = 1.5,
                         edge_width: float = 2.0,
                         figsize: tuple = (10, 8)):
        """
        可视化 Quiver，支持使用 Graphviz 的布局。

        :param quiver: Quiver 实例。
        :param filename: 输出文件名（不包含扩展名）。
        :param format: 输出文件格式，如 'png', 'pdf'。
        :param layout: 布局类型，如 'spring', 'circular', 'shell', 'kamada_kawai', 'dot'。
        :param node_color: 节点颜色。
        :param edge_color: 边颜色。
        :param node_shape: 节点形状。
        :param font_size: 字体大小。
        :param font_color: 字体颜色。
        :param arrowstyle: 箭头样式。
        :param arrowsize: 箭头大小。
        :param node_size: 节点大小。
        :param linewidths: 节点边缘线宽。
        :param edge_width: 边线宽。
        :param figsize: 图形尺寸。
        """
        G = quiver.get_graph()
        
        
        #The catpy visualization tools can help users draw pictures.
        #  And these pictures can show objects,morphisms and categories.
        #  It support different layouts like spring, circular, shell and dot. 
        # And the users can also change the color, 
        # shapes, size of node to make the graph clearer

        if layout == 'spring':
            pos = nx.spring_layout(G, k=0.5, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'shell':
            pos = nx.shell_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        elif layout == 'dot':
            try:
                pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
            except ImportError:
                print("pygraphviz 未安装，无法使用 'dot' 布局。请安装 pygraphviz 或选择其他布局。")
                pos = nx.spring_layout(G, k=0.5, iterations=50)
        else:
            print(f"未知的布局类型 '{layout}'，使用默认的 spring_layout。")
            pos = nx.spring_layout(G, k=0.5, iterations=50)
        
        plt.figure(figsize=figsize)
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_color=node_color, node_shape=node_shape,
                               node_size=node_size, linewidths=linewidths, edgecolors='black')
        # 绘制边
        nx.draw_networkx_edges(G, pos, edge_color=edge_color, arrowstyle=arrowstyle,
                               arrowsize=arrowsize, width=edge_width)
        # 绘制节点标签
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_color=font_color)
        # 绘制边标签
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=10)
        
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"{filename}.{format}", format=format)
        plt.close()
