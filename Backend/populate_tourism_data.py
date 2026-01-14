import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'natourcam.settings')
django.setup()

from tourism.models import Region, TouristSite

def populate_data():
    # Create regions
    regions_data = [
        {'name': 'Littoral', 'code': 'LT', 'description': 'Coastal region including Douala'},
        {'name': 'Centre', 'code': 'CE', 'description': 'Central region including Yaoundé'},
        {'name': 'Northwest', 'code': 'NW', 'description': 'Northwestern region including Bamenda'},
        {'name': 'Southwest', 'code': 'SW', 'description': 'Southwestern region including Buea'},
        {'name': 'West', 'code': 'OU', 'description': 'Western region including Bafoussam'},
    ]
    
    regions = []
    for region_data in regions_data:
        region, created = Region.objects.get_or_create(
            code=region_data['code'],
            defaults=region_data
        )
        regions.append(region)
        if created:
            print(f"Created region: {region.name}")
        else:
            print(f"Region already exists: {region.name}")
    
    # Create tourist sites
    sites_data = [
        {
            'name': 'Douala Zoo',
            'description': 'A large zoo with diverse wildlife from across Cameroon',
            'region': regions[0],  # Littoral
            'latitude': 4.0482,
            'longitude': 9.7742,
            'address': 'Douala, Littoral Region',
            'entrance_fee': 1500,
            'is_active': True
        },
        {
            'name': 'Mount Cameroon',
            'description': 'An active volcano and the highest peak in Cameroon',
            'region': regions[3],  # Southwest
            'latitude': 4.2033,
            'longitude': 9.1900,
            'address': 'Buea, Southwest Region',
            'entrance_fee': 3000,
            'is_active': True
        },
        {
            'name': 'Bamenda Mountain',
            'description': 'Beautiful mountainous area with scenic views',
            'region': regions[2],  # Northwest
            'latitude': 6.5789,
            'longitude': 10.1628,
            'address': 'Bamenda, Northwest Region',
            'entrance_fee': 2000,
            'is_active': True
        },
        {
            'name': 'Mefou National Park',
            'description': 'Primate sanctuary and national park near Yaoundé',
            'region': regions[1],  # Centre
            'latitude': 3.7500,
            'longitude': 11.5833,
            'address': 'Mefou, Centre Region',
            'entrance_fee': 2500,
            'is_active': True
        },
        {
            'name': 'Waza National Park',
            'description': 'Famous for its lion population and diverse wildlife',
            'region': regions[4],  # West
            'latitude': 12.0000,
            'longitude': 15.0000,
            'address': 'Waza, Far North Region',
            'entrance_fee': 3500,
            'is_active': True
        }
    ]
    
    for site_data in sites_data:
        site, created = TouristSite.objects.get_or_create(
            name=site_data['name'],
            defaults=site_data
        )
        if created:
            print(f"Created tourist site: {site.name}")
        else:
            print(f"Tourist site already exists: {site.name}")

if __name__ == '__main__':
    populate_data()
    print("Data population completed!")