# Create your views here.

from django.template import RequestContext,loader
#from django.template import Context,loader #if we use shortcuts there is no need for this import
from django.views.decorators.csrf import csrf_protect #
from django.core.context_processors import csrf
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect #we have no redirects on server side 
from django.core.urlresolvers import reverse #we have no redirects here on server side 
from admin.models import *


def index(request,id=None):
    '''
    The view of users-list window
    '''
    
    if id!=None:
        id = int(id)
    
    if id>0:
        user = TestUsersAuth.objects.get(pk=id)
        user.delete()
        return HttpResponseRedirect('/admin/')
        
    users_list = TestUsersAuth.objects.all() #.order_by('cr_date')
    
    #By default render_to_response uses Context TEMPLATE_CONTEXT_PROCESSORS
    return render_to_response('admin/users_list.html',{'users_list':users_list})
    

#@csrf_protect
def edit(request,id,save=None):
    '''
    The view of user-edit popup 
        -load the initial view containing the form and csrf token
            -the form may be empty when id==0
            -the form may be filled when id>0
        -display the view containing the form csrf token and errors
            -the form will be filled and id>0
        -redirect the output to index page
    '''
    #print 'save="%s"' % 'None' if save==None else save
    
    id = abs(int(id))
    if save==None:
        if id>0:
            user = get_object_or_404(TestUsersAuth,pk=id)
        else:
            user = TestUsersAuth(id=0)
        #By default render_to_response uses Context TEMPLATE_CONTEXT_PROCESSORS
        response = render_to_response('admin/user_edit.html',{'user':user},
            context_instance=RequestContext(request)
        )
    elif save == 'save':
        if id == 0:
            user = TestUsersAuth()
            user_form = TestUsersAuthForm(request.POST, instance=user)
        elif id > 0:
            user = TestUsersAuth.objects.get(pk=id)
            user_form = TestUsersAuthForm(request.POST, instance=user)
        
        try:
            #Validation happens on save
            user_form.save()
            
            #if all savings are ok we will send a simple ajax response to tell the client
            #that main page can be reloaded (by the client) to refresh the users_list
            response = HttpResponse('Saved==True', mimetype="text/plain")
        except Exception,e:
            #TEMPLATE_CONTEXT_PROCESSORS are simple functions that automatically add to templates
            #specific parameters (for ex. rel. to security) like: csrf_token
            #RequestContext always use django.core.context_processors.csrf 
            #render_to_response can be forced to use RequestContext context
            user.error = e
            if user.error:
                user.id=0
            response = render_to_response('admin/user_edit.html',{'user':user},
                context_instance=RequestContext(request)
                #,[] #here we can add context processors functions (even our custom)
            )
            '''
            #only for test
            response = HttpResponse(e)
            '''
            
    else:
        raise Http404
    
    #this is a response to an ajax request
    return response
    

