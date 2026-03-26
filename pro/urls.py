from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.login_view,name='login_view'),
    path('home',views.home,name='home'),
    path('pd',views.pd,name='pd'),
    path('cart_view',views.cart_view,name='cart_view'),
    path('add_cart/<int:id>',views.add_cart,name='add_cart'),
    path('buy',views.buy,name='buy'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('about/<int:id>',views.about,name='about'),
    path('logout/', views.logout_view, name='logout'),

    # path('cart/<int:id>',views.cart,name='cart'),

    path('addcat',views.addcat,name='addcat'),
    path('cl',views.cl,name='cl'),
    path('deletecat/<int:id>/',views.deletecat,name='deletecat'),
    path('editcat/<int:id>/',views.editcat,name='editcat'),
    path('cate_pro/<int:id>/',views.cate_pro,name='cate_pro'),
    path('show_pro/<int:id>/',views.show_pro,name='show_pro'),

    path('remove_cart/<int:id>',views.remove_cart,name='remove_cart'),
    path('update_cart/<int:id>/<str:action>/',views.update_cart,name='update_cart'),
    
    path('register/',views.register,name="register"),

    path('login/',views.login_view,name="login"),

    path('forgot/',views.forgot_password,name="forgot"),

    path('forgot/', views.forgot_phone_view, name='forgot'),

    path('verify/',views.verify_otp,name="verify_otp"),

    path('reset/',views.reset_password,name="reset_password"),
    
    path('otp/', views.otp_view, name='otp'),

    # path('aboutcat/<int:id>',views.aboutcat,name='aboutcat'),

]
