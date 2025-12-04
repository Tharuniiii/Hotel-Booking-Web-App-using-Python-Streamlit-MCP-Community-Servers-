import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Hotel Booking Platform",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #FF5A5F 0%, #FF385C 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #FF385C 0%, #E31C5F 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 90, 95, 0.4);
    }
    .hotel-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .hotel-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    .price-tag {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FF5A5F;
    }
    .rating-badge {
        background: #00A699;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    h1 {
        color: #FF5A5F;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .search-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'hotels' not in st.session_state:
    st.session_state.hotels = []
if 'booking_confirmed' not in st.session_state:
    st.session_state.booking_confirmed = False
if 'selected_hotel' not in st.session_state:
    st.session_state.selected_hotel = None

# Sample hotel data generator
def generate_hotels(location, check_in, check_out, guests, min_price, max_price, property_types, amenities):
    """Generate sample hotel data based on filters"""
    hotel_names = [
        "Grand Luxury Resort", "Seaside Paradise Hotel", "Mountain View Inn",
        "Urban Boutique Hotel", "Tranquil Garden Resort", "Skyline Tower Hotel",
        "Riverside Retreat", "Historic Grand Hotel", "Modern Art Hotel",
        "Tropical Oasis Resort", "City Center Plaza", "Sunset Beach Resort",
        "Alpine Lodge", "Metropolitan Suites", "Zen Garden Hotel"
    ]
    
    property_type_list = ["Hotel", "Resort", "Apartment", "Villa", "Hostel", "Boutique"]
    amenities_list = ["WiFi", "Pool", "Gym", "Spa", "Parking", "Breakfast", "Pet Friendly", "Air Conditioning"]
    
    hotels = []
    for i, name in enumerate(hotel_names[:12]):
        price = random.randint(min_price, max_price)
        rating = round(random.uniform(4.0, 5.0), 1)
        property_type = random.choice(property_types if property_types else property_type_list)
        hotel_amenities = random.sample(amenities_list, random.randint(3, 6))
        
        # Filter by amenities if specified
        if amenities and not any(amt in hotel_amenities for amt in amenities):
            continue
            
        hotels.append({
            'id': i + 1,
            'name': name,
            'location': location,
            'property_type': property_type,
            'price_per_night': price,
            'rating': rating,
            'reviews': random.randint(50, 500),
            'amenities': hotel_amenities,
            'image_url': f"https://picsum.photos/400/300?random={i}",
            'description': f"Beautiful {property_type.lower()} located in the heart of {location}. Perfect for your stay with {guests} guests.",
            'check_in': check_in,
            'check_out': check_out,
            'guests': guests,
            'total_price': price * ((check_out - check_in).days if check_out > check_in else 1)
        })
    
    return hotels

# Main App
def main():
    # Header
    st.markdown('<div class="search-header"><h1>🏨 Find Your Perfect Stay</h1><p style="font-size: 1.2rem; margin-top: 0.5rem;">Discover amazing hotels and book your next adventure</p></div>', unsafe_allow_html=True)
    
    # Sidebar for search filters
    with st.sidebar:
        st.header("🔍 Search Filters")
        
        # Location
        location = st.text_input("📍 Where are you going?", value="New York", placeholder="Enter city or destination")
        
        # Date selection
        st.subheader("📅 Dates")
        col1, col2 = st.columns(2)
        with col1:
            check_in = st.date_input("Check-in", value=datetime.now() + timedelta(days=1), min_value=datetime.now())
        with col2:
            check_out = st.date_input("Check-out", value=datetime.now() + timedelta(days=3), min_value=check_in + timedelta(days=1))
        
        # Guest selection
        st.subheader("👥 Guests")
        adults = st.number_input("Adults", min_value=1, max_value=16, value=2)
        children = st.number_input("Children", min_value=0, max_value=10, value=0)
        infants = st.number_input("Infants", min_value=0, max_value=5, value=0)
        total_guests = adults + children
        
        # Price range
        st.subheader("💰 Price Range")
        price_range = st.slider("Price per night ($)", 50, 500, (100, 300), 10)
        min_price, max_price = price_range
        
        # Property type
        st.subheader("🏠 Property Type")
        property_types = st.multiselect(
            "Select property types",
            ["Hotel", "Resort", "Apartment", "Villa", "Hostel", "Boutique"],
            default=["Hotel", "Resort", "Apartment"]
        )
        
        # Amenities
        st.subheader("✨ Amenities")
        amenities = st.multiselect(
            "Select amenities",
            ["WiFi", "Pool", "Gym", "Spa", "Parking", "Breakfast", "Pet Friendly", "Air Conditioning"],
            default=[]
        )
        
        # Sort by
        st.subheader("🔀 Sort By")
        sort_by = st.selectbox(
            "Sort results by",
            ["Price: Low to High", "Price: High to Low", "Rating: High to Low", "Reviews: Most Popular"],
            index=0
        )
        
        # Search button
        search_button = st.button("🔍 Search Hotels", type="primary", use_container_width=True)
        
        # Clear filters
        if st.button("🔄 Clear Filters", use_container_width=True):
            st.rerun()
    
    # Main content area
    if search_button or st.session_state.hotels:
        if search_button:
            # Validate dates
            if check_out <= check_in:
                st.error("❌ Check-out date must be after check-in date!")
                return
            
            # Generate hotels
            with st.spinner("🔍 Searching for hotels..."):
                st.session_state.hotels = generate_hotels(
                    location, check_in, check_out, total_guests,
                    min_price, max_price, property_types, amenities
                )
        
        # Display results
        if st.session_state.hotels:
            st.header(f"🏨 {len(st.session_state.hotels)} Hotels Found")
            
            # Sort hotels
            hotels_df = pd.DataFrame(st.session_state.hotels)
            if sort_by == "Price: Low to High":
                hotels_df = hotels_df.sort_values('price_per_night')
            elif sort_by == "Price: High to Low":
                hotels_df = hotels_df.sort_values('price_per_night', ascending=False)
            elif sort_by == "Rating: High to Low":
                hotels_df = hotels_df.sort_values('rating', ascending=False)
            elif sort_by == "Reviews: Most Popular":
                hotels_df = hotels_df.sort_values('reviews', ascending=False)
            
            # Display hotel cards
            for idx, hotel in hotels_df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        # Hotel image placeholder
                        st.image(hotel['image_url'], use_container_width=True, caption=hotel['name'])
                    
                    with col2:
                        st.markdown(f"### {hotel['name']}")
                        st.markdown(f"**{hotel['property_type']}** • 📍 {hotel['location']}")
                        
                        # Rating and reviews
                        rating_col, review_col = st.columns([1, 2])
                        with rating_col:
                            st.markdown(f'<span class="rating-badge">⭐ {hotel["rating"]}</span>', unsafe_allow_html=True)
                        with review_col:
                            st.caption(f"({hotel['reviews']} reviews)")
                        
                        # Amenities
                        amenities_str = " • ".join([f"✓ {amt}" for amt in hotel['amenities'][:4]])
                        st.markdown(f"**Amenities:** {amenities_str}")
                        
                        # Description
                        st.caption(hotel['description'])
                    
                    with col3:
                        st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
                        st.markdown(f'<p class="price-tag">${hotel["price_per_night"]}</p>', unsafe_allow_html=True)
                        st.caption("per night")
                        
                        nights = (check_out - check_in).days
                        total = hotel['price_per_night'] * nights
                        st.markdown(f"**${total:.0f}** total for {nights} nights")
                        
                        if st.button(f"Book Now", key=f"book_{hotel['id']}", use_container_width=True):
                            st.session_state.selected_hotel = hotel.to_dict()
                            st.session_state.booking_confirmed = False
                            st.rerun()
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.divider()
        
        else:
            st.warning("No hotels found matching your criteria. Try adjusting your filters.")
    
    else:
        # Welcome screen
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h2>Welcome to Hotel Booking Platform</h2>
            <p style="font-size: 1.2rem; color: #666; margin-top: 1rem;">
                Use the sidebar to search for hotels by location, dates, guests, and more!
            </p>
            <div style="margin-top: 3rem;">
                <h3>✨ Features</h3>
                <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                    <div>📍 Location Search</div>
                    <div>📅 Date Selection</div>
                    <div>👥 Guest Options</div>
                    <div>💰 Price Filters</div>
                    <div>🏠 Property Types</div>
                    <div>✨ Amenities</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Booking confirmation modal
    if st.session_state.selected_hotel and not st.session_state.booking_confirmed:
        st.markdown("---")
        st.header("📋 Booking Details")
        
        hotel = st.session_state.selected_hotel
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(hotel['name'])
            st.write(f"**Location:** {hotel['location']}")
            st.write(f"**Check-in:** {check_in.strftime('%B %d, %Y')}")
            st.write(f"**Check-out:** {check_out.strftime('%B %d, %Y')}")
            st.write(f"**Guests:** {total_guests} ({adults} adults, {children} children, {infants} infants)")
            st.write(f"**Property Type:** {hotel['property_type']}")
            st.write(f"**Amenities:** {', '.join(hotel['amenities'])}")
        
        with col2:
            st.markdown("### Price Summary")
            nights = (check_out - check_in).days
            st.write(f"**${hotel['price_per_night']}** × {nights} nights")
            st.write(f"**Total:** ${hotel['price_per_night'] * nights:.2f}")
            
            st.markdown("---")
            st.subheader("Guest Information")
            guest_name = st.text_input("Full Name")
            guest_email = st.text_input("Email")
            guest_phone = st.text_input("Phone Number")
            special_requests = st.text_area("Special Requests (optional)")
            
            if st.button("✅ Confirm Booking", type="primary", use_container_width=True):
                if guest_name and guest_email and guest_phone:
                    st.session_state.booking_confirmed = True
                    st.success("🎉 Booking confirmed! Check your email for confirmation details.")
                    st.balloons()
                else:
                    st.error("Please fill in all required fields.")
        
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.selected_hotel = None
            st.rerun()
    
    # Booking confirmation screen
    if st.session_state.booking_confirmed and st.session_state.selected_hotel:
        st.markdown("---")
        st.success("""
        # 🎉 Booking Confirmed!
        
        Your reservation has been successfully processed. A confirmation email has been sent to your registered email address.
        
        **Booking Reference:** HOTEL-{}-{}
        """.format(
            st.session_state.selected_hotel['id'],
            random.randint(1000, 9999)
        ))
        
        if st.button("🔄 Book Another Hotel"):
            st.session_state.booking_confirmed = False
            st.session_state.selected_hotel = None
            st.rerun()

if __name__ == "__main__":
    main()

