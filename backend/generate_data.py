import random
import json

cities_data = [
    # North India
    ("New Delhi", "Delhi", "The capital city of India, a blend of history and modernity.", "delhi.jpg", "Capital City", "Oct-Mar", 3000, "3-4 Days", 28.6139, 77.2090, "Historical", "North", ["Historical", "Cultural", "Shopping"]),
    ("Jaipur", "Rajasthan", "The Pink City, famous for its palaces and forts.", "jaipur.jpg", "Pink City", "Oct-Mar", 2500, "2-3 Days", 26.9124, 75.7873, "Historical", "North", ["Historical", "Cultural", "Royal"]),
    ("Agra", "Uttar Pradesh", "Home to the Taj Mahal, a symbol of eternal love.", "agra.jpg", "City of Taj", "Oct-Mar", 2000, "1-2 Days", 27.1767, 78.0081, "Historical", "North", ["Historical", "Romantic"]),
    ("Varanasi", "Uttar Pradesh", "The spiritual capital of India, situated on the banks of the Ganges.", "varanasi.jpg", "Spiritual Capital", "Oct-Mar", 1500, "2-3 Days", 25.3176, 82.9739, "Spiritual", "North", ["Spiritual", "Cultural"]),
    ("Amritsar", "Punjab", "Home to the Golden Temple, the holiest shrine of Sikhism.", "amritsar.jpg", "Golden City", "Oct-Mar", 2000, "1-2 Days", 31.6340, 74.8723, "Spiritual", "North", ["Spiritual", "Foodie"]),
    ("Rishikesh", "Uttarakhand", "The Yoga Capital of the World, gateway to the Himalayas.", "rishikesh.jpg", "Yoga Capital", "Sep-Nov, Mar-May", 1500, "2-3 Days", 30.0869, 78.2676, "Adventure", "North", ["Spiritual", "Adventure", "Nature"]),
    ("Manali", "Himachal Pradesh", "A high-altitude Himalayan resort town famous for backpacking.", "manali.jpg", "Valley of Gods", "Oct-Jun", 2500, "3-4 Days", 32.2432, 77.1892, "Nature", "North", ["Nature", "Adventure", "Honeymoon"]),
    ("Shimla", "Himachal Pradesh", "The Queen of Hills, a popular hill station with colonial architecture.", "shimla.jpg", "Queen of Hills", "Mar-Jun", 3000, "2-3 Days", 31.1048, 77.1734, "Nature", "North", ["Nature", "Colonial", "Relaxation"]),
    ("Leh", "Ladakh", "A high-desert city in the Himalayas, known for its Buddhist sites.", "leh.jpg", "Land of High Passes", "May-Sep", 3500, "4-5 Days", 34.1526, 77.5770, "Adventure", "North", ["Adventure", "Nature", "Spiritual"]),
    ("Srinagar", "Jammu & Kashmir", "Famous for its houseboats, gardens, and natural beauty.", "srinagar.jpg", "Paradise on Earth", "Apr-Oct", 3000, "3-4 Days", 34.0837, 74.7973, "Nature", "North", ["Nature", "Romantic", "Relaxation"]),
    ("Haridwar", "Uttarakhand", "An ancient city and important Hindu pilgrimage site.", "haridwar.jpg", "Gateway to God", "Oct-Mar", 1500, "1-2 Days", 29.9457, 78.1642, "Spiritual", "North", ["Spiritual", "Cultural"]),
    ("Lucknow", "Uttar Pradesh", "The City of Nawabs, known for its food and architecture.", "lucknow.jpg", "City of Nawabs", "Oct-Mar", 2000, "2-3 Days", 26.8467, 80.9462, "Cultural", "North", ["Cultural", "Foodie", "Historical"]),
    ("Chandigarh", "Punjab/Haryana", "A planned city known for its architecture and urban design.", "chandigarh.jpg", "The City Beautiful", "Oct-Mar", 2500, "1-2 Days", 30.7333, 76.7794, "Modern", "North", ["Modern", "Shopping", "Relaxation"]),
    ("Dehradun", "Uttarakhand", "Capital of Uttarakhand, gateway to Mussoorie and Rishikesh.", "dehradun.jpg", "Doon Valley", "Mar-Jun", 2000, "1-2 Days", 30.3165, 78.0322, "Nature", "North", ["Nature", "Relaxation"]),
    ("Mussoorie", "Uttarakhand", "Queen of the Hills, famous for its scenic beauty.", "mussoorie.jpg", "Queen of Hills", "Mar-Jun", 2500, "2-3 Days", 30.4599, 78.0664, "Nature", "North", ["Nature", "Honeymoon", "Relaxation"]),

    # West India
    ("Mumbai", "Maharashtra", "The financial capital of India, home to Bollywood.", "mumbai.jpg", "City of Dreams", "Oct-Mar", 4000, "3-4 Days", 19.0760, 72.8777, "Modern", "West", ["Modern", "Shopping", "Nightlife"]),
    ("Goa", "Goa", "Famous for its beaches, nightlife, and Portuguese heritage.", "goa.jpg", "Party Capital", "Nov-Feb", 3500, "3-5 Days", 15.2993, 74.1240, "Beach", "West", ["Beach", "Party", "Relaxation"]),
    ("Udaipur", "Rajasthan", "The City of Lakes, known for its lavish royal residences.", "udaipur.jpg", "City of Lakes", "Oct-Mar", 3000, "2-3 Days", 24.5854, 73.7125, "Romantic", "West", ["Romantic", "Historical", "Royal"]),
    ("Ahmedabad", "Gujarat", "The first UNESCO World Heritage City in India.", "ahmedabad.jpg", "Manchester of East", "Oct-Mar", 2000, "2-3 Days", 23.0225, 72.5714, "Cultural", "West", ["Cultural", "Historical", "Foodie"]),
    ("Pune", "Maharashtra", "The Oxford of the East, a vibrant cultural and educational hub.", "pune.jpg", "Oxford of East", "Oct-Mar", 2500, "2-3 Days", 18.5204, 73.8567, "Modern", "West", ["Modern", "Cultural", "Nightlife"]),
    ("Jaisalmer", "Rajasthan", "The Golden City, located in the heart of the Thar Desert.", "jaisalmer.jpg", "Golden City", "Oct-Mar", 2500, "2-3 Days", 26.9157, 70.9083, "Desert", "West", ["Desert", "Historical", "Adventure"]),
    ("Lonavala", "Maharashtra", "A popular hill station known for its green valleys and waterfalls.", "lonavala.jpg", "Jewel of Sahyadri", "Jun-Sep", 2500, "1-2 Days", 18.7515, 73.4056, "Nature", "West", ["Nature", "Relaxation"]),
    ("Mahabaleshwar", "Maharashtra", "Famous for its strawberries and scenic viewpoints.", "mahabaleshwar.jpg", "Land of Strawberries", "Oct-Jun", 3000, "2-3 Days", 17.9237, 73.6586, "Nature", "West", ["Nature", "Honeymoon", "Relaxation"]),
    ("Nashik", "Maharashtra", "The Wine Capital of India, also a holy city.", "nashik.jpg", "Wine Capital", "Oct-Mar", 2000, "1-2 Days", 19.9975, 73.7898, "Spiritual", "West", ["Spiritual", "Wine", "Relaxation"]),
    ("Aurangabad", "Maharashtra", "Gateway to the Ajanta and Ellora Caves.", "aurangabad.jpg", "City of Gates", "Oct-Mar", 2000, "2-3 Days", 19.8762, 75.3433, "Historical", "West", ["Historical", "Cultural"]),
    ("Surat", "Gujarat", "Known for diamonds and textiles.", "surat.jpg", "Diamond City", "Oct-Mar", 2000, "1-2 Days", 21.1702, 72.8311, "Modern", "West", ["Shopping", "Foodie"]),
    ("Vadodara", "Gujarat", "Cultural capital of Gujarat.", "vadodara.jpg", "Cultural City", "Oct-Mar", 1800, "1-2 Days", 22.3072, 73.1812, "Cultural", "West", ["Cultural", "Historical"]),
    ("Kutch", "Gujarat", "Famous for the Great Rann of Kutch white desert.", "kutch.jpg", "White Desert", "Nov-Feb", 3000, "2-3 Days", 23.7337, 69.8597, "Desert", "West", ["Desert", "Cultural", "Nature"]),
    ("Mount Abu", "Rajasthan", "The only hill station in Rajasthan.", "mount_abu.jpg", "Oasis in Desert", "Sep-Mar", 2500, "2-3 Days", 24.5926, 72.7156, "Nature", "West", ["Nature", "Relaxation"]),
    ("Jodhpur", "Rajasthan", "The Blue City, dominated by the massive Mehrangarh Fort.", "jodhpur.jpg", "Blue City", "Oct-Mar", 2500, "2-3 Days", 26.2389, 73.0243, "Historical", "West", ["Historical", "Cultural"]),

    # South India
    ("Bangalore", "Karnataka", "The Silicon Valley of India, known for its parks and nightlife.", "bangalore.jpg", "Silicon Valley", "Sep-Mar", 3000, "2-3 Days", 12.9716, 77.5946, "Modern", "South", ["Modern", "Nightlife", "Shopping"]),
    ("Chennai", "Tamil Nadu", "A major cultural hub known for its temples and beaches.", "chennai.jpg", "Detroit of India", "Nov-Feb", 2500, "2-3 Days", 13.0827, 80.2707, "Cultural", "South", ["Cultural", "Beach", "Historical"]),
    ("Hyderabad", "Telangana", "A city of pearls, biryani, and tech.", "hyderabad.jpg", "City of Pearls", "Oct-Mar", 2500, "2-3 Days", 17.3850, 78.4867, "Historical", "South", ["Historical", "Foodie", "Modern"]),
    ("Kochi", "Kerala", "A major port city with a mix of colonial and local culture.", "kochi.jpg", "Queen of Arabian Sea", "Oct-Mar", 2500, "2-3 Days", 9.9312, 76.2673, "Cultural", "South", ["Cultural", "Historical", "Nature"]),
    ("Mysore", "Karnataka", "Famous for its royal palace and Dasara festival.", "mysore.jpg", "City of Palaces", "Oct-Mar", 2000, "1-2 Days", 12.2958, 76.6394, "Historical", "South", ["Historical", "Royal", "Cultural"]),
    ("Ooty", "Tamil Nadu", "A popular hill station in the Nilgiri Hills.", "ooty.jpg", "Queen of Hill Stations", "Mar-Jun", 2500, "2-3 Days", 11.4102, 76.6950, "Nature", "South", ["Nature", "Honeymoon", "Relaxation"]),
    ("Coorg", "Karnataka", "Known for its coffee plantations and misty hills.", "coorg.jpg", "Scotland of India", "Oct-Mar", 3000, "2-3 Days", 12.3375, 75.8069, "Nature", "South", ["Nature", "Adventure", "Relaxation"]),
    ("Pondicherry", "Puducherry", "A former French colony with a unique vibe.", "pondicherry.jpg", "French Riviera of East", "Oct-Mar", 2500, "2-3 Days", 11.9416, 79.8083, "Beach", "South", ["Beach", "Cultural", "Relaxation"]),
    ("Munnar", "Kerala", "Famous for its tea gardens and scenic beauty.", "munnar.jpg", "Kashmir of South", "Sep-Mar", 3000, "2-3 Days", 10.0889, 77.0595, "Nature", "South", ["Nature", "Honeymoon", "Relaxation"]),
    ("Alleppey", "Kerala", "Known for its backwaters and houseboat cruises.", "alleppey.jpg", "Venice of East", "Nov-Feb", 3500, "1-2 Days", 9.4981, 76.3388, "Nature", "South", ["Nature", "Relaxation", "Romantic"]),
    ("Madurai", "Tamil Nadu", "An ancient city famous for the Meenakshi Temple.", "madurai.jpg", "Temple City", "Oct-Mar", 1500, "1-2 Days", 9.9252, 78.1198, "Spiritual", "South", ["Spiritual", "Cultural"]),
    ("Hampi", "Karnataka", "A UNESCO World Heritage site with ancient ruins.", "hampi.jpg", "City of Ruins", "Oct-Mar", 2000, "2-3 Days", 15.3350, 76.4600, "Historical", "South", ["Historical", "Adventure", "Backpacking"]),
    ("Gokarna", "Karnataka", "A temple town known for its pristine beaches.", "gokarna.jpg", "Beach Trek Hub", "Oct-Mar", 2000, "2-3 Days", 14.5479, 74.3188, "Beach", "South", ["Beach", "Spiritual", "Relaxation"]),
    ("Kodaikanal", "Tamil Nadu", "A misty hill station with a star-shaped lake.", "kodaikanal.jpg", "Princess of Hill Stations", "Mar-Jun", 2500, "2-3 Days", 10.2381, 77.4892, "Nature", "South", ["Nature", "Honeymoon", "Relaxation"]),
    ("Wayanad", "Kerala", "Known for its waterfalls, caves, and spice plantations.", "wayanad.jpg", "Green Paradise", "Oct-May", 2500, "2-3 Days", 11.6854, 76.1320, "Nature", "South", ["Nature", "Adventure", "Relaxation"]),

    # East/Northeast India
    ("Kolkata", "West Bengal", "The cultural capital of India.", "kolkata.jpg", "City of Joy", "Oct-Mar", 2000, "2-3 Days", 22.5726, 88.3639, "Cultural", "East", ["Cultural", "Historical", "Foodie"]),
    ("Darjeeling", "West Bengal", "Famous for its tea and the Himalayan Railway.", "darjeeling.jpg", "Queen of Hills", "Mar-Jun", 2500, "2-3 Days", 27.0410, 88.2663, "Nature", "East", ["Nature", "Honeymoon", "Relaxation"]),
    ("Puri", "Odisha", "Known for the Jagannath Temple and beaches.", "puri.jpg", "Spiritual City", "Oct-Mar", 2000, "1-2 Days", 19.8135, 85.8312, "Spiritual", "East", ["Spiritual", "Beach"]),
    ("Gangtok", "Sikkim", "Capital of Sikkim, known for its monasteries and views.", "gangtok.jpg", "Land of Monasteries", "Mar-Jun", 3000, "2-3 Days", 27.3389, 88.6065, "Nature", "East", ["Nature", "Adventure", "Spiritual"]),
    ("Shillong", "Meghalaya", "Known for its rolling hills and waterfalls.", "shillong.jpg", "Scotland of East", "Mar-Jun", 2500, "2-3 Days", 25.5788, 91.8933, "Nature", "East", ["Nature", "Adventure", "Relaxation"]),
    ("Bhubaneswar", "Odisha", "The Temple City of India.", "bhubaneswar.jpg", "Temple City", "Oct-Mar", 2000, "1-2 Days", 20.2961, 85.8245, "Spiritual", "East", ["Spiritual", "Historical"]),
    ("Guwahati", "Assam", "Gateway to the Northeast.", "guwahati.jpg", "Gateway to NE", "Oct-Mar", 2000, "1-2 Days", 26.1445, 91.7362, "Nature", "East", ["Nature", "Spiritual"]),
    ("Kaziranga", "Assam", "Famous for one-horned rhinoceroses.", "kaziranga.jpg", "Rhino Land", "Nov-Apr", 4000, "2-3 Days", 26.5775, 93.1711, "Nature", "East", ["Nature", "Wildlife", "Adventure"]),
    ("Konark", "Odisha", "Famous for the Sun Temple.", "konark.jpg", "Sun City", "Oct-Mar", 1500, "1 Day", 19.8876, 86.0945, "Historical", "East", ["Historical", "Cultural"]),
    ("Sundarbans", "West Bengal", "Largest mangrove forest and tiger reserve.", "sundarbans.jpg", "Mangrove Forest", "Sep-Mar", 3500, "2-3 Days", 21.9497, 88.8995, "Nature", "East", ["Nature", "Wildlife", "Adventure"]),

    # Central India
    ("Bhopal", "Madhya Pradesh", "City of Lakes, known for its greenery.", "bhopal.jpg", "City of Lakes", "Oct-Mar", 2000, "1-2 Days", 23.2599, 77.4126, "Nature", "Central", ["Nature", "Historical"]),
    ("Khajuraho", "Madhya Pradesh", "Famous for its erotic sculptures and temples.", "khajuraho.jpg", "Temple City", "Oct-Mar", 2500, "1-2 Days", 24.8318, 79.9199, "Historical", "Central", ["Historical", "Cultural"]),
    ("Indore", "Madhya Pradesh", "Cleanest city in India, food hub.", "indore.jpg", "Food City", "Oct-Mar", 2000, "1-2 Days", 22.7196, 75.8577, "Modern", "Central", ["Foodie", "Shopping"]),
    ("Gwalior", "Madhya Pradesh", "Known for its massive fort and palaces.", "gwalior.jpg", "Fort City", "Oct-Mar", 2000, "1-2 Days", 26.2183, 78.1828, "Historical", "Central", ["Historical", "Cultural"]),
    ("Ujjain", "Madhya Pradesh", "An ancient holy city on the banks of Shipra.", "ujjain.jpg", "City of Temples", "Oct-Mar", 1500, "1-2 Days", 23.1765, 75.7819, "Spiritual", "Central", ["Spiritual", "Cultural"])
]

attraction_types = [
    ("Temple", "Spiritual"), ("Fort", "Historical"), ("Palace", "Historical"), 
    ("Museum", "Cultural"), ("Park", "Nature"), ("Market", "Shopping"), 
    ("Lake", "Nature"), ("Beach", "Beach"), ("Viewpoint", "Nature"), 
    ("Mall", "Shopping"), ("Cafe", "Foodie"), ("Restaurant", "Foodie"),
    ("Waterfall", "Nature"), ("Cave", "Adventure"), ("Zoo", "Nature")
]

def generate_attractions(city_name, city_category):
    attractions = []
    for i in range(1, 11): # 10 attractions per city
        atype, acat = random.choice(attraction_types)
        
        # Try to match city category if possible
        if i <= 4: # First 4 match city vibe
            if city_category == "Historical":
                atype, acat = random.choice([("Fort", "Historical"), ("Palace", "Historical"), ("Museum", "Cultural")])
            elif city_category == "Nature":
                atype, acat = random.choice([("Park", "Nature"), ("Lake", "Nature"), ("Viewpoint", "Nature"), ("Waterfall", "Nature")])
            elif city_category == "Spiritual":
                atype, acat = random.choice([("Temple", "Spiritual"), ("Ghat", "Spiritual")])
            elif city_category == "Beach":
                atype, acat = random.choice([("Beach", "Beach"), ("Shack", "Relaxation")])
        
        name = f"{city_name} {atype} {i}"
        desc = f"A beautiful {atype.lower()} in {city_name} that attracts many visitors. Perfect for {acat.lower()} lovers."
        entry = random.choice([0, 50, 100, 200, 500])
        rating = round(random.uniform(3.5, 5.0), 1)
        
        attractions.append((name, desc, acat, entry, rating))
    return attractions

sql_content = """-- ============================================
-- Smart City Guide - Sample Data
-- Generated Data for 55 Cities
-- ============================================

SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM favorites;
DELETE FROM reviews;
DELETE FROM bookings;
DELETE FROM attractions;
DELETE FROM cities;
DELETE FROM users;

ALTER TABLE favorites AUTO_INCREMENT = 1;
ALTER TABLE reviews AUTO_INCREMENT = 1;
ALTER TABLE bookings AUTO_INCREMENT = 1;
ALTER TABLE attractions AUTO_INCREMENT = 1;
ALTER TABLE cities AUTO_INCREMENT = 1;
ALTER TABLE users AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;

-- Users
INSERT INTO users (email, username, hashed_password, full_name, is_admin, is_verified) VALUES
('admin@smartcityguide.com', 'admin', 'scrypt:32768:8:1$HMRaFhJVyTb0OuAu$7085a9f2e60e5632e67be4b91a6c48819176df815ff8022d247960ed5c779a81d14f2b0c74fede60f0c380831a589c93ac1fd6881dfb8f361a35e2b8e39b9834', 'System Admin', TRUE, TRUE),
('user@example.com', 'user1', 'scrypt:32768:8:1$HMRaFhJVyTb0OuAu$7085a9f2e60e5632e67be4b91a6c48819176df815ff8022d247960ed5c779a81d14f2b0c74fede60f0c380831a589c93ac1fd6881dfb8f361a35e2b8e39b9834', 'Demo User', FALSE, TRUE),
('traveler@example.com', 'traveler', 'scrypt:32768:8:1$HMRaFhJVyTb0OuAu$7085a9f2e60e5632e67be4b91a6c48819176df815ff8022d247960ed5c779a81d14f2b0c74fede60f0c380831a589c93ac1fd6881dfb8f361a35e2b8e39b9834', 'World Traveler', FALSE, TRUE);

-- Cities
INSERT INTO cities (name, state, description, image_url, badge, best_season, avg_budget_per_day, recommended_days, latitude, longitude, category, region, trip_types) VALUES
"""

city_values = []
attraction_values = []

for i, city in enumerate(cities_data):
    name, state, desc, img, badge, season, budget, days, lat, lon, cat, reg, types = city
    types_json = json.dumps(types)
    city_values.append(f"('{name}', '{state}', '{desc.replace("'", "''")}', '{img}', '{badge}', '{season}', {budget}, '{days}', {lat}, {lon}, '{cat}', '{reg}', '{types_json}')")
    
    # Generate attractions for this city (city_id = i + 1)
    attractions = generate_attractions(name, cat)
    for att in attractions:
        aname, adesc, acat, aentry, arating = att
        attraction_values.append(f"({i+1}, '{aname}', '{adesc.replace("'", "''")}', '{acat}', {aentry}, '9:00 AM - 6:00 PM', {lat + random.uniform(-0.05, 0.05)}, {lon + random.uniform(-0.05, 0.05)}, {arating})")

sql_content += ",\n".join(city_values) + ";"

sql_content += "\n\n-- Attractions\nINSERT INTO attractions (city_id, name, description, category, entry_fee, opening_hours, latitude, longitude, rating) VALUES\n"
sql_content += ",\n".join(attraction_values) + ";"

sql_content += """

-- Reviews (Sample)
INSERT INTO reviews (user_id, city_id, rating, comment) VALUES
(2, 1, 5, 'Amazing city with rich history!'),
(3, 1, 4, 'Great food but crowded.'),
(2, 2, 5, 'Jaipur is absolutely beautiful!'),
(3, 18, 5, 'Best beach vacation ever!'),
(2, 18, 4, 'Great nightlife.');

-- Favorites (Sample)
INSERT INTO favorites (user_id, city_id) VALUES
(2, 1), (2, 2), (2, 18), (3, 1), (3, 18);
"""

with open('sample_data.sql', 'w', encoding='utf-8') as f:
    f.write(sql_content)

print("sample_data.sql generated successfully!")
