# Tom Tom API

This folder contains code to help you make API calls to TomTom to collect historic traffic information. 

The [AreaAnalysisApi.ipynb](AreaAnalysisApi.ipynb) notebook allows us to collect information about traffic volumes across all segments of the DFW network over the course of a day.

The [RouteAnalysisApi.ipynb](RouteAnalysisApi.ipynb) lets us query for information about how a particular route behaved (in terms of travel time) over the course of a day.

[CurbsideVolumeBreakdown.ipynb](CurbsideVolumeBreakdown.ipynb) uses a series of segment ids from *Tom Tom* to determine how many unique vehicles passed over a curb in a given hour.

The [CombineAreaAnalysisFiles.ipynb](CombineAreaAnalysisFiles.ipynb) notebook combines a collection of separate *geojson* files into one combined file.  This combined data may be visualized:

        https://observablehq.com/@mqueen-nrel/tomtom-area-analysis-api.

## Helpful links
[Tom Tom API Documentation](https://developer.tomtom.com/traffic-stats/traffic-stats-apis) Use the menu on the left to delve into the various APIs.
