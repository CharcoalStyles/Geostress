import arcpy
import os

workspaceDirectory = "D:\\GeoStress"
dataFile = "D:\\GeoStress\data.csv"
localGDB = "GeoStress.gdb"

print("Geostress v1.0")

timings = []
tasks = []

timings.append(time.time())
tasks.append("Start")
print(tasks[-1])

tasks.append("Create file GDB")
print(tasks[-1])
arcpy.CreateFileGDB_management(workspaceDirectory, localGDB)
arcpy.env.workspace = workspaceDirectory + '\\' + localGDB
timings.append(time.time()) 

tasks.append("CSV to XYEventLayer")
print(tasks[-1])
arcpy.management.MakeXYEventLayer(dataFile, "long", "lat", "dataPoints")
timings.append(time.time())

tasks.append("XY to FeatureClass")
print(tasks[-1])
arcpy.management.CopyFeatures("dataPoints", "GeoStressPoints")
timings.append(time.time())

tasks.append("Buffer Feature")
print(tasks[-1])
arcpy.analysis.Buffer("GeoStressPoints", "GeoStressBuffer", "radius", "FULL", "ROUND", "NONE", None, "PLANAR")
timings.append(time.time())

tasks.append("Intersect Buffer")
print(tasks[-1])
arcpy.analysis.Intersect("GeoStressBuffer #", "GeoStressIntersect", "ALL", None, "INPUT")
timings.append(time.time())

tasks.append("Rasterize Intersect")
print(tasks[-1])
arcpy.conversion.FeatureToRaster("GeoStressIntersect", "Shape_Area", "GeoStressRaster", 0.01)
timings.append(time.time())

tasks.append("Create Random Raster")
print(tasks[-1])
arcpy.management.CreateRandomRaster(arcpy.env.workspace, "RandomRaster", "UNIFORM 0.0 1.0", "12333410.0177972 -5540366.58691725 17279891.5911963 -1008859.26216395", 750)
timings.append(time.time())

print("\n\nFinished!")
totalTime = timings[-1] - timings[0]
print("Total Time: " + str(totalTime))
print("------===========------")
print("Individual task times\n")
for i in range(1,len(timings)):
    taskTime = timings[i] - timings[i - 1]
    print("\t" + tasks[i] + " - \t" + str(taskTime))

print("------===========------")
print("Wiki table row\n")

print("|-")
print("|<CPU>")
print("|<RAM>")
print("|<HDD|SDD>")
for i in range(1,len(timings)):
    taskTime = timings[i] - timings[i - 1]
    print("|{0:.2f}".format(taskTime))
print("|{0:.2f}".format(totalTime))