from collections import defaultdict
import numpy as np
import pandas as pd


class Customer:

    def __init__(self, transcript, customer):

        self.id = customer

        ## Events attribute: data frame of events where customer is participant
        self.events = transcript[transcript.person == customer].reset_index(drop=True)

        ## timelapse attribute: time days from the first event until the last event
        self.timelapse = max(self.events.time) - min(self.events.time)

        ## offers attribute: dictionary with all offer features including time for received, viewed and completed
        self.offers = dict()
        offers = self.events[self.events.event == "offer received"].offer_id.values

        # Because more than one offer with the same id can be received, new type of ids are created: every offer
        # received has different id id, even if it's the same offer

        # Initiate objects to assign ids

        offer_counter = 0
        new_offer_id = list()

        def list_type():
            return list()

        offers_received_mapping = defaultdict(list_type)
        offers_received_notviewed_mapping = defaultdict(list_type)
        offers_completed_mapping = defaultdict(list_type)
        new_offer_set = set([])

        # iterate the events in search of offers
        for row in range(self.events.shape[0]):

            offer_id = self.events.offer_id[row]

            # Every offer received has a new id. We keep track of the events in which the same offer is received
            if self.events.event[row] == "offer received":
                offer_counter += 1
                offers_received_mapping[offer_id].append(offer_counter)
                offers_received_notviewed_mapping[offer_id].append(offer_counter)
                new_offer_id.append(offer_counter)
                new_offer_set.add(
                    offer_counter)  # later we iterate over offers to add the features to the offers attribute

            # Ids for offer viewed events are assigned to the last offer received and not viewed
            # (sometimes an offer is viewed after completion)
            elif self.events.event[row] == "offer viewed":
                offer_key = offers_received_notviewed_mapping[offer_id].pop(-1)
                new_offer_id.append(offer_key)

            # Id for offer completed events are assigned to the last offer received
            elif self.events.event[row] == "offer completed":
                offer_key = offers_received_mapping[offer_id].pop(-1)
                offers_completed_mapping[offer_id].append(offer_key)

                new_offer_id.append(offer_key)

            # transaction events are filled with nan
            else:
                new_offer_id.append(np.nan)

        self.events['offer_reception_id'] = new_offer_id

        # print(self.events)

        # add features to offers attribute. The new ids will be the keys. Features will be the values
        for offer in new_offer_set:

            offer_events = self.events[self.events.offer_reception_id == offer]
            original_offer_id = offer_events[offer_events.event == "offer received"].offer_id.values[0]
            # print(original_offer_id)

            self.offers[offer] = dict()
            self.offers[offer]["id"] = original_offer_id
            self.offers[offer]["type"] = str(offer_events.offer_type.values[0])
            self.offers[offer]["duration"] = int(offer_events.duration.values[0])
            self.offers[offer]["when_received"] = int(offer_events[self.events.event == "offer received"].time.values)
            self.offers[offer]["when_viewed"] = None
            self.offers[offer]["when_completed"] = None

            # taking into account that the same offer can be viewed more than once. We only count the first time it is viewed
            if len(offer_events[offer_events.event == "offer viewed"].time.values != 0) and self.offers[offer][
                "when_viewed"] is None:
                self.offers[offer]["when_viewed"] = int(offer_events[self.events.event == "offer viewed"].time.values)

            if len(offer_events[offer_events.event == "offer completed"].time.values != 0):
                self.offers[offer]["when_completed"] = int(
                    offer_events[self.events.event == "offer completed"].time.values)

        ## Amounts attribute: dictionary with every amount spent, including timestamp

        self.transactions = dict()

        transaction_counter = 0
        for row in range(self.events.shape[0]):

            if self.events.iloc[row].event == "transaction":
                transaction_event = self.events.iloc[row]

                transaction_counter += 1
                self.transactions[transaction_counter] = dict()
                self.transactions[transaction_counter]["amount"] = transaction_event.value["amount"]
                self.transactions[transaction_counter]["time"] = transaction_event.time

    def get_completion_status(self):

        '''Returns a data frame with the completion status for one customer and other relevant information:
        the customer id, the offer id and when the offer has been received

        RETURNS

            DataFrame including the completion status for each offer received by a customer'''

        # initiate list of status completion and other relevant data
        offer_status = []

        for offer in self.offers:

            offer_id = self.offers[offer]['id']

            # an offer has to be viewed in order to be completed
            if self.offers[offer]["when_viewed"] is None:
                completed = 0

            # in order to complete the informational there has to be at least a transaction within the time
            # consider for the offer to have an influence
            elif self.offers[offer]["type"] == "informational":
                transaction_times = np.array([tr['time'] for tr in self.transactions.values()])

                completed = np.any((self.offers[offer]["when_received"] < transaction_times) &
                                   (self.offers[offer]["when_received"] + self.offers[offer][
                                       "duration"] >= transaction_times)) * 1

            # for the other types, when the offer has been viewed is considered completed
            # when we have registered a completion time before viewed time

            else:
                completed = (self.offers[offer]["when_completed"] is not None and
                             self.offers[offer]["when_completed"] >=
                             self.offers[offer]["when_viewed"]) * 1

            # append series with relevant information of the offer status
            offer_status.append((self.id, offer_id, completed, self.offers[offer]["when_received"]))

        # transform list of tuples into a data frme
        return pd.DataFrame(data=offer_status, columns=["client_id", "offer_id", "completed", "when_received"])
