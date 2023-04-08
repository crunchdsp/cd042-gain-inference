# cd042 Gain Inference

# Design

## Data generator
```
signals-\-----------{clean}---[device]--{clean}-\           
         \                                       +--[estimator]--> y={gains}
          +-[mixer]-{noisy}-\-[device]--{dirty}-/                 
         /                   \                                   
noises--/                     +----------------------------------> x={dirty}
```                     


```
signals-\----------+-{clean}--[device]---> y={ideal gains}           
         \        /          /       \            
          +-[mixer]-{noisy}-/         +--> x={noisy audio}                   
         /                                                              
noises--/                     
```                     

### Parameters

* mixer

    * sample rate [Hz]
    
    * gain

        * signals [linear]

        * noise [linear]

* device
    
    * ignore initial [seconds]

    * block size [samples]

    * window [option]

    * FFT size [samples]

    * calibration [dBFS-to-dBSPL]

* estimator
    
    * ignore initial [seconds]

    * block size [samples]

    * window [option]

    * FFT size [samples]

    * calibration [dBFS-to-dBSPL]


## Trainer
```
                                  model---+
                                           \
y={gains}--\             /-training-set--\  \    
            +--[loader]-+                 [fitter]--fitted    
x={psds}---/             \-testing-set---/                \
                          \                                \
                           \                                [validate]-> results
                            +=validating-set---------------/
```

### Parameters

* load
    
    * count [vectors]

* train
    
    * optimizer

    * loss function
    
    * metrics

    * epochs


# Tensorflow
https://www.tensorflow.org/tutorials/quickstart/beginner
