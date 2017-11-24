from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index),
  url(r'^register', views.register),
  url(r'^login', views.login),
  url(r'^dashboard', views.dashboard),
  url(r'^logout', views.logout),
  url(r'^new_item', views.new_item),
  url(r'^add_wish', views.add_wish),
  url(r'^remove_wish/(?P<item_id>\d+)$', views.remove_wish),
  url(r'^wish_item/(?P<item_id>\d+)$', views.wish_item),
  url(r'^delete/(?P<item_id>\d+)$', views.delete),
  url(r'^add_item/(?P<item_id>\d+)/(?P<user_id>\d+)$', views.add_item),

]