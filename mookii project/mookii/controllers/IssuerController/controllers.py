from turbogears import controllers, expose, redirect, flash
from turbogears import validate, validators, flash, error_handler, exception_handler, config
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.sql import and_
from sqlalchemy import *
from mookii.model import session, Auction, AuctionItem, Item
from turbogears.widgets import WidgetsList, TableForm
from turbogears.paginate import paginate
from turbogears.widgets import TextField, DataGrid, Tabber, PaginateDataGrid, CalendarDatePicker, ResetButton, SingleSelectField, AutoCompleteField
from types import IntType, LongType, FloatType, StringType, FunctionType
from decimal import Decimal as DecimalType
from turbogears import identity
from turbogears import url
from cherrypy import request
#from turbogears import paginate
import logging
import locale
import time
from datetime import datetime
from kid.element import Element, SubElement

#from mookii.controllers.AuctionController import AuctionController
#from mookii.controllers.AuctionItemController import AuctionItemController
#from mookii.controllers.ItemController import ItemController

log = logging.getLogger("mookii.controllers.IssuerController")
locale.setlocale(locale.LC_ALL, '')



user_fields = []
group_fields = []
auction_fields = [('Auction Date', 'auction_date'),
                   ('Start of Auction', 'time_start'),
                   ('End of Auction', 'cut_off'),
                   ('Auction Status', 'status'),                
                   ('Created', 'created'), 
                ]


""" PAGINATION DEFINITIONS ARE CURRENTLY ON STAND BY, BUT READILY AVAILABLE ANYTIME """

paginate_auction_fields = PaginateDataGrid(
    fields=[
        PaginateDataGrid.Column('auction_date', 'auction_date', 'Auction Date'),
        PaginateDataGrid.Column('time_start', 'time_start', 'Start of Auction'),
        PaginateDataGrid.Column('cut_off', 'cut_off', 'End of Auction'),
        PaginateDataGrid.Column('status', 'status', 'Auction Status'),
        PaginateDataGrid.Column('created', 'created', 'Created'),
        ])




def isNumber(n):
    if type(n) in (IntType, LongType, FloatType, DecimalType):
        return True
    elif type(n) is (StringType):
        try:
            float(n)
            return True
        except:
            return False
    return False

def isDecimal(n):
    if type(n) is (DecimalType):
        return True
    elif type(n) is (StringType):
        try:
            float(n)
            return True
        except:
            return False
    return False


def convertNumberToCurrency(number):
        converted = ""
        temp = ""
        if str(number).find("(")>-1:
            temp = number.strip("()")
            converted = locale.format('%.2f',float(temp),grouping=True)
            converted = "(" + converted + ")"
        else:
            converted = locale.format('%.2f',float(number),grouping=True)        
        return converted

class ConvertIsoDate(validators.DateConverter):
    '''Converts date (yyyy-mm-dd) to mm-dd-yyyy'''

    def _to_python(self,value,state):
        value = value.replace('/','-')
        res = value.split('-',1)
        res.reverse()
        new_val = '-'.join(res)
        return validators.DateConverter._to_python(self,new_val,state)
                                                                                                                                                                                                                                       

#TODO:  Add additional format functionality to this function.
#         Example, alignment='right' should produce template code <td align="right"></td>

def format_field(record, field, element = '', alignment='', commatized='', font_face='', font_color='', font_size='', font=''):
    if type(field) is FunctionType:
        return field(record)
    try:
        output = getattr(record,field)
    except:
        output = "Unknown field: " + str(field)
        log.debug("Unknown field: " + str(field))
        return output
        
    if commatized == 'True':
        if isDecimal(getattr(record,field)):
            output = convertNumberToCurrency(getattr(record,field))                                             

            
    if alignment=='right' or alignment == 'left' or alignment == 'center':
        e = Element('div',align=alignment)
        e.text = output
        output = e
    
    return output


def details_url(record):
        
    #_url =  url("/trades/show/") + str(self.trade_date) + "_" + self.user_reference
    
    _url =  url(request.base + request.path + "show/") + str(record.trade_date) + "_" + record.user_reference
    #_url =  url("/trades/show/") + str(record.trade_date) + "_" + record.user_reference
    #link = ET.Element('a', href="http://localhost/repo/", style='text-decoration: underline' )
    link = Element('a', href="javascript:printThisPage('"+_url+"')", style='text-decoration: underline')
    #link = Element('a', href=_url, style='text-decoration: underline')
    link.text = "Show Details"
    return link    


class IssuerFields(WidgetsList):
    pass
    
class AutoCompleteValidator(validators.Schema):
    pass

class IssuerSchema(validators.Schema):
    pass

class IssuerForm(TableForm):
    fields = IssuerFields()
    validator = IssuerSchema()


issuer_form = IssuerForm()



class IssuerController(controllers.Controller,identity.SecureResource):
    require=identity.in_group("issuer")  
    
    #auction = AuctionController()
    @expose()
    def index(self, tg_errors=None, **kw):
        if tg_errors:          
            log.info('***********************************************************')
            log.info('TG_ERRORS: ' + str(tg_errors))
            log.info('KEYWORDS: ' + str(kw))
            log.info('***********************************************************')
            
            return self.__Issuer(tg_errors, **kw)        
        
        if(identity.in_group("issuer")):                        
            return self.__Issuer(**kw)        
        
        return {}

    expose()
    def __Issuer(self):
        
        a_fields = auction_fields[:]

        auction_grid = DataGrid(fields=a_fields)
        
        auctions = session.query(Auction)      
        
        return dict(tg_template="kid:mookii.templates.issuer",
                    auction_grid = auction_grid,
                    auctions = auctions,
                    Issuer_tabber=Tabber(),
                    now=datetime.today().strftime("%A, %d %b %Y")
                    )

    def default(self):
        raise redirect("index")

    @expose(template='kid:mookii.controllers.IssuerController.templates.list')
    #@paginate('records')
    def list(self, **kw):
        """List records in model"""
        records = session.query(Auction)

        return dict(records = records, modelname=self.modelname)

    @expose(template="kid:mookii.controllers.IssuerController.templates.paginate1")
    @paginate('auctions')
    def paginate1(self):
        
    
        auctions = session.query(Auction)
        return dict(auctions=auctions)


    @expose(template="kid:mookii.controllers.IssuerController.templates.paginate2")
    @paginate('auctions', default_order='auction_date')
    def paginate2(self):
        
        auction_list = PaginateDataGrid(
            fields=[
                PaginateDataGrid.Column('auction_date', 'auction_date', 'Auction Date'),
                PaginateDataGrid.Column('time_start', 'time_start', 'Start of Auction'),
                PaginateDataGrid.Column('cut_off', 'cut_off', 'End of Auction'),
                PaginateDataGrid.Column('status', 'status', 'Auction Status'),
                PaginateDataGrid.Column('created', 'created', 'Created'),
                ])

        sortable_auction_list = PaginateDataGrid(
            fields=[
                PaginateDataGrid.Column('auction_date', 'auction_date', 'Auction Date',
                                        options=dict(sortable=True, reverse_order=True)),
                PaginateDataGrid.Column('status', 'status', 'Auction Status',
                                        options=dict(sortable=True, reverse_order=True)),            
            ])
    
        auctions = session.query(Auction)
        return dict(auctions=auctions, list = sortable_auction_list)    

