# Create your views here.

from django.template import RequestContext,loader
#from django.template import Context,loader #if we use shortcuts there is no need for this import
from django.views.decorators.csrf import csrf_protect #
from django.core.context_processors import csrf
from django.shortcuts import render_to_response,get_object_or_404
from django.http import QueryDict,HttpResponse,Http404,HttpResponseRedirect #we have no redirects on server side 
from django.core.urlresolvers import reverse #we have no redirects here on server side 
from exadmin.models import *


def index(request,id=None):
    '''
    The view of users-list window
    '''
    
    if id!=None:
        id = int(id)
    
    if id>0:
        user = TestUsersAuth.objects.get(pk=id)
        user.delete()
        #return HttpResponseRedirect('/exadmin/')
        return HttpResponseRedirect(reverse('exadmin.views.index'))
        
    users_list = TestUsersAuth.objects.all().order_by('username')
    
    #By default render_to_response uses Context TEMPLATE_CONTEXT_PROCESSORS
    return render_to_response('exadmin/users_list.html',{'users_list':users_list})
    

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
    
    #print request.POST
    
    id = abs(int(id))
    if save==None:
        if id>0:
            #user = get_object_or_404(TestUsersAuth,pk=id)
            user = TestUsersAuth.objects.get(pk=id)
            #user.password=''
        else:
            user = TestUsersAuth(id=0)
            #we don't want the password to be displayed in form
            
        user_form = TestUsersAuthForm(instance=user)
        
        #By default render_to_response uses Context TEMPLATE_CONTEXT_PROCESSORS
        response = render_to_response('exadmin/user_edit.html',{
            'user_form':user_form,
            'user':user                 #only for the id hidden field
            },
            context_instance=RequestContext(request)
        )
    elif save == 'save':
        if id == 0:
            user = TestUsersAuth()
            user.id=id
        elif id > 0:
            user = TestUsersAuth.objects.get(pk=id)
            
        
        user_form = TestUsersAuthForm(request.POST, instance=user)
        
        if user_form.is_valid():
            #a global Validation happens on save
            
            user_form.save()
            
            #if all savings are ok we will send a simple ajax response to tell the client
            #that main page can be reloaded (by the client) to refresh the users_list
            response = HttpResponse('Saved==True', mimetype="text/plain")
            
        else:
            response = render_to_response('exadmin/user_edit.html',{
                'user_form':user_form,
                'user':user             #only for id hidden field
                },
                context_instance=RequestContext(request)
                #,[] #here we can add context processors functions (even our custom)
            )
    else:
        raise Http404
    
    #this is a response to an ajax request
    return response
    


def index_1(request):
    '''
    The view of users-list window
    '''
    
    users_list = TestUsersAuth.objects.all().order_by('username')
    
    #By default render_to_response uses Context TEMPLATE_CONTEXT_PROCESSORS
    return render_to_response('exadmin/users_list.html',{'users_list':users_list})
    

def edit_1(request,id,save=None):
    id = abs(int(id))
    if save==None:
        if id>0:
            #user = get_object_or_404(TestUsersAuth,pk=id)
            user = TestUsersAuth.objects.get(pk=id)
            #user.password=''
        else:
            user = TestUsersAuth(id=0)
            #we don't want the password to be displayed in form
            
        user_form = TestUsersAuthForm(instance=user)
        
        #By default render_to_response uses Context TEMPLATE_CONTEXT_PROCESSORS
        response = render_to_response('exadmin/user_edit.html',{
            'user_form':user_form,
            'user':user                 #only for the id hidden field
            },
            context_instance=RequestContext(request)
        )
    elif save == 'save':
        if id == 0:
            user = TestUsersAuth()
            user.id=id
        elif id > 0:
            user = TestUsersAuth.objects.get(pk=id)
        
        user_form = TestUsersAuthForm(request.POST, instance=user)
        
        if user_form.is_valid():
            if id==0:
                #user_form.instance.objects.create_user()
                TestUsersAuth.objects.create_user(user_form.data)
            elif id > 0:
                #user_form.instance.objects.update_user()
                TestUsersAuth.objects.update_user(user_form.data)
            
            #if all savings are ok we will send a simple ajax response to tell the client
            #that main page can be reloaded (by the client) to refresh the users_list
            response = HttpResponse('Saved==True', mimetype="text/plain")
        else:
            response = render_to_response('exadmin/user_edit.html',{
                'user_form':user_form,
                'user':user             #only for id hidden field
                },
                context_instance=RequestContext(request)
                #,[] #here we can add context processors functions (even our custom)
            )
    else:
        raise Http404
    
    #this is a response to an ajax request
    return response
    

def delete_1(request,id):
    '''
    The delete
    '''
    
    id = int(id)
    if id>0:
        data = QueryDict('id=%d' % id)
        TestUsersAuth.objects.delete_user(data)
    
    return HttpResponseRedirect(reverse('exadmin.views.index_1'))
    