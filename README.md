# view finder
### a service to find different points of view on news stories

# Introduction
News outlets often tend to cover stories from a particular point of view and emphasize on that alone. There is no easy-to-use tool to find from other points of view. View Finder is a prototype to fill the gap.

# How to Use it
A user can copy/paste a snippet of text from the story they are reading into News Finder and News Finder finds relevant stories related to the snippet, each story labeled as liberal/conservative based on the bias in the story.

# Details
4k political news stories scraped from 4 different news websites
Trained model 1 to identify topics and keywords, using tfidif and nmf
Trained model 2 to classify content as conservative/liberal using Multinomial Naive Bayes
Used Bing Search API to find news stories based on topic keywords

# Coming Soon
Web app on AWS
Auto-detect and scrape webpage based on the url
More sources
