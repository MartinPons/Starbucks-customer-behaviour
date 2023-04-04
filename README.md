# Predicting customer behaviour using Starbucks data

## Background 

Targeted marketing has become a necessity in the communication strategy of every company. The hability to discern who is going to have a positive reaction to promotions, offers and other types forms of engagement can have a direct and major impact in the form of revenue.

A data agnostic strategy that relies heavily on mass emails messages and other forms of communication  not only requires a significant investment in marketing campaigns but can also be counterproductive when the messages are perceived as an annoyance or lacking of value for the potential customer. Such negative perceptions can have a detrimental impact on the company's image as a whole, and can ultimately discourage future purchases or engagement.

The Starbucks simulated dataset, which mimics real data of customer behaviour relative to different offers the company send to people in its data base proviedes an excelent opportunity to analyze how different types of customers react to different promotions. One way to analyze consumer behavior is by examining the probability of them completing an offer sent by Starbucks, by cross-referencing the consumer's demographic characteristics and the features of the offer itself, mainly, which type of offer generates a higher response for every type of customer. With a sensible data exporation and simple modeling one can extract interesting and useful insights that could be applied in practice for future campaigns.

[In this blog post](https://medium.com/@martin.pons.martinez/two-discounted-coffees-better-than-one-34fc726f1bfb) there is a more detailed and complete version of the analysis

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

Since the major difference among the offer characteristics is the offer type, the main goal of the analysis is to know how different customer characteristics affect the likelihood of completion for each type of offer. Since this goal is explanatory in nature, a model which provides an explanatory outcome is needed. Taking this in mind two different logistic models have been fitted . These models differ in how the offer type has been introduced: in the first model, it's specified as a predictor together with other potential predictors like income or age. In the second model the offer type interacts with every other variable in the model. If this second model perform better than the former., it's concluded that the offer types affect in a different way different groups of people. Parameter tunning has also been conducted in order to obtain additional improvements from these models.

No additional models have been tested. A more complex modeling could have been tried, increasing interception layers corrisng, age, gender and channel in a unique predictor for instance, but simplicity for the results has been prioritized over a more accuracte prediction.

Before fitting, the data is separated in a training set and in a validation set. Precision, recall and F1 score are produced to compare the two models. To measure the influence of the variables in the outcome, practical effects computing effect sizes through the odds-ratio have been prefered over p-values in search of statistically significant effects (with such a high number of observations is not rare to find statistically significant effects with almost null practicall effects).


## Results

The model with interaction performs slighly better than the base model. Being the F1 score for non-completion 0.73, and the F1 score for completion 0.59. Generally, people from the second generation, females, people who identify with other gender, people older than 35 and people who receive the offer through social channels have a higher liklelihood of completion. The influence of social channels is strong specially for Discount offers while being from Gen 2 is also important in predicting completion for BOGO offers. This two type of offers however, don't present strong differences when it comes to age and gender. It was found that overall, income does not significantly affect the likelihood of completing an offer.

Below there is a plot summarizing the likelihood of completing an offer for every group in the validation set, leaving the income to its average value.

![Discount prob plot](https://github.com/MartinPons/Starbucks-customer-behaviour/blob/main/visualizations/probability_groups_point_discount.jpg)


## File description

- **StarbucksAnalysis**: module made specifically for this analysis. It's structured in three files.
	- Customer.py: contains the `Customer` class. It's use to wrangle the data of the log events in the `transcript` data frame. In its current form, it only contains one method to properly classify the offers according to the completion status, but more methods are going to be added in the future in order to enrich and refocus the analysis, like a method to assign total amounts that are made because of an offer, and amounts corresponding to transactions made with no offer being the cause.
	- model.py: contains the function `fit_logistic` to prepare and fit the data of logistic models, with and without interactions with the type of offer, and other functions  to print the outcome and the model summary in a more readable way.
	-  visualizations.py: functions for visualize the data for communicative purposes.
- **processed_data**: folder containing a csv file and a pickle file, which are the result of running the wrangling and EDA notebooks and obtaining tables with the offer completion status in different states of cleanliness.
- **raw_data**: folder containing the three files from the Starbucks dataset: `portfolio`, `profile` and `transcript`.
- **visualizations**: folder with the visualizations used to communicate the findings of the analysis.
- **01-Data Wrangling.ipynb** notebook with the data wrangling process. The outcome of this process is the `offers` data frame, with the completion status of each offer properly classified.
- **02-EDA.ipynb**: notebook with the data exploration which includes visualization, tables and briefly explains the interesting findings. Additional cleaning is also perfomed in this notebook.
- **03-Modeling.ipynb**: notebook containing the model fitting and the outcome.
- **04-visualizations.ipynb**: notebook with the codes for the visualizations that are used to communicate the results.
- **README.md**: a readme file with a summary of the analysis.
- **requirements.txt**: requirements file with the modules used in the analysis.

## Installation and libraries

This code runs with Python version 3.9.13. This are the libraries that have been use for this project

matplotlib==3.5.2
numpy==1.21.5
pandas==1.4.4
patsy==0.5.2
scikit_learn==1.2.2
seaborn==0.11.2
statsmodels==0.13.2


# Adnowledgements

The Data from this project is provided by Starbucks, which uses a program to simulate "how people make purchasing decisions and how those decisions are influenced by promotional offers". The dataset is part of a set of projects in the Data Science nanodegree by Udacity, and it's currently available in the [Kaggle website](https://www.kaggle.com/datasets/ihormuliar/starbucks-customer-data).




