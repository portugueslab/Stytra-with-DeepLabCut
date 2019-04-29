# Stytra extension example

[![DLC screenshot](dlc.png?raw=true)](http://www.portugueslab.com/files/dlc.mp4)

This example shows how to add custom tracking pipelines to [Stytra](https://github.com/portugueslab/stytra), in this case mice with [DeepLabCut](https://github.com/AlexEMG/DeepLabCut).
The model data was obtained by running an [example notebook](https://github.com/AlexEMG/DeepLabCut/blob/master/examples/Demo_labeledexample_Openfield.ipynb)
using the version [2.0.2](https://github.com/AlexEMG/DeepLabCut/commit/2a575d5941996949de470758c119c787efc7950b)*. If the API of DeepLabCut changes, we make no
guarantees that this will work with future versions, however it should be straightforward to adapt.
 
The example demonstrates a closed loop experiment in an open-arena tracking situation, using the video provided with DeepLabCut (openfield-Pranav-2018-10-30). 
The stimulus is a dot tracking the snout position for demonstration purposes, for implementing any other open or closed-loop stimuli please refer
 to the [Stytra documentation](http://www.portugueslab.com/stytra) or the stytra [examples](https://github.com/portugueslab/stytra/tree/master/stytra/examples).
 
If you are using Stytra for your research, please [cite us](https://www.biorxiv.org/content/early/2018/12/10/492553)! 

Note:
The 2.0.2 version of DeepLabCut had fixed dependencies for some libraries, which required some small workarounds. It should not be the case anymore though, but we have not tested the integration with the newest release.