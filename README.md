(eng):
Dance Movement Sequence Generation for Musical Theatre and Classical Ballet using Markov Chains

The goal of this project was to develop a system that automatically generates realistic and aesthetically 
appropriate dance sequences in the styles of musical theatre and classical ballet. 

The system uses Markov chains to model the sequences, and the fluidity of transitions between movements is ensured by Catmull-Rom spline interpolation.
The repository contains two matrices that define the transition probabilities between dance elements:

- matrica.muzickiteatar.json
- matrica.klasicanbalet.json
  
The repository also contains video clips of the individual dance elements. The video filenames
(e.g., grandplie.mp4) directly correspond to the names of the states ("movements") defined in the JSON matrices, which allows for their easy mapping.
The system was developed using a subset of the publicly available AIST++ dataset.

https://google.github.io/aistplusplus_dataset/visualizer/index.html?c=gWA
