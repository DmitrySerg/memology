# Memology
**Memes - why so popular?**

My workshop talk at DataFest4 about parsing websites (including KnowYourMeme) can be found [here](https://it.mail.ru/video/933/).

### The project

[Memology.ipynb](https://github.com/DmitrySerg/memology/blob/master/Memology.ipynb) contains a short exploration of the dataset, with some graphs, statistics, etc., and, of course, text analysis and modelling. Based on the average views of the meme per day I have created 5 groups of "popularity" varying from "very unpopular" to "viral". To deal with the description texts I used TF-IDF transformation, which then passed to Logit regression and Random Forest. Overall, the quality of the models was quite satisfactory, achieving accuracy of 0.43 (with the naive constant baseline of 0.2)


![](https://lh3.googleusercontent.com/2lV4Nm6oa9_hY2t-9tBbo3RAuEzcraalogZT0oPDmBqic4tWXliMP_PPWMfG4nnr0vxF=h1264)
