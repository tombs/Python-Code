from mookii.model import *
from turbogears.database import session, metadata
from datetime import date, timedelta, datetime
from sqlalchemy import *
import random
import itertools


    
def basic_groups():    
    groups={'issuer':Group(**dict(group_name='issuer')),'bidder':Group(**dict(group_name='bidder')),'admin':Group(**dict(group_name='admin'))}
    session.flush()

    

def sample_auction(with_bids=False):

    try:
        bidder_group=session.query(Group).filter_by(group_name='bidder').one()
        issuer_group=session.query(Group).filter_by(group_name='issuer').one()
        admin_group =session.query(Group).filter_by(group_name='admin').one()
    except:
        print "Error in retreiving groups, exitting.."
        return

    groups = {'issuer':issuer_group, 'bidder':bidder_group, 'admin':admin_group}
    
    bidder1 = Member(**dict(member_name='Bidder1'))
    bidder2 = Member(**dict(member_name='Bidder2'))
    issuer1 = Member(**dict(member_name='Issuer1'))
    issuer2 = Member(**dict(member_name='Issuer2'))
    session.flush()

    b1User1 = User(**dict(user_name='user1@bidder1', display_name='User1@Bidder1', password='password'))
    b1User2 = User(**dict(user_name='user2@bidder1', display_name='User2@Bidder1', password='password'))
    b2User1 = User(**dict(user_name='user1@bidder2', display_name='User1@Bidder2', password='password'))
    b2User2 = User(**dict(user_name='user2@bidder2', display_name='User2@Bidder2', password='password'))

    i1User1 = User(**dict(user_name='user1@issuer1', display_name='User1@Issuer1', password='password'))
    i1User2 = User(**dict(user_name='user2@issuer1', display_name='User2@Issuer1', password='password'))
    i2User1 = User(**dict(user_name='user1@issuer2', display_name='User1@Issuer2', password='password'))
    i2User2 = User(**dict(user_name='user2@issuer2', display_name='User2@Issuer2', password='password'))
    session.flush()
    
    b1User1.members.append(bidder1)
    b1User2.members.append(bidder1)
    b2User1.members.append(bidder2)
    b2User2.members.append(bidder2)

    i1User1.members.append(issuer1)
    i1User2.members.append(issuer1)
    i2User1.members.append(issuer2)
    i2User2.members.append(issuer2)

    b1User1.groups.append(groups['bidder'])
    b1User2.groups.append(groups['bidder'])
    b2User1.groups.append(groups['bidder'])
    b2User2.groups.append(groups['bidder'])

    i1User1.groups.append(groups['issuer'])
    i1User2.groups.append(groups['issuer'])
    i2User1.groups.append(groups['issuer'])
    i2User2.groups.append(groups['issuer'])                          
    session.flush()

    i1Item1 = Item(**dict(owner_member_id=issuer1.member_id,name='Item1'))
    i1Item2 = Item(**dict(owner_member_id=issuer1.member_id,name='Item2'))
    i1Item3 = Item(**dict(owner_member_id=issuer1.member_id,name='Item3'))

    i2Item1 = Item(**dict(owner_member_id=issuer2.member_id,name='Item1'))
    i2Item2 = Item(**dict(owner_member_id=issuer2.member_id,name='Item2'))
    i2Item3 = Item(**dict(owner_member_id=issuer2.member_id,name='Item3'))                          

    auction1 = Auction(**dict(auction_date=datetime.today(),member_id=issuer1.member_id))
    auction2 = Auction(**dict(auction_date=datetime.today(),member_id=issuer2.member_id))

    session.flush()
    
    print "auction1.auction_id: ", auction1.auction_id
    print "auction2.auction_id: ", auction2.auction_id

    print "i1Item1.item_id: ", i1Item1.item_id
    print "i1Item2.item_id: ", i1Item2.item_id
    print "i2Item1.item_id: ", i2Item1.item_id
    print "i2Item2.item_id: ", i2Item2.item_id
    
    
    a1Item1 = AuctionItem(**dict(auction_id=auction1.auction_id,item_id=i1Item1.item_id))
    a1Item2 = AuctionItem(**dict(auction_id=auction1.auction_id,item_id=i1Item2.item_id))
    a2Item1 = AuctionItem(**dict(auction_id=auction2.auction_id,item_id=i2Item1.item_id))
    a2Item2 = AuctionItem(**dict(auction_id=auction2.auction_id,item_id=i2Item2.item_id))

    session.flush()

    if with_bids == True:
        b1Bid1 = Bid(**dict(auction_item_id=a1Item1.auction_item_id,
                            member_id=bidder1.member_id,
                            initial_bid_amount='100.00',
                            maximum_bid_amount='500.00',                            
                            ))

        b2Bid1 = Bid(**dict(auction_item_id=a1Item1.auction_item_id,
                            member_id=bidder1.member_id,
                            initial_bid_amount='200.00',
                            maximum_bid_amount='600.00',                            
                            ))

        b1Bid2 = Bid(**dict(auction_item_id=a2Item1.auction_item_id,
                            member_id=bidder1.member_id,
                            initial_bid_amount='1000.00',
                            maximum_bid_amount='5000.00',                            
                            ))

        b2Bid2 = Bid(**dict(auction_item_id=a2Item1.auction_item_id,
                            member_id=bidder1.member_id,
                            initial_bid_amount='2000.00',
                            maximum_bid_amount='6000.00',                            
                            ))
        session.flush()

        b1Sub1 = SubBid(**dict(bids_id=b1Bid1.bids_id, bid_amount='300.00'))
        
        b2Sub1 = SubBid(**dict(bids_id=b2Bid1.bids_id, bid_amount='400.00'))

        b1Sub2 = SubBid(**dict(bids_id=b1Bid2.bids_id, bid_amount='3000.00'))

        b2Sub1 = SubBid(**dict(bids_id=b2Bid1.bids_id, bid_amount='4000.00'))
        session.flush()

    
    
    
    


def main(argv=None):
    
    foo = input("Enter a value: ")
    print "The value is: ", foo
        
        

if __name__ == "__main__":
    sys.exit(main())    
    
    
        
        
