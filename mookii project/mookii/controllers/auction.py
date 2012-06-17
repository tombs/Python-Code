"""prints winning bid"""

class Auction(object):
    def __init__(self, end_time, start_time=None, not_public=False):
        """Default action object"""
        if start_time:
            self.start_time = start_time
        else:
            self.start_time = datetime.now()

        self.end_time = end_time
        self.not_public = not_public

    def times_up(self):
        return self.end_time < datetime.now()

    def cancel(self,bid_id):
        """Cancel a bid 
        """
        #FIXME: must validate ow
        print "in cancelling", bid_id
        bid = None
        for b in self.bids:
            if b.bid_id == bid_id:
                bid = b

        if bid:
            self.bids.remove(b)
            print "removed", b.bid_id, b.bidder_id, b.value

import time, random
def test_vickerey(npart):
    v = Vickery('vickery',100)
    bids = [] 
    for i in range(npart):
        bids.append(Bid(random.randint(1,npart),random.random()))
        v.accept(bids[-1])
        time.sleep(random.random())
        if(random.randint(1,10)>=8):
            v.cancel(bids[random.randint(0,lent(bids)-1)].bid_id)

    v.winner()


def test_dutch(npart):
    d = Dutch('dutch',100, 10, 5)
    bids = [] 
    for i in range(npart):
        bids.append(Bid(random.randint(1,npart), random.random()))
        d.accept(bids[-1])
        time.sleep(random.random())
        if(random.randint(1,10)>=11):
            print "cancelling"
            d.cancel(bids[random.randint(0,len(bids)-1)].bid_id)

    d.winner()

from datetime import datetime, timedelta
class Vickery(Auction):
    def __init__(self,name, duration, npart=None, reverse_value=False):
        print "Vickerey! No! This is actually a wrong implementation of 2nd sealed bid, wrong becuase you can bid multiple times "
        self.bids = []
        self.reverse_value = reverse_value
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(0,duration)

    def accept(self, bid):
        self.bids.append(bid)
        print "Got your bid %g, assigned with bidder number %d"%(bid.value,bid.bidder_id)
        if self.times_up():
            self.winner()
        return len(self.bids)

    def winner(self):
        """TODO: check for tie breaks, correct algo is get the winning bid but only pay/deduct the value of the second highest bid"""

        if not self.reverse_value:
            self.bids.sort()
        else:
            self.bids.reverse()
        win_value = self.bids[-2].value
        bid_id = self.bids[-1].bidder_id
        print "Winning Bid! Value:", win_value, "Bid id", bid_id


class English(Auction):
    def __init__(self,name, duration, participants=[], reserve_price=None, reverse_value=False):
        self.not_public = False
        self.bids = []
        self.reverse_value = reverse_value
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(0,duration)
        self.reserve_price = reserve_price

    def accept(self, bid):
        index = 0

        if self.times_up():
            self.winner()
            return

        for b in self.bids:
            if not self.reverse_value:
                if b.value<bid.value:
                    index += 1
                    continue
                else:
                    self.bids.insert(index,bid)
                    return
            else:
                if b.value>bid.value:
                    index += 1
                    continue
                else:
                    self.bids.insert(index,bid)
                    return
                

        self.bids.append(bid) #highest

    def highest(self):
        return self.bids[-1]

    def winner(self):
        winner = highest()
        if self.reserve_price and winner.value > self.reserve_price:
            print "winning bid:", winner.bidder_id, winner.value()
            return winner
        else:
            print "No winner, expecting price of:",  self.reserve_price, "got highest price of", winner.value, "from", winner.bidder_id
            return None

    
        
class Dutch(Auction):
    def __init__(self, name, duration, npart=None, quantity=1, reverse_value=False):
        print "Dutch!"
        self.not_public = False
        self.bids = []
        self.start_time = datetime.now()
        self.quantity = quantity
        self.end_time = self.start_time + timedelta(0,duration)

    def accept(self, bid, quantity=1):
        if self.times_up():
            self.winner()
            return

        index = 0

        for b in self.bids:
            if not self.reverse_value:
                if b.value<bid.value:
                    index += 1
                    continue
                else:
                    for q in range(quantity):
                        print "Got your bid %g, assigned with bidder number %d"%(bid.value,bid.bidder_id)
                        self.bids.insert(index,bid)
                        index += 1
                    return
            else:
                if b.value>bid.value:
                    index += 1
                    continue
                else:
                    for q in range(quantity):
                        print "Got your bid %g, assigned with bidder number %d"%(bid.value,bid.bidder_id)
                        self.bids.insert(index,bid)
                        index += 1
                    return

        self.bids.append(bid)
        print "Got your bid %g, assigned with bidder number %d"%(bid.value,bid.bidder_id)

    def winner(self):
        """Get rankings, allocate to highest bidder the required quantity at lowest qualifying price and proceed """
        winners = self.bids[-self.quantity:]
        print "Winning bid at" , winners[0].value
        for b in winners:
            print "bidder", b.bidder_id , "got 1 item"


       

import hashlib,random
class Bid(object):
    """Sample representation of bid object"""
    def __init__(self, bidder_id, value):
        self.bidder_id = bidder_id 
        self.value = value
        self.creation_stamp = datetime.now()
        self.status = 1 #{0:'in-active',1:'active',-1:'cancelled'}
        #FIXME: might there be a faster and simpler way of putting a unique id?
        self.bid_id = hashlib.sha256(self.creation_stamp.strftime("%X %x %N")+str(self.bidder_id)+str(random.random())).hexdigest()
        print "bid id:", self.bid_id

    def __cmp__(self,other):
        if self.value < other.value:
            return -1
        elif self.value == other.value:
            return 0
        elif self.value > other.value:
            return 1

        


class Bidder(object):
    """An entity with a capability to send/execute a bid"""
    def __init__(self):
        self.name = None
        self.credits = 0.0

class BidMatcher(object):
    def __init__(self,name):
        self.name = name
        print "Matcher:", self.name

if __name__ == "__main__":
    import sys
    #test_vickerey(int(sys.argv[1]))
    test_dutch(int(sys.argv[1]))
