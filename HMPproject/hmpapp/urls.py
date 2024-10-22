from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # path("projects/", views.projects, name="projects"),
    path("projects/<str:myslug>/", views.projects, name="projects"),  # Updated slug path
    path("addproject/", views.addproject, name="addproject"),
    path("projectdetails/<int:myid>/", views.projectdetails, name="projectdetails"),
    # path("projectdetails/", views.projectdetails, name="projectdetails"),

    
    # path("request/", views.request_view, name="request"),
    path("addrequest/", views.addrequest, name="addrequest"),
    path("request/<str:myslug>/", views.request_view, name="request_view"),  # Updated slug path

    path("updateRequestStatus/<int:req_id>/<str:new_status>/", views.updateRequestStatus, name="updateRequestStatus"),


    path("account/", views.account, name="account"),
    path("accounts/login/", views.user_login, name="user_login"),


    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_register/', views.user_register, name='user_register'),








    # path("viewNodes/", views.viewNodes, name="viewNodes"),
    # path("viewNodeData/", views.viewNodeData, name="viewNodeData"),
    # path("viewclusterData/", views.viewclusterData, name="viewclusterData"),
    # path("addnode/", views.addnode, name="addnode"),
    # path("addcluster/", views.addcluster, name="addcluster"),

  
    # path('user_login/', views.user_login, name='user_login'),
    # path('user_logout/', views.user_logout, name='user_logout'),
    # path('user_register/', views.user_register, name='user_register'),
  
    # path('sensor_data/', views.sensor_data, name='sensor_data'),
    # path('read_sensor_data/', views.read_sensor_data, name='read_sensor_data'),
    # path('apikeyGen/', views.your_view_function, name='your_view_function'),

    # path("contact/", views.contact, name="ContactUs"),
    # # path("products/<int:myid>", views.productView, name="ProductView"),
    # path("products/<str:myslug>", views.productView, name="ProductView"),
]
