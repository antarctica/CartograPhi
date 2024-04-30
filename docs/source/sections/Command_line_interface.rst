###############################
Command Line Interface
###############################

The MeshiPhi package provides CLI entry points, used to build a digital environment from a heterogeneous collection of
source data. This digital environment file (mesh) can then be exported to a variety of file formats for use in other
systems, such as GIS software. The produced mesh file also interfaces directly with `PolarRoute <https://github.com/antarctica/PolarRoute>`_,
BAS's route planning software, to provide optimal routes for a vehicle travelling through the mesh.

^^^^^^^^^^^
create_mesh
^^^^^^^^^^^

The *create_mesh* entry point builds a digital environment file from a collection of source data, which can then be saved
to a file for visualisation or use in other software.

::

    create_mesh <config.json>

positional arguments:

::

    config : A configuration file detailing how to build the digital environment. JSON parsable

The format of the required *<config.json>* file can be found in the :ref:`configuration - mesh construction` section of the documentation.
There are also example configuration files available in the directory :code:`examples/environment_config/grf_example.config.json` on GitHub.

optional arguments:

::

    -v (verbose logging)
    -o <output location> (set output location for mesh)


The format of the returned mesh.json file is explain in :ref:`the mesh.json file` section of the documentation.



^^^^^^^^^^^
export_mesh
^^^^^^^^^^^
Once a mesh has been built using the :ref:`create_mesh` command, it can be exported other file types for 
use in other systems (such as GIS software) using the the *export_mesh* command.

::

    export_mesh <mesh.json> <output_location> <output_format> 

positional arguments:

::

    mesh : A digital environment file.
    output_location : The location to save the exported mesh.
    output_format : The format to export the mesh to.


supported output formats are:
  * .json (default) [JSON]
  * geo.json (collection of polygons for each cell in the mesh) [GEOJSON]
  * .tif (rasterised mesh) [TIF]
  * .png [PNG]

optional arguments:

::

    -v : verbose logging
    -o : output location
    -format_conf: configuration file for output format (required for TIF export, optional for GEOJSON)

an example of the format of the *<format_conf.json>* file required for .tif export is as follows:

::

    {
        "data_name": "elevation",
        "sampling_resolution": [
            150,
            150
        ],
        "projection": "3031",
        "color_conf": "path to/color_conf.txt"
    }

where the variables are as follows:
  * **data_name** : The name of the data to be exported. This is the name of the data layer in the mesh.
  * **sampling_resolution** : The resolution of the exported mesh. This is a list of two values, the first being the x resolution and the second being the y resolution.
  * **projection** : The projection of the exported mesh. This is a string of the EPSG code of the projection.
  * **color_conf** : The path to the color configuration file. This is a text file containing the color scheme to be used when exporting the mesh. The format of this file is as follows:
                                    
::

    0 240 250 160  
    30 230 220 170  
    60 220 220 220 
    100 250 250 250 

The color_conf.txt contains 4 columns per line: the data_name value and the 
corresponding red, green, blue value between 0 and 255.

When using the *-format_conf* option for GEOJSON output the only variable required is the **data_name**. This specifies
which of the data layers you want to export as a single GEOJSON file.

^^^^^^^^^^^^
rebuild_mesh
^^^^^^^^^^^^

Once a mesh has been built using the :ref:`create_mesh` command the *rebuild_mesh* command allows a user to rebuild it based on the
original configs stored within the mesh file. This is primarily useful for debugging or to update old meshes produced with an older version
of the package.

::

    rebuild_mesh <mesh.json>

optional arguments:

::

    -v : verbose logging
    -o : output location


^^^^^^^^^^^^^^
merge_mesh
^^^^^^^^^^^^^^

When multiple compatilble meshes have been created using the :ref:`create_mesh` command, they can be merged together using the :ref:`merge_mesh` command.
This will combine the meshes into a single mesh file, replacing cellboxes in mesh1 with cellboxes in mesh2 where they overlap.


::

    merge_mesh <mesh1.json> <mesh2.json>

positional arguments:

::

    mesh1 : A digital environment file.
    mesh2 : A digital environment file.
   
optional arguments:

::

    -v : verbose logging
    -o : output location


^^^^^^^^^^^^^^^^^^^^^
plot_mesh (GeoPlot)
^^^^^^^^^^^^^^^^^^^^^
Meshes produced at any stage in the route planning process can be visualised using the GeoPlot 
library found at the relevant `GitHub page <https://github.com/antarctica/GeoPlot>`_. Meshes and routes can also be
plotted in other GIS software such as QGIS or ArcGIS by exporting the mesh to a common format such as .geojson or .tif
using the :ref:`export_mesh` command.

::

    plot_mesh <mesh.json>

optional arguments:

:: 
    
        -v : verbose logging
        -o : output location
