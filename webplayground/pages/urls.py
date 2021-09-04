from django.urls import path

from .views import PageListView, PageDetailView, PageCreate, PageUpdate, PageDelete

# De esta forma permite acceder a las url internamente pages:name_path
pages_patterns = ([
                      path('', PageListView.as_view(), name='pages'),
                      path('/<int:pk>/<slug:page_slug>/', PageDetailView.as_view(), name='page'),
                      path('/create/', PageCreate.as_view(), name='create'),
                      path('/update/<int:pk>/', PageUpdate.as_view(), name='update'),
                      path('/delete/<int:pk>/', PageDelete.as_view(), name='delete'),
                  ], 'pages')
