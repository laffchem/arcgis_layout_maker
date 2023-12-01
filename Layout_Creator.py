import json
aprx = arcpy.mp.ArcGISProject("CURRENT")
mapx = aprx.listMaps()[0]
lyt = aprx.listLayouts()

#Ensure this value is "Parcel_"
lyt = lyt[1]
print(lyt)
print(lyt.name)

lyr = mapx.listLayers("Parcel")[0]
print(lyr.name)
mf = lyt.listElements("MAPFRAME_ELEMENT")[0]
print(mf.name)





program_running = True
while program_running:
    parcel_id = input('Enter the parcel id for the utility availability request.\n')

    if len(parcel_id) == 15:
        try:
            parcel_id = int(parcel_id)
        except ValueError:
            print(f"Error: Your entry: '{parcel_id}' is invalid. You need to enter a 15 numeric character parcel id.")
        else:
            parcel_ids = str(parcel_id)
            print('Creating map...')
            program_running = False
    else:
        print(f"Input error... Your entry: '{parcel_id}' needs to be 15 numeric characters.")

lyr.definitionQuery = f"PARCEL = '{parcel_id}'"
desired_scale = input('What scale would you like the map to be?\n')


lyr_extent = mf.getLayerExtent(lyr)
mf.camera.setExtent(lyr_extent)
mf.camera.scale = float(desired_scale)
print(mf.camera.scale)

# Change the title
title = lyt.listElements("TEXT_ELEMENT", "Title")[0]
title.text = f'Utility Availability Request\nParcel ID: {parcel_id}'
parcel_layoutCIM = lyt.getDefinition("V3")
divisionUnit = float(desired_scale) / 24

for elm in parcel_layoutCIM.elements:
    if elm.name == "Scale Bar":
        elm.division = divisionUnit
        print(elm.division)
lyt.setDefinition(parcel_layoutCIM)

lyt.exportToPDF(out_pdf=f"C:\\Projects\\Utilities Availability Requests\\Completed\\Parcel_{parcel_id}.pdf")



lyr.definitionQuery = None
print('Run through the code again to create a new layout.')


