# Higher Order Network - Node + Edge file creation

Input sequence text files, output edge files to be used to analyse networks.


### Prerequisites

Code written by Xu Jian for the HON implementation, available at: https://github.com/xyjprc/hon. Has been modified slightly to accept our sequence files, so best to just download all python files in this folder.

### How to Use

Open up jianxu_main.py in a text editor (e.g. gedit, vim). 

Look for the following line near the top of the code (at the moment of writing this README, line 20):

```
""" Initialise Algorithm Parameters / input or output filenames """
```

Set MaxOrder and MinSupport variables in the following lines, using the comments given as explanation.

```
_## For each path, the rule extraction process attempts to increase the order until the maximum order is reached. The default value of 5 should be sufficient for most applications. Setting this value as 1 will yield a conventional first-order network. Discussion of this parameter (how it influences the accuracy of representation and the size of the network) is given in the supporting information of the paper.
MaxOrder = 3

_## Observations that are less than min-support are discarded during preprocessing.
_## For example, if the patter [Shanghai, Singapore] -> [Tokyo] appears 500 times and [Zhenjiang, Shanghai, Singapore] -> [Tokyo] happened only 3 times, and min-support is 10, then [Zhenjiang, Shanghai, Singapore] -> [Tokyo] will not be considered as a higher-order rule.
MinSupport = 10
```

Next, initialise user parameters (input / output filenames) as desired. Typically input filename should be e.g. sequence.txt or sequence3.txt (make sure to copy it over from the Raw_processing folder, else give the direct filepath to that.

Finally, run the programme from the terminal. No command line arguments are required.

```
$python3 jianxu_main.py 
```
