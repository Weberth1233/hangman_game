from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("game/", include("game.urls")),
    # path('api-auth/', include('rest_framework.urls'))
    #path('admin/', admin.site.urls),
]
