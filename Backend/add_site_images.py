import os
import sys
import django
import urllib.request
from io import BytesIO
from django.core.files import File

# Add the project directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'natourcam.settings')
django.setup()

from tourism.models import TouristSite, SiteImage

def download_image(url, filename):
    """Download image from URL and return a Django File object"""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status == 200:
                return File(BytesIO(response.read()), name=filename)
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

def add_images():
    # Image URLs for each site (using Unsplash and Pexels)
    site_images = {
        'Douala Zoo': [
            'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=800',  # Zoo animals
            'https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=800',  # Lion
        ],
        'Mount Cameroon': [
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',  # Mountain peak
            'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800',  # Mountain landscape
        ],
        'Limbe Botanical Garden': [
            'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800',  # Botanical garden
            'https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=800',  # Garden path
        ],
        'Kribi Beach': [
            'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',  # Beach
            'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800',  # Tropical beach
        ],
        'Chutes de la Lobé': [
            'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800',  # Waterfall
            'https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=800',  # Waterfall ocean
        ],
        'Mefou National Park': [
            'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=800',  # Gorilla
            'https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=800',  # Wildlife
        ],
        'Waza National Park': [
            'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800',  # Elephant
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=800',  # Giraffe
        ],
        'Rhumsiki Peak': [
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',  # Mountain peak
            'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800',  # Mountain landscape
        ],
        'Dja Faunal Reserve': [
            'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800',  # Forest elephant
            'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800',  # Rainforest
        ],
        'Foumban Royal Palace': [
            'https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800',  # Palace architecture
            'https://images.unsplash.com/photo-1548013146-72479768bada?w=800',  # Traditional building
        ],
        'Lac Ossa': [
            'https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=800',  # Lake
            'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800',  # Serene lake
        ],
        'Bafut Palace': [
            'https://images.unsplash.com/photo-1548013146-72479768bada?w=800',  # Traditional palace
            'https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800',  # Palace courtyard
        ],
        'Ekom-Nkam Waterfalls': [
            'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800',  # Waterfall
            'https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=800',  # Forest waterfall
        ],
        'Korup National Park': [
            'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800',  # Rainforest
            'https://images.unsplash.com/photo-1511497584788-876760111969?w=800',  # Forest canopy
        ],
        'Bamenda Ring Road': [
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',  # Mountain road
            'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800',  # Scenic road
        ],
    }
    
    for site_name, image_urls in site_images.items():
        try:
            site = TouristSite.objects.get(name=site_name)
            
            # Delete existing images for this site
            SiteImage.objects.filter(site=site).delete()
            
            # Add new images
            for idx, url in enumerate(image_urls):
                filename = f"{site_name.replace(' ', '_').lower()}_{idx+1}.jpg"
                image_file = download_image(url, filename)
                
                if image_file:
                    SiteImage.objects.create(
                        site=site,
                        image=image_file,
                        caption=f"{site_name} - View {idx+1}",
                        is_primary=(idx == 0)  # First image is primary
                    )
                    print(f"Added image {idx+1} for {site_name}")
                else:
                    print(f"Failed to download image {idx+1} for {site_name}")
                    
        except TouristSite.DoesNotExist:
            print(f"Site not found: {site_name}")
        except Exception as e:
            print(f"Error processing {site_name}: {e}")

if __name__ == '__main__':
    print("Adding images to tourist sites...")
    add_images()
    print("Image addition completed!")
