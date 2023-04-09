# cd042 Gain Inference

# Design

## Preprocessor

* Resampling

* Amplitude normalisation

* Silence removal


```
signals----[preprocessor]-----{signal}
noises-----[preprocessor]-----{noises}
```

## Mixer

* Truncation to common length

* Randomised gain, and sum

```
signals-\-----------{signal}
         \
          +-[mixer]-{mixed}
         /                   
noises--/-----------{noise}
```                     

## Analyser

* Windowing

* Frequency analysis

* Level calculation = x

* Ideal gain calculation = y


```
{signal}--[analyser]-\-----{levels}---x           
          /           \                 
{mixed}--/             \---{gains}----y    
                  
```                     

### Parameters


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


# Tensorflow
https://www.tensorflow.org/tutorials/quickstart/beginner
