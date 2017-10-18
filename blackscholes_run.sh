#!/bin/sh
#Note had to add export STACK_YAML="/home/pwoh/Dropbox/Thesis/notes/examples-hs/stack.yaml" to bashrc

#python timer.py [number of options] [size increment] [json] [times to run] [output filename]
python timer.py 5000 50 '{
   "columns":[
      "Number of options",
      "Tensorflow (unvectorised)",
      "Accelerate-CUDA (unvectorised)",
      "Accelerate-TF (unvectorised)"
   ],
   "python":[
      {
         "filename":"blackscholes.py",
         "maxDim":5000,
         "args":["map"]
      }
   ],
   "stack":[
      {
         "filename":"examples-hs-exe",
         "maxDim":5000,
         "yaml":"/home/pwoh/Dropbox/Thesis/notes/examples-hs/stack.yaml",
         "args":["bs"]
      },
      {
         "filename":"Main",
         "maxDim":5000,
         "yaml":"/home/pwoh/Thesis/accelerate-tf/stack.yaml",
         "args":["accbs", "--docker", "--docker-image=tensorflow/haskell:v0"]
      }
   ]
}' 1 "blackscholes_results-"
