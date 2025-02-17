
def ut_prediction(user_occupants, user_bathroom, user_price, user_amenities):
    from bs4 import BeautifulSoup
    import requests
    import re
    from regex import extract_dorm_info
    from transformers import pipeline  # NLP model for flexible feature matching

    ### === STEP 1: SCRAPE ALL RESIDENCE HALL LINKS === ###
    BASE_URL = "https://housing.utexas.edu/housing/residence-halls/residence-hall-locations"
    page_to_scrape = requests.get(BASE_URL)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")

    halls = soup.findAll("span", attrs={"class": "field field--name-title field--type-string field--label-hidden view-mode-utprop-list-1 field-node-utprop-property field-node-utprop-property--title"})
    halls_list = [hall.text.strip() for hall in halls]

    halls_links = {
        hall: f"{BASE_URL}/{hall.replace(' ', '-')}"
        for hall in halls_list
    }

    print(f"✅ Found {len(halls_list)} residence halls.")

    ### === STEP 2: USER INPUT FOR PREFERENCES === ###
    #print("\n🔍 Enter your room preferences below:")
    #user_occupants = input("Preferred number of occupants (One, Two, etc.): ").strip()
    #user_bathroom = input("Preferred bathroom type (Private, Shared, Community, etc.): ").strip()
    #user_price = float(input("Maximum price you are willing to pay: ").strip())
    #user_amenities = input("Preferred amenities/features (comma-separated): ").strip().lower().split(", ")

    ### === STEP 3: SCRAPE & EXTRACT ROOM DETAILS FOR ALL HALLS === ###
    class Room:
        def __init__(self, hall, title, occupants, bathroom, price, amenities):
            self.hall = hall
            self.title = title
            self.occupants = occupants
            self.bathroom = bathroom
            self.price = price
            self.amenities = amenities

        def __repr__(self):
            return f"{self.hall} | {self.title} | {self.occupants} | {self.bathroom} | ${self.price} | Amenities: {', '.join(self.amenities)}"

    all_rooms = []

    for hall, link in halls_links.items():
        print(f"\n📍 Scraping: {hall} ...")
        hall_page = requests.get(link)
        hall_soup = BeautifulSoup(hall_page.text, "html.parser")

        # Extract all room details
        room_types = hall_soup.findAll("article", attrs={"class": "node node--type-utprop-property-space node--view-mode-utprop-alt-1"})
        room_details = [room.text.replace("\n", " ").replace("*", "").strip() for room in room_types if "$" in room.text]

        # Extract amenities
        amenities_list = [
            amenity.get_text(strip=True).lower()
            for amenity in hall_soup.findAll("li", attrs={"class": "field__item field-node-utprop-property__item"})
            if amenity.get_text(strip=True)
        ]

        for room_text in room_details:
            room_text = re.sub(r'(?<=[a-z])([A-Z])', r' \1', room_text)  # Add spaces before capital letters
            extracted_info = extract_dorm_info(room_text).split(", ")

            if len(extracted_info) == 4:
                title, occupants, bathroom, price = extracted_info
                price = float(price)  # Convert price to float for comparison
                all_rooms.append(Room(hall, title, occupants, bathroom, price, amenities_list))

    print(f"\n✅ Extracted {len(all_rooms)} rooms across all halls!")

    ### === STEP 4: FILTER ROOMS BASED ON USER PREFERENCES === ###
    # Initialize NLP model for similarity checking (Mistral-7B Instruct for better results)
    # Load the correct zero-shot classification model
    # Load the zero-shot classification model
    # Load the zero-shot classification model
    from fuzzywuzzy import fuzz  # Faster string similarity matching

    def rate_room(room, strict_occupants, strict_bathroom, max_price, preferred_amenities):
        """Rate a room on a 100-point scale for precise scoring and convert to 5-star scale."""
        
        rating = 0  # Base rating (will increment)

        ### STRICT MATCHING (High Importance)
        if strict_occupants.lower() in room.occupants.lower():
            rating += 40  # ✅ +40 points if occupants match exactly
        else:
            return 0  # 🚫 Completely reject the room if occupants don't match

        if strict_bathroom.lower() in room.bathroom.lower():
            rating += 30  # ✅ +30 points if bathroom matches exactly
        elif fuzz.ratio(strict_bathroom.lower(), room.bathroom.lower()) > 75:
            rating += 15  # ✅ +15 points if it's a close match (e.g., "Shared" vs. "Community")
        else:
            return 0  # 🚫 Completely reject the room if bathroom doesn't match

        if room.price <= max_price:
            rating += 20  # ✅ +20 points if price is within budget
        elif room.price <= max_price * 1.1:  # ✅ Allow up to 10% over budget with penalty
            rating += 10  # ✅ +10 points if price is within 10% over budget
        else:
            return 0  # 🚫 Completely reject the room if price is too high

        ### FLEXIBLE MATCHING WITH FAST FUZZY STRING COMPARISON (Lower Importance)
        if preferred_amenities and room.amenities:  # If user selected amenities
            amenity_score = sum(
                1 for amenity in preferred_amenities 
                if max(fuzz.partial_ratio(amenity.lower(), room_amenity.lower()) for room_amenity in room.amenities) > 75
            )
            rating += min(amenity_score * 5, 10)  # ✅ Up to +10 points for amenity matches

        ### NO AMENITIES SELECTED (Neutral Handling)
        else:
            rating += 5  # ✅ Default boost if no amenities are selected (so user still gets results)

        ### CONVERT TO 5-STAR SCALE
        star_rating = round(rating / 20, 1)  # Convert to decimal-based 5-star rating
        return min(star_rating, 5.0)  # Cap at 5.0 stars


    ### === STEP 5: FIND & DISPLAY BEST MATCHES WITH DECIMAL RATINGS === ###
    rated_rooms = [
        (room, rate_room(room, user_occupants, user_bathroom, user_price, user_amenities))
        for room in all_rooms
    ]

    # Remove rooms that got a 0-star rating (didn't pass strict filtering)
    rated_rooms = [room for room in rated_rooms if room[1] > 0]

    # Sort by highest rating
    rated_rooms.sort(key=lambda x: x[1], reverse=True)
    top_3_rooms = rated_rooms[:3]
    top_10_rooms = rated_rooms[:10]
    # Display Top Rated Dorms
    if top_3_rooms:
        print("\n🏠 **Top Rated Dorm Rooms for You:**")
        
        for room, stars in top_3_rooms:
            print(f"⭐️ {stars}/5 | {room}")
        return top_3_rooms, top_10_rooms
        
    else:
        print("\n⚠️ No matching dorms found. Try adjusting your filters!")
        return "None", "None"

    print("\nℹ️ *Information may not be 100% accurate, please check your college website for more accurate details.*")


