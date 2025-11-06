"""Convert a VTU file to STL format using VTK."""

import vtk

if __name__ == "__main__":
    # Input and output file paths
    input_file = "/workspace/inputfiles/sample.vtu"
    output_file = "/workspace/output/sample_vtu.stl"

    # Read the VTU file
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(input_file)
    reader.Update()

    # Extract geometry
    geometry = vtk.vtkGeometryFilter()
    geometry.SetInputData(reader.GetOutput())
    geometry.Update()

    # Write STL file
    writer = vtk.vtkSTLWriter()
    writer.SetInputData(geometry.GetOutput())
    writer.SetFileName(output_file)
    writer.Write()

    print(f"Converted {input_file} to {output_file}")
