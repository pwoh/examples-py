#!/bin/sh
#Note had to add export STACK_YAML="/home/pwoh/Dropbox/Thesis/notes/examples-hs/stack.yaml" to bashrc

#python timer.py [number of options] [size increment] [json] [times to run] [output filename]
python timer.py 10000 1 '{
   "columns":[
      "Number of options",
      "Tensorflow",
      "Tensorflow (no-op)"
   ],
   "python":[
      {
         "filename":"blackscholes.py",
         "maxDim":10000,
         "args":["map"]
      },
      {
         "filename":"blackscholes.py",
         "maxDim":10000,
         "args":["noop"]
      }
   ],
   "stack":[
   ]
}' 1 "blackscholes_results-"
