from django.urls import path
from .views import register_shop, search_shops, index, shop_list, update_shop, delete_shop

app_name = 'shops'

urlpatterns = [
    path('register/', register_shop, name='register_shop'),  # Path to register a shop
    path('search/', search_shops, name='search_shops'),  # Path to search shops by location
    path('list/', shop_list, name='shop_list'),  # Path to list all shops
    path('index/', index, name='shops_index'),  # Index page to show shop overview
    path('update/<int:shop_id>/', update_shop, name='update_shop'),  # Path to update a shop
    path('delete/<int:shop_id>/', delete_shop, name='delete_shop'),  # Path to delete a shop
]
