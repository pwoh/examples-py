#!/bin/sh
#Note had to add export STACK_YAML="/home/pwoh/Dropbox/Thesis/notes/examples-hs/stack.yaml" to bashrc

#python timer.py [vector/matrix size] [size increment] [json] [times to run] [output filename]
python timer.py 5000 1 '{
   "columns":[
      "Vector size",
      "Tensorflow (unvectorised)",
      "Tensorflow (vectorised)",
      "Tensorflow (matmul)",
      "Tensorflow (no-op)",
      "Accelerate (unvectorised)",
      "Accelerate (no-op)"
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
         "args":["dotp"]
      },
      {
         "filename":"examples-hs-exe",
         "maxDim":5000,
         "args":["noop"]
      }
   ]
}' 50 "dotp_results-"
