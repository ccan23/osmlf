# OSMLF
Version 0.0.1

OpenStreetMap Location Features is a Python library that utilizes the OpenStreetMap (OSM) database and Overpass API to retrieve location features and perform various calculations based on the given location. It allows you to extract information about amenities, landuse, leisure, tourism, natural features, highways, railways, and waterways for a specified location.

The following are keys provided by OpenStreetMap (OSM). Each link is a reference to the official OSM Wiki.
* Amenities: https://wiki.openstreetmap.org/wiki/Key:amenity
* Landuse  : https://wiki.openstreetmap.org/wiki/Key:landuse
* Leisure  : https://wiki.openstreetmap.org/wiki/Key:leisure
* Tourism  : https://wiki.openstreetmap.org/wiki/Key:tourism
* Natural  : https://wiki.openstreetmap.org/wiki/Key:natural
* Highway  : https://wiki.openstreetmap.org/wiki/Key:highway
* Railway  : https://wiki.openstreetmap.org/wiki/Key:railway
* Waterway : https://wiki.openstreetmap.org/wiki/Key:waterway

### Important Note: 
The images included in this README file are taken from the Overpass API. While these images represent the responses of queries used in this module, it should be noted that this module does not return any visual content; it only provides the corresponding response data.
## Requirements
```sh
certifi==2023.5.7
geographiclib==2.0
geopy==2.3.0
numpy==1.25.0
overpy==0.6
pyproj==3.6.0
shapely==2.0.1
```
## Usage
Here's examples
```py
# Import the osmlf module
>>> from osmlf import osmlf
```

For example let's look New York City, USA. osmlf will find best result from given location automatically
```py
>>> lf = osmlf('New York City, USA')
>>> lf
osmlf(City of New York, New York, United States)
```
### Default Values
Here are the default values for each key. These are the values that are checked when the key parameter in the relational method's parameter is left blank by the user. You can access and modify these default values if needed:
```py
>>> lf.default_values
{
    'amenity': [
        'bar', 'cafe', 'fast_food', 'food_court', 'pub', 'restaurant',
        'college', 'library', 'school', 'university', 'atm', 'bank',
        'clinic', 'dentist', 'doctors', 'hospital', 'pharmacy', 'veterinary',
        'cinema', 'conference_centre', 'theatre', 'courthouse', 'fire_station',
        'police', 'post_office', 'townhall', 'marketplace', 'grave_yard'
    ],
    'landuse': ['forest', 'residential', 'commercial', 'industrial', 'farming'],
    'leisure': ['marina', 'garden', 'park', 'playground', 'stadium'],
    'tourism': [
        'aquarium', 'artwork', 'attraction', 'hostel', 'hotel', 
        'motel', 'museum', 'theme_park', 'viewpoint', 'zoo'
    ],
    'natural': ['beach'],
    'highway': [
        
    ],
    'railway': ['platform', 'station', 'stop_area'],
    'waterway': []
}
```

### Administrative
Retrieves and returns administrative information about the location from the Overpass API.

**Note:** The total_area variable is expressed in square kilometers.
```py
>>> admin = lf.administrative()
>>> admin
{
    'core': (40.7127281, -74.0060152),
    'subareas': {
        'total_subareas': 5,
        'subarea_relation_ids': [
            8398124,
            9691750,
            9691819,
            9691916,
            9691948
        ]
    },
    'total_area': 1147.9149733707309
}
```
![New York City with subareas](docs/new_york_city_administrative.png)

### Amenity
Let's examine the amenities in the Financial District, Manhattan:
```py
>>> lf = osmlf('Financial District, Manhattan, New York')
>>> lf
osmlf(Financial District, Manhattan, New York County, City of New York, New York, United States)

# Search with default amenity values
>>> amenity = lf.amenity()
>>> amenity.keys()
dict_keys(['nodes', 'ways'])
```
Nodes represent locations with a single latitude and longitude pair. Most often, nodes represent smaller areas, such as banks, cafes, bars, restaurants, etc.

Ways, on the other hand, represent areas with multiple latitude and longitude pairs. They usually represent relatively large areas like hospitals, schools, government buildings, etc.

![Financial District Amenities](docs/financial_district_amenities.png)

```py
>>> amenity['nodes'].keys()
dict_keys(['bar', 'cafe', 'fast_food', 'food_court', 'pub', 'restaurant', 'college', 'library', 'school', 'university', 'atm', 'bank', 'clinic', 'dentist', 'doctors', 'hospital', 'pharmacy', 'veterinary', 'cinema', 'conference_centre', 'theatre', 'courthouse', 'fire_station', 'police', 'post_office', 'townhall', 'marketplace', 'grave_yard'])
```
For example, let's examine the bars in the Financial District. To do this, we must check both nodes and ways keys:

```py
# Number of bars in Financial District
>>> len(amenity['nodes']['bar'])
11

# Lets check first bar in that list
>>> amenity['nodes']['bar'][0]
{
    'id': 3450976122,
    'tags': {'addr:city': 'New York',
        'addr:housenumber': '36',
        'addr:postcode': '10004',
        'addr:state': 'NY',
        'addr:street': 'Water Street',
        'alt_name': 'Porterhouse Bar',
        'amenity': 'bar',
        'name': 'The Porterhouse Brew Co',
        'opening_hours': 'Mo-Fr 11:00-22:00',
        'outdoor_seating': 'yes',
        'website': 'http://www.zigolinis.com',
        'wheelchair': 'no'},
    'coordinate': (40.703439, -74.0106749)
}
```
In this example, we retrieve all the information available from the Overpass API. There are 11 bars in the Financial District represented as nodes. Let's check if there are any bars represented as way objects:

```py
>>> amenity['ways']['bar']
{'ways': [], 'way_count': 0, 'total_area': 0}   # Empty result
```

Now, let's examine the hospitals in the Financial District.

Unfortunately, we can't see the number of way objects using the len function. The number of ways is returned in the way_count key in the dictionary.

**Note:** This is a known issue that will be fixed in the future.
```py
# Number of hospitals as nodes
>>> len(amenity['nodes']['hospital'])
0

# Number of hospitals as ways
>>> amenity['ways']['hospital']['way_count']
1

# Get all the hospitals
>>> amenity['ways']['hospital']
{
    'ways': [
        {
            'way_id': 799488173,
            'tags': {'amenity': 'hospital',
                'beds': '132',
                'building': 'yes',
                'healthcare': 'hospital',
                'name': 'NewYork-Presbyterian Lower Manhattan Hospital',
                'wikidata': 'Q7013458'
            },
            'coordinates': [
                (40.7108086, -74.0050874),
                (40.7102038, -74.0044209),
                (40.7101336, -74.0045362),
                (40.7101256, -74.0045289),
                (40.7101041, -74.0045094),
                (40.7098032, -74.0048554),
                (40.7103763, -74.0054502),
                (40.7104325, -74.0055085),
                (40.7104501, -74.0054787),
                (40.7106556, -74.0051304),
                (40.7107336, -74.0052148),
                (40.7108086, -74.0050874)
            ],
           'area': 0.004740726486962053
        }
    ],
 'way_count': 1,
 'total_area': 0.004740726486962053
}
```

In this example, amenity information is fetched using default keys, but you could also specify the keys like so:

```py
# Get bars only
>>> bars = lf.amenity('bar')

# Get hospitals only
>>> hospitals = lf.amenity('hospital')

# Get bars and hospitals both at the same time
>>> multiple_amenities = lf.amenity(['bar', 'hospital']) # TODO: Use *args
```

**Note:** The amenity function works the same way with the landuse, leisure, tourism, natural, railway, and waterway functions. The only difference is the highway function.

### Landuse
Retrieves landuse information about the location from the Overpass API

```py
# Amsterdam
>>> lf = osmlf('Amsterdam, Netherlands')
>>> lf
osmlf(Amsterdam, Noord-Holland, Nederland)

# Get general info (administrative) of Amsterdam
>>> admin = lf.administrative()
>>> admin
{
    'core': (52.3730796, 4.8924534), 
    'subareas': {
        'total_subareas': 0, 
        'subarea_relation_ids': []
    }, 
    'total_area': 184.6089486197638
}
```
When examining a relatively large area like Amsterdam, the landuse function can return a large amount of data, which can sometimes be challenging to process. To manage this, let's first fetch only the residential landuses instead of using the default keys, which would fetch all landuses at once.
```py
# Residential areas of Amsterdam
>>> residential = lf.landuse('residential')
```
![Residential Areas of Amsterdam](docs/amsterdam_residential_areas.png)
```py
>>> residential.keys()
dict_keys(['nodes', 'ways'])

# No nodes for residential
>>> residential['nodes']
{'residential': []}

# Number of residential areas
>>> residential['ways']['residential']['way_count']
192

# Total area of residential areas in square kilometers
>>> residential['ways']['residential']['total_area']
57.0395957478018
```
To retrieve the first residential area among the 192 areas:

```py
# Get first residential area
>>> residential['ways']['residential']['ways'][0]
{
    'way_id': 6337974, 
    'tags': {
        'landuse': 'residential'
    }, 
    'coordinates': [
        (52.3873421, 4.7586896), (52.3873206, 4.7586027), (52.3872219, 4.7584746), 
        (52.3866635, 4.75788), (52.3864955, 4.7576667), (52.3863743, 4.757529), 
        (52.386242, 4.7574293), (52.3860862, 4.7573364), (52.3858845, 4.7572697), 
        (52.385709, 4.757234), (52.385652, 4.7574567), (52.3854924, 4.7581755), 
        (52.3851405, 4.7585499), (52.3849747, 4.7587018), (52.3848464, 4.7587884), 
        (52.3846829, 4.7588023), (52.3845282, 4.7588045), (52.3844951, 4.7587922), 
        (52.3844981, 4.7588234), (52.3845006, 4.7588549), (52.3845013, 4.7588649), 
        (52.3845012, 4.7588741), (52.3845008, 4.7588833), (52.384499, 4.7588903), 
        (52.3844969, 4.7588936), (52.3844944, 4.7588953), (52.3844892, 4.7589017),
        (52.3844685, 4.7589349), (52.3844671, 4.7589385), (52.3844668, 4.7589431), 
        (52.3844451, 4.7589556), (52.3843481, 4.7589603), (52.3842382, 4.7589889),
        (52.3842136, 4.7589874), (52.3841915, 4.7589649), (52.3841589, 4.7588225), 
        (52.383, 4.7588), (52.3826, 4.7586), (52.3818, 4.7589), 
        (52.3807655, 4.7567289), (52.3801312, 4.7558144), (52.3798, 4.755), 
        (52.3808, 4.7532), (52.3816, 4.7514), (52.382, 4.7506), 
        (52.3824794, 4.7500095), (52.3826319, 4.7498799), (52.3832, 4.7499), 
        (52.3842501, 4.7499516), (52.3842911, 4.7497662), (52.38449, 4.7499965), 
        (52.384483, 4.750057), (52.3845537, 4.7501347), (52.3845904, 4.7501106), 
        (52.3847177, 4.7500748), (52.3847762, 4.7500795), (52.3848649, 4.7502082),
        (52.3848693, 4.750215), (52.384874, 4.7502226), (52.3849298, 4.7503128), 
        (52.3849465, 4.7503394), (52.384978, 4.7503975), (52.3849832, 4.7504213), 
        (52.3849919, 4.7504401), (52.3850028, 4.7504572), (52.3850106, 4.7504758), 
        (52.3850236, 4.7505078), (52.3850305, 4.7505329), (52.3850346, 4.7505578),
        (52.3850667, 4.7506094), (52.3850853, 4.7506021), (52.3851002, 4.7505518),
        (52.3852322, 4.7506344), (52.3852225, 4.7506759), (52.3852483, 4.7507373),
        (52.3852518, 4.7507611), (52.3852675, 4.750849), (52.3852746, 4.7509073),
        (52.3852804, 4.7509674), (52.3852878, 4.7510422), (52.38529, 4.7510516), 
        (52.3853052, 4.7510889), (52.3853194, 4.7511319), (52.3861569, 4.7519683), 
        (52.3871396, 4.7527243), (52.3883416, 4.7534281), (52.3881, 4.7549), 
        (52.3876, 4.7573), (52.3873421, 4.7586896)
    ], 
    'area': 0.39929878337602165
}
```

In this example, we're only showing residential areas, but landuse can fetch more than just residential areas—it can also fetch forests, commercial areas, industrial areas, farming areas, etc.

For example:

```py
# Get total area of forest, meadow and grass in Amsterdam
# It will take some time
>>> landuse = lf.landuse(['forest', 'meadow', 'grass'])

# Show keys
>>> landuse['ways'].keys()
dict_keys(['forest', 'meadow', 'grass'])

# Forest area in square kilometers
>>> landuse['ways']['forest']['total_area']
9.608440158531183

# Meadow area in square kilometers
>>> landuse['ways']['meadow']['total_area']
10.776521682770907

# Grass area in square kilometers
>>> landuse['ways']['grass']['total_area']
31.5818360868127
```
![Amsterdam Forest Meadow Grass](docs/amsterdam_forest_grass_meadow.png)

### Tourism
Retrieves tourism information about the location from the Overpass API.
```py
>>> lf = osmlf('Venice, Italy')
>>> lf
osmlf(Venezia, Veneto, Italia)

>>> tourism = lf.tourism()

# The iconic Campanile di San Marco
>>> tourism['ways']['attraction']['ways'][31]
{
    'way_id': 252637693,
    'tags': {
        'building': 'yes',
        'height': '98.6',
        'historic': 'yes',
        'man_made': 'tower',
        'name': 'Campanile di San Marco',
        'name:be': 'Кампаніла сабора Святога Марка',
        'name:ca': 'Campanar de Sant Marc',
        'name:de': 'Markusturm',
        'name:en': "St Mark's Campanile",
        'name:eo': 'Kampanilo de Sankta Marko',
        'name:es': 'Campanile de San Marcos',
        'name:fr': 'Campanile de Saint-Marc',
        'name:he': 'הקמפנילה של סן מרקו',
        'name:it': 'Campanile di San Marco',
        'name:ja': '鐘楼（サンマルコ広場）',
        'name:ko': '산마르코의 종탑',
        'name:pl': 'Dzwonnica św. Marka',
        'name:pt': 'Campanário de São Marcos',
        'name:ro': 'Campanila San Marco',
        'name:ru': 'Кампанила собора Святого Марка',
        'name:th': 'หอระฆังซันมาร์โก',
        'name:tr': "Aziz Mark'ın Çan kulesi",
        'name:uk': 'Кампаніла собору святого Марка',
        'name:vec': 'Canpanièl de San Marco',
        'name:zh': '圣马可钟楼',
        'tourism': 'attraction',
        'tower:construction': 'brick',
        'tower:height': '95',
        'tower:type': 'bell_tower',
        'wheelchair': 'yes',
        'wikidata': 'Q754194',
        'wikipedia': 'it:Campanile di San Marco',
        'wikipedia:fr': 'Campanile de Saint-Marc'
    },
    'coordinates': [
        (45.4340712, 12.3389421),
        (45.4340844, 12.3389951),
        (45.4340901, 12.3389922),
        (45.434095, 12.3390124),
        (45.4340894, 12.3390152),
        (45.4341083, 12.3390916),
        (45.434001, 12.3391464),
        (45.4339639, 12.338997),
        (45.4340712, 12.3389421)
    ],
    'area': 0.0001583511784691957
}
```

The data also includes information on hotels. For example, the number of hotels can be retrieved with:

```py
>>> len(tourism['nodes']['hotel']) # Hotels node object
328

>>> tourism['ways']['hotel']['way_count'] # Hotels way object
30

# First element of hotel in nodes
>>> tourism['nodes']['hotel'][0]
{
    'id': 313715870,
    'tags': {
        'addr:housenumber': '29',
        'addr:place': 'Isola Torcello',
        'addr:postcode': '30142',
        'amenity': 'restaurant',
        'check_date:opening_hours': '2022-09-26',
        'name': 'Locanda Cipriani',
        'opening_hours:signed': 'no',
        'tourism': 'hotel'
    },
    'coordinate': (45.4978252, 12.4179196)
}

# First element of hotel in ways
>>> tourism['ways']['hotel']['ways'][0]
{
    'way_id': 60996087,
    'tags': {
        'addr:city': 'Lido di Venezia',
        'addr:housenumber': '41',
        'addr:postcode': '30126',
        'addr:street': 'Lungomare Guglielmo Marconi',
        'internet_access': 'wlan',
        'internet_access:fee': 'no',
        'name': 'Hotel Excelsior Venice',
        'stars': '5',
        'tourism': 'hotel',
        'wikidata': 'Q1542590'
    },
    'coordinates': [(
        45.4045649, 12.3668121),
        (45.4038431, 12.3661057),
        (45.4037498, 12.3662666),
        (45.403303, 12.365826),
        (45.4033521, 12.3656791),
        (45.4032686, 12.3655952),
        (45.4031311, 12.3659029),
        (45.4043489, 12.3671408),
        (45.4044618, 12.3668611),
        (45.4045158, 12.366917),
        (45.4045649, 12.3668121)
    ],
    'area': 0.004546061610650756
}
```
![Venice Tourism](docs/venice_tourism.png)

### Natural
This function retrieves natural feature information about the location from the Overpass API. The default value for the natural key is beach.

```py
>>> lf = osmlf('Fethiye, Mugla, Turkey')
>>> lf
osmlf(Fethiye, Muğla, Ege Bölgesi, Türkiye)

>>> natural = lf.natural()

# Number of beaches in Fethiye
>>> len(natural['nodes']['beach']) # Beaches as node object
5

# Get the first beach node object
>>> natural['nodes']['beach'][0]
{
    'id': 769903797,
    'tags': {
        'fee': 'yes',
        'name': 'Sun City Beach',
        'natural': 'beach',
        'surface': 'sand'
    },
    'coordinate': (36.5555012, 29.1067139)
}

# Get the first beach way object
>>> natural['ways']['beach']['ways'][0]
{
    'way_id': 87294614,
    'tags': {
        'access': 'yes',
        'fee': 'yes',
        'name': 'Kıdrak Plajı',
        'name:en': 'Kıdrak Beach',
        'name:ru': 'Кидрак пляж',
        'natural': 'beach',
        'source': 'Bing'
    },
    'coordinates': [
        (36.5282195, 29.1274236),
        (36.5283159, 29.1275884),
        (36.5286952, 29.1279593),
        (36.5287867, 29.1279884),
        (36.5290436, 29.1280701),
        (36.5297094, 29.1281279),
        (36.5303753, 29.1280027),
        (36.5309869, 29.127757),
        (36.5313553, 29.1277077),
        (36.5313843, 29.1280615),
        (36.5315474, 29.1280792),
        (36.5320484, 29.1279282),
        (36.5321612, 29.1276559),
        (36.5322553, 29.127576),
        (36.5321443, 29.126832),
        (36.5319627, 29.1264458),
        (36.5310326, 29.1270217),
        (36.5299757, 29.1273724),
        (36.529036, 29.1274781),
        (36.5282195, 29.1274236)
    ],
    'area': 0.030907790857999908
}
```
![Fethiye Beach](docs/fethiye_beach.png)

### Highway
Highways function a bit differently compared to other functions. For instance, unlike the tourism function where we can search for the hotel key, in the highway function we can't find tags by keys because it only lists the items.
```py
>>> lf = osmlf('sodermalm, stockholm, sweden')
>>> lf
osmlf(Södermalm, Södermalms stadsdelsområde, Stockholm, Stockholms kommun, Stockholms län, Sverige)
```

The total_length key provides the total length of every road listed in info in kilometers.

```py
# Get highway information
>>> highway = lf.highway()

>>> highway.keys()
dict_keys(['total_length', 'info'])
```
`total_lenght` is total length of every road in `info` in kilometers

![Stockholm Highway](docs/stockholm_highways.png)

```py
# Get total length of all roads returned in kilometers
>>> highway['total_length']
279.45176280917764
```

In the info list, we have details about every road. We can filter by type, such as motorways, pedestrian, residential roads, etc.

```py
# Get residential roads
>>> residential = lf.highway('residential')

# Total length of residential
>>> residential['total_length']
58.977220710878655

# Get first residential road in list
>>> residential['info'][0]
{
    'tags': {
        'highway': 'residential',
        'maxspeed': '30',
        'name': 'Hornsgatan',
        'surface': 'asphalt',
        'wikidata': 'Q3140664',
        'wikipedia': 'sv:Hornsgatan'
    },
    'coordinates': [
        (59.3148503, 18.0316059),
        (59.3150171, 18.0318446),
        (59.315038, 18.031897),
        (59.3150498, 18.0319613),
        (59.3152164, 18.0333084)
    ],
    'length': 0.10962269653879471
}
```
### Railway
Retrieves railway information about the location from the Overpass API.
```py
>>> lf = osmlf('Moscow, Russia')
>>> lf
osmlf(Москва, Центральный федеральный округ, Россия)

>>> railway = lf.railway()


>>> railway.keys()
dict_keys(['nodes', 'ways'])

# Number of stations
>>> len(railway['nodes']['station'])
312

# Get first station
>>> railway['nodes']['station'][0]
{
    'id': 26999673,
    'tags': {
        'alt_name': 'Москва-Октябрьская',
        'esr:user': '060073',
        'loc_name': 'Москва-Ленинградская',
        'loc_name:website': 'http://www.tutu.ru/station.php?nnst=79310',
        'name': 'Москва-Пассажирская',
        'nat_name': 'Москва',
        'network': 'РЖД',
        'official_name': 'Москва-Пассажирская',
        'official_name:esr': 'Москва-Пассажирская',
        'official_name:esr:website': 'http://cargo.rzd.ru/cargostation/public/ru?STRUCTURE_ID=5101&layer_id=4829&page4821_2705=1&refererLayerId=4821&id=1090',
        'official_name:express-3': 'Москва-Октябрьская',
        'official_name:express-3:website': 'http://bilet.ru/rus/TrainDirectory.htm?firstsymb=%u041c',
        'official_name:website': 'http://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=5104&layer_id=5368&id=278&node_id=19',
        'operator': 'Октябрьская железная дорога',
        'public_transport': 'station',
        'railway': 'station',
        'train': 'yes',
        'uic_name': 'Moskva Oktiabrskaia',
        'uic_ref': '2006004'
    },
    'coordinate': (55.7788343, 37.6537207)
}
```

![Moscow Railway](docs/moscow_railway.png)

### Waterway
Doesn't work properly. TODO: Fix it