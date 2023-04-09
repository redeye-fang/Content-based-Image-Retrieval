import scipy.fftpack
import streamlit as st
import os
import glob
from PIL import Image
import imagehash
import time
from functools import partial
from multiprocessing import Pool

def generateHash(image_path):

    image = Image.open(image_path)
    imageName = os.path.basename(image_path)
    hashTemp = imagehash.phash(image)
    return [imageName, str(hashTemp), image_path]

    # return (image_path, str(hashTemp))

class hashes:
    def __init__(self, path):
        self.path = path
        self.flag = False
        self.Files = glob.glob(path + '/**/*.*', recursive=True)
        self.image_paths = []
        self.hashValues = []

        for file in self.Files:
                if file.endswith((".jpg")):
                    self.image_paths.append(file)

    #### Parallel Implementation
    @st.cache(hash_funcs = {st.delta_generator.DeltaGenerator: lambda _: None}, suppress_st_warning=True)
    def getHashValues(self):

        self.compute_hashes_parallel(self.image_paths, os.cpu_count())

    def compute_hashes_serial(self):

        for imagePath in self.image_paths:
            self.hashValues.append(generateHash(imagePath))
        
        if len(self.image_paths) != 0 and len(self.hashValues) == len(self.image_paths):
            self.flag = True

        return (self.flag, self.hashValues)

    def compute_hashes_parallel(self, num_workers=12):

        hashingPool = Pool(processes=num_workers)
        self.hashValues = hashingPool.map(partial(generateHash), self.image_paths)
        hashingPool.close()
        hashingPool.join()

        # for imageName, hashTemp, image_path in tmp_list:
        #     self.hashValues.append([imageName, hashTemp, image_path])

        if len(self.image_paths) != 0 and len(self.hashValues) == len(self.image_paths):
            self.flag = True
        
        return (self.flag, self.hashValues)