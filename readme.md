# cd042 Gain Inference

# Design

## Data model
```
signals--\           
          +-[mixer]---{mixed}--[device]---> y={gains}
noises---/                           \
                                      +--> x={psds}
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

    * gain criteria [dBFS-to-dBSPL]


## Training & validation
```
                                  model---+
                                           \
y={gains}--\             /-training-set--\  \    
            +--[loader]-+                 [trainer]--fitted    
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
