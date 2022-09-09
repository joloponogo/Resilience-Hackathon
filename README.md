# VeloSafe

## Description
VeloSafe is an open-source application with the aim of finding the safest route for biking between two points in the city of Zurich.
It is based on OpenStreetMap, OSMnx, osmdroid, and AndroidStudio, which grants it a reproducible character. Among the challenges
faced upon VeloSafe's development, three must be highlighted: acquiring the comprehension around how to extract and work on data
available from OpenStreetMaps, especially the construction of custom weighted graphs from it; the implementation of a
cohesive, user-friendly interface via AndroidStudio; the integration of both back- and frontends in the future.  

### The idea
Upon opening the application, a map is shown alongside a search bar where start and endpoints of a journey are to be input, which can also be directly pinned on the map. In doing so, the routing-algorithm will then calculate and showcase the safest route between the selected coordinates according to how safe the path is for cyclists (for instance, having proper bicycle tracks along the way rather than shared lanes as well as user ratings). As the user travels, their real-time location is also tracked. After finishing a journey, the user is allowed to rate segments on a scale from 1 to 5 (1 being worst, 5 best).

## Documentation
### Frontend
The whole frontend is located in the frontend folder, and is one single project made with [Android Studio](https://developer.android.com/studio).  
Everything not documented inside the java code was already given by the **"Phone and Tablet" -> "Basic Activity" Template** of Android Studio.
The map service we are using is [OpenStreetMap](https://www.openstreetmap.org), integrated into the code through the [osmdroid library](https://github.com/osmdroid/osmdroid/wiki).

### Backend
The backend code is located in the backend folder. It contains python scripts to generate interactible views that compare normal routing to VeloSafe routing.
It leverages the functionality of [OSMnx](https://github.com/gboeing/osmnx) to fetch and interpret [OpenStreetMap](https://www.openstreetmap.org) data.

## Credits
Maitraya Desai  
Matthias Lott  
Moritz Mani  
Oliver Graf  
Paulo Sepúlveda  

## License
VeloSafe is completely open-source, hence one is free to adapt, change and increment its original code for whatever desired purposes.
