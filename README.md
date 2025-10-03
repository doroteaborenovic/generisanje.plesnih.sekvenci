Dance Movement Sequence Generation for Musical Theatre and Classical Ballet using Markov Chains

The goal of this project was to develop a system that automatically generates realistic and aesthetically 
appropriate dance sequences in the styles of musical theatre and classical ballet. 

The system uses Markov chains to model the sequences, and the fluidity of transitions between movements is ensured by Catmull-Rom spline interpolation.
The repository contains two matrices that define the transition probabilities between dance elements:

- matrica.muzickiteatar.json
- matrica.klasicanbalet.json
  
The repository also contains video clips of the individual dance elements. The video filenames
(e.g., grandplie.mp4) directly correspond to the names of the states ("movements") defined in the JSON matrices, which allows for their easy mapping.
The system was developed using a subset of the publicly available AIST++ database.


Musical színházi és klasszikus balett tánc-szekvenciák generálása Markov-láncok segítségével

A projekt célja egy olyan rendszer kifejlesztése volt, amely automatikusan generál valósághű és esztétikailag megfelelő 
táncszekvenciákat a musical színház és a klasszikus balett stílusában. A rendszer Markov-láncokat használ a szekvenciák modellezésére, a mozdulatok 
közötti átmenetek folyamatosságát pedig Catmull-Rom spline interpoláció biztosítja.
A repozitóriumban két mátrix található, amelyek a táncelemek közötti átmenetek valószínűségét definiálják:

- matrica.muzickiteatar.json
- matrica.klasicanbalet.json
  
A repozitóriumban megtalálhatók az egyes táncelemeket bemutató videófelvételek is. A videófájlok nevei (pl. grandplie.mp4) közvetlenül megfelelnek
a JSON mátrixokban definiált állapotok ("mozdulatok") neveinek, ami lehetővé teszi azok könnyű leképezését.
A rendszer a nyilvánosan elérhető AIST++ adatbázis egy részhalmazán alapul.

https://google.github.io/aistplusplus_dataset/visualizer/index.html?c=gWA
