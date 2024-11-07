import logging
from typing import Any, Callable, Literal
from matplotlib import pyplot as plt
import networkx as nx
import osmnx as ox
import shapely
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.widgets import PolygonSelector, Button


logger = logging.getLogger(__name__)


def get_graph(
    place: str, network_type: Literal["all", "all_public", "drive", "bike", "walk"]
) -> nx.MultiDiGraph:
    logger.info("Querying place %r with type %r", place, network_type)
    graph = ox.graph_from_address(place, dist=2000, network_type=network_type)
    return graph


def plot_graph(
    graph: nx.MultiDiGraph, ax: Axes, edge_linewidth: int, resize: bool = True
) -> tuple[Figure, Axes]:
    if not resize:
        # north, south, east, west = bbox
        west, east = ax.get_xlim()
        south, north = ax.get_ylim()
        bbox = north, south, east, west
    else:
        bbox = None
    logger.info("Plotting graph %s", graph)
    fig, ax = ox.plot_graph(
        graph,
        node_size=0,
        bgcolor="white",
        edge_color="#111111",
        show=False,
        bbox=bbox,
        ax=ax,
        edge_linewidth=edge_linewidth,
    )
    return fig, ax


def submit_function_factory(
    polygon_selector: PolygonSelector, draw_ax: Axes
) -> Callable[[], None]:
    def submit_polygon() -> None:
        logger.info("Submiting polygon")
        vertices = list(polygon_selector.verts)
        if not vertices:
            return
        polygon_selector.clear()
        polygon = shapely.Polygon(vertices)
        walking_graph = ox.graph_from_polygon(
            polygon, network_type="walk", retain_all=True, truncate_by_edge=True
        )
        plot_graph(walking_graph, draw_ax, 1, resize=False)

    return submit_polygon


def main() -> None:
    place = "Piedmont, California, USA"
    place = "Paris, France"
    place = "173 rue de Charenton, Paris 75012, France"
    fig, axs = plt.subplots()
    ax1 = axs
    # ax1, ax2 = axs
    # (ax1, ax2), (ax3, _) = axs

    graph = get_graph(place, "drive")
    plot_graph(graph, ax1, 2)

    selector = PolygonSelector(ax1, lambda *args: None)
    # polygon = [
    #     (-122.23141880009764, 37.82407415622793),
    #     (-122.23337938871202, 37.82297715526384),
    #     (-122.23484983017279, 37.822719037389945),
    #     (-122.23574843328772, 37.82258997845299),
    #     (-122.23550335971092, 37.82194468376824),
    #     (-122.23632027163357, 37.8214929774889),
    #     (-122.23681041878717, 37.82129938908348),
    #     (-122.2364836540181, 37.82084768280415),
    #     (-122.23574843328772, 37.820589564930245),
    #     (-122.23501321255733, 37.82000879971397),
    #     (-122.23419630063468, 37.820589564930245),
    #     (-122.23370615348108, 37.820266917587865),
    #     (-122.2322357120203, 37.82142844802043),
    #     (-122.23264416798163, 37.821880154299755),
    #     (-122.23092865294404, 37.82323527313775),
    # ]
    # selector.verts = polygon
    submit_func = submit_function_factory(polygon_selector=selector, draw_ax=ax1)

    def submit_func_selector(*args) -> None:
        logger.debug("Key was pressed %s", args)
        submit_func()

    selector.onselect = submit_func_selector

    def key_press_event(event: Any) -> None:
        key = event.key
        logger.debug("Key was pressed %s %s", event, key)
        if key.lower() == "d":
            submit_func()

    fig.canvas.mpl_connect("key_press_event", key_press_event)

    # submit_button = Button(ax2, label="Submit")

    # def button_submit_function(event: Any) -> None:
    #     logger.debug("Submit button was pressed %s", event)
    #     submit_button.active = False
    #     try:
    #         submit_func()
    #     finally:
    #         submit_button.active = True

    # submit_button.on_clicked(button_submit_function)
    plt.show()


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
