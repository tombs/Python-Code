#coding=utf-8
from turbogears import controllers, expose, redirect
from turbogears import validate, validators, flash, error_handler
from mookii.model import session, Bidder, Group
from mookii.controllers.crud import show_link, edit_link, destroy_link
from turbogears.widgets import WidgetsList, TableForm
# import required widget fields
from turbogears.widgets import TextField, PasswordField, CheckBoxList, PaginateDataGrid, SingleSelectField
from turbogears import identity
from turbogears import paginate
from datetime import datetime
import logging
log = logging.getLogger("mookii.controllers.BidderController")

class BidderFields(WidgetsList):
    """Replace to your Fields"""
    name = TextField(name="Bidder_name", label="Bidder Name")
    display = TextField(name="display_name", label="Display Name")
    status = SingleSelectField("status",   
                                options=["DISABLED","LOCKED","ENABLED"],  
                                default="DISABLED")
    groups = CheckBoxList(label = "Groups", name= "Bidder_groups", validator=validators.Int,
                          options=[(entry.group_id, entry.group_name) for entry in Group.select()])

    password = PasswordField(
      label=_(u'Password'),
      attrs=dict(maxlength=50),
      help_text=_(u'Specify your password.'))
    password_confirm = PasswordField(
      label=_(u'Confirm'),
      attrs=dict(maxlength=50),
     help_text=_(u'Enter the password again to confirm.')) 
   
    

class BidderSchema(validators.Schema):
    """
    separate validation schema from the fields definition
    make it possible to define a more complex schema
    that involves field dependency or logical operators
    """
    Bidder_name = validators.String(not_empty=True, max=16)
    status = validators.OneOf(['ENABLED','LOCKED','DISABLED'])
    password = validators.UnicodeString(max=50)
    password_confirm = validators.UnicodeString(max=50)
    chained_validators = [
      validators.FieldsMatch('password', 'password_confirm')
    ]

class BidderForm(TableForm):
    #name="Bidder"
    fields = BidderFields()
    validator = BidderSchema() # define schema outside of BidderFields
    #method="post"
    submit_text = "Create"


model_form = BidderForm()

class BidderEditFields(WidgetsList):
    """Replace to your Fields"""
 
              
    name = TextField(name="Bidder_name", label="Bidder Name")
    display = TextField(name="display_name", label="Display Name")
    status = SingleSelectField("status",   
                                options=["DISABLED","LOCKED","ENABLED"],  
                                default="DISABLED")                
    groups = CheckBoxList(label = "Groups", name= "Bidder_groups", validator=validators.Int,
                          options=[(entry.group_id, entry.group_name) for entry in Group.select()])

    password = PasswordField(
      label=_(u'Password'),
      attrs=dict(maxlength=50),
      help_text=_(u'Specify your password.'))
    password_confirm = PasswordField(
      label=_(u'Confirm'),
      attrs=dict(maxlength=50),
     help_text=_(u'Enter the password again to confirm.')) 
   
   

class BidderEditSchema(validators.Schema):
    """
    separate validation schema from the fields definition
    make it possible to define a more complex schema
    that involves field dependency or logical operators
    """
    Bidder_name = validators.String(not_empty=True, max=16)
    status = validators.OneOf(['ENABLED','LOCKED','DISABLED'])
    password = validators.UnicodeString(max=50)
    password_confirm = validators.UnicodeString(max=50)
    chained_validators = [
      validators.FieldsMatch('password', 'password_confirm')
    ]

class BidderEditForm(TableForm):
    #name="Bidder"
    fields = BidderEditFields()
    validator = BidderEditSchema() # define schema outside of BidderFields
    #method="post"
    submit_text = "Edit"

model_edit_form = BidderEditForm()


#protect BidderController with identity by include
#identity.SecureResource in superclass
class BidderController(controllers.Controller,identity.SecureResource):
    """Basic model admin interface"""
    modelname="Bidder"
    require=identity.in_group("bidder")

    @expose()
    def default(self, tg_errors=None):
        """handle non exist urls"""
        raise redirect("list")


    #require = identity.in_group("admin")
    @expose()
    def index(self):
        raise redirect("list")

    @expose(template='kid:mookii.templates.crudlist')
    @paginate('records')
    def list(self, **kw):
        """List records in model"""
        records = Bidder.select()

        grid = PaginateDataGrid(fields=[('Bidder Id', 'Bidder_id'),
            ('Bidder Name', 'Bidder_name'),('Show',show_link),('Edit',edit_link),('Delete',destroy_link)])

        return dict(records = records, modelname=self.modelname, grid=grid,
                    now=datetime.today().strftime("%A, %d %b %Y"))



    @expose(template='kid:mookii.controllers.BidderController.templates.new')
    def new(self, **kw):
        """Create new records in model"""

        return dict(modelname = self.modelname, form = model_form,
                    now= datetime.today().strftime("%A, %d %b %Y"))

    @expose(template='kid:mookii.controllers.BidderController.templates.edit')
    def edit(self, id, **kw):
        """Edit record in model"""

        try:
            record = Bidder.get(int(id))
            group_defaults=[entry.group_id for entry in record.groups]
        except:
            flash = "Not valid edit"
        
        log.info("Bidder_name: "+str(record.Bidder_name))    
        log.info("group_defaults: "+str(group_defaults))                       

        return dict(modelname = self.modelname,                    
                    record = record,
                    value=dict(Bidder_name = record.Bidder_name,status=record.status,Bidder_groups = group_defaults, display_name=record.display_name, password='password', password_confirm='password'),                    
                    #options=dict(Bidder_groups=[(entry.group_id, entry.group_name) for entry in Group.select()]),
                    form = model_edit_form,
                    now= datetime.today().strftime("%A, %d %b %Y"))

    @expose(template='kid:mookii.controllers.BidderController.templates.show')
    def show(self,id, **kw):
        """Show record in model"""
        record = Bidder.get(int(id))

        return dict(record = record,
                    now= datetime.today().strftime("%A, %d %b %Y"))

    @expose()
    def destroy(self, id):
        """Destroy record in model"""
        record = Bidder.get(int(id))
        session.delete(record)
        flash("Bidder was successfully destroyed.")
        raise redirect("../list")

    @validate(model_form)
    @error_handler(new)
    @expose()
    def save(self, id=None, **kw):
        """Save or create record to model"""
        #update kw
        
        log.info('kw: ' + str(kw))
        log.info('kw: ' + str(kw))
        log.info('kw: ' + str(kw))
        log.info('kw: ' + str(kw))
        log.info('kw: ' + str(kw))
        

        try:
            if isinstance(kw['Bidder_groups'],list):
                groups = Group.select(Group.c.group_id.in_(*kw['Bidder_groups']))
            else:
                groups = Group.select(Group.c.group_id.in_(kw['Bidder_groups']))
        except:
            groups = []
            
        

        #create
        if not id:                
            kw['groups']=groups
            Bidder(**kw)
            flash("Bidder was successfully created.")
            raise redirect("list")
        #update
        else:

            record = Bidder.get_by(Bidder_id=int(id))
            for attr in kw:
                setattr(record, attr, kw[attr])
            record.groups = groups
            log.info("Saved update on Bidder " + record.Bidder_name + str(kw))

            flash("Bidder was successfully updated.")
            raise redirect("../list")

    @validate(model_edit_form)
    @error_handler(edit)
    @expose()
    def update(self, id=None, **kw):
        """Save or create record to model"""
        #update kw
        
        log.info('kw: ' + str(kw))
        log.info('kw: ' + str(kw))
        log.info('kw: ' + str(kw))
        log.info('kw: ' + str(kw))
        log.info('kw: ' + str(kw))
        

        try:
            if isinstance(kw['Bidder_groups'],list):
                groups = Group.select(Group.c.group_id.in_(*kw['Bidder_groups']))
            else:
                groups = Group.select(Group.c.group_id.in_(kw['Bidder_groups']))
        except:
            groups = []
            
        

        #create
        if not id:                
            kw['groups']=groups
            Bidder(**kw)
            flash("Bidder was successfully created.")
            raise redirect("list")
        #update
        else:

            record = Bidder.get_by(Bidder_id=int(id))
            for attr in kw:
                if attr == 'password':
                    setattr(record, attr, identity.encrypt_password(kw[attr]))
                else:
                    setattr(record, attr, kw[attr])
            record.groups = groups
            log.info("Saved update on Bidder " + record.Bidder_name + str(kw))

            flash("Bidder was successfully updated.")
            raise redirect("../list")        
