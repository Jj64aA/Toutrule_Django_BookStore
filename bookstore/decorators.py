from django.shortcuts import redirect 
#----------------------------------------------------


def notLoggedUsers(view_func):
   def wrapper_func(request,*args,**Kwargs):
      if request.user.is_authenticated: 
         return redirect('/')
      else:
         return view_func(request,*args,**Kwargs)
   return wrapper_func    

#----------------------------------------------------

def allowedUsers(allowedGroups=[]):
   def decorator(view_func):
      def wrapper_func(request,*args,**Kwargs):
         group = None
         if  request.user.groups.exists():
            group = request.user.groups.all()[0].name
         if group in allowedGroups:
            return view_func(request,*args,**Kwargs)
         else :
            return redirect('user/')
      return wrapper_func
   return decorator
#----------------------------------------------------              
def forAdmins(view_func):
   def wrapper_func(request,*args,**Kwargs):
      group = None
      if  request.user.groups.exists():
         group = request.user.groups.all()[0].name
      if group =='admin':
         return view_func(request,*args,**Kwargs)
      if group =='customer':
         return redirect('user_profile')    
   return wrapper_func