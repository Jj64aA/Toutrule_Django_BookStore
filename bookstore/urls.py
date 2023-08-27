from django.urls import path,include 
from  . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('' ,views.home,name="home"),
    path('books/' ,views.books,name="books"),
    path('customer/<str:pk>' ,views.customer,name="customer"),
    #path('create/' ,views.create,name="create"),
    path('create/<str:pk>' ,views.create,name="create"),
    path('update/<str:pk>' ,views.update,name="update"),
    path('delete/<str:pk>' ,views.delete,name="delete"),

    path('register/',views.register,name="register"),
    path('login/',views.userlogin,name="login"),
    path('logout/',views.userlogout,name="logout"),

    path('admin/',views.home,name="admin"),
    path('addbook/',views.addbook,name="addbook"),
    path('user/',views.userProfile,name="user_profile"),
    path('profile/',views.profileInfo,name="profile_info"),




    path('rest_password/',auth_views.PasswordResetView.as_view,name="rest_password"),
    path('rest_password_sent/',auth_views.PasswordResetDoneView.as_view,name="rest_password_done"),
    path('rest/<uid64>/<token>/',auth_views.PasswordResetConfirmView.as_view,name="rest_password_confirm"),
    path('rest_password/',auth_views.PasswordResetCompleteView.as_view,name="rest_password_complete"),
]   

#templates
#my_order_form.html,name

#path('admin/',views.admin,name="admin")