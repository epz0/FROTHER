# FROTHER Dataset

Based on the dataset originally published by [Toh & Miller (2018)](https://sites.psu.edu/creativitymetrics/2018/07/18/milkfrother/).

The original dataset included a single pdf file with 934 digitised sketches created by participants and a spreadsheet with the "creativity", "novelty" and "quality" values for the ideas.

The **FROTHER dataset** builds from this data, systematically organising and extending the dataset. Below is a summary of the contents:

##

## Contents
**Images**: 933 .png images. Image names are sequential as in the original dataset.
**Spreadsheet** (WIP): Spreadsheet creating unique ids to each idea and liking them to the image files, adding a collumn with the Idea Description as extracted from the image file and a Idea Summary. The original analysis are also kept.

## Data processing
To create this updated dataset the following steps were taken:

### 1. Splitting the pdf original pdf file
Given that the original podf file contained 1 image per page, we obtained 934 pdf files. We used [pdf24](https://www.pdf24.org/en/) for this step.

### 2. Convertting each individual pdf file to png
We used [pdf24](https://www.pdf24.org/en/) to convert each of the pdfs into .png files. The image names corresponded to the page number. The output images were in A4 size, whereas the actual area that was used for sketching and annottations was smaller, in the center of the page.

### 3. Cropping the images
We cropped the 934 images to focus only on the actual area that was used for sketching and annottations. The images were subsequently rescaled to 1020 x 764 pixels. We used [XnView MP](https://www.xnview.com/en/) to batch process the images.

### 4. Linking participant IDs, idea numbers and images
We looked through all the images, noting the participant ID shown, the idea number and the filename. We created a spreadsheet linking this information. A unique identifier was created in the format ```P_X-Y``` where X is the participant ID number and Y is the idea number. In this process the following issues were identified and addressed:
- For participant 75, the idea 10 was rejected. This idea was present on the original dataset (```page 434```) but was not present in the analysis spreadsheet. As such, we deleted image 434.png from the dataset and adjusted the idea numbers for participant 75.
- Participant 19 had 2 ideas analysed in the original spreadsheet. However only one image (```002.png```) was found with the Participant Id #19. We saw that image ```001.png``` had no participant ID and was similar in content and handwriting to the image ```002.png```. Hence we  attributed image ```001.png``` to participant 19.
- For participant 145, no idea #2 was found, thus the numbers were adjusted accordingly (see image ```827.png``` onwards).
- For participant 122, no idea #1 was found, thus the numbers were adjusted accordingly (see image ```685.png``` onwards).
- Whenever idea numbers were adjusted the corresponding original analysis has been appropriatelly linked.

### 5. Final pool of images
Given the need to exclude image ```434.png``` as it was a rejected idea, the final number of images in this dataset is **933**.

### 6. Extracting idea description and idea summary
All images have a field called "Idea Description" in which participants had to describe their image. We used the OpenAI API vision capabilities (model ```gpt-4o-2024-08-06```).
The prompts are structured in ```jinja``` files. We use ```pydantic``` to format the output.
The final output is saved as a ```.xlsx``` format.
The cost was approximatelly $2.50.

### 7. Validating descriptions and summaries
To validate the descriptions and summaries of the ideas we calculated that the sample size that needs to be checked is 210 for the given the dataset population (933), a confidence level of 90% and a margin of error of 5%.
As such, a random list of 210 image IDs was generated and the images were manually checked against the descriptions and summaries.\
We deemed an "idea description": ```valid (1)``` if the description exactly matched the image one and ```invalid (0)``` if it did not perfectly matched.\
We deemed a "summary": to be ```valid (1)``` if it conveyed the main function and overall priciple of the idea and ```invalid (0)``` otherwise.\
We further analysed the inconsistencies identifying instances where minor mistakes (e.g., single word missing/replaced) happpened. This analysis is detailed in the ```validation.xlsx``` document.\

We specified **a priori** a threshold of 70%&#177;5% as the target range. If after the validation process the estimated proportion of correct idea descriptions and summaries, the prompts will be adjusted and the whole process done again.

**Validation results**\
a. _Idea Description_\
```absolute error rate = 15.24% (n=32)```\
```error rate disconsidering minor mistakes = 10.48% (n=22)```\
\
For these values we can say with 90% confidence that the percentage of **absolute errors** in the generation of **descriptions** ranges between **11.16%** and **19.32%**.\
If we disregard the minor mistakes the percentage of **errors disconsidering minorones** ranges between **7.00%** and **13.95%**.\
\
Thus, in both cases, the percentage of correct ideas is well above the _a priori_ specified threshold of 70%&#177;5%.\
\
b. _Idea Summary_\
```absolute error rate = 2.86% (n=6)```\
For this value we can say with 90% confidence that the percentage of **absolute errors** in the generation of **idea summaries** ranges between **0.97%** and **4.75%**.\
\
Thus, the percentage of correct idea summaries is well above the _a priori_ specified threshold of 70%&#177;5%.\
\
Based on this, the generated text descriptions and summaries are deemed to be satisfactory an it will not be necessary to re-run the analysis.\

### 8. Extracting text embedding for the descriptions
Once all the images have a summary em get the text embedding for each idea using the OpenAI API (model ```text-embedding-3-large```).
Subsequently a pairwise distance matrix is calculated, using the cosine distance between each idea.
The final output is saved as a ```.npy``` format.
The cost was negligible.
