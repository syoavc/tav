#TAV: Text Analysis and Visualization System

The Discourse Attributes Analysis Program ([DAAP](https://github.com/DAAP/DAAP09.6)) is a computer-based text analysis system designed by Willma Bucci and Bernard Maskit, whose features include the use of both weighted and unweighted dictionaries and whose output includes measures based on an exponential smoothing operator.

The Text Analysis and Visualization (TAV) system was originated by Liat Tsuman-Caspi, as part of her post-doctoral research with Professor Bucci. TAV lets the DAAP user visualize the linguistic data that DAAP produces and superimposes it on the original text. In addition, the system generates useful statistics about the frequency in the text of certain linguistic styles.

**What can you do with the Text Analysis and Visualization (TAV) system?**

1. Mark texts for low, average, and high levels of WRAD (Weighted Referential Activity Dictionary), REF (Reflection), and DF (disfluency). You may be able to use only one or two of the three measures, but you would have to change the configuration files (described below) accordingly. 

Three visual modes of representations are used to indicate low, average, and high levels of the three DAAP measures, allowing a visual representation of different combinations of these measures:

The three modes of representations are:

- Font style – for WRAD: 

  - Low WRAD = italics
  - Average WRAD = regular
  - High WRAD = underline 

- Font size – for DF:
  - Low DF = small 
  - Average DF = medium
  - High DF = large

- Highlighting color – for REF:
  - Low REF = green
  - Average REF = no color
  - High REF = yellow 

The visualized text will be produced as an HTML file.

For example, the following short segment is marked for low, average, and high levels of WRAD (font style), REF (color), and DF (font size):

![example](https://github.com/syoavc/tav/blob/master/example.png)

In this example, you can see that the segment begins with high DF, low Ref, and average WRAD, changes to high WRAD, and average Ref and DF, and ends with high Ref, Low DF and average to low WRAD.

The idea behind the specific markers used above (i.e., font's style, color, and size) is that they can be superimposed on one another to reflect a combination of different levels of three measures, which may represent different styles of speech.

1. The TAV system produces statistics for the various combinations of the three measures. Specifically, you can obtain the following data:
  1. The total number of words in the text produced by the interviewee (S1)
  2. The number of words in the text that represent specific combinations of the measures. For example: of a 2400-word narrative, 270 words represent the combination of High WRAD\_Low Ref\_Low DF (i.e., story-telling)
  3. The percentage of words in the text that represent specific combinations of the measures. For example: of a 2400-word narrative, 11.25% (i.e., 270 words) represent the combination of High WRAD\_Low Ref\_Low DF.
  4. The number of words in the text that represent specific combinations of the measures and constitute segments of speech of a certain minimum length. For example: of the 270 words that represent the combination of High WRAD\_Low Ref\_Low DF, only 120 words meet the criterion of segments of 50 words or more. In other words, this would mean that there are one or two segments in the text that have the quality of story-telling. You can go back to the HTML file and find these segments using the visual markings. 

The idea behind the length filter is to allow the identification of segments of text that are long enough to meaningfully reflect the measure or combination of measures. For example, working with interviews of psychotherapists about their professional work, segments of 50 words or more were found to meaningfully represent distinct styles of speech. 

1. 
  1. The percentage of words in the text that represent the combinations of measures and constitute segments of speech of a certain minimum length. For example: of the 2400 words of the narrative that represent the combination of High WRAD\_Low Ref\_Low DF, 5% (i.e., 120 words) constitute segments of 50 words or more.  

**How to use the TAV System?**

**Software required:**

- Excel
- Text editor
- Python 

**Files you will need:**

1. Texts transcribed according to DAAP transcription rules and saved as text files. 
2. The DAAP Raw file for your dataset: This file contains a list of all the (counted) words in the file; for each word, the file shows the number of the speaker and the dictionary values assigned to the word.
3. The DAAP SMT (smooth data) file for your dataset: This file contains the data needed to make a chart of the smoothed dictionary density functions. The columns are ordered first by speaker and then by dictionary.
4. The DAAP TRN file (CSV; comma delimited format) for your dataset. This file contains a separate row for each turn of speech within a narrative. It also includes the number of words for each turn of speech and the number of the word at which this turn of speech starts. The data in this file are useful when you want to use a specific segment of a text rather than the entire text. You can use this file to help you identify the corresponding segments in the RAW and SMT files. 
5. The DAAP overall Main Aggregation File (AG0): This file has separate rows for each text file, one row for each speaker, and a final row for all speakers combined. You can use the data in this file to determine the levels of your measures. 
6. The DAAP First Variations file (AG1): This file contains a separate set of rows for each text. For each text, there is a separate row for each speaker and for each actualization of each category.You can use the data in this file to determine the levels of your measures. 
7. Configuration files (you will create these in step II)
8. analyze.py file 

For a more elaborated description of the DAAP's files and transcription rules, please refer to:

[http://figshare.com/articles/DAAP\_Operating\_Instructions/947740](http://figshare.com/articles/DAAP_Operating_Instructions/947740)

 [https://github.com/DAAP/DAAP09.6/blob/master/DAAP09.6OPERATINGINSTRUCTIONS.md](https://github.com/DAAP/DAAP09.6/blob/master/DAAP09.6OPERATINGINSTRUCTIONS.md)

**Step I: Plan your study**

1. Determine the dataset to be used.
2. Decide on the measures (i.e., WRAD, REF, and DF) and the specific levels of the measures that are of interest to you. 
3. Compute the thresholds for the different levels of your measures:
  1. Low, average and high levels of measures can be determined using the means and SD of the subject/sample/norms. 
  2. Determine the SD unit by which you define your levels. For example, for determining DF levels you may decide that 1 SD above the subject's mean DF would signify high DF, 1 SD below the mean would be low DF, and the range in between would be average DF. Alternatively, you may decide to be more conservative and use 1.5 SD above/below the mean. 
  3. At the end of this phase you should have a list for each subject that specifies the numerical data for the different levels for each measure as illustrated in the following simplified example: 

**Example:** you are interested in looking at the different combinations of high and low levels of REF and WRAD and you have 2 subjects. You decided to use the subjects' own means and SD's to determine levels of REF and the general norms to determine levels of WRAD. You further decided that 1 SD above and below the mean would signify high and low levels, respectively.

1. Subject 1: mean Ref= .093, SD= .026
2. Subject 2: mean Ref= .081, SD= .017
3. Norms for WRAD: mean WRAD= .45, SD: .04

| Subject | Low Ref | High Ref | Low WRAD | High WRAD |
| --- | --- | --- | --- | --- |
| 1 | .067 | .119 | .41 | .49 |
| 2 | .064 | .098 | .41 | .49 |

**Step II: Create the required data folders and files:**

1. Save the analyze.py file to a desired location on your computer. 
2. For each subject/narrative, create a separate folder (e.g., numbered folders: 01, 02, 03…).
3. Each subject's folder should contain: 
  1. The transcribed narrative in text format according to the DAAP transcription rules.
  2. The SMT and RAW files for that subject/narrative. 
  3. To make it easier with later steps, it is recommended that the different files will be signified consistently across the narratives with a prefix that indicates the subject's id. 

For example, for subject # 01, you may have the following files:

* 01.txt (narrative for subject 1)

* 01DAAPSMT.csv

* 01DAAPRAW.csv.

For subject #2, you would have the following files:

* 02.txt,

* 02DAAPSMT.csv 

* 02DAAPRAW.csv 

1. In addition, each subject's folder would contain the specific configuration files for that subject: 

A configuration file is a text-format file. It determines the specific configuration of measures and levels of measures for which the code produces numerical data and a visualized html file. Each specific combination of measures (and levels of measures) requires its own configuration file.

For example, if you wanted to focus on different combinations of high and low levels of REF and WRAD, you would have 4 configuration files, one for each of the following combinations of measures:

1. High REF, High WRAD
2. High REF, Low WRAD
3. Low REF, High WRAD
4. Low REF, Low WRAD

The following are PC and Mac versions of the same configuration file, which you can use as a template to create your own configuration files according to the guidelines specified below: 

**Configuration files:**

**PC version:**
```python
{

    "text\_file": "C:\\Users\\Liat\\Research\\DAAP\\Mapping\\04\\04 - DAAP.txt",

     "measures\_file": "C:\\Users\\Liat\\Research\\DAAP\\Mapping\\04\\04DAAPSMT.csv",

    "raw\_file": "C:\\Users\\Liat\\Research\\DAAP\\Mapping\\04\\04DAAPRAW.csv",

    "out\_file": "C:\\Users\\Liat\\Research\\DAAP\\Mapping\\04\\04.html",

    "cond":     [

        ["DF(S1)", 0.090, 0.115],

            ["WRAD(S1)", 0.398, 0.500],

            ["R(S1)", 0.060, 0.102]

    ],

    "stats": {

        "R(S1)": 2,

        "DF(S1)": 1,

             "WRAD(S1)": 2

    },

    "consecutive\_threshold": 50

}
```

**Mac Version:**
```python
{

    "text\_file": "/Users/Liat/Research/DAAP/Mapping/04/04 - DAAP.txt",

     "measures\_file": "/Users/Liat/Research/DAAP/Mapping/04/04DAAPSMT.csv",

    "raw\_file": "/Users/Liat/Research/DAAP/Mapping/04/04DAAPRAW.csv",

    "out\_file": "/Users/Liat/Research/DAAP/Mapping/04/04.html",

    "cond":     [

        ["DF(S1)", 0.079, 0.094],

            ["WRAD(S1)", 0.398, 0.500],

            ["R(S1)", 0.066, 0.102]

    ],

    "stats": {

        "R(S1)": 2,

        "DF(S1)": 1,

             "WRAD(S1)": 2

    },

    "consecutive\_threshold": 50   

}
```

Creating your own configuration files:

- The first three rows of the configuration file specify the location of the data files for each narrative that are used in this process: 
  - The text file
  - The SMT DAAP file
  - The Raw DAAP file

- That is, in this example, the three files (for subject #4) are located in folder "4," which is in folder "mapping" and so on: 

**C:\\Users\\Liat\\Research\\DAAP\\Mapping\\04**

- Each row ends with the name of the specific file that will be used: 04 - DAAP.txt, 04DAAPSMT, 04DAAPRAW 

- Thus, in order to adapt the configuration file to your needs, you would have to change the location of the three files and their names.
- The fourth row specifies the location and name of the html file that the code will produce – the file that shows the visualized narrative (i.e., font size, style, and color), which represent the measures and the levels you chose. As with the first three rows, you need to change the location and name of file according to your own needs.
- The condition part specifies the thresholds for the levels of your measures of interest, which you determined beforehand:
  - The number on the left represents the highest threshold for the low level of the measure.
  - The number on the right represents the lowest threshold for the high level of the measure.

In the example below, for DF, segments that represent DF that is below .09 are considered low DF, above .115 – are high DF, and in between – are average DF.

```python
"cond":     [

            ["DF(S1)", 0.090, 0.115],

                ["WRAD(S1)", 0.398, 0.500],

                ["R(S1)", 0.060, 0.102]
```

- Thus, you would need to change the measures and their thresholds accordingly. 

- The next segment in the analyze.py file determines the specific combination of levels that interests you for which the code will produce numerical data: 

```python
"stats": {

    "R(S1)": 2,

    "DF(S1)": 1,

         "WRAD(S1)": 2
```

0= low level, 1=average level, 2=high level

- As mentioned previously, each configuration file represents one combination of levels of measures. You would need to create as many configuration files as the number of combinations you want. In this example, this configuration file represents the combination of high Ref, High WRAD, and average DF. That is, you will get the number and percentage of words that represent a combination of high Ref, High WRAD, and average DF. If you are interested in only one or two measures, you would have to change the configuration file accordingly. 

- Finally, you can use a length filter that determines the minimum number of consecutive words that represent the specific combination of measures. In the example, the threshold was set for 50 consecutive words. If there are no segments in the narrative that represent that combination and are at least 50-word long, the number "zero" will be produced. The output will also produce the number of words that represent the combination of measures without the filter. 
- As mentioned above, you would have to create configuration files for each of the combination of measures you are interested in. You would create the same list of configuration files for each narrative/subject, differentiated only by the parts of the name that signify the subject. In other words, once you created the list of configuration files for one subject, you can "copy" and "paste" it to other subjects' folders and make the necessary changes (e.g., location, subject id). 

Once you have separate folders for each subject, each containing the narrative file, DAAP Raw and SMT files, and configuration files, you can proceed to the step III: producing the numerical data and the visualized html file.

**Step III: Produce the numerical data and visualized HTML file**

- Open a terminal window:
  - In PC: click on the start button and in the search box type "cmd." 
  - In Mac: Navigate to /Applications/Utilities and double-click on Terminal.
  - If this does not work, check in google how to open a terminal window in your specific operating system. 

In PC, in order to paste commands into this window need to use: right click. In order to copy data from this window you need to use: enter

**Commands:**

- There are three commands, which you would have to initially adapt to your study and, subsequently, to each subject and configuration file.
- These are the commands that you would run in the terminal window. 
- You would run these commands after you had created the required files described in previous steps. 
- The commands you would need are as follows:

**PC version:** 
```
cd C:\Users\Liat\DAAP\Mapping
python analyze.py --conf C:\Users\Liat\ DAAP\Mapping\01\conf01\_LDF\_AR\_HWRAD.txt --debug
python analyze.py --conf C:\Users\Liat\DAAP\Mapping\01\conf01\_LDF\_AR\_HWRAD.txt --stats-only
```

**Mac version:**
```
cd /Users/Liat/ DAAP/Mapping
python analyze.py --conf /Users/Liat/DAAP/Mapping/01/conf01\_LDF\_AR\_HWRAD.txt --debug
python analyze.py --conf /Users/Liat/DAAP/Mapping/01/conf01\_LDF\_AR\_HWRAD.txt --stats-only
```


**Adapting the commands to your study:**

**The first command** : 

```
cd /Users/Liat/ DAAP/Mapping
```

- This command specifies the location of the "analyze.py" file. You would have to change the location accordingly (In the above example, the "analyze.py" file is located in the folder Mapping, which is located on drive C, in folder "Liat," which is in folder "Users.)" 
- Each time you begin working with the terminal window you have to begin with the first command to change the directory to the location of the analyze.py file. 

**The second command ("debug"):**

```
python analyze.py --conf /Users/Liat/DAAP/Mapping/01/conf01\_LDF\_AR\_HWRAD.txt --debug
```

- You would have to run this command only once for each subject/ narrative at the beginning (after running the first command) prior to running the third command.
- The specific combination (i.e., name of configuration file) you use for the debug command (in the above example – Low DF, Average Ref, High WRAD) does not matter as long as it corresponds to an existing configuration file that you had created. 
- The purpose of the "debug" command is to make sure that the narrative file (text format) and the DAAP Raw file, which are located in the subject's folder, match. That is, each word in the text file corresponds to the respective word in the RAW file and consequently to the relevant linguistic data. 
- Once you ran the "debug" command it would create a long column of pairs of words (the left column are words from the narrative text and the right one from the RAW file), which should be identical. If the pairs of words are not identical you need to locate where the mismatch begins and correct the errors in the text file. The errors are typically due to incorrect transcription. You may have to repeat this step several times until the two columns match one other. 
- This command will also produce the visualized HTML file. 

Once the two columns correspond, you can move to the third command.

**Third command ("stats"):**

```
python analyze.py --conf /Users/Liat/DAAP/Mapping/01/conf01\_LDF\_AR\_HWRAD.txt --stats-only
```

- This command produces the statistics described above according to the different specification in the respective configuration file. Notice that the last part of the location in the command is the name of the specific configuration file. That is you would run this command for each of the configuration file, each time changing the command the name of the configuration file. 

In this example the configuration file is located in folder 01 (which stands for subject 01), in folder Mapping, in Liat and so on.

The configuration file was named: conf01\_LDF\_AR\_HWRAD.txt

What the name signifies is that it is the configuration file for subject # 01 for the combination of Low DF, Average Ref, and High WRAD. That is, the numbers that will be produced for this configuration file will show the total number of how words (and their percentage) in the narrative that represent this specific combination. In addition, the number and percentage of words that are in segments of 50 words or more and represent this combination will also be produced.

For example, the output would be:
```
Number of words after filtering: 364 (2.94903994167%)

Number of words after filtering, of groups of 50 and more: 62 (0.502309001053%)
```
This means that 364 words in the narrative represent the above combination, constituting 3% of the narrative. Out of the 364, 62 words constitute a segment of 50 words or more, which means in this case 1 segment. 

As mentioned above, you would adapt and run the "stats" command for each subject and for all the configuration files that you created.
