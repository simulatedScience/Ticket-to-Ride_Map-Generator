"""
This module implements task edit functionality for the TTR board layout GUI.

This is done via a class Task_Editor_Gui which can be seen as an extension of `Board_Layout_GUI`, which is the intended way to use it.

"""
import tkinter as tk
from typing import Tuple, List, Callable

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import PickEvent, MouseEvent

from auto_scroll_frame import Auto_Scroll_Frame
from ttr_particle_graph import TTR_Particle_Graph
from ttr_task import TTR_Task


class Task_Editor_GUI:
  def __init__(self,
      master: tk.Tk,
      color_config: dict[str, str],
      grid_padding: Tuple[float, float],
      tk_config_methods: dict[str, Callable],
      particle_graph: TTR_Particle_Graph,
      task_edit_frame: tk.Frame,
      ax: plt.Axes,
      canvas: FigureCanvasTkAgg,
      max_pick_range: float = 0.2
      ):
    """
    This class implements task edit functionality for the TTR board layout GUI. Changes are made to the given particle graph `particle_graph` and the graph is displayed in the given matplotlib Axes object `ax` and tkinter canvas `canvas`.

    Args:
        master (tk.Tk): The master widget of the GUI.
        color_config (dict[str, str]): A dictionary containing the colors used in the GUI.
        grid_padding (Tuple[float, float]): The padding of the grid in the GUI.
        tk_config_methods (dict[str, Callable]):  Dictionary of methods to configure tkinter widgets (see `Board_Layout_GUI`). These should add styles to the widgets. Expect the following keys:
            - `add_frame_style(frame: tk.Frame)`
            - `add_label_style(label: tk.Label, headline_level: int, font_type: str)
            - `add_button_style(button: tk.Button)`
            - `add_entry_style(entry: tk.Entry, justify: str)`
            - `add_checkbutton_style(checkbutton: tk.Checkbutton)
            - `add_radiobutton_style(radiobutton: tk.Radiobutton)
            - `add_browse_button(frame: tk.Frame, row_index: int, column_index: int, command: Callable) -> tk.Button`
        particle_graph (TTR_Particle_Graph): The particle graph of the GUI.
        task_edit_frame (tk.Frame): The frame containing the task edit GUI.
        ax (plt.Axes): The axes where the graph is drawn.
        canvas (FigureCanvasTkAgg): The canvas for the graph.
        max_pick_range (float, optional): The maximum range for picking a node. Defaults to 0.2.
    """
    self.master: tk.Tk = master
    self.color_config: dict[str, str] = color_config
    self.particle_graph: TTR_Particle_Graph = particle_graph
    self.task_edit_frame: tk.Frame = task_edit_frame
    self.ax: plt.Axes = ax
    self.canvas: FigureCanvasTkAgg = canvas
    self.max_pick_range: float = max_pick_range

    # save grid padding for later use
    self.grid_pad_x = grid_padding[0]
    self.grid_pad_y = grid_padding[1]

    # extract tkinter style methods
    self.add_frame_style = tk_config_methods["add_frame_style"]
    self.add_label_style = tk_config_methods["add_label_style"]
    self.add_button_style = tk_config_methods["add_button_style"]
    self.add_entry_style = tk_config_methods["add_entry_style"]
    self.add_checkbutton_style = tk_config_methods["add_checkbutton_style"]
    self.add_radiobutton_style = tk_config_methods["add_radiobutton_style"]
    self.add_browse_button = tk_config_methods["add_browse_button"]

    self.init_task_edit_gui()


  def init_task_edit_gui(self):
    """
    This method initializes the task edit GUI with all its widgets.
    """
    # set up task edit variables
    self.task_visibility_vars: List[tk.BooleanVar] = []

    # set up task edit frame
    self.draw_task_overview()


  def clear_task_edit_frame(self):
    """
    Clears the task edit frame.
    """
    for widget in self.task_edit_frame.winfo_children():
      widget.destroy()


  def draw_task_overview(self):
    """
    Draws an overview of all tasks in the task edit frame. This includes:
      - a headline
      - a button to calculate all task lengths
      - a checkbutton to toggle visibility of all tasks
      - a button to add a new task, and
      - a list of all tasks.
    """
    # clear task edit frame
    self.clear_task_edit_frame()

    row_index: int = 0
    # create task edit headline
    headline_label = tk.Label(self.task_edit_frame, text="Task Overview")
    self.add_label_style(headline_label, font_type="bold")
    headline_label.grid(
        row=row_index,
        column=0,
        columnspan=2,
        sticky="nw",
        padx=self.grid_pad_x,
        pady=self.grid_pad_y)
    row_index += 1
    # add button to calculate all task lengths
    calc_task_lengths_button = tk.Button(
        self.task_edit_frame,
        text="Calculate Task Lengths",
        command=self.calculate_all_task_lengths)
    self.add_button_style(calc_task_lengths_button)
    calc_task_lengths_button.grid(
        row=row_index,
        column=0,
        columnspan=2,
        sticky="new",
        padx=self.grid_pad_x,
        pady=self.grid_pad_y)
    row_index += 1
    # add checkbutton to toggle visibility of all tasks
    toggle_task_visibility_button = tk.Checkbutton(
        self.task_edit_frame,
        text="Show/hide all",
        command=self.toggle_all_tasks_visibility)
    self.add_checkbutton_style(toggle_task_visibility_button)
    toggle_task_visibility_button.grid(
        row=row_index,
        column=0,
        sticky="nw",
        padx=self.grid_pad_x,
        pady=self.grid_pad_y)
    # add button to add new task
    add_task_button = tk.Button(
        self.task_edit_frame,
        text="Add Task",
        command=self.add_task)
    self.add_button_style(add_task_button)
    add_task_button.grid(
        row=row_index,
        column=1,
        sticky="nw",
        padx=(0, self.grid_pad_x),
        pady=self.grid_pad_y)
    row_index += 1
    
    # add task list
    task_list_outer_frame = tk.Frame(
        self.task_edit_frame,
        background="#8844cc", #self.color_config["bg_color"],
        height=250)
    task_list_outer_frame.grid(
        row=row_index,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=0)
    task_list_outer_frame.grid_rowconfigure(0, weight=1)
    task_list_auto_frame = Auto_Scroll_Frame(
        task_list_outer_frame, 
        frame_kwargs=dict(background=self.color_config["bg_color"]),
        scrollbar_kwargs=dict(
            troughcolor=self.color_config["bg_color"],
            activebackground=self.color_config["button_active_bg_color"],
            bg=self.color_config["button_bg_color"],
            border=0,
            width=10,
            highlightthickness=0,
            highlightbackground=self.color_config["bg_color"],
            highlightcolor=self.color_config["bg_color"],
            )
        )
    task_list_frame: tk.Frame = task_list_auto_frame.scrollframe
    task_list_frame.grid_columnconfigure(0, weight=1)
    row_index += 1
    # add tasks to subframe
    task_row_index: int = 0
    self.task_widget_frames: List[tk.Frame] = []
    self.ttr_tasks: List[TTR_Task] = []
    for loc_1, loc_2 in self.particle_graph.tasks:
      self.add_task_view_widgets(task_list_frame, task_row_index, loc_1, loc_2)
      task_row_index += 1

    task_list_auto_frame._on_configure()

  def add_task_view_widgets(self,
      task_list_frame: tk.Frame,
      task_row_index: int,
      loc_1: str,
      loc_2: str):
    """
    Adds the widgets for a single task to the task list frame.

    Args:
        task_list_frame (tk.Frame): The frame to add the widgets to.
        task_row_index (int): The row index to add the widgets to.
        i (int): The index of the task.
        loc_1 (str): The name of the first location.
        loc_2 (str): The name of the second location.
    """
    ttr_task: TTR_Task = TTR_Task(node_names=[loc_1, loc_2])
    task_var: tk.BooleanVar = tk.BooleanVar(value=False)
    self.task_visibility_vars.append(task_var)
    task_frame = tk.Frame(task_list_frame)
    self.add_frame_style(task_frame)
    task_frame.grid(
        row=task_row_index,
        column=0,
        sticky="nsew",
        padx=0,
        pady=(self.grid_pad_y, 0))
    self.task_widget_frames.append(task_frame)
    task_frame.grid_columnconfigure(1, weight=1)
    # add task number
    task_number_label = tk.Label(task_frame, text=f"{task_row_index+1}.")
    self.add_label_style(task_number_label, font_type="bold")
    task_number_label.grid(
        row=0,
        column=0,
        rowspan=2,
        sticky="w",
        padx=(self.grid_pad_x, 0),
        pady=0)
    # task_row_index += 1
    # add checkbutton to toggle visibility of task
    task_name = ttr_task.name
    if " - " in task_name:
      task_name = "\n".join(task_name.split(" - "))
    task_visibility_button = tk.Checkbutton(
        task_frame,
        text=task_name,
        justify="left",
        variable=task_var,
        command=lambda task_var=task_var, task=ttr_task: self.toggle_task_visibility(task_var, task))
    self.add_checkbutton_style(task_visibility_button)
    task_visibility_button.grid(
        row=0,
        column=1,
        rowspan=2,
        sticky="w",
        padx=self.grid_pad_x,
        pady=self.grid_pad_y)
    # add label to show task length. If task has bonus points, show them as well
    task_length_text = f"length: {ttr_task.points}"
    if ttr_task.points_bonus is not None: # add task bonus points
      task_length_text += " + " + str(ttr_task.points_bonus)
    task_length_label = tk.Label(
        task_frame,
        text=task_length_text)
    self.add_label_style(task_length_label)
    task_length_label.grid(
        row=0,
        column=2,
        columnspan=2,
        sticky="nw",
        padx=(0, self.grid_pad_x),
        pady=(self.grid_pad_y,0))
    # add button to edit task
    edit_task_button = tk.Button(
        task_frame,
        text="Edit",
        command=lambda task=ttr_task: self.edit_task(task))
    self.add_button_style(edit_task_button)
    edit_task_button.grid(
        row=1,
        column=2,
        sticky="ne",
        padx=0, # (0, self.grid_pad_x),
        pady=0)
    # add button to delete task
    delete_task_button = tk.Button(
        task_frame,
        text="Delete",
        command=lambda task=ttr_task: self.delete_task(task))
    self.add_button_style(delete_task_button)
    delete_task_button.config(
        bg=self.color_config["delete_button_bg_color"],
        fg=self.color_config["delete_button_fg_color"])
    delete_task_button.grid(
        row=1,
        column=3,
        sticky="nw",
        padx=0,
        pady=0)


  def calculate_all_task_lengths(self):
    """
    Calculates the length of all tasks in the task edit frame.
    """
    raise NotImplementedError() # TODO: implement

  def add_task(self):
    """
    Adds a new task to the task edit frame.
    """
    raise NotImplementedError() # TODO: implement

  def toggle_all_tasks_visibility(self):
    """
    Toggles the visibility of all tasks.
    """
    raise NotImplementedError() # TODO: implement

  def toggle_task_visibility(self, task_visibility_var: tk.BooleanVar, task: TTR_Task):
    """
    Toggles the visibility of the given task.
    If all task visibility variables were True and this one is now False, uncheck the "Show/hide all" checkbutton.
    If all task visibility variables are now True, check the "Show/hide all" checkbutton.
    """
    raise NotImplementedError() # TODO: implement

  def edit_task(self, task: TTR_Task):
    """
    Open edit mode for the given task.
    """
    raise NotImplementedError() # TODO: implement

  def delete_task(self, task: TTR_Task):
    """
    Deletes the given task:
    - remove it from the task edit frame
    - remove it from the particle graph
    - remove the corresponding task visibility variable
    - if it was shown, remove it from the canvas
    """
    raise NotImplementedError() # TODO: implement


  def draw_task_edit_mode(self, task: TTR_Task):
    """
    Clears the task edit frame and creates all widgets for editing the given task.
    """
    raise NotImplementedError() # TODO: implement