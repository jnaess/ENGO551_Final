# ENGO551_Final

The result of the sequence shown in Figure 2 is an API response that farmers can use to see which assets accessed a field over a specified time period. When requested, the API performs the following query within the PostGIS database. 


SELECT asset_locations.asset_id


FROM asset_locations, fields


WHERE crop_type = '{field_type}' 


AND date BETWEEN '{start}'::timestamp AND '{end}'::timestamp 


AND ST_Contains(fields.geompoly, asset_locations.geompt) ;


This query allows the user to retrieve assets that have been within a field of a certain crop type within a set time duration. The following URL shows an example of the API to retrieve assets in pea fields from April 23 to April 26.


http://127.0.0.1:5000/api/assets_locations?start=2022-04-23%2000:00:00&end=2022-04-26%2000:00:00&field_type=peas&key=password


The API displays the resultant query in JSON format, in example, the response may look like:


{"asset_id":{"0":6,"1":6}}


Where the integer within the quotations represents the “nth” asset in the response, followed by that asset’s id number.
