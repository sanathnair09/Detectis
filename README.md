# Detectis
Sigmoid Hacks 2021 

By Sanath Nair

## Inspiration

With technology expanding and social media platforms being used more and more misinformation is also on the rise. Currently there is no easy way to detect whether an article is fake or not making it really hard to determine whether the information is actually trustworthy. To solve this I decided to use machine learning techniques that would be able to tell users whether or not an article is fake or not and other useful information.

## What it does

Detectis uses NLP to determine whether an article is fake or not. Users simply give the program the url to the news article they want to check and if they want a small section of the news article. The NLP model uses the information to then give a result about whether an article is biased or not. 

## How I built it

Detectis uses IBM’s Watson to get relevant metadata about an article such as the title, authors, and publisher. I also used Watson to get a document level sentiment and emotion analysis, which would help users gain a better understanding of the document's overall theme. Using the metadata I used Fakebox, which is a pretrained NLP model that determines whether an article is biased or not. The Fakebox model takes in the article url and title as input and optionally the content of the article. The NLP model then returns whether the article is biased or not and the confidence for that decision in JSON format. I then parse the information into a user readable format making it easy for people to view the result.

## Challenges I ran into

One challenge that I ran into was trying to get Watson to analyze the article and give me the relevant information that I needed. Originally I was only able to get Watson to give me the sentiment and emotion of the article but the metadata which I needed to feed into the Fakebox NLP model. After reading the docs I was able to find a solution which helped me with the relevant metadata. Another problem that I faced overall was processing the data that Watson and Fakebox returned. Since these API’s both returned the results in JSON format I had to make a program that would process the data and return only the information that I needed. 

## Accomplishments that I'm proud of

I am proud that I was able to determine whether the article was fake or not with high accuracy only being given a url. I originally thought that I would need to write a web scraper to get the content of the article and then pass that information but I realized that Watson would be able to do the same thing with a much high accuracy increasing the overall accuracy of my program. 

## What I learned

I learned about NLP and how machine learning can be used to find patterns in text. Since computers can’t directly understand text we need to do a little preprocessing of the data which converts the text into vectors which the computer can then use to make predictions or find patterns. 

## What's next for Detectis

I would like to create a website and host my program so that it is easy to use. I would also like to use transfer learning on the Fakebox model so that the accuracy is better. 
