1. Complete code in the dog_project notebook.

2. Please make sure that the required data is downloaded before you run the project. I've only submitted the code, not data.

3. I had issues using many classes from tf module. The issue seems to be replacing all the keras.this.this.this imports with tensorflow.this.this.this imports.

4. Also, you should run the export commands. Notice, how the "from keras ..." import here as well is changed to "tensorflow.keras ...". Similar changes I had done in extract_bottleneck_features.py that came with the project. See the statements like "from tensorflow.keras.applications.xception import Xception, preprocess_input" --> tensorflow.keras instead of just keras.

export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64
KERAS_BACKEND=tensorflow python -c "from tensorflow.keras import backend"

5. If you have trouble there always is the final dog_project.html in the root directory of the github repo.

