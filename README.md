# Fusion360 - DXF Exporter Addin

## What
An adding for Fusion 360 to allow users to quickly export all selected sketches as DXF files. All files will be saved in a single folder and named like the sketchname.

## Installing
Clone this repo locally and install the addin (folder DxfExporter) as instructed here: [How to install Scripts and Addins](https://rawgit.com/AutodeskFusion360/AutodeskFusion360.github.io/master/Installation.html)


## How to
1. Start the addin from the Add-ins menu. Once started a new button will appear in the Add-ins toolbar.
2. Select several sketches (either the sketches themselves, or the sketches folder to include all sketches in the  folder). Make sure to name your sketches appropriately since this will be the filename!
3. Click the new button 'Export DXF' from the dropdown menu.
4. A popup will appear to select a folder to save all the files. Simple select a folder.
5. Done, all sketches are saved as DXF's in that folder. You'll get a messagebox indicating it's done.

## Attention
- If the file allready exist, a new version will be created with an index appended: filename(index).dxf. So if you're exporting into the same folder twice, you should delete the contents first! This behaviour was implemented in case you have 2 sketches (from different components) with an identical name.
- With "select several sketches" I don't mean select them in your main view, but you need to select them in the object browser on the left!

## Changelog
- 0.0.1_beta: First release
