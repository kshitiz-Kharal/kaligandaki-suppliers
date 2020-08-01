from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop', views.shop, name='shop'),
    path('search', views.search, name='search'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('<int:product_id>', views.prodView, name='prodView'),
    path('signup', views.handleSignup, name='signup'),
    path('login', views.handleLogin, name='login'),
    path('logout', views.handleLogout, name='logout'),
    path('Checkout', views.checkout, name='checkout'),
    path('trackorder', views.tracker, name='tracker'),
    path('cart/', views.cart, name='cart'),
    path('postComment', views.postComment, name="postComment"),
    path('handlePayment', views.handlePayment, name='handlePayment'),
    path('<str:nopage>', views.nopage, name="nopage")
]
