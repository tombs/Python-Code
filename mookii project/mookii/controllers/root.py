from turbogears import controllers, expose, flash, url
from mookii.controllers.IssuerController import IssuerController
import pkg_resources
try:
    pkg_resources.require("SQLAlchemy>=0.3.10")
except pkg_resources.DistributionNotFound:
    import sys
    print >> sys.stderr, """You are required to install SQLAlchemy but appear not to have done so. 
Please run your projects setup.py or run `easy_install SQLAlchemy`.
"""
    sys.exit(1)
from turbogears import identity, redirect
from cherrypy import request, response

class Root(controllers.RootController):
    @expose(template="mookii.templates.welcome")
    def index(self):
        import time
        flash("Your application is now running")
        return dict(now=time.ctime())

    issuer = IssuerController()
    #bidder = BidderController()
    #admin = AdminController()

    @expose(template="mookii.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            if identity.in_group("issuer"):
                forward_url= url("issuer")
            elif identity.in_group("bidder"):
                forward_url= url("bidder")
            elif identity.in_group("admin"):
                forward_url = url("admin")           
            raise redirect(forward_url)

        forward_url=None
        previous_url= request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")
            
        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")
