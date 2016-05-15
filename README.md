# TRADEIT

Tradeit is a facebook messenger bot that allows you to trade with other users.

Using facebook messenger you start by uploading a picture and adding a description to the item you want to trade.

![alt text](https://scontent-sin1-1.xx.fbcdn.net/v/t34.0-12/13246140_120300000003876160_922088848_n.png?oh=89f8c0de998cc6dee876ea789aaca439&oe=573A0165 "Logo Title Text 1")

Once you start trading you will be matched with another item!
![alt text](https://scontent-sin1-1.xx.fbcdn.net/v/t34.0-12/13180928_120300000004207234_2003940716_n.png?oh=ac058cf6890d30bf2837a534c82f1e65&oe=5739C174 "Logo Title Text 1")

The description of the item is parsed using Tay Yi's NLP parser which gives us semantic tags about the description. The NLP Parser used amazon api to find additional attributes like price and rating which is eventually used for our matching.

With the use of the addition generated meta data we use cosine similarity to match items to each other.

This project was created by five NTU students using Django as the main engine and interfacing with Facebook's bot api.
