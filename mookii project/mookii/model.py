from datetime import datetime
from turbogears.database import metadata, mapper, session
# import some basic SQLAlchemy classes for declaring the data model
# (see http://www.sqlalchemy.org/docs/04/ormtutorial.html)
from sqlalchemy import Table, Column, ForeignKey, Numeric, Text
from sqlalchemy.orm import relation
# import some datatypes for table columns from SQLAlchemy
# (see http://www.sqlalchemy.org/docs/04/types.html for more)
from sqlalchemy import String, Unicode, Integer, DateTime
from turbogears import identity




# your data tables

# your_table = Table('yourtable', metadata,
#     Column('my_id', Integer, primary_key=True)
# )


# your model classes


# class YourDataClass(object):
#     pass


# set up mappers between your data tables and classes

# mapper(YourDataClass, your_table)


issuers_table = Table('issuers', metadata,
    Column('issuer_id', Integer, primary_key=True),
    Column('issuer_name', String(40), nullable=False),
    Column('created', DateTime, nullable=False, default=datetime.now),
)

members_table = Table('members', metadata,
    Column('member_id', Integer, primary_key=True),
    Column('member_name', String(40), nullable=False, unique=True),
    Column('created', DateTime, nullable=False, default=datetime.now),
)

members_users_table = Table('members_users', metadata,
    Column('member_id', Integer, ForeignKey('members.member_id')),
    Column('user_id', Integer, ForeignKey('tg_user.user_id'))
)

auctions_table = Table('auctions', metadata,
    Column('auction_id', Integer, primary_key=True),
    Column('auction_date', DateTime, nullable=False),
    Column('time_start', Text, nullable=False, default='08:00'),
    Column('cut_off', Text, nullable=False, default='14:00'),
    Column('status', Integer, default=1),
    Column('member_id', Integer, ForeignKey('members.member_id')),
    Column('created', DateTime, nullable=False, default=datetime.now),
)

auction_items_table = Table('auction_items', metadata,
    Column('auction_item_id', Integer, primary_key=True),
    Column('auction_id', Integer, ForeignKey('auctions.auction_id')),
    Column('item_id', Integer, ForeignKey('items.item_id')),
    Column('minimum_bid', Numeric(length=2, precision=12), default='0.00'),
    Column('maximum_bid', Numeric(length=2, precision=12), default='0.00'),
    Column('status', Integer, default=1),
    Column('auction_type', Text(20), default='English'),
    Column('reverse_value', Integer, default=0),
    Column('created', DateTime, nullable=False, default=datetime.now),
)


items_table = Table('items', metadata,
    Column('item_id', Integer, primary_key=True),
    Column('name', Text),
    Column('description', Text,default=None),                    
    Column('owner_member_id', Integer, ForeignKey('members.member_id')),
    Column('status', Integer, default=1),  # status: created, acquired, auctioned, for settlement                    
    Column('created', DateTime, nullable=False, default=datetime.now),
)

item_history_table = Table('items_history', metadata,
    Column('item_history_id', Integer, primary_key=True),
    Column('item_id', Integer, ForeignKey('items.item_id')),
    Column('seller_member_id', Integer, ForeignKey('members.member_id')),
    Column('buyer_member_id', Integer, ForeignKey('members.member_id')),
    Column('settled', Integer, default=0),  # status: created, acquired, auctioned, for settlement                    
    Column('created', DateTime, nullable=False, default=datetime.now),
)

bids_table = Table('bids', metadata,
    Column('bids_id', Integer, primary_key=True),
    Column('auction_item_id', Integer, ForeignKey('auction_items.auction_item_id')),
    Column('member_id', Integer, ForeignKey('members.member_id')),
    Column('initial_bid_amount', Numeric(length=2, precision=12)),
    Column('maximum_bid_amount', Numeric(length=2, precision=12)),
    Column('status', Integer, default=1),  # status: created, acquired, auctioned, for settlement                                   
    Column('created', DateTime, nullable=False, default=datetime.now),
)

sub_bids_table = Table('sub_bids', metadata,
    Column('sub_bids_id', Integer, primary_key=True),
    Column('bids_id', Integer, ForeignKey('bids.bids_id')),
    Column('bid_amount', Numeric(length=2, precision=12)),
    Column('created', DateTime, nullable=False, default=datetime.now),
)


# the identity schema

visits_table = Table('visit', metadata,
    Column('visit_key', String(40), primary_key=True),
    Column('created', DateTime, nullable=False, default=datetime.now),
    Column('expiry', DateTime)
)

visit_identity_table = Table('visit_identity', metadata,
    Column('visit_key', String(40), primary_key=True),
    Column('user_id', Integer, ForeignKey('tg_user.user_id'), index=True)
)

groups_table = Table('tg_group', metadata,
    Column('group_id', Integer, primary_key=True),
    Column('group_name', Unicode(16), unique=True),
    Column('display_name', Unicode(255)),
    Column('created', DateTime, default=datetime.now)
)

users_table = Table('tg_user', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', Unicode(16), unique=True),
    Column('email_address', Unicode(255), unique=True),
    Column('display_name', Unicode(255)),
    Column('password', Unicode(40)),
    Column('created', DateTime, default=datetime.now)
)

permissions_table = Table('permission', metadata,
    Column('permission_id', Integer, primary_key=True),
    Column('permission_name', Unicode(16), unique=True),
    Column('description', Unicode(255))
)

user_group_table = Table('user_group', metadata,
    Column('user_id', Integer, ForeignKey('tg_user.user_id',
        onupdate='CASCADE', ondelete='CASCADE')),
    Column('group_id', Integer, ForeignKey('tg_group.group_id',
        onupdate='CASCADE', ondelete='CASCADE'))
)

group_permission_table = Table('group_permission', metadata,
    Column('group_id', Integer, ForeignKey('tg_group.group_id',
        onupdate='CASCADE', ondelete='CASCADE')),
    Column('permission_id', Integer, ForeignKey('permission.permission_id',
        onupdate='CASCADE', ondelete='CASCADE'))
)


# the identity model

class Bid(object):
    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)

class SubBid(object):
    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)

class Item(object):
    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)
class ItemHistory(object):
    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)

class Auction(object):
    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)
                
class AuctionItem(object):
    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)

class Member(object):
    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)

class MemberUser(object):
    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)

class Visit(object):
    """
    A visit to your site
    """
    def lookup_visit(cls, visit_key):
        return cls.query.get(visit_key)
    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(object):
    """
    A Visit that is link to a User object
    """
    pass


class Group(object):
    """
    An ultra-simple group definition.
    """
    pass


class User(object):
    """
    Reasonably basic User definition.
    Probably would want additional attributes.
    """

    def __init__(self,*args,**kw):
        for k,v in kw.iteritems():
            if hasattr(self,k):
                #print "setting", k, "with value", v
                if k == 'password':
                    v = identity.encrypt_password(v)
                setattr(self,k,v)
                
    def permissions(self):
        perms = set()
        for g in self.groups:
            perms |= set(g.permissions)
        return perms
    permissions = property(permissions)

    def by_email_address(cls, email):
        """
        A class method that can be used to search users
        based on their email addresses since it is unique.
        """
        return cls.query.filter_by(email_address=email).first()

    by_email_address = classmethod(by_email_address)

    def by_user_name(cls, username):
        """
        A class method that permits to search users
        based on their user_name attribute.
        """
        return cls.query.filter_by(user_name=username).first()

    by_user_name = classmethod(by_user_name)

    def _set_password(self, password):
        """
        encrypts password on the fly using the encryption
        algo defined in the configuration
        """
        self._password = identity.encrypt_password(password)

    def _get_password(self):
        """
        returns password
        """
        return self._password

    password = property(_get_password, _set_password)


class Permission(object):
    """
    A relationship that determines what each Group can do
    """
    pass


# set up mappers between identity tables and classes

mapper(Bid, bids_table)

mapper(SubBid, sub_bids_table,
        properties=dict(bids=relation(Bid, backref='sub_bids')))

mapper(Auction, auctions_table,
       properties=dict(members=relation(Member, backref='auctions')))

mapper(AuctionItem, auction_items_table,
       properties=dict(auction_items=relation(Auction, backref='auction_items')))

mapper(Item, items_table,
       properties=dict(members=relation(Member, backref='items')))

mapper(ItemHistory, item_history_table,
       properties=dict(items=relation(Item, backref='item_history')))

mapper(Member, members_table,
       properties=dict(users=relation(User, secondary=members_users_table, backref='members')))

mapper(Visit, visits_table)


mapper(VisitIdentity, visit_identity_table,
        properties=dict(users=relation(User, backref='visit_identity')))

mapper(User, users_table,
        properties=dict(_password=users_table.c.password))

#mapper(Group, groups_table)

mapper(Group, groups_table,
        properties=dict(users=relation(User,
                secondary=user_group_table, backref='groups')))

mapper(Permission, permissions_table,
        properties=dict(groups=relation(Group,
                secondary=group_permission_table, backref='permissions')))
