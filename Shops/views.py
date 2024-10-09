from django.shortcuts import render, redirect
from .models import Shop
from django.http import HttpResponse
from .forms import ShopRegistrationForm
from django.http import JsonResponse
import math

def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'shops/shop_list.html', {'shops': shops})

def index(request):
    shops = Shop.objects.all()  # Retrieve all registered shops
    return render(request, 'shops/index.html', {'shops': shops})

def register_shop(request):
    if request.method == 'POST':
        form = ShopRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shops:shop_list')  # Redirect to a list view after registration
    else:
        form = ShopRegistrationForm()
    return render(request, 'shops/register_shop.html', {'form': form})

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers
    
def search_shops(request):
    if request.method == 'POST':
        user_latitude = request.POST.get('latitude')
        user_longitude = request.POST.get('longitude')

        if user_latitude and user_longitude:
            try:
                user_latitude = float(user_latitude)
                user_longitude = float(user_longitude)
            except ValueError:
                return HttpResponse("Invalid latitude or longitude values", status=400)
            
            # Fetch all shops from the database
            shops = Shop.objects.all()

            # Calculate distances between user and shops
            shop_distances = []
            for shop in shops:
                shop_distance = haversine(user_latitude, user_longitude, shop.latitude, shop.longitude)
                shop_distances.append((shop, shop_distance))

            # Sort shops by distance
            shop_distances.sort(key=lambda x: x[1])

            # Render the template with shop distances
            return render(request, 'shops/search_results.html', {'shop_distances': shop_distances})
        else:
            return HttpResponse("Both latitude and longitude must be provided", status=400)
    else:
        return render(request, 'shops/search_shops.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Shop
from .forms import ShopRegistrationForm
from django.http import HttpResponse, JsonResponse
import math

# Existing functions...

def update_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    if request.method == 'POST':
        form = ShopRegistrationForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shops:shop_list')  # Redirect to shop list after updating
    else:
        form = ShopRegistrationForm(instance=shop)
    return render(request, 'shops/register_shop.html', {'form': form})

def delete_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)  # Get the shop object or return 404 if not found
    if request.method == 'POST':
        shop.delete()  # Delete the shop
        messages.success(request, f'Shop "{shop.name}" has been deleted successfully.')  # Add success message
        return redirect('shops:shop_list')  # Redirect to the shop list page

