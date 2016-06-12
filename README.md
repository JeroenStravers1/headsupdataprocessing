# headsupdataprocessing

Disclaimer: you will probably have to tweak some paths for this to work correctly.

Dependencies: 
  OpenFaceImageInterpreter: requires OpenFace https://cmusatyalab.github.io/openface/setup/
  
  designed to work with the file structure generated by using https://github.com/JeroenStravers1/headsupimagelabeller

Usage:
  run openface_image_interpreter.py (check paths) to have openface interpret image head poses
  run generate_arff.py (check paths) to combine the results in a single arff file (comment/uncomment balancing method)
  point WEKA to the arff file, analyze
  