# FIST-Biclustering-Python
Implementation of FIST algorithm for generating Biclusters, Frequent Closed Patterns, Association Rules using Python


**Abstract**

Association rule mining and biclustering are two popular techniques in data mining that can be used to uncover interesting patterns and relationships in large datasets. However, these techniques are often computationally expensive and can be challenging to apply to large da-tasets. This paper presents a novel approach that combines association rule mining and bi-clustering using a suffix tree data structure. It is based on the frequent closed itemsets framework and requires a unique scan of the database. This data structure is used to reduce memory usage and improve the extraction efficiency, allowing parallel processing of the tree branches. Experimental results show that the proposed algorithm (Frequent Itemset Suffix Tree: FIST) is effective in uncovering meaningful patterns and relationships in large datasets and outperforms existing state-of-the-art algorithms in terms of efficiency and scalability.

**USER GUIDE**

In this section of the chapter, we will discuss how to use this python implementation of the algorithm. We will be briefly discussing the following topics:

- Environment & python installation
- Installation of external Libraries
- Using the source code or the package
- Transforming input dataset to suitable form
- Integrating the dataset with the python program and generating outputs
- Results

**1. Environment & python installation:**

I have used an windows PC with 64-bit operating system, x64-based processor for running the python program.

To run the program, a suitable python installation is required. I have used Python 3.10.6.

To install Python 3 on your machine, Visit the official Python website [https://www.python.org](https://www.python.org/) and navigate to the Downloads section. Download a version of Python 3.10 or onwards.

**2. Installation of external libraries:**

In this project we are using 2 external libraries on top of default python installation:

- Pandas
- PyDot

We are using pandas for the useful functionalities it provides for handling CSV files and DataFrames. PyDot is an interface to GraphViz which helps in creating graph based diagrams using python script.

To install Pandas use: python -m pip install pandas

To install PyDot: python -m pip install pydot

You may additionally need to install a GraphViz driver for PyDot to work properly.

**3. <a name="_hlk136724867"></a>Using the source code or the package**

The source code of the program can be cloned from this git repository.

Source Code: <https://github.com/Mijanur08/biclusturing-using-suffixTree>

The program is also uploaded in pypi.org as a python package. The latest version is 2023.5.31.3

Package link: <https://pypi.org/project/biclustering/>

Instead of cloning the git repository, the package can be directly installed using the following pip install command.

|python -m pip install biclustering --user|
| :- |

**4. Transforming Input Dataset into Suitable Form**

The input dataset must be in csv file and have the following 2 attributes:

- An ID attribute which is unique for each of the rows
- An itemsets attribute which contains comma separated names or values – each name or value representing an item.

An example of the input dataset is –

**Exampledata.csv**

ID,Itemsets

O1,"P1,P3,A2,A4"

O2,"P1,P3,A1,A2"

O3,"P2,P5,A3"

O4,"P1,P3,P4,A2,A4"

O5,"P1,P2,P3,P5,A2,A4"

**5. Integrating the dataset with our python program and generating output**

Our python implementation has module named fist.py. This file acts as an interface between the user and the complete algorithmic process.

First import the class FIST from the fist module and initialize a FIST class.

If we are using the source code from git repository, we need to specify the fist.py file while importing FIST class.

|<p>from fist import FIST</p><p>fist = FIST()</p>|
| :- |

Otherwise, if we are directly using the package after installing it by pip, then we need to specify the package name ‘biclustering’.

|<p>from biclustering import FIST</p><p>fist = FIST()</p><p></p>|
| :- |


Next step is to call the fist.process function. This function has 9 parameters. The function signature and description of all parameters are given below-

|<p>def process(self, input\_file\_dir: str, input\_dataset\_name:str,</p><p>id\_attribute: str, itemset\_attribute: str, max\_entries = 10000,</p><p>min\_supp\_percent=1.0, min\_conf\_percent=0.0,</p><p>min\_supp\_count\_outputs = 1,produce\_final\_img=False)->none</p><p></p>|
| - |


<table><tr><th colspan="3" valign="top"><b>Parameters</b></th></tr>
<tr><td rowspan="4" valign="top">Input_file_dir</td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">NA</td></tr>
<tr><td valign="top">Description</td><td valign="top">Path to the directory where the input CSV file (dataset) is located and the outputs will be generated in an output folder in that directory.</td></tr>
<tr><td rowspan="4" valign="top">input_dataset_name</td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">NA</td></tr>
<tr><td valign="top">Description</td><td valign="top">Filename of the input CSV file including its file extension</td></tr>
<tr><td rowspan="4" valign="top">id_attribute</td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">NA</td></tr>
<tr><td valign="top">Description</td><td valign="top">Name of the ID column of the dataset. The ID column must have unique value for each row.</td></tr>
<tr><td rowspan="4" valign="top">itemset_attribute</td><td valign="top">Datatype</td><td valign="top">String Literal</td></tr>
<tr><td valign="top">Optional</td><td valign="top">No</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">NA</td></tr>
<tr><td valign="top">Description</td><td valign="top">Name of the Item List column of the dataset. This column should contain comma separated item names. These item names will form itemsets.</td></tr>
<tr><td rowspan="4" valign="top">max_entries</td><td valign="top">Datatype</td><td valign="top">Integer</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">10000</td></tr>
<tr><td valign="top">Description</td><td valign="top">It specifies maximum number of  rows are to be read in a dataset. If a dataset has total number of rows greater than max_entries, the first max_entries number of rows will be read during the execution.</td></tr>
<tr><td rowspan="4" valign="top">min_support_percent</td><td valign="top">Datatype</td><td valign="top">Float</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">1\.0</td></tr>
<tr><td valign="top">Description</td><td valign="top"><p>The provided percentage of the total number of rows will be used as minimum support count for constructing the number table.</p><p>This value will also be embedded within the file name of generated files.</p></td></tr>
<tr><td rowspan="4" valign="top">min_conf_percent</td><td valign="top">Datatype</td><td valign="top">Float</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">0\.0</td></tr>
<tr><td valign="top">Description</td><td valign="top"><p>Minimum confidence filters the generated association rules. If confidence of an association rule is greater than min_conf_percent, only then it will be written in the output.</p><p>This value will also be embedded within the file name of generated files.</p></td></tr>
<tr><td rowspan="4" valign="top">min_supp_count_outputs</td><td valign="top">Datatype</td><td valign="top">Integer</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">1</td></tr>
<tr><td valign="top">Description</td><td valign="top">To extract the FCPs and Bi-clusters we can use a different support count than the previous minimum support. This parameter carries the value of minimum support count which is used for generating the outputs.</td></tr>
<tr><td rowspan="4" valign="top">produce_final_img</td><td valign="top">Datatype</td><td valign="top">Boolean</td></tr>
<tr><td valign="top">Optional</td><td valign="top">Yes</td></tr>
<tr><td valign="top">Default Value</td><td valign="top">False</td></tr>
<tr><td valign="top">Description</td><td valign="top">This parameter decides whether to generate the image of the suffix tree or not.</td></tr>
</table>


Here is the sample code for execution in python :

|fist.process(“./”,”sample.csv”,”ID”,”Itemsets”,min\_support\_percent=30,min\_conf\_percent=40,produce\_final\_img=True)|
| - |

**6. Results**

To avoid error during the execution, ensure that output folder exists in the input file directory. All the output files will be generated in this output folder. After execution, total 24 files including the image of the suffix tree is generated. They are as follows:

<table><tr><th valign="top">Number Table</th><th valign="top">NumberTable.dataset={dataset name}.minSupport={value}.csv</th></tr>
<tr><td valign="top">SFD</td><td valign="top">SFD.dataset={dataset name}.minSupport={value}.csv</td></tr>
<tr><td rowspan="2" valign="top">Suffix Tree</td><td valign="top">suffixTree.dataset={dataset name}.minSupport={value}.csv</td></tr>
<tr><td valign="top">suffixTree.dataset={dataset name}.minSupport={value}.json</td></tr>
<tr><td rowspan="2" valign="top">FCPs</td><td valign="top">FCP.dataset={dataset name}.minSupport={value}.csv</td></tr>
<tr><td valign="top">FCP.dataset={dataset name}.minSupport={value}.json</td></tr>
<tr><td rowspan="2" valign="top">Generators</td><td valign="top">Generators.dataset={dataset name}.minSupport={value}.csv</td></tr>
<tr><td valign="top">Generators.dataset={dataset name}.minSupport={value}.json</td></tr>
<tr><td rowspan="4" valign="top">Bi-clusters</td><td valign="top">biclusters.dataset={dataset name}.minSupport{value}.minSize={value}.csv</td></tr>
<tr><td valign="top">biclusters.dataset={dataset name}.minSupport{value}.minSize={value}.json</td></tr>
<tr><td valign="top">Biclusters.withNames.dataset={dataset name}.minSupport{value}.minSize={value}.csv</td></tr>
<tr><td valign="top">Biclusters.withNames.dataset={dataset name}.minSupport{value}.minSize={value}.json</td></tr>
<tr><td rowspan="4" valign="top"><p>Association Rules</p><p></p><p>- Exact</p><p>- PB</p><p>- SB</p></td><td valign="top">rule.{type}.dataset={dataset name}.minSupport={value}.minConf={value}.csv</td></tr>
<tr><td valign="top">rule.{type}.dataset={dataset name}.minSupport={value}.minConf={value}.json</td></tr>
<tr><td valign="top">rule.withNames.{type}.dataset={dataset name}.minSupport={value}.minConf={value}.csv</td></tr>
<tr><td valign="top">rule.withNames.{type}.dataset={dataset name}.minSupport={value}.minConf={value}.json</td></tr>
</table>


**7. References**

1\. Kartick Chandra Mondal, Nicolas Pasquier, Anirban Mukhopadhyay, Ujjwal Maulik, and Sanghamitra Bandhopadyay: A New Approach for Association Rule Mining and Bi-clustering Using Formal Concept Analysis. (2012) [[Link](https://link.springer.com/chapter/10.1007/978-3-642-31537-4_8)]

2\. Katick Chandra Mondal: Algorithms for Data Mining and Bio-informatics. (2016) [[Link](https://hal.science/tel-01330152/document)]


