from meshiphi.dataloaders.vector.abstract_vector import VectorDataLoader

import logging
 
import xarray as xr


class BalticCurrentDataLoader(VectorDataLoader):
    def import_data(self, bounds):
        """
        Reads in current data from a copernicus baltic sea physics reanalysis NetCDF file.
        Renames coordinates to 'lat' and 'long', and renames variable to
        'uC, vC'

        Args:
            bounds (Boundary): Initial boundary to limit the dataset to

        Returns:
            xr.Dataset:
                Baltic currents dataset within limits of bounds.
                Dataset has coordinates 'lat', 'long', and variable 'uC', 'vC'
        """
        # Open Dataset
        if len(self.files) == 1:    data = xr.open_dataset(self.files[0])
        else:                       data = xr.open_mfdataset(self.files)

        # Reduce and drop unused depth dimension
        data = data.isel(depth=0)
        data = data.reset_coords(names="depth", drop=True)
        # Change column names
        data = data.rename({'latitude': 'lat',
                            'longitude': 'long',
                            'uo': 'uC',
                            'vo': 'vC'})

        # Trim to initial datapoints
        data = self.trim_datapoints(bounds, data=data)

        # Reduce along time dimension
        data = data.mean(dim="time")
        
        return data
