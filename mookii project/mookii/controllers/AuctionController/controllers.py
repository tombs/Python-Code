#coding=utf-8
from turbogears import controllers, expose, redirect
from turbogears import validate, validators, flash, error_handler
from repo.model import session, User, Group
from repo.controllers.crud import show_link, edit_link, destroy_link
from turbogears.widgets import WidgetsList, TableForm
# import required widget fields
from turbogears.widgets import TextField, PasswordField, CheckBoxList, PaginateDataGrid, SingleSelectField
from turbogears import identity
from turbogears import paginate
from datetime import datetime
import logging
log = logging.getLogger("repo.controllers.UserController")

class UserFields(WidgetsList):
    """Replace to your Fields"""
    name = TextField(name="user_name", label="User Name")
    display = TextField(name="display_name", label="Display Name")
    status = SingleSelectField("status",   
                                options=["DISABLED","LOCKED","ENABLED"],  
                                default="DISABLED")
    groups = CheckBoxList(label = "Groups", name= "user_groups", validator=validators.Int,
                          options=[(entry.group_id, entry.group_name) for entry in Group.select()])

    password = PasswordField(
      label=_(u'Password'),
      attrs=dict(maxlength=50),
      help_text=_(u'Specify your password.'))
    password_confirm = PasswordField(
      label=_(u'Confirm'),
      attrs=dict(maxlength=50),
     help_text=_(u'Enter the password again to confirm.')) 
   
    

class UserSchema(validators.Schema):
    """
    separate validation schema from the fields definition
    make it possible to define a more complex schema
    that involves field dependency or logical operators
    """
    user_name = validators.String(not_empty=True, max=16)
    status = validators.OneOf(['ENABLED','LOCKED','DISABLED'])
    password = validators.UnicodeString(max=50)
    password_confirm = validators.UnicodeString(max=50)
    chained_validators = [
      validators.FieldsMatch('password', 'password_confirm')
    ]

class UserForm(TableForm):
    #name="User"
    fields = UserFields()
    validator = UserSchema() # define schema outside of UserFields
    #method="post"
    submit_text = "Create"


model_form = UserForm()

class UserEditFields(WidgetsList):
    """Replace to your Fields"""
 
              
    name = TextField(name="user_name", label="User Name")
    display = TextField(name="display_name", label="Display Name")
    status = SingleSelectField("status",   
                                options=["DISABLED","LOCKED","ENABLED"],  
                                default="DISABLED")                
    groups = CheckBoxList(label = "Groups", name= "user_groups", validator=validators.Int,
                          options=[(entry.group_id, entry.group_name) for entry in Group.select()])

    password = PasswordField(
      label=_(u'Password'),
      attrs=dict(maxlength=50),
      help_text=_(u'Specify your password.'))
    password_confirm = PasswordField(
      label=_(u'Confirm'),
      attrs=dict(maxlength=50),
     help_text=_(u'Enter the password again to confirm.')) 
   
   

class UserEditSchema(validators.Schema):
    """
    separate validation schema from the fields definition
    make it possible to define a more complex schema
    that involves field dependency or logical operators
    """
    user_name = validators.String(not_empty=True, max=16)
    status = validators.OneOf(['ENABLED','LOCKED','DISABLED'])
    password = validators.UnicodeString(max=50)
    password_confirm = validators.UnicodeString(max=50)
    chained_validators = [
      validators.FieldsMatch('password', 'password_confirm')
    ]

class UserEditForm(TableForm):
    #name="User"
    fields = UserEditFields()
    validator = UserEditSchema() # define schema outside of UserFields
    #method="post"
    submit_text = "Edit"

model_edit_form = UserEditForm()


#protect UserController with identity by include
#identity.SecureResource in superclass
class UserController(controllers.Controller,identity.SecureResource):
    """Basic model admin interface"""
    modelname="User"
    require=identity.in_group("admin")

    @expose()
    def default(self, tg_errors=None):
        """handle non exist urls"""
        raise redirect("list")


    #require = identity.in_group("admin")
    @expose()
    def index(self):
        raise redirect("list")

    @expose(template='kid:repo.templates.crudlist')
    @paginate('records')
    def list(self, **kw):
        """List records in model"""
        records = User.select()

        grid = PaginateDataGrid(fields=[('User Id', 'user_id'),
            ('User Name', 'user_name'),('Show',show_link),('Edit',edit_link),('Delete',destroy_link)])

        return dict(records = records, modelname=self.modelname, grid=grid,
                    now=datetime.today().strftime("%A, %d %b %Y"))



    @expose(template='kid:repo.controllers.UserController.templates.new')
    def new(self, **kw):
        """Create new records in model"""

        return dict(modelname = self.modelname, form = model_form,
                    now= datetime.today().strftime("%A, %d %b %Y"))

    @expose(template='kid:repo.controllers.UserController.templates.edit')
    def edit(self, id, **kw):
        """Edit record in model"""

        try:
            record = User.get(int(id))
            group_defaults=[entry.group_id for entry in record.groups]
        except:
            flash = "Not valid edit"
        
        log.info("user_name: "+str(record.user_name))    
        log.info("group_defaults: "+str(group_defaults))                       

        return dict(modelname = self.modelname,                    
                    record = record,
                    value=dict(user_name = record.user_name,status=record.status,user_groups = group_defaults, display_name=record.display_name, password='password', password_confirm='password'),                    
                    #options=dict(user_groups=[(entry.group_id, entry.group_name) for entry in Group.select()]),
                    form = model_edit_form,
                    now= datetime.today().strftime("%A, %d %b %Y"))

    @expose(template='kid:repo.controllers.UserController.templates.show')
    def show(self,id, **kw):
        """Show record in model"""
        record = User.get(int(id))

        return dict(record = record,
                    now= datetime.today().strftime("%A, %d %b %Y"))

    @expose()
    def destroy(self, id):
        """Destroy record in model"""
        record = User.get(int(id))
        session.delete(record)
        flash("User was successfully destroyed.")
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
            if isinstance(kw['user_groups'],list):
                groups = Group.select(Group.c.group_id.in_(*kw['user_groups']))
            else:
                groups = Group.select(Group.c.group_id.in_(kw['user_groups']))
        except:
            groups = []
            
        

        #create
        if not id:                
            kw['groups']=groups
            User(**kw)
            flash("User was successfully created.")
            raise redirect("list")
        #update
        else:

            record = User.get_by(user_id=int(id))
            for attr in kw:
                setattr(record, attr, kw[attr])
            record.groups = groups
            log.info("Saved update on user " + record.user_name + str(kw))

            flash("User was successfully updated.")
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
            if isinstance(kw['user_groups'],list):
                groups = Group.select(Group.c.group_id.in_(*kw['user_groups']))
            else:
                groups = Group.select(Group.c.group_id.in_(kw['user_groups']))
        except:
            groups = []
            
        

        #create
        if not id:                
            kw['groups']=groups
            User(**kw)
            flash("User was successfully created.")
            raise redirect("list")
        #update
        else:

            record = User.get_by(user_id=int(id))
            for attr in kw:
                if attr == 'password':
                    setattr(record, attr, identity.encrypt_password(kw[attr]))
                else:
                    setattr(record, attr, kw[attr])
            record.groups = groups
            log.info("Saved update on user " + record.user_name + str(kw))

            flash("User was successfully updated.")
            raise redirect("../list")        
