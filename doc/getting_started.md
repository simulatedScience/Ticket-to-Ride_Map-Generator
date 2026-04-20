# Creating a custom Ticket To Ride map
Start the mapmaker program by running `_ttr_mapmaker_gui.py`.  
For example, you can open a terminal, navigate to `src/ttr_map_maker` and run `python _ttr_mapmaker_gui.py`
This opens a GUI.

# Overview
The program is meant to aid in the creation of custom Ticket to Ride maps.
On the left, there is a large viewport that will display your map, locations, edges and occasionally other things. On the right, there is a sidebar menu.

The program treats a ticket to ride map as a [graph](https://en.wikipedia.org/wiki/Graph_(abstract_data_type)) where the Ticket to Ride locations are the graph's nodes and the connections between them are the graph's edges. The program allows you to create and edit this graph. We call the connections between nodes "edges". They can have a color and a length (= number of train pieces needed).
The labels are separate objects that are created automatically for each node and can be moved manually.

To save progress, the program uses human-readable .json files. You can edit these manually - occasionally that's faster than using the GUI, but you can also break things.


### Keyboard shortcuts:
* Pressing F11 enters fullscreen mode.
* On many buttons where you choose between mutliple options, you can use the scroll wheel to quickly switch between options. This includes location selection for tasks and edges, edge color, edge length and more.

### What you need beyond this program:
* A background image for your map.
  * A score track
  * a legend to tell players how many points they earn for each edge they built
* physical materials
  * a printer to print the board and task cards
  * cards (e.g. Pokémon energy cards)
  * train pieces (e.g. 1x3 or 1x4 LEGO bricks)

## The sidebar menu
### GUI modes
At the top, there are 6 mode buttons. Opening a mode often adds a new section to the sidebar menu with more buttons and options. The modes are:
* **Graph View:** View your graph without editing anything. This is the default mode when you start the program.
* **Graph Editor:** This is the main mode for creating your map. It allows you to add nodes and edges, edit them, assign individual images and more. In the new sidebar section, you can enable moving nodes, edges and labels. Once the corresponding option is enabled, you can move them via drag and drop in the viewport. While moving edges, you can use the scroll wheel to rotate them.
* **Graph Optimizer:** This is meant to automatically find a good layout for your graph, respositioning edges. The Graph optimizer does not work well, I recommend manually moving nodes, edges and labels in the Graph Editor instead.
* **Task Editor:** Here, you can add and edit tasks (destination tickets). Clicking on a location will show all tasks starting or ending in that location.
* **Task Export:** This is the mode to export each task as an individual image file for printing.
* **Graph Analysis:** Used for balancing the map, this mode shows statistics about your graph: How many edges are there of each color? How many edges connect to the locations? Assuming shortest routes, how often is each color needed to complete all tasks? If no tasks are defined, this mode shows 6 subplots. If there are tasks for your map, it shows 9 subplots.

### File Inputs
Below the mode buttons, there are file path inputs and buttons to load each file. The edge images are loaded automatically when needed.
The most important inputs are particle graph and background image. The particle graph is a .json file that contains everything needed by the program: positions, names, etc. of nodes, edges, labels, tasks and more. This also contains paths to images and settings for the GUI like background image size, scaling factors, font size etc..

### Toggles
This sections modifies the viewport:
* Whether nodes, labels and the background image are shown
* Whether to show a plot frame to better judge node and edge positions
* debug/ bugfix tools (see [Usage notes](#usage-notes) below)
* selector how to show edges:
  * **Hidden:** Edges are invisible.
  * **Neutral:** Edges are shown as simple gray rectangles. Good for judging layout and connectivity of the graph.
  * **Flat colors:** Edges are colored. This is great for editing the graph as it shows all information cleanly.
  * **Edge images:** This is the mode you want for final map export. It places a image at each edge rectangle. Editing in this mode is has VERY poor performance, so you should always use neutral or flat color modes for that. Edge images are loaded from the folder specified in the "edge img Folder" input.
  * **Show tasks:** This colors the edges according to how many tasks require them for the shortest path between the task's locations. This is a great tool for balancing your map, but it only works if you have defined tasks for your map.
  * **Edge importance:** Similar to "Show tasks", this is a balancing tool. It shows by how much the shortest path for solving a task increases if each edge is removed. Black edges mean that at least one task becomes impossible without that edge. Gray edges mean there are other paths to solve a task without lengthening the shortest path. Pink edges increase at least one task's length if removed. Look at the colorbar to the right to see how much the shortest path increases for each color.

### Buttons
* **Save Graph:** Saves the current graph as a .json file. This is the main way to save your progress. You can also edit the .json file manually, but be careful not to break the format.
* **Save img:** This is the way to export your map including locations, edges and labels. This exports at pretty high resolution. Export may take a few seconds or even minutes on slow computers.
* **Snap labels:** Reposition all location labels to their corresponding nodes. Great when you are repositioning nodes. Careful: There is no Undo option. Already repositioned labels will be snapped back to their nodes.
* **Snap edges:** Straightens all edges between their corresponding nodes. Great when you are repositioning nodes. The individual edge rectangles will be spaced evenly between the nodes. Careful: There is no Undo option. Already repositioned edges will be snapped back to their nodes.
* **Scale graph:** This applies the scale factors specified in the next section. If you changed the size of your board, this can be used to readjust the node, edge and label positions to fit the new board size. Caution: Pressing the button multiple times applies the scaling multiple times. There can be small numerical errors during scaling, but they usually shouldn't be noticable.
* **Scale img:** Scale the backgorund image to the size specified in the next section. This is often necessary when you load a new background image. By default, a new image treats each pixel as one unit in size. With this, you can scale everything so that the numbers in the program correspond to centimeters or inches as you please.

### Board scaling
* **Background image size:** specifies width and height of your background image in the viewport. By default, the edges are 0.8x3.2 units in size, corresponding to the size of 1x4 LEGO bricks. The default background image size is roughly the printable area of a 3x3 set of A4 sheets.
* **Background image offset:** This moves the background image in the viewport. This is useful when you want to align the background image with the graph's nodes and edges.
* **Scale factors:** These refer to the graph objects
  * **board size:** ?
  * **graph positions:** Multiply positions of all nodes, labels and edeges by this factor.
  * **node size:** This changes the size of the circles representing the nodes in the viewport. If you load images for the nodes, they are also affected by this. Press "apply to nodes" to set all nodes to the specified size.
  * **label font:** Here, you can specify a font (.ttf file path) to use for location labels and task card texts.
  * **label size:** Adjusts the font size used for location labels. Text size on task cards is separately defined in the task export mode.

## The viewport
If you've ever used matplotlib diagrams, The controls in the bottom left will be familiar - they are the same.
* The home button resets the view to the default position and zoom level.
* The left and right arrow buttons undo and redo your last view changes.
* Use the magnifying glass to zoom in and out. With left click, you can drag a rectangle to zoom in. With right click, you can drag a rectangle to zoom out.
* Use the four arrows to pan the view.
* The configure subplots button opens a menu where you can change the spacing between subplots (e.g. for the Graph analysis mode). You almost certainly won't need this.
* The save button can be used to save the current view as an image, but the resolution of that image will depend on your screen resolution, how much you zoom in and include more area than you may want. The intended way to export is the "Save img" button in the sidebar menu. This also exports the current view but does so hat higher resolution and with more suitable default settings.
* The bottom right corner shows the coordinates of the tip of your mouse cursor. If you hover over an image, it also shows the RGBA color values of the pixel under the cursor. Sometimes this appears with values between 0 and 1, sometimes between 0 and 255.

# Starting a project
recommendation: create a new project folder for your new map:
```
src
doc
projects
|- example_project
   |- mapmaker files
   |- reference images
   |- edge images
```

### GUI workflow
1. Click the load "Nodes" button underneath the large "Load Graph" button in the topmost section of the sidebar menu. This will create a new graph with example locations.
2. at the top of the sidebar, open the Graph Editor mode. This adds a new section to the bottom of the sidebar menu.
3. In the Graph Editor, you can add new nodes and edges between nodes. You can also click on edges or nodes to edit them. The selected node or edge will be highlighted in pink and a settings panel will open at the bottom of the sidebar. Here, you can change location names, edge color, etc.  
   Edges can be shortened, but not lengthened. To increase the length of an edge, you must delete it and add a new one.
4. save your graph frequently by pressing "Save Graph" in the sidebar.

### .txt file workflow (legacy)
This workflow allows you to create many nodes, edges and tasks at once by writing them in .txt files and loading them into the program. This is usually faster than creating them one by one in the GUI, but requires more planning ahead.
This is a legacy workflow that may not work perfectly anymore. Paths (=edges) as well as tasks can now be created in the GUI.

1. create `locations.txt` file: one location name per line. see `doc/example_files/locations.txt` for an example. You can also just load that file and change the location names in the GUI later.  
  *Linebreaks (via `\n`) are only partially supported and may cause issues.*
1. create `paths.txt` file: specified as `[location1] ; [location2] ; [length] ; [color]` one path per line. see `doc/example_files/paths.txt` for an example.  
  *location names must match those in `locations.txt` exactly.*  
1. create `tasks.txt` file: specified as `[location1] ; [location2]` one task per line. see `doc/example_files/tasks.txt` for an example.  
  *location names must match those in `locations.txt` exactly.*

Load locations first, then paths and tasks, each via the specific load buttons in the GUI, located underneath the large "Load Graph" button.

### Continue a project
Whenever you made notable progress, save your graph via the "Save Graph" button. This creates a .json file that contains all information about your graph, including paths to images and settings for the GUI. When you want to continue working on your map, load this .json file via the "Load Graph" button at the top of the sidebar menu.

### Create Task cards
Task cards often have a different aspect ratio from the main board. Therefore, you may need a separate background image for them. You can load this image via the "Background image" file input in the sidebar menu. Then, you can switch to Task Export mode and export each task as an individual image file for printing.

### Finish a project
When you are finished with your map, you can export it as an image via the "Save img" button in the sidebar menu. You can use an external image editing program to add a score track, a legend and other details to the exported image or to your background image before exporting.
Export your task cards via the Task Export mode as described above. There are options to export a single task card or export all of them. The latter can take several minutes.


To prepare your exported board and task cards for printing, there are two scripts that fit the images to the printable area of A4 sheets and add crop marks. For this, you need to have LaTeX installed on your computer.

#### `_split_board.py` 
Splits a large board image into multiple smaller images and creates a .tex and .pdf file to print them. Occasionally, the automatic LaTeX compilation doesn't work. In that case, you can compile the .tex file like any other LaTeX document.  
The `_split_board.py` script also takes into account the gaps that occur between printed sheets when they are glued onto separate parts of a folding board, specified as `inner_margin`.  
See `folding patterns.png` for recommended way to arrange multiple sheets of paper for a folding board. See `board_margins_overview.png` for an explanation of the board splitting margins.

#### `_prepare_task_cards.py`
This script takes as input a folder of task card images and a single backside image. Then, it creates a .tex and .pdf file to print the task cards. Each page contains 4 task cards that can be folded in the middle to create the full card.

### Usage notes
* There are some bugs regarding the edges (connections between nodes) where their internal values get messed up by some actions. Pressing "Repair Connection IDs" fixes this issue. "Show edge attractors" is a debug tool to see if a repair is necessary. If everything is working, this should show small arrows (or triangular arrow heads) that point from each end of an edge towards the nearest node or other edge. If you see any very long arrows, you should repair the connection IDs.

* Occasionally, there are other bugs. Many of these can be fixed by switching to another mode (e.g. Graph View) and back.

### What if I want to change x?
* Change size of **edge rectangles** (e.g. to fit 1x3 LEGO bricks, Catan road pieces or original TTR pieces): You can open the particle graph .json file and use the search and replace function of your text editor to find and replace the edge size values. For this, you want to modify the `"bounding_box_size"` attribute of all `Particle_Edge` objects. You can search for:
```
        "bounding_box_size": [
          3.36,
          0.96
        ],
```

---
---

## comments

default particle graph options are defined in `ttr_particle_graph.py/setup_project_dict()`