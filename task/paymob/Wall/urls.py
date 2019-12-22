from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static


from .views import (SignUp , account_activation_sent , activate ,
                    WallList , WallDetailsView ,YourWall,
                    WallCreate , WallUpdate , WallDelete,
                    )


urlpatterns = [
    path('', WallList.as_view() ,name='home'),
    path('wall/', YourWall ,name='wall'),
    path('signup/', SignUp ,name='signup'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>/',
        activate, name='activate'),
    path('new/' , WallCreate ,name='wall_create'),
    path('<slug:slug>/' ,WallDetailsView.as_view() ,name='wall_detail'),
    path('<str:slug>/edit' ,WallUpdate , name='wall_update'),
    path('<slug:slug>/remove' ,WallDelete , name='wall_delete'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
