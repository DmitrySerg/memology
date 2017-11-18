# Memology
**Memes - why so popular?**


This project is dedicated to the greatest achievement of humanity - Memes. Finding out the popularity of a meme based on its description and some other data from [KnowYourMeme.com](http://KnowYourMeme.com) sounds like a great idea for me. 

My workshop talk at DataFest4 about parsing websites (including KnowYourMeme) can be found [here](https://it.mail.ru/video/933/).

Parser outputs (*should output*) a csv file with the following fields:
- *name* - name of the meme
- *added* - date when it was added to the site
- *views* - guess what
- *comments* - quite obvious, eh?
- *status* - if the meme has been approved
- *year* - year of the appearence of the origin of the meme
- *tags* - what tags have been given to the meme
- *about* - description
- *origin* - another description - where the meme has come from
- *spread* - usually an empty fiels, sometimes it says what is the area of spread of the meme

The parser had three main versions:
- 1st - I was naive and hoped that the site would not ban me for my suspicious activities involving sending tons of requests, unfortunately, my IP got banned :(
- 2nd - I was less naive and tried to write a letter to the support team with the entreaty to unban me "because I was doing project, for science anb blah-blah". The answer was short and clear **"It's been unbanned"** with no sign of human being involved. Having that in mind I decided to create a spam-bot to send a letter to the support each time they ban my scrapper. And it worked! Partially...Our bots had been sending mails to one another for a couple of hours, I scrapped, they banned, I sent a letter - they replied. Those bots could chat happily ever after if not for the evil progressive increase of the ban time which made the whole system, well, entirely pointless. 
- 3rd - Let the anonymity strike! The final solution to the problem was to introduce a system with a dinamically changing IP, and this is where the [TOR](https://www.torproject.org/projects/torbrowser.html.en) brouser came in handy. Thanks to it, I was able to change my IP each and every two-three minutes which gave me anough time to scrap all the thing I wanted from several pages before being noticed and banned. Hourrah!

### Totally Awesome interface
![](https://habrastorage.org/files/d64/47e/ac9/d6447eac989f4453839529414b0bc20e.png)

### The project itself

[Memology.ipynb](https://github.com/DmitrySerg/memology/blob/master/Memology.ipynb) contains a short exploration of the dataset, with some graphs, statistics, etc., and, of course, text analysis and modelling. Based on the average views of the meme per day I have created 5 groups of "popularity" varying from "very unpopular" to "viral". To deal with the description tesx I used TF-IDF transformation, which then passed to Logit regression and Random Forest. Overall, the quality of the models was quite satisfactory, achieving accuracy of 0.43 (with the naive constant baseline of 0.2)


![](https://lh3.googleusercontent.com/2lV4Nm6oa9_hY2t-9tBbo3RAuEzcraalogZT0oPDmBqic4tWXliMP_PPWMfG4nnr0vxF=h1264)
