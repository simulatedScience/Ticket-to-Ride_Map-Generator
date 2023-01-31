"""
A class representing nodes of a particle graph. Each node has a current and target position and a label.
There is an attraction force between the node and target position as well as between the node and the label.

A node can be connected to other nodes by edges.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.transforms as transforms

from graph_particle import Graph_Particle
from particle_node import Particle_Node


class Particle_Edge(Graph_Particle):
  def __init__(self,
        color: str,
        location_1_name: str,
        location_2_name: str,
        id: int,
        position: np.ndarray = np.array([0, 0]),
        rotation: float = 0,
        mass: float = 0.1,
        bounding_box_size: tuple = (4, 1),
        border_color: str = "#555555",
        node_attraction: float = 0.1,
        edge_attraction: float = 0.1,
        interaction_radius: float = 5,
        velocity_decay: float = 0.9999,
        angular_velocity_decay: float = 0.9999,
        repulsion_strength: float = 1,
        path_index: int = 0,
        ):
    """
    initialize a particle edge as a part of a connection two nodes `location_1` and `location_2`.  `path_index` is the index of the edge along the path between the two given locations. Counting starts at index 0, up  to path length -1.

    Args:
        color (str): color of the edge
        location_1_name (str): name of the first location
        location_2_name (str): name of the second location
        id (int): unique numeric id of the particle
        position (np.ndarray, optional): position of the edge. Defaults to np.array([0, 0]).
        rotation (float, optional): rotation of the edge in radians. Defaults to 0.
        mass (float, optional): mass of the edge. Defaults to 0.1.
        node_attraction (float, optional): attraction force between the edge and connected nodes. Defaults to 0.1.
        edge_attraction (float, optional): attraction force between the edge and the other edges. Defaults to 0.1.
        interaction_radius (float, optional): interaction radius of the edge for repulsion. Defaults to 5.
        velocity_decay (float, optional): velocity decay factor of the edge. Defaults to 0.9999.
        repulsion_strength (float, optional): repulsion strength of the edge. Defaults to 1.
        path_index (int, optional): index of the edge along the path between the two given locations. Defaults to 1.
    """
    super().__init__(
        id,
        position=position,
        rotation=rotation,
        target_position=None,
        mass=mass,
        bounding_box_size=bounding_box_size,
        interaction_radius=interaction_radius,
        velocity_decay=velocity_decay,
        angular_velocity_decay=angular_velocity_decay,
        repulsion_strength=repulsion_strength,
    )
    self.node_attraction = node_attraction
    self.edge_attraction = edge_attraction
    self.color = color
    self.border_color = border_color
    self.location_1_name = location_1_name
    self.location_2_name = location_2_name
    self.path_index = path_index
    self.image_file_path = None


  def get_attraction_forces(self, other_particle):
    """get attraction force between this particle and the other particle

    Args:
        other_particle (Graph_Particle): other particle

    Returns:
        np.ndarray: attraction force
    """
    if isinstance(other_particle, Particle_Edge):
      return self.get_edge_attraction_force(other_particle)
    else: # other_particle is Particle_Node
      return self.get_node_attraction_force(other_particle)


  def get_edge_attraction_force(self, other_edge: "Particle_Edge"):
    """
    get attraction force between this particle and the other edge depending on the minimum distance between midpoints of edge's bounding boxes shortest edges.
    This uses the helper function `get_edge_midpoints()`

    Args:
        other_edge (Particle_Edge): other edge

    Returns:
        np.ndarray: attraction force
    """
    min_distance = np.inf
    closest_points = np.zeros((2, 2))
    for point_1 in self.get_edge_midpoints():
      for point_2 in other_edge.get_edge_midpoints():
        distance = np.linalg.norm(point_1 - point_2)
        if distance < min_distance:
          min_distance = distance
          closest_points[0, :] = point_1
          closest_points[1, :] = point_2
    
    force_direction = (closest_points[1, :] - closest_points[0, :]) / min_distance
    translation_force = self.edge_attraction * self.attraction_from_distance(min_distance) * force_direction
    return translation_force, closest_points[0, :]


  def get_node_attraction_force(self, node: Graph_Particle):
    """
    get attraction force between this particle and the node depending on the minimum distance between the node and the edge's bounding box's shortest edges.
    This uses the helper function `get_edge_midpoints()`

    Args:
        node (Particle_Node): node

    Returns:
        np.ndarray: attraction force
    """
    min_distance = np.inf
    closest_point = np.zeros(2)
    for point in self.get_edge_midpoints():
      distance = np.linalg.norm(point - node.position)
      if distance < min_distance:
        min_distance = distance
        closest_point = point

    force_direction = (node.position - closest_point) / min_distance
    translation_force = self.node_attraction * self.attraction_from_distance(min_distance) * force_direction

    force_anchor = closest_point

    return translation_force, force_anchor


  def get_edge_midpoints(self, eps=1e-8):
    """
    get the midpoints of the edges of the bounding box of this edge

    Returns:
        np.ndarray: midpoints of the edges of the bounding box of this edge
    """
    midpoints = np.zeros((2, 2))
    found_n_shortest_edges = 0
    for i in range(4):
      corner_1 = self.bounding_box[i]
      corner_2 = self.bounding_box[(i + 1) % 4]
      if np.linalg.norm(corner_1 - corner_2) - np.min(self.bounding_box_size) < eps:
        midpoints[found_n_shortest_edges, :] = (corner_1 + corner_2) / 2
        found_n_shortest_edges += 1
        if found_n_shortest_edges == 2:
          break
    return midpoints

  
  def attraction_from_distance(self, distance):
    """
    get attraction force depending on the distance

    Args:
        distance (float): distance

    Returns:
        float: attraction force
    """
    return distance**2 / 2
    # return (np.exp(distance) - 1) / 3


  def set_parameters(self, edge_parameters):
    """
    set parameters of this edge

    Args:
        edge_parameters (dict): dictionary with parameters for this edge
    """
    self.node_attraction = edge_parameters.get("edge-node", self.node_attraction)
    self.edge_attraction = edge_parameters.get("edge-edge", self.edge_attraction)
    self.mass = edge_parameters.get("edge_mass", self.mass)
    self.color = edge_parameters.get("color", self.color)
    self.velocity_decay = edge_parameters.get("velocity_decay", self.velocity_decay)
    self.repulsion_strength = edge_parameters.get("repulsion_strength", self.repulsion_strength)
    self.interaction_radius = edge_parameters.get("interaction_radius", self.interaction_radius)


  def set_image(self, image_file_path: str = None):
    """
    Set edge to display the image at the given filepath when drawn.
    If `image_file_path` is `None`, the image will be removed and the edge is drawn as a flat colored rectangle.

    Args:
        image_file_path (str, optional): filepath to image file. Image aspect ratio should match bounding box aspect ratio. Otherwise the image gets stretched. Defaults to None.
    """
    self.image_file_path = image_file_path

  def draw(self,
      ax: plt.Axes,
      color: str = None,
      border_color: str = None,
      alpha: float = 0.7,
      zorder: int = 2,
      picker: bool = True) -> None:
    """
    draw this edge as a rectangle

    Args:
        ax (plt.Axes): matplotlib axes
        color (str, optional): color. Defaults to None.
        alpha (float, optional): alpha. Defaults to 0.7.
        zorder (int, optional): zorder. Defaults to 4.
    """
    if self.image_file_path is None: # draw mpl Rectangle
      if color is None:
        color = self.color
      if border_color is None:
        # if particle has no  border color, initialize it as gray
        try:
          border_color = self.border_color
        except AttributeError:
          border_color = "#555555"
          self.border_color = border_color
      super().draw_bounding_box(ax, color, border_color, alpha, zorder, picker)
      # midpoints = self.get_edge_midpoints()
      # self.plotted_objects.append(
      #     ax.plot(midpoints[:, 0], midpoints[:, 1], color=color, alpha=alpha, zorder=zorder))
    else:
      if picker is False: # mpl requires picker to be None to disable picking
        picker = None
      mpl_image = mpimg.imread(self.image_file_path)
      edge_extent = (
        self.position[0] - self.bounding_box_size[0] / 2,
        self.position[0] + self.bounding_box_size[0] / 2,
        self.position[1] - self.bounding_box_size[1] / 2,
        self.position[1] + self.bounding_box_size[1] / 2)
      plotted_image = ax.imshow(mpl_image, extent=edge_extent, zorder=zorder, picker=picker)
      # rotate image using transformation
      # keep image upright
      image_rotation = self.get_image_rotation()
      # print(f"image rotation {self.location_1_name}-{self.location_2_name}-{self.path_index}: {image_rotation}")
      plotted_image.set_transform(
        transforms.Affine2D().rotate_around(self.position[0], self.position[1], image_rotation) + ax.transData
      )
      self.plotted_objects.append(plotted_image)

  # def highlight(self, ax: plt.Axes,  highlight_color: str = "#cc00cc"):
  #   self.erase()
  #   self.draw(ax=ax, border_color=highlight_color)

  # def remove_highlight(self):
  #   return super().remove_highlight()

  def get_image_rotation(self) -> float:
    """
    calculate image rotation based on `self.rotation` and the location of the nodes this edge is connected to.

    Returns:
        float: rotation in radians
    """
    # find noes this edge is connected to
    visited_particle_ids = {self.get_id()}
    connected_nodes = [self, self]
    for i in range(2):
      while True:
        connected_index = 0
        new_node = connected_nodes[i].connected_particles[connected_index]
        while True:
          if not new_node.get_id() in visited_particle_ids:
            break
          # print(f"visited {type(new_node)}: id = {new_node.get_id()} at {new_node.position}")
          connected_index += 1
          if connected_index >= len(connected_nodes[i].connected_particles):
            raise ValueError("Could not find connected particle that has not been visited yet. Ensure that the graph is connected properly.")
          new_node = connected_nodes[i].connected_particles[connected_index]
        connected_nodes[i] = new_node
        visited_particle_ids.add(connected_nodes[i].get_id())
        if isinstance(connected_nodes[i], Particle_Node):
          break
    # calculate normal vector of direct connection between nodes
    node_1_position = connected_nodes[0].position
    node_2_position = connected_nodes[1].position
    node_1_to_node_2 = node_2_position - node_1_position
    norm = np.linalg.norm(node_1_to_node_2)
    if norm == 0:
      print(f"WARNING: edge {self.location_1_name}-{self.location_2_name} has length zero. Using original rotation of edge particle.")
      return self.rotation
    node_1_to_node_2 = node_1_to_node_2 / norm
    normal_vector = np.array([-node_1_to_node_2[1], node_1_to_node_2[0]]) # rotate by 90°
    # ensure that normal vector direction is always pointing upwards
    if normal_vector[1] < 0:
      normal_vector = -normal_vector
    # if normal vector is to the right of the current rotation vector, rotate by 180°
    # this aligns the image with the normal vector
    if np.cross(normal_vector, np.array([np.cos(self.rotation), np.sin(self.rotation)])) > 0:
      return self.rotation + np.pi
    return self.rotation


  def add_json_info(self, particle_info: dict) -> dict:
    """
    add edge-specific particle information to json dictionary for saving.

    Args:
        particle_info (dict): json dictionary

    Returns:
        dict: json dictionary with edge-specific information
    """
    particle_info["node_attraction"] = self.node_attraction
    particle_info["edge_attraction"] = self.edge_attraction
    particle_info["color"] = self.color
    particle_info["border_color"] = self.border_color
    particle_info["location_1_name"] = self.location_1_name
    particle_info["location_2_name"] = self.location_2_name
    particle_info["path_index"] = self.path_index
    return particle_info