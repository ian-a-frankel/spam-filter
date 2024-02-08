This is an implementation of the multinomial naive Bayes algorithm to determine if a text message is spam.

The dataset in the file SMSSpamCollection was put together by Tiago A. Almeida and José María Gómez Hidalgo, and it can be downloaded from the The UCI Machine Learning Repository:

https://archive.ics.uci.edu/dataset/228/sms+spam+collection

It has been saved as SMSSpamCollection in this repository.

The dataset contains 5574 SMS messages, classified as spam or not spam by humans. About 13 percent of the messages are marked as spam.

Randomly selecting about 80% of the messages as training data, we test the model on the remaining messages. We find it predicts whether or not a message is spam with 98-99 percent accuracy.