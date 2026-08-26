import streamlit as st
import pandas as pd
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="KisanConnect | Fresh From Farm",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. State Initializations
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {"Order ID": "ORD-108", "Crop": "Hajipur GI-Tag Banana", "Farmer": "Sunil Mahato", "Location": "GPS: 25.68, 85.21 (Khet Direct)", "Buyer": "Gaurav Supermart", "Qty": 150, "Total (₹)": 4200, "Status": "Escrow Locked 🔒"}
    ]

# Default Product Catalog with GPS Farm Coordinates
CATALOG = [
    {
        "ID": 101,
        "Crop": "Sweet Corn / Maize (Desi Makka)",
        "Category": "Grains",
        "Farmer": "Birendra Paswan",
        "Phone": "+91 98350 11223",
        "Price": 18,
        "Qty": 1500,
        "Location": "Khagaria Hub",
        "GPS": "📍 GPS: 25.5941° N, 86.4810° E (Direct Field Pickup)",
        "Quality": "Grade-A Sweet Cob",
        "Rating": "⭐ 4.9 (42 Orders)",
        "Image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 102,
        "Crop": "High-Sucrose Sugarcane (Taaza Ganna)",
        "Category": "Cash Crops",
        "Farmer": "Manoj Upadhyay",
        "Phone": "+91 97722 33445",
        "Price": 8,
        "Qty": 4500,
        "Location": "West Champaran",
        "GPS": "📍 GPS: 27.1146° N, 84.5020° E (Farm Gate Delivery)",
        "Quality": "Fresh Juice Cane",
        "Rating": "⭐ 4.8 (29 Orders)",
        "Image": "https://images.unsplash.com/photo-1589135233689-d561a3375b43?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 103,
        "Crop": "Hajipur GI-Tag Banana (Chiniya Kela)",
        "Category": "Fruits",
        "Farmer": "Sunil Mahato",
        "Phone": "+91 91234 56780",
        "Price": 28,
        "Qty": 1200,
        "Location": "Hajipur Mandi",
        "GPS": "📍 GPS: 25.6830° N, 85.2100° E (Bagmati Riverbank Farm)",
        "Quality": "Naturally Ripened",
        "Rating": "⭐ 5.0 (65 Orders)",
        "Image": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 104,
        "Crop": "Organic Raw Turmeric (Haldi Ganth)",
        "Category": "Spices",
        "Farmer": "Rajendra Prasad",
        "Phone": "+91 94312 88990",
        "Price": 65,
        "Qty": 600,
        "Location": "Gaya Mandi Hub",
        "GPS": "📍 GPS: 24.7914° N, 85.0002° E (Greenhouse Plot #4)",
        "Quality": "5.2% High Curcumin",
        "Rating": "⭐ 4.9 (38 Orders)",
        "Image": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=600&auto=format&fit=crop&q=80"
    }
]

if 'listings' not in st.session_state:
    st.session_state.listings = CATALOG

# 3. Background Styling (Farm Wallpaper for Login & Crisp White for Portal)
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
        * { font-family: 'Plus+Jakarta+Sans', sans-serif; }
        
        .stApp {
            background: linear-gradient(135deg, rgba(6, 95, 70, 0.85) 0%, rgba(5, 150, 105, 0.78) 100%),
                        url('https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?w=1600&auto=format&fit=crop&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .login-card {
            background: rgba(255, 255, 255, 0.96);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 35px 30px;
            box-shadow: 0 20px 45px rgba(0,0,0,0.25);
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        * { font-family: 'Plus+Jakarta+Sans', sans-serif; }
        
        .stApp { background-color: #ffffff; color: #1e293b; }
        .top-navbar { background: #2e7d32; padding: 16px 28px; border-radius: 12px; color: white; display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
        .hero-banner-container { background: #eef7ee; border-radius: 18px; padding: 35px 30px; margin-bottom: 30px; border: 1px solid #d4ecd5; }
        .badge-cat { background: #e8f5e9; color: #2e7d32; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-block; }
        .badge-trust { background: #fef3c7; color: #b45309; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-block; margin-left: 4px; }
        .price-main { font-size: 1.5rem; font-weight: 800; color: #2e7d32; }
        .farmer-profile-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 12px; margin: 10px 0; font-size: 0.85rem; }
        .gps-tag { color: #0284c7; font-weight: 700; font-size: 0.82rem; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)# ================= 4. AUTHENTICATION GATEWAY (SIGN IN FIRST) =================
if not st.session_state.authenticated:
    _, center_col, _ = st.columns([1, 1.8, 1])
    
    with center_col:
        st.markdown("""
        <div class="login-card">
            <div style="text-align: center;">
                <h1 style="color: #2e7d32; margin: 0; font-size: 2.2rem; font-weight: 800;">🌾 KisanConnect</h1>
                <p style="color: #64748b; font-size: 0.95rem; margin-top: 5px; margin-bottom: 15px;">Direct Farm-to-Customer Marketplace & Khet Pickup</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        login_tab, signup_tab, face_tab = st.tabs(["🔑 Sign In / Login", "📝 New Registration", "📸 Kisan Face ID / Voice"])
        
        with login_tab:
            auth_mode = st.radio("Sign In Via:", ["📱 Mobile OTP", "📧 Email & Password"], horizontal=True)
            
            if auth_mode == "📱 Mobile OTP":
                u_mob = st.text_input("Mobile Number", placeholder="+91 98765 43210")
                u_role = st.selectbox("I am a:", ["🛒 Consumer / Bulk Buyer", "👨‍🌾 Kisan (Farmer - Direct Khet)"])
                if st.button("📲 Send & Verify OTP", use_container_width=True):
                    if len(u_mob) >= 10:
                        st.session_state.authenticated = True
                        st.session_state.user_info = {"name": "Gaurav Buyer", "contact": u_mob, "role": u_role}
                        st.success("✅ Signed in successfully!")
                        st.rerun()
                    else:
                        st.error("Enter valid 10-digit mobile number.")
            else:
                u_email = st.text_input("Email ID", placeholder="user@gmail.com")
                u_pwd = st.text_input("Password", type="password", placeholder="••••••••")
                u_role = st.selectbox("Role:", ["🛒 Consumer / Bulk Buyer", "👨‍🌾 Kisan (Farmer - Direct Khet)"], key="r_email")
                if st.button("🚀 Sign In to Portal", use_container_width=True):
                    if u_email and u_pwd:
                        st.session_state.authenticated = True
                        st.session_state.user_info = {"name": u_email.split('@')[0].capitalize(), "contact": u_email, "role": u_role}
                        st.success("✅ Signed in successfully!")
                        st.rerun()
                    else:
                        st.error("Enter email and password.")

        with signup_tab:
            s_name = st.text_input("Full Name", placeholder="e.g. Rameshwar Singh")
            s_contact = st.text_input("Phone Number", placeholder="+91 9XXXXXXXXX")
            s_role = st.selectbox("Register as:", ["👨‍🌾 Farmer / Producer", "🛒 Buyer / Retailer"], key="s_role")
            if st.button("✨ Complete Registration", use_container_width=True):
                if s_name and s_contact:
                    st.session_state.authenticated = True
                    st.session_state.user_info = {"name": s_name, "contact": s_contact, "role": s_role}
                    st.success("🎉 Registered & Signed In!")
                    st.rerun()
                else:
                    st.error("Please fill all details.")

        with face_tab:
            st.info("📸 **Kisan Biometric Login:** Anpadh kisan ke liye chehra scan karke direct login karein.")
            face_cam = st.camera_input("Kisan Face Scan")
            if face_cam is not None:
                st.session_state.authenticated = True
                st.session_state.user_info = {"name": "Rameshwar Singh (Kisan)", "contact": "+91 98765 11111", "role": "👨‍🌾 Kisan (Farmer - Direct Khet)"}
                st.success("✅ Face Recognized! Welcome Rameshwar Ji.")
                st.balloons()
                st.rerun()# ================= 5. MAIN LOGGED-IN PORTAL =================
else:
    st.markdown("""
    <div class="top-navbar">
        <div style="font-size: 1.5rem; font-weight: 800; display:flex; align-items:center; gap:8px;">
            🌾 KisanConnect • Direct Khet Pickup & Live Mart
        </div>
        <div style="font-size: 0.95rem; font-weight: 600; opacity: 0.95;">
            Home &nbsp;&nbsp;|&nbsp;&nbsp; GPS Field Nav &nbsp;&nbsp;|&nbsp;&nbsp; Orders
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 👤 User Account")
        st.info(f"**{st.session_state.user_info.get('name', 'User')}**\n\n📌 Role: `{st.session_state.user_info.get('role', 'Member')}`\n\n📞 `{st.session_state.user_info.get('contact', 'Verified')}`")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.cart.clear()
            st.rerun()

        st.markdown("---")
        menu = st.radio("Portal Navigation:", [
            "🛒 Home & Farm Marketplace",
            "🛍️ My Cart & Escrow Checkout",
            "👨‍🌾 Farmer Produce & GPS Field Desk",
            "📦 Live Orders Ledger",
            "📊 Mandi Price Intelligence",
            "📈 Impact Analytics"
        ])
        
        st.markdown("---")
        total_cart_kg = sum(x["qty"] for x in st.session_state.cart.values())
        st.metric("🛍️ Cart Items", f"{total_cart_kg} kg")

    # SCREEN 1: HOME & MARKETPLACE
    if menu == "🛒 Home & Farm Marketplace":
        st.markdown("""
        <div class="hero-banner-container">
            <div style="color:#b45309; font-size:0.85rem; font-weight:800; text-transform:uppercase; margin-bottom:8px;">DIRECT KHET-TO-TRUCK PICKUP NETWORK</div>
            <div style="color:#1b5e20; font-size:2.4rem; font-weight:800; margin-bottom:10px;">Fresh crops straight from farmer's field.</div>
            <p style="color:#475569; font-size:1rem; margin:0;">Har product ke sath kisan ke khet ka live GPS coordinate milega jahan truck/vehicle direct ja sakti hai.</p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🛒 Browse Farm Produce & GPS Coordinates")

        f1, f2 = st.columns([1, 2])
        with f1:
            cat_filter = st.selectbox("🏷️ Category", ["All", "Grains", "Vegetables", "Fruits", "Cash Crops", "Spices"])
        with f2:
            loc_filter = st.selectbox("📍 Hub Region", ["All"] + sorted(list(set(x["Location"] for x in st.session_state.listings))))

        filtered = [
            x for x in st.session_state.listings
            if (cat_filter == "All" or x["Category"] == cat_filter) and (loc_filter == "All" or x["Location"] == loc_filter)
        ]

        for i in range(0, len(filtered), 3):
            cols = st.columns(3)
            row = filtered[i:i+3]
            for col, item in zip(cols, row):
                with col:
                    st.image(item["Image"], use_container_width=True)
                    st.markdown(f"""
                    <span class="badge-cat">{item['Category']}</span>
                    <span class="badge-trust">{item['Quality']}</span>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                        <h3 style="margin:0; font-size:1.15rem; font-weight:700;">{item['Crop']}</h3>
                        <span class="price-main">₹{item['Price']}<small style="font-size:0.80rem; color:#64748b;">/kg</small></span>
                    </div>
                    <div class="farmer-profile-box">
                        👨‍🌾 <b>Kisan:</b> {item['Farmer']} | 📞 <code>{item['Phone']}</code><br>
                        📍 <b>Mandi Hub:</b> {item['Location']}<br>
                        <div class="gps-tag">{item['GPS']}</div>
                        <small style="color:#b45309; font-weight:600;">{item['Rating']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    order_kg = st.number_input(f"Qty (kg)", min_value=5, max_value=max(5, item["Qty"]), value=20, key=f"q_{item['ID']}")
                    if st.button("🛒 Add to Cart", key=f"btn_{item['ID']}", use_container_width=True):
                        st.session_state.cart[item["ID"]] = {
                            "id": item["ID"],
                            "crop": item["Crop"],
                            "farmer": item["Farmer"],
                            "price": item["Price"],
                            "qty": order_kg,
                            "location": item["Location"],
                            "gps": item["GPS"]
                        }
                        st.success(f"Added {order_kg} kg {item['Crop']} to Cart!")
                        st.rerun()

    # SCREEN 2: CART & CHECKOUT
    elif menu == "🛍️ My Cart & Escrow Checkout":
        st.subheader("🛍️ Shopping Cart & Khet Pickup Settlement")
        
        if not st.session_state.cart:
            st.info("Your cart is empty! Pick fresh crops from marketplace.")
        else:
            cart_data = []
            total_bill = 0
            for k, v in list(st.session_state.cart.items()):
                sub = v["qty"] * v["price"]
                total_bill += sub
                cart_data.append({
                    "Crop Produce": v["crop"],
                    "Farmer Name": v["farmer"],
                    "Pickup GPS": v["gps"],
                    "Rate": f"₹{v['price']}/kg",
                    "Qty": f"{v['qty']} kg",
                    "Subtotal": f"₹{sub:,.2f}"
                })

            st.table(pd.DataFrame(cart_data))
            st.markdown(f"### 💳 Total Amount: :green[**₹{total_bill:,.2f}**]")
            st.caption("🔒 Escrow payment held securely until vehicle arrives at kisan's field GPS location.")

            st.markdown("---")
            b1, b2 = st.columns(2)
            with b1:
                b_name = st.text_input("Buyer Name", value=st.session_state.user_info.get("name", ""))
                b_phone = st.text_input("Mobile Number", value=st.session_state.user_info.get("contact", ""))
            with b2:
                b_addr = st.text_input("Truck / Vehicle Number (for Khet Pickup)", placeholder="e.g. BR-01-AB-1234")
                slot = st.selectbox("Pickup Time Slot", ["Morning Khet Load (6 AM)", "Evening Khet Load (4 PM)"])

            if st.button("🚀 Pay & Confirm Direct Khet Pickup Order", use_container_width=True):
                if b_name and b_phone:
                    for cid, cval in st.session_state.cart.items():
                        st.session_state.orders.append({
                            "Order ID": f"ORD-{len(st.session_state.orders) + 101}",
                            "Crop": cval["crop"],
                            "Farmer": cval["farmer"],
                            "Location": cval["gps"],
                            "Buyer": f"{b_name} ({b_phone})",
                            "Qty": cval["qty"],
                            "Total (₹)": cval["qty"] * cval["price"],
                            "Status": "Escrow Locked 🔒"
                        })
                    st.session_state.cart.clear()
                    st.balloons()
                    st.success("🎉 Order Placed! GPS navigation sent to vehicle driver for direct khet pickup.")
                    st.rerun()
                else:
                    st.error("Please fill buyer details.")

    # SCREEN 3: FARMER PRODUCE & GPS DESK
    elif menu == "👨‍🌾 Farmer Produce & GPS Field Desk":
        st.subheader("👨‍🌾 Uneducated Farmer Simple Voice & GPS Listing Desk")
        st.info("💡 **Voice & Visual Mode for Farmers:** Agar kisan likh nahi sakta, toh wo mic icon dabakar ya photo khichkar apni fasal list kar sakta hai.")
        
        fc1, fc2 = st.columns(2)
        with fc1:
            f_name = st.text_input("Kisan Full Name", value="Rameshwar Singh")
            f_phone = st.text_input("Mobile Number", value="+91 98765 43210")
            f_crop = st.selectbox("Fasal (Crop)", ["Sweet Corn (Makka)", "Sugarcane (Ganna)", "Banana (Kela)", "Turmeric (Haldi)", "Basmati Rice", "Tomato", "Wheat"])
            f_cat = st.selectbox("Category", ["Grains", "Vegetables", "Fruits", "Cash Crops", "Spices"])
        with fc2:
            f_qty = st.number_input("Kitna Kilo hai? (Qty in kg)", min_value=10, value=500)
            f_price = st.number_input("Rate (₹/kg)", min_value=1, value=25)
            f_loc = st.selectbox("District / Hub", ["Patna Rural", "Hajipur Mandi", "Muzaffarpur Hub", "Khagaria Hub", "West Champaran"])
            f_gps = st.text_input("Khet ka Live GPS Tag (Auto-fetched from Mobile)", value="📍 GPS: 25.6120° N, 85.1376° E (Direct Field)")

        if st.button("🎙️ Voice Command Se Listing Publish Karein", use_container_width=True):
            st.session_state.listings.append({
                "ID": len(st.session_state.listings) + 101,
                "Crop": f_crop,
                "Category": f_cat,
                "Farmer": f_name,
                "Phone": f_phone,
                "Price": f_price,
                "Qty": f_qty,
                "Location": f_loc,
                "GPS": f_gps,
                "Quality": "Grade-A Field Harvest",
                "Rating": "⭐ Voice Verified Kisan",
                "Image": "https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?w=600&auto=format&fit=crop&q=80"
            })
            st.success("✅ Fasal live ho gayi! Ab buyer direct aapke khet ke GPS par aayega.")
            st.rerun()

    # SCREEN 4: LIVE ORDERS
    elif menu == "📦 Live Orders Ledger":
        st.subheader("📦 Real-Time Transaction & GPS Field Ledger")
        st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)
        st.markdown("---")
        if st.button("🔐 Verify Delivery OTP & Release Money to Kisan Bank", use_container_width=True):
            st.success("✅ OTP Verified! 100% Payment sent directly to Kisan's bank account.")

    # SCREEN 5: MANDI BENCHMARKING
    elif menu == "📊 Mandi Price Intelligence":
        st.subheader("📊 Mandi vs KisanConnect Direct Price")
        st.table(pd.DataFrame({
            "Crop": ["Sweet Corn", "Sugarcane", "Banana", "Turmeric", "Basmati Rice"],
            "Govt Mandi Rate (₹/kg)": [14, 4.5, 18, 45, 30],
            "KisanConnect Direct Rate (₹/kg)": [18, 8, 28, 65, 36],
            "Farmer Profit Gain": ["+28.5%", "+77.7%", "+55.5%", "+44.4%", "+20.0%"]
        }))

    # SCREEN 6: IMPACT ANALYTICS
    elif menu == "📈 Impact Analytics":
        st.subheader("📈 Hackathon Impact Metrics")
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Farmer Income Boost", "+38.2%")
        with m2: st.metric("Direct Khet Pickups", "1,240+")
        with m3: st.metric("Middlemen Eliminated", "₹ 11.4 Lakhs")
