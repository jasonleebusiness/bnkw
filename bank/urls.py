from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import views
from home.sitemaps import StaticViewSitemap
from django.contrib.sites.models import Site

sitemaps = {
    'static': StaticViewSitemap,
}

handler400 = 'home.views.handler400'
handler403 = 'home.views.handler403'
handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'
# handler400 = 'home.views.handler400'


urlpatterns = [
    path('bank-admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('account.urls')),
    path('robots.txt', include('robots.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('', include('django.contrib.auth.urls'))

]



admin.site.index_title = "Barclays"
admin.site.site_header = "Barclays Admin"
admin.site.site_title = "Barclays Admin"




if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
