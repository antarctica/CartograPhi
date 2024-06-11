
import unittest
import copy
from meshiphi.mesh_generation.direction import Direction
from meshiphi.mesh_generation.neighbour_graph import NeighbourGraph
from meshiphi.mesh_generation.metadata import Metadata
from meshiphi.dataloaders.factory import DataLoaderFactory
from meshiphi.mesh_generation.cellbox import CellBox

from meshiphi.mesh_generation.boundary import Boundary


def create_ng_from_dict(ng_dict, global_mesh=False):
    ng = NeighbourGraph()
    ng.neighbour_graph = copy.deepcopy(ng_dict)
    ng._is_global_mesh = global_mesh

    return ng

class TestNeighbourGraph (unittest.TestCase):
    
    def setUp(self):
        
        # Cases to account for
        # 3x3 grid
        # 1x2
        # 1x2 on antimeridian
        # 1x(0.5+0.5)
        # global
        
        self.ng_dict_3x3 = {"1": {1: [ ], 2: [2], 3: [5], 4: [4], -1: [ ], -2: [ ], -3: [ ], -4: [ ]},
                            "2": {1: [ ], 2: [3], 3: [6], 4: [5], -1: [4], -2: [1], -3: [ ], -4: [ ]},
                            "3": {1: [ ], 2: [ ], 3: [ ], 4: [6], -1: [5], -2: [2], -3: [ ], -4: [ ]},
                            "4": {1: [2], 2: [5], 3: [8], 4: [7], -1: [ ], -2: [ ], -3: [ ], -4: [1]},
                            "5": {1: [3], 2: [6], 3: [9], 4: [8], -1: [7], -2: [4], -3: [1], -4: [2]},
                            "6": {1: [ ], 2: [ ], 3: [ ], 4: [9], -1: [8], -2: [5], -3: [2], -4: [3]},
                            "7": {1: [5], 2: [8], 3: [ ], 4: [ ], -1: [ ], -2: [ ], -3: [ ], -4: [4]},
                            "8": {1: [6], 2: [9], 3: [ ], 4: [ ], -1: [ ], -2: [7], -3: [4], -4: [5]},
                            "9": {1: [ ], 2: [ ], 3: [ ], 4: [ ], -1: [ ], -2: [8], -3: [5], -4: [6]}}
        
        # Non-global 3x3 Neighbour graph, "5" in the middle, with the others all surrounding it
        self.arbitrary_neighbour_graph = create_ng_from_dict(self.ng_dict_3x3)
        
        # 1x2 Neighbour graph, oriented E-W
        self.antimeridian_neighbour_graph = {"1":{1: [ ], 2: [2], 3: [ ], 4: [ ], -1: [ ], -2: [ ], -3: [ ], -4: [ ]},
                                             "2":{1: [ ], 2: [ ], 3: [ ], 4: [ ], -1: [ ], -2: [1], -3: [ ], -4: [ ]}}


    def test_from_json(self):

        ng = NeighbourGraph.from_json(self.ng_dict_3x3)

        self.assertIsInstance(ng, NeighbourGraph)
        self.assertEqual(ng.neighbour_graph, self.ng_dict_3x3)

    
    def test_increment_ids(self):
        
        increment = 10
        ng = create_ng_from_dict(self.ng_dict_3x3)
        ng.increment_ids(10)
        
        # Add 'increment' to nodes and neighbours stored within the neighbourgraph dict
        # Creates a dict of form {str(node + increment): {direction: [neighbours + increment]}}
        manually_incremented_dict = {
            str(int(node) + increment): {direction: [neighbour + increment for neighbour in neighbours] 
                                        for direction, neighbours in dir_map.items() 
            } for node, dir_map in self.ng_dict_3x3.items()
        }
        manually_incremented_ng = create_ng_from_dict(manually_incremented_dict)
        
        self.assertEqual(ng.get_graph(), manually_incremented_ng.get_graph())

    
    def test_get_graph(self):
        
        ng_dict = self.arbitrary_neighbour_graph.get_graph()
        self.assertEqual(ng_dict, self.ng_dict_3x3)
    
    def test_update_neighbour(self):
        
        node_to_update = "1"
        direction_to_update = 1
        updated_neighbours = [1,2,3,4,5]

        ng = create_ng_from_dict(self.ng_dict_3x3)
        ng.update_neighbour(node_to_update, direction_to_update, updated_neighbours)

        manually_updated_ng = copy.deepcopy(self.ng_dict_3x3)
        manually_updated_ng[node_to_update][direction_to_update] = updated_neighbours

        self.assertEqual(ng.get_graph(), manually_updated_ng)
    
    def test_add_neighbour(self):
        node_to_update = "1"
        direction_to_update = 1
        neighbour_to_add = 123

        ng = create_ng_from_dict(self.ng_dict_3x3)
        ng.add_neighbour(node_to_update, direction_to_update, neighbour_to_add)

        manually_added_ng_dict = copy.deepcopy(self.ng_dict_3x3)
        manually_added_ng_dict[node_to_update][direction_to_update].append(neighbour_to_add)

        self.assertEqual(ng.get_graph(), manually_added_ng_dict)
    
    def test_remove_node_and_update_neighbours(self):
        
        # node_to_remove = '5'

        # ng = create_ng_from_dict(self.ng_dict_3x3)
        # ng.remove_node_and_update_neighbours(node_to_remove)
        
        # manually_removed_ng_dict = copy.deepcopy(self.ng_dict_3x3)
        # for node, dir_map in manually_removed_ng_dict.items():
        #     for direction in dir_map.keys():
        #         if node_to_remove in node[direction]:
        #             node[direction].pop(node_to_remove)
        # manually_removed_ng_dict.pop(node_to_remove)

        # self.assertEqual(ng.get_graph(), manually_removed_ng_dict)


        ## I think there's a bug in remove_node_in_neighbours
        raise NotImplementedError
    
    def test_get_neighbours(self):
        dir_obj = Direction()

        for cb_index in self.ng_dict_3x3.keys():
            for direction in dir_obj.__dict__.values():
                ng_neighbours = self.arbitrary_neighbour_graph.get_neighbours(cb_index, direction)
                self.assertEqual(ng_neighbours, self.ng_dict_3x3[cb_index][direction])
    
    def test_add_node(self):

        index_to_add = '999'
        neighbour_map_to_add = {1: [123], 2: [234], 3: [345], 4: [456], -1: [567], -2: [678], -3: [789], -4: [890]}

        ng = create_ng_from_dict(self.ng_dict_3x3)
        ng.add_node(index_to_add, neighbour_map_to_add)

        manually_added_ng_dict = copy.deepcopy(self.ng_dict_3x3)
        manually_added_ng_dict[index_to_add] = neighbour_map_to_add

        self.assertEqual(ng.get_graph(), manually_added_ng_dict)
    
    def test_remove_node(self):

        index_to_remove = '5'
        ng = create_ng_from_dict(self.ng_dict_3x3)
        ng.remove_node(index_to_remove)

        manually_removed_ng_dict = copy.deepcopy(self.ng_dict_3x3)
        manually_removed_ng_dict.pop(index_to_remove)

        self.assertEqual(ng.get_graph(), manually_removed_ng_dict)
    
    def test_update_neighbours(self):
        ## I think there's a bug in remove_node_in_neighbours
        raise NotImplementedError
    
    def test_remove_node_from_neighbours(self):
        ## I think there's a bug in remove_node_in_neighbours
        raise NotImplementedError
    
    def test_update_corner_neighbours(self):
        raise NotImplementedError
    
    def test_get_neighbour_case_bounds(self):
        raise NotImplementedError
    
    def test_get_neighbour_case(self):
        raise NotImplementedError
    
    def test_get_global_mesh_neighbour_case(self):
        raise NotImplementedError
    
    def test_remove_neighbour(self):
        raise NotImplementedError
    
    def test_initialise_neighbour_graph(self):
        raise NotImplementedError
    
    def test_initialise_map(self):
        raise NotImplementedError
    
    def test_set_global_mesh(self):
        global_ng = create_ng_from_dict(self.ng_dict_3x3,    global_mesh=True)
        nonglobal_ng = create_ng_from_dict(self.ng_dict_3x3, global_mesh=False)

        self.assertTrue(global_ng._is_global_mesh)
        self.assertFalse(nonglobal_ng._is_global_mesh)

    def test_is_global_mesh(self):
        global_ng = create_ng_from_dict(self.ng_dict_3x3,    global_mesh=True)
        nonglobal_ng = create_ng_from_dict(self.ng_dict_3x3, global_mesh=False)

        self.assertTrue(global_ng.is_global_mesh())
        self.assertFalse(nonglobal_ng.is_global_mesh())
    
    def test_get_neighbour_map(self):
        ng = create_ng_from_dict(self.ng_dict_3x3)

        self.assertEqual(ng.get_neighbour_map("1"), self.ng_dict_3x3["1"])



   # def setUp(self):
   #       boundary = Boundary([-85,-80], [-135,-130], ['1970-01-01','2021-12-31'])
   #       cellbox = CellBox (boundary , 0)
   #       params = {
   #    'file': '../../datastore/bathymetry/GEBCO/gebco_2022_n-40.0_s-90.0_w-140.0_e0.0.nc',
	# 	'downsample_factors': (5,5),
	# 	'data_name': 'elevation',
	# 	'aggregate_type': 'MAX',
   #     'value_fill_types': "parent"
   #       }
   #       split_conds = {
	# 'threshold': 620,
	# 'upper_bound': 0.9,
	# 'lower_bound': 0.1
	# }
        
   #       gebco = DataLoaderFactory().get_dataloader('GEBCO', boundary , params, min_dp = 5)
   #       cellbox.set_data_source ([Metadata (gebco , [split_conds] ,  params ['value_fill_types'])])
   #       self.cellboxes = cellbox.split(0)
   #       cell_width = 2.5
   #       grid_width = (boundary.get_long_max() - boundary.get_long_min()) / cell_width
   #       self.neighbour_graph = NeighbourGraph (self.cellboxes ,grid_width )
         

   # def test_initialize_NG(self):
   #    self.assertEqual ( 4 , len (self.neighbour_graph.get_graph()))
   #    self.assertEqual ( {1: [3], 2: [1], 3: [], 4: [], -1: [], -2: [], -3: [], -4: [2]} , self.neighbour_graph.get_graph()[0]) # NW cellbox
   #    self.assertEqual ( {1: [], 2: [], 3: [], 4: [], -1: [], -2: [0], -3: [2], -4: [3]} , self.neighbour_graph.get_graph()[1]) # NE cellbox
   #    self.assertEqual ( {1: [], 2: [3], 3: [1], 4: [0], -1: [], -2: [], -3: [], -4: []} , self.neighbour_graph.get_graph()[2]) # SW cellbox
   #    self.assertEqual ( {1: [], 2: [], 3: [], 4: [1], -1: [0], -2: [2], -3: [], -4: []} , self.neighbour_graph.get_graph()[3]) # SE cellbox

   
   # def test_remove_neighbour (self):
   #    self.neighbour_graph.remove_neighbour(0 ,  Direction.east , 1)
   #    self.assertEqual ( {1: [3], 2: [], 3: [], 4: [], -1: [], -2: [], -3: [], -4: [2]} , self.neighbour_graph.get_graph()[0]) # NW cellbox
   #    self.neighbour_graph.update_neighbour(0 , Direction.east , [1]) # undo the remove

   # def test_update_neighbour (self):
   #    self.neighbour_graph.update_neighbour(0 ,  Direction.south_east , [3])
   #    self.assertEqual ( {1: [3], 2: [1], 3: [3], 4: [], -1: [], -2: [], -3: [], -4: [2]} , self.neighbour_graph.get_graph()[0]) # NW cellbox
   #    self.neighbour_graph.remove_neighbour(0 ,  Direction.south_east , 3)# undo the update
  
   # def test_get_neighbour_case(self):
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[0] , self.cellboxes[1])
   #    self.assertEqual ( 2, case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[0] , self.cellboxes[2])
   #    self.assertEqual ( 4, case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[0] , self.cellboxes[3])
   #    self.assertEqual (3 , case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[2] , self.cellboxes[0])
   #    self.assertEqual ( -4, case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[1] , self.cellboxes[2])
   #    self.assertEqual ( -1, case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[2] , self.cellboxes[1])
   #    self.assertEqual ( 1, case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[3] , self.cellboxes[0])
   #    self.assertEqual ( -3, case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[3] , self.cellboxes[2])
   #    self.assertEqual ( -2, case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[3] , self.cellboxes[1])
   #    self.assertEqual ( -4, case)
   #    case = self.neighbour_graph.get_neighbour_case(self.cellboxes[1] , self.cellboxes[3])
   #    self.assertEqual ( 4, case)

   # def test_update_neighbours (self):
   #    self.neighbour_graph.update_neighbours(0, [2,1], Direction.north_east, self.cellboxes)
   #    self.assertEqual (  {1: [], 2: [], 3: [], 4: [1], -1: [], -2: [2,2], -3: [], -4: [1]} , self.neighbour_graph.get_graph()[3]) # SE cellbox
   #    self.neighbour_graph.update_neighbour(3, Direction.south, [1]) # undo the first update 
   #    self.neighbour_graph.update_neighbour(3, Direction.west, [2]) # undo the first update 
   #    self.neighbour_graph.update_neighbour(3, Direction.north, []) # undo the first update 
  
   # def test_update_corner_neighbours(self):
   #    self.neighbour_graph.update_corner_neighbours (3 , -1, -1, -1, -1 )
   #    self.assertEqual ( {1: [-1], 2: [1], 3: [], 4: [], -1: [], -2: [], -3: [], -4: [2]} , self.neighbour_graph.get_graph()[0]) # SE cellbox
