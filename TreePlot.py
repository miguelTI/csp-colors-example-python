import pydot
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pylab as pl
import CSP


class TreePlot:
    def __init__(self):
        self.graph = pydot.Dot(graph_type='graph', dpi=800)
        self.index = 0

    def create_graph(self, node, currentNode):
        image = node.state.draw_state()
        html_string = "<<table>"
        rows, cols, _ = image.shape
        for i in range(rows):
            html_string += "<tr>"
            for j in range(cols):
                if image[i, j, 0] == 255:
                    html_string += "<td bgcolor='#FF0000'>&nbsp;</td>"
                elif image[i, j, 1] == 255:
                    html_string += "<td bgcolor='#00FF00'>&nbsp;</td>"
                elif image[i, j, 2] == 255:
                    html_string += "<td bgcolor='#0000FF'>&nbsp;</td>"
                else:
                    html_string += "<td bgcolor='#000000'>&nbsp;</td>"
            html_string += "</tr>"
        html_string += "</table>>"

        parent_graph_node = pydot.Node(str(self.index), shape="plaintext", label=html_string)
        self.index += 1

        # add node
        self.graph.add_node(parent_graph_node)

        # call this method for child nodes
        for child_node in node.children:
            child_graph_node = self.create_graph(child_node, currentNode)

            # create edge
            edge = pydot.Edge(parent_graph_node, child_graph_node)

            # add edge
            self.graph.add_edge(edge)

        return parent_graph_node

    def generate_diagram(self, rootNode, currentNode):
        self.create_graph(rootNode, currentNode)

        f = pl.figure()
        f.add_subplot(1, 2, 1)
        self.graph.write_png('graph.png')
        img = mpimg.imread('graph.png')
        pl.imshow(img)
        pl.axis('tight')
        pl.axis('off')

        f.add_subplot(1, 2, 2)
        pl.imshow(currentNode.state.draw_state())
        pl.axis('tight')
        pl.axis('off')
        font = {'family': 'serif',
                'color': 'white',
                'weight': 'normal',
                'size': 20,
                }

        ax = f.add_subplot(1, 3, 3)
        pl.imshow(currentNode.state.draw_possible_values())
        ax.set_yticks(range(len(CSP.variables)))
        ax.set_yticklabels(CSP.variables)

        for variable in CSP.variables:
            avgx = 0
            avgy = 0
            for (posx, posy) in CSP.positions[variable]:
                avgx += posx
                avgy += posy
            avgx /= len(CSP.positions[variable])
            avgy /= len(CSP.positions[variable])
            plt.text(avgy - 0.3, avgx, variable, fontdict=font)

        mng = plt.get_current_fig_manager()
        #mng.window.state('zoomed')
        plt.axis('tight')
        plt.axis('off')
        plt.show()
