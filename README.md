# Predicting customer behaviour using Starbucks data

## Background 

Targeted marketing has become a necessity in the communication strategy of every company. The hability to discern who is going to have a positive reaction to promotions, offers and other types forms of engagement can have a direct and major impact in the form of revenue.

A data agnostic strategy that relies heavily on mass emails messages and other forms of communication  not only requires a significant investment in marketing campaigns but can also be counterproductive when the messages are perceived as an annoyance or lacking of value for the potential customer. Such negative perceptions can have a detrimental impact on the company's image as a whole, and can ultimately discourage future purchases or engagement.

The Starbucks simulated dataset, which mimics real data of customer behaviour relative to different offers the company send to people in its data base proviedes an excelent opportunity to analyze how different types of customers react to different promotions. One way to analyze consumer behavior is by examining the probability of them completing an offer sent by Starbucks, by cross-referencing the consumer's demographic characteristics and the features of the offer itself, mainly, which type of offer generates a higher response for every type of customer. With a sensible data exporation and simple modeling one can extract interesting and useful insights that could be applied in practice for future campaigns.

## Data

The Starbucks dataset consists in three tables

- *profile*: table of 17.000 customers with demographic data, like age, income and gender, and suscription date
- *portfolio*: table containing the features of the different offers. There are 10 rows corresponding to 10 differnt feature combinations
- *transcript*: log of events containing offers recevied, viewed and completed, and transactions.


The transcript table is a log event for different profiels that entered in the database or "became member", from jul. 2013 to jul. 2018. Events are registered for aprrox. one month for each client.

THe main feature that differenciates the offers, present in the *portafilo* table is the offer type. There are three different types of offers

- **BOGO** (buy one, get one)
- **Discount**
- **Informational**

The first two have a reward for the customer, that are self explanatory. The informational offer is just that. It doesn't involve any kind of reward.




## Preparation

The nature of the log of events table and the very concept of completion offer makes the data wrangling an arduous process, where one have to keep track of when an offer is received, viewed and completed. Since one can only infere that an offer has influenced the desicion to buy a product if it has been viewed, an offer can only be counted as completed if there is a *view* event that goes before a *completion* event. 

For a more proper management of the event log data a `Custormer` class has been created, which structures each customer in a jerarquical structure where the information is contained in separate attributes for offers and transactions.


## Exploration

The exploration phase gave some interesting features, specially one related to the time a person became member: there are two periods when the number of customers spikes sudenly, and remains constant until the next spike, giving three different generations of customers.


![generations](https://github.com/MartinPons/Starbucks-customer-behaviour/blob/main/visualizations/generations.jpg)

It turns out this variable is one of the strongers predictors of the likelihood of a completion for BOGO offers, even when controlling for income, age and sex. There must be some underlying factor that define in a relevant way the characteristics of these three generations. The following plot reveals this difference when controling for gender.

![seniority_gender](https://github.com/MartinPons/Starbucks-customer-behaviour/blob/main/visualizations/completion_rate_by_seniority_and_gender.jpg)

Strong effects were also found for the channel distribution, and effects of some importance for age and gender, which are detailed in the blog post...


## Modeling

Since the major difference among the offer characteristics is the offer type, the main goal of the analysis is to know how different customer characteristics affect the likelyhood of completion for each type of offer. And since having an explicative outocme is essencial to ... two logistic models have been fitted

The difference between these models is how the offer type has been introduced: in the first model, it's specified as a predictor together with other potential predictors like income or age. In the second model the offer type interacts with every other variable in the model. If this second model perform better than the former. It's concluded that the offer types affect in a different way different groups of people.

No additional models have been tested. A more complex modeling could have been tried, increasing interception layers corrisng, age, gender and channel in a unique predictor for instance, but simplicity for the results has been prioritized over a more accuracte prediction.


## Evaluation

Before fitting, the data is separated in a training set and in a validation set. Precision, recall and F1 score are produced to compare the two models.

The model with interaction performs slighly better than the base model. Being the F1 score for non-completion 0.73, and the F1 score for completion 0.59. Generally, people from the second generation, females, people who identify with other gender, people older than 35 and people who receive the offer through social channels have a higher liklelihood of completion. The influence of social channels is strong specially for Discount offers while,  being from Gen 2 is more important for BOGO offers. This two type of offers however, don't present strong differences when it comes to demographic features like age or gender. It was found that overall, the in come does not significantly affect the likelihood of completing an offer.

Below there is a plot summarizing the likelihood of completing an offer for every group in the validation set, leaving the income to its average value

![Discount prob plot](https://github.com/MartinPons/Starbucks-customer-behaviour/blob/main/visualizations/probability_groups_point_discount.jpg)







