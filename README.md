# POI_extractor

This small script can retrieve POI saved on Garmin devices as .fit files, and save them to a chosen format. 

*NOTE* : The datafields identification was found by deduction and by thinkering with the device.
The field identification codes for Garmin FIT POI file type seems to be proprietary, and I have only tested them on a Garmin edge device. 

**Usage**

    python POIextractor.py INPUT_FILE OUTPUT_FILE

The output format should be specified by the output file name extension.
