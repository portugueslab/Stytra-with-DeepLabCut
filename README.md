# Stytra extension example

This example shows how to add custom tracking pipelines to Stytra, in this case rats with [DeepLabCut](https://github.com/AlexEMG/DeepLabCut).
The model data was obtained by running an [example notebook](https://github.com/AlexEMG/DeepLabCut/blob/master/examples/Demo_labeledexample_Openfield.ipynb)
using the version [2.0.2](https://github.com/AlexEMG/DeepLabCut/commit/2a575d5941996949de470758c119c787efc7950b). As the API of DeepLabCut keeps changing, we make no
guarantees that this will work with future versions, however it should be straightforward to adapt. Also, getting correct dependencies for Stytra and DeepLabCut at the same time might require some workarounds.
(e.g. DeepLabCut has the numpy dependency at 1.14 and Matplotlib dependency fixed at 2.2.2, whereas we usually work with the latest versions. This required a minor change in the DeepLabCutCode to run:
 changing `Toolbar` into `NavigationToolbar2WxAgg` in labeling_toolbox.py)
 
The example demonstrates a closed loop experiment in an open-arena tracking situation, using the video provided with DeepLabCut (openfield-Pranav-2018-10-30). 
The stimulus is a dot tracking the snout position for demonstration purposes, for implementing any other open or closed-loop stimuli please refer
 to the [Stytra documentation](http://www.portugueslab.com/stytra) or the stytra [examples](https://github.com/portugueslab/stytra/tree/master/stytra/examples).
 
If you are using Stytra for your research, please [cite us](https://www.biorxiv.org/content/early/2018/12/10/492553)! 