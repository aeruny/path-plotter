from data_plotter import DataPlotter

file = "../data/hostageLocations.txt"
size = [-1000, 1000]
connect_dots = True

# Instantiate the plotter
plotter = DataPlotter(file, size, connect_dots)

print(plotter.coordinates)

# Plot Data
#  Note that Unity's default coordinate system is where:
#  x-axis represents the horizontal distance
#  y-axis represents the vertical distance (height)
#  z-axis represents the depth
#  so a top-down perspective is represented in an xz-plane
plotter.plot2D()
plotter.plot3D()
