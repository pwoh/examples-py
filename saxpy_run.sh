#!/bin/sh

#python timer.py [vector size] [size increment] [json] [times to run] [output filename]
python timer.py 5000 50 '{
   "columns":[
      "Vector size",
      "Tensorflow (unvectorised)",
      "Tensorflow (vectorised)",
      "Accelerate-CUDA (unvectorised)",
      "Accelerate-TF (unvectorised)",
      "Tensorflow-Haskell (vectorised)"
   ],
   "python":[
      {
         "filename":"saxpy.py",
         "maxDim":5000,
         "args":["unvectorised"]
      },
      {
         "filename":"saxpy.py",
         "maxDim":5000,
         "args":["vectorised"]
      }
   ],
   "stack":[
      {
         "filename":"examples-hs-exe",
         "maxDim":5000,
         "yaml":"/home/pwoh/Dropbox/Thesis/notes/examples-hs/stack.yaml",
         "args":["saxpy"]
      },
      {
         "filename":"Main",
         "maxDim":5000,
         "yaml":"/home/pwoh/Thesis/accelerate-tf/stack.yaml",
         "args":["accsaxpy", "--docker", "--docker-image=tensorflow/haskell:v0"]
      },
      {
         "filename":"Main",
         "maxDim":5000,
         "yaml":"/home/pwoh/Thesis/accelerate-tf/stack.yaml",
         "args":["tfsaxpy", "--docker", "--docker-image=tensorflow/haskell:v0"]
      }
   ]
}' 10 "saxpy_results-"
