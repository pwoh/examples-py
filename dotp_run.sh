#!/bin/sh

#python timer.py [vector/matrix size] [size increment] [json] [times to run] [output filename]
python timer.py 5000 50 '{
   "columns":[
      "Vector size",
      "Tensorflow (unvectorised)",
      "Tensorflow (vectorised)",
      "Tensorflow (matmul)",
      "Tensorflow (no-op)",
      "Accelerate-CUDA (unvectorised)",
      "Accelerate-CUDA (no-op)",
      "Accelerate-TF (no-op)",
      "Accelerate-TF (unvectorised)",
      "Tensorflow-Haskell (vectorised)"
   ],
   "python":[
      {
         "filename":"dotp.py",
         "maxDim":5000,
         "args":["unvectorised"]
      },
      {
         "filename":"dotp.py",
         "maxDim":5000,
         "args":["vectorised"]
      },
      {
         "filename":"dotp.py",
         "maxDim":5000,
         "args":["matmul"]
      },
      {
         "filename":"dotp.py",
         "maxDim":5000,
         "args":["noop"]
      }
   ],
   "stack":[
      {
         "filename":"examples-hs-exe",
         "maxDim":5000,
         "yaml":"/home/pwoh/Dropbox/Thesis/notes/examples-hs/stack.yaml",
         "args":["dotp"]
      },
      {
         "filename":"examples-hs-exe",
         "maxDim":5000,
         "yaml":"/home/pwoh/Dropbox/Thesis/notes/examples-hs/stack.yaml",
         "args":["noop"]
      },
      {
         "filename":"Main",
         "maxDim":5000,
         "yaml":"/home/pwoh/Thesis/accelerate-tf/stack.yaml",
         "args":["noop", "--docker", "--docker-image=tensorflow/haskell:v0"]
      },
      {
         "filename":"Main",
         "maxDim":5000,
         "yaml":"/home/pwoh/Thesis/accelerate-tf/stack.yaml",
         "args":["accdotp", "--docker", "--docker-image=tensorflow/haskell:v0"]
      },
      {
         "filename":"Main",
         "maxDim":5000,
         "yaml":"/home/pwoh/Thesis/accelerate-tf/stack.yaml",
         "args":["tfdotp", "--docker", "--docker-image=tensorflow/haskell:v0"]
      }
   ]
}' 10 "dotp_results-"
