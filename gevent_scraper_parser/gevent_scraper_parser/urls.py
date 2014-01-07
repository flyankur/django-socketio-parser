from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# import pdb
# pdb.set_trace()
urlpatterns = patterns('',
	url(r'^', include('solomon_comm.urls')),

    # Examples:

    url(r'^scrape/', 'gevent_scraper_parser.views.scrapeData'),
    # url(r'^gevent_scraper_parser/', include('gevent_scraper_parser.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
