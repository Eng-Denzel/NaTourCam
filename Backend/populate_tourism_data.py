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
            'description': 'A large zoo with diverse wildlife from across Cameroon, featuring lions, elephants, gorillas, and exotic birds in natural habitats.',
            'region': regions[0],  # Littoral
            'latitude': 4.0482,
            'longitude': 9.7742,
            'address': 'Douala, Littoral Region',
            'entrance_fee': 1500,
            'is_active': True
        },
        {
            'name': 'Mount Cameroon',
            'description': 'An active volcano and the highest peak in West Africa at 4,040m. Offers challenging hiking trails with breathtaking views of the Atlantic Ocean.',
            'region': regions[3],  # Southwest
            'latitude': 4.2033,
            'longitude': 9.1900,
            'address': 'Buea, Southwest Region',
            'entrance_fee': 3000,
            'is_active': True
        },
        {
            'name': 'Limbe Botanical Garden',
            'description': 'Historic botanical garden established in 1892, featuring over 1,500 plant species, beautiful walking trails, and stunning ocean views.',
            'region': regions[3],  # Southwest
            'latitude': 4.0167,
            'longitude': 9.2167,
            'address': 'Limbe, Southwest Region',
            'entrance_fee': 1000,
            'is_active': True
        },
        {
            'name': 'Kribi Beach',
            'description': 'Pristine white sand beaches with crystal clear waters, perfect for swimming, surfing, and relaxation. Famous for fresh seafood and beach resorts.',
            'region': regions[0],  # Littoral
            'latitude': 2.9500,
            'longitude': 9.9167,
            'address': 'Kribi, South Region',
            'entrance_fee': 500,
            'is_active': True
        },
        {
            'name': 'Chutes de la Lobé',
            'description': 'Spectacular waterfalls that flow directly into the Atlantic Ocean. One of the few waterfalls in the world that falls into the sea.',
            'region': regions[0],  # Littoral
            'latitude': 2.9167,
            'longitude': 9.9333,
            'address': 'Near Kribi, South Region',
            'entrance_fee': 2000,
            'is_active': True
        },
        {
            'name': 'Mefou National Park',
            'description': 'Primate sanctuary and national park near Yaoundé, home to rescued chimpanzees, gorillas, and other endangered primates in their natural habitat.',
            'region': regions[1],  # Centre
            'latitude': 3.7500,
            'longitude': 11.5833,
            'address': 'Mefou, Centre Region',
            'entrance_fee': 2500,
            'is_active': True
        },
        {
            'name': 'Waza National Park',
            'description': 'Cameroon\'s most famous national park, renowned for its lion population, elephants, giraffes, and diverse birdlife. Best visited during dry season.',
            'region': regions[4],  # West
            'latitude': 11.3667,
            'longitude': 14.5333,
            'address': 'Waza, Far North Region',
            'entrance_fee': 3500,
            'is_active': True
        },
        {
            'name': 'Rhumsiki Peak',
            'description': 'Dramatic volcanic plug rising from the Mandara Mountains, offering spectacular panoramic views and unique rock formations. A photographer\'s paradise.',
            'region': regions[4],  # West
            'latitude': 10.7500,
            'longitude': 13.8333,
            'address': 'Rhumsiki, Far North Region',
            'entrance_fee': 1500,
            'is_active': True
        },
        {
            'name': 'Dja Faunal Reserve',
            'description': 'UNESCO World Heritage Site, one of Africa\'s largest and best-protected rainforests. Home to forest elephants, gorillas, and over 100 mammal species.',
            'region': regions[1],  # Centre
            'latitude': 3.0000,
            'longitude': 13.0000,
            'address': 'Dja Reserve, East Region',
            'entrance_fee': 4000,
            'is_active': True
        },
        {
            'name': 'Foumban Royal Palace',
            'description': 'Historic palace of the Bamoun Kingdom, featuring a museum with royal artifacts, traditional art, and centuries of cultural heritage.',
            'region': regions[4],  # West
            'latitude': 5.7333,
            'longitude': 10.9000,
            'address': 'Foumban, West Region',
            'entrance_fee': 2000,
            'is_active': True
        },
        {
            'name': 'Lac Ossa',
            'description': 'Serene crater lake surrounded by lush rainforest, perfect for boat rides, fishing, and wildlife watching. Home to manatees and diverse bird species.',
            'region': regions[0],  # Littoral
            'latitude': 3.7833,
            'longitude': 10.0500,
            'address': 'Dizangue, Littoral Region',
            'entrance_fee': 1500,
            'is_active': True
        },
        {
            'name': 'Bafut Palace',
            'description': 'Traditional palace of the Bafut Kingdom, showcasing Grassfields architecture and culture. Features beautiful courtyards and historical artifacts.',
            'region': regions[2],  # Northwest
            'latitude': 6.0833,
            'longitude': 10.1000,
            'address': 'Bafut, Northwest Region',
            'entrance_fee': 1000,
            'is_active': True
        },
        {
            'name': 'Ekom-Nkam Waterfalls',
            'description': 'Majestic 80-meter high waterfall featured in the Tarzan movie. Surrounded by dense tropical rainforest with hiking trails and swimming pools.',
            'region': regions[0],  # Littoral
            'latitude': 4.9667,
            'longitude': 10.4833,
            'address': 'Melong, Littoral Region',
            'entrance_fee': 2500,
            'is_active': True
        },
        {
            'name': 'Korup National Park',
            'description': 'One of Africa\'s oldest and most diverse rainforests, with over 400 tree species, rare primates, and the famous canopy walkway experience.',
            'region': regions[3],  # Southwest
            'latitude': 5.0667,
            'longitude': 8.8500,
            'address': 'Mundemba, Southwest Region',
            'entrance_fee': 3500,
            'is_active': True
        },
        {
            'name': 'Bamenda Ring Road',
            'description': 'Scenic 367km circular route through the Grassfields, offering stunning mountain views, traditional villages, and cultural experiences.',
            'region': regions[2],  # Northwest
            'latitude': 6.0000,
            'longitude': 10.1500,
            'address': 'Bamenda Region, Northwest',
            'entrance_fee': 0,
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