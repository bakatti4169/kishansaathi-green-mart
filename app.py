import streamlit as st
import pandas as pd
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="KisanSaathi | Direct Agri Marketplace",
    page_icon="🌱",
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
        {"Order ID": "ORD-108", "Crop": "Hajipur GI-Tag Banana", "Farmer": "Sunil Mahato", "Buyer": "Gaurav Supermart (Patna)", "Qty": 150, "Total (₹)": 4200, "Status": "Escrow Locked 🔒"}
    ]

# Default Product Catalog
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
        "Quality": "5.2% High Curcumin",
        "Rating": "⭐ 4.9 (38 Orders)",
        "Image": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 105,
        "Crop": "Basmati Rice (Sharbati Chawal)",
        "Category": "Grains",
        "Farmer": "Santosh Kumar",
        "Phone": "+91 98112 33445",
        "Price": 36,
        "Qty": 900,
        "Location": "Buxar District",
        "Quality": "Aromatic Aged Basmati",
        "Rating": "⭐ 4.9 (51 Orders)",
        "Image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 106,
        "Crop": "Fresh Red Tomato (Desi Tamatar)",
        "Category": "Vegetables",
        "Farmer": "Amit Yadav",
        "Phone": "+91 99887 76655",
        "Price": 22,
        "Qty": 550,
        "Location": "Muzaffarpur Hub",
        "Quality": "Farm Fresh Harvest",
        "Rating": "⭐ 4.7 (18 Orders)",
        "Image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 107,
        "Crop": "Certified Golden Wheat (Sharbati Gehu)",
        "Category": "Grains",
        "Farmer": "Rameshwar Singh",
        "Phone": "+91 98765 43210",
        "Price": 25,
        "Qty": 850,
        "Location": "Patna Rural",
        "Quality": "100% Organic Grade-A",
        "Rating": "⭐ 4.9 (44 Orders)",
        "Image": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 108,
        "Crop": "Storage Red Onion (Patna Pyaz)",
        "Category": "Vegetables",
        "Farmer": "Dinesh Kushwaha",
        "Phone": "+91 97711 22334",
        "Price": 20,
        "Qty": 1100,
        "Location": "Patna Central",
        "Quality": "Dry Clean Sorted",
        "Rating": "⭐ 4.8 (30 Orders)",
        "Image": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 109,
        "Crop": "Cold-Storage Desi Potato (Aloo)",
        "Category": "Vegetables",
        "Farmer": "Ram Naresh",
        "Phone": "+91 94300 22114",
        "Price": 14,
        "Qty": 1600,
        "Location": "Hajipur Mandi",
        "Quality": "Graded Uniform Size",
        "Rating": "⭐ 4.6 (22 Orders)",
        "Image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 110,
        "Crop": "Pure Mustard Seeds (Pili Sarson)",
        "Category": "Oilseeds",
        "Farmer": "Bhola Sah",
        "Phone": "+91 93344 55667",
        "Price": 54,
        "Qty": 400,
        "Location": "Bhagalpur Hub",
        "Quality": "High 42% Oil Yield",
        "Rating": "⭐ 4.9 (35 Orders)",
        "Image": "https://images.unsplash.com/photo-1508873696983-2df5293cb395?w=600&auto=format&fit=crop&q=80"
    }
]

if 'listings' not in st.session_state:
    st.session_state.listings = CATALOG

# 3. Dynamic Styling
if not st.session_state.authenticated:
    # Login Screen Styling with Full Farm Hero Wallpaper
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
        * { font-family: 'Plus+Jakarta+Sans', sans-serif; }
        
        .stApp {
            background: linear-gradient(135deg, rgba(6, 95, 70, 0.82) 0%, rgba(5, 150, 105, 0.75) 100%),
                        url('https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?w=1600&auto=format&fit=crop&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .login-card {
            background: rgba(255, 255, 255, 0.96);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 35px 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.25);
            border: 1px solid rgba(255, 255, 255, 0.4);
            margin-top: 20px;
        }
        
        .brand-badge {
            background: #10b981;
            color: white;
            font-size: 0.85rem;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 50px;
            display: inline-block;
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # Main Portal Styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        * { font-family: 'Plus+Jakarta+Sans', sans-serif; }
        
        .stApp {
            background: linear-gradient(180deg, #f0fdf4 0%, #ecfdf5 40%, #e6fcf5 100%);
            background-attachment: fixed;
        }

        .hero-container {
            background: linear-gradient(135deg, #047857 0%, #10b981 60%, #059669 100%);
            padding: 30px 25px;
            border-radius: 22px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 12px 30px rgba(16, 185, 129, 0.22);
        }

        .badge-cat {
            background: #dcfce7;
            color: #15803d;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 5px 12px;
            border-radius: 50px;
            display: inline-block;
        }

        .badge-trust {
            background: #fef3c7;
            color: #b45309;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 5px 12px;
            border-radius: 50px;
            display: inline-block;
            margin-left: 6px;
        }

        .price-main {
            font-size: 1.55rem;
            font-weight: 800;
            color: #047857;
        }

        .farmer-profile-box {
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 12px;
            padding: 10px 14px;
            margin: 10px 0;
            font-size: 0.86rem;
        }

        .stat-card {
            background: #ffffff;
            border-radius: 18px;
            padding: 20px;
            border-left: 6px solid #10b981;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        }
    </style>
    """, unsafe_allow_html=True)


# ========================================================
# 4. AUTHENTICATION GATEWAY (LOGIN / SIGN UP)
# ========================================================
if not st.session_state.authenticated:
    _, center_col, _ = st.columns([1, 1.8, 1])
    
    with center_col:
        st.markdown("""
        <div class="login-card">
            <div style="text-align: center;">
                <span class="brand-badge">🌾 Direct Farm-to-Consumer Gateway</span>
                <h1 style="color: #065f46; margin: 0; font-size: 2.2rem; font-weight: 800;">Welcome to KisanSaathi</h1>
                <p style="color: #64748b; font-size: 0.95rem; margin-top: 5px; margin-bottom: 20px;">Sign in to access verified farmer listings, instant escrow payouts & mandi rates.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        login_tab, signup_tab = st.tabs(["🔑 Quick Login", "📝 New Registration"])
        
        # --- LOGIN TAB ---
        with login_tab:
            auth_mode = st.radio("Login Via:", ["📱 Mobile OTP", "📧 Email & Password"], horizontal=True)
            
            if auth_mode == "📱 Mobile OTP":
                user_mobile = st.text_input("Mobile Number", placeholder="+91 98765 43210")
                user_role = st.selectbox("I am a:", ["🛒 Consumer / Bulk Buyer", "👨‍🌾 Kisan (Farmer)", "🚚 Logistics Partner"])
                
                if st.button("📲 Send & Verify OTP", use_container_width=True):
                    if len(user_mobile) >= 10:
                        st.session_state.authenticated = True
                        st.session_state.user_info = {
                            "name": "Verified User",
                            "contact": user_mobile,
                            "role": user_role
                        }
                        st.success("✅ OTP Verified! Redirecting to KisanSaathi Marketplace...")
                        st.rerun()
                    else:
                        st.error("Please enter a valid 10-digit mobile number.")
            else:
                user_email = st.text_input("Registered Email ID", placeholder="user@gmail.com")
                user_pwd = st.text_input("Password", type="password", placeholder="••••••••")
                user_role = st.selectbox("Account Role:", ["🛒 Consumer / Bulk Buyer", "👨‍🌾 Kisan (Farmer)", "🚚 Logistics Partner"], key="role_email")
                
                if st.button("🚀 Sign In to Dashboard", use_container_width=True):
                    if user_email and user_pwd:
                        st.session_state.authenticated = True
                        st.session_state.user_info = {
                            "name": user_email.split('@')[0].capitalize(),
                            "contact": user_email,
                            "role": user_role
                        }
                        st.success("✅ Signed in successfully!")
                        st.rerun()
                    else:
                        st.error("Please enter both email and password.")

        # --- SIGNUP TAB ---
        with signup_tab:
            st.write("#### Create your KisanSaathi Account")
            new_name = st.text_input("Full Name", placeholder="e.g. Rameshwar Kumar")
            new_contact = st.text_input("Phone / Email", placeholder="+91 9XXXXXXXXX")
            new_role = st.selectbox("Register as:", ["👨‍🌾 Farmer / Producer", "🛒 Buyer / Retailer / Hotel", "🏢 Mandi Trader"], key="signup_role")
            new_loc = st.selectbox("Primary District", ["Patna", "Hajipur", "Muzaffarpur", "Khagaria", "West Champaran", "Gaya", "Bhagalpur"])
            
            if st.button("✨ Complete Registration", use_container_width=True):
                if new_name and new_contact:
                    st.session_state.authenticated = True
                    st.session_state.user_info = {
                        "name": new_name,
                        "contact": new_contact,
                        "role": new_role,
                        "location": new_loc
                    }
                    st.balloons()
                    st.success("🎉 Registration successful! Taking you to the mart...")
                    st.rerun()
                else:
                    st.error("Please complete all registration fields.")

# ========================================================
# 5. MAIN LOGGED-IN MARKETPLACE
# ========================================================
else:
    # Top Hero Header
    st.markdown("""
    <div class="hero-container">
        <h1 style="margin:0; font-size: 2.4rem; font-weight:800; color:white;">🌾 KisanSaathi Direct Mart</h1>
        <p style="margin:6px 0 0 0; font-size:1.05rem; opacity:0.95;">100% Direct Farm Trade • 0% Middleman Cut • Smart Escrow & OTP Delivery</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Profile & Navigation
    with st.sidebar:
        st.markdown(f"### 👤 Logged In")
        st.info(f"**{st.session_state.user_info.get('name', 'User')}**\n\n📌 Role: `{st.session_state.user_info.get('role', 'Member')}`\n\n📞 `{st.session_state.user_info.get('contact', 'Verified')}`")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.cart.clear()
            st.rerun()

        st.markdown("---")
        menu = st.radio("Portals:", [
            "🛒 Shop Live Produce",
            "🛍️ My Cart & Escrow Checkout",
            "👨‍🌾 Farmer Listing Desk",
            "📦 Live Orders & Transparency",
            "📊 Mandi Intelligence Benchmarking",
            "📈 Impact Analytics"
        ])
        
        st.markdown("---")
        total_cart_kg = sum(x["qty"] for x in st.session_state.cart.values())
        st.metric("🛍️ Cart Items", f"{total_cart_kg} kg")

    # ----------------- SCREEN 1: SHOPPING -----------------
    if menu == "🛒 Shop Live Produce":
        st.subheader("🥬 Farm-Fresh Produce (Direct from Kisan)")
        
        f1, f2 = st.columns([1, 2])
        with f1:
            cat_filter = st.selectbox("🏷️ Category Filter", ["All", "Grains", "Vegetables", "Fruits", "Cash Crops", "Spices", "Oilseeds"])
        with f2:
            loc_filter = st.selectbox("📍 Hub Location", ["All"] + sorted(list(set(x["Location"] for x in st.session_state.listings))))

        filtered = [
            x for x in st.session_state.listings
            if (cat_filter == "All" or x["Category"] == cat_filter) and (loc_filter == "All" or x["Location"] == loc_filter)
        ]

        st.markdown("---")

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
                        <span class="price-main">₹{item['Price']}<small style="font-size:0.8rem; color:#64748b;">/kg</small></span>
                    </div>
                    <div class="farmer-profile-box">
                        👨‍🌾 <b>Farmer:</b> {item['Farmer']}<br>
                        📞 <b>Contact:</b> <code>{item['Phone']}</code><br>
                        📍 <b>Hub:</b> {item['Location']} | 📦 <b>Stock:</b> {item['Qty']} kg<br>
                        <small style="color:#d97706; font-weight:600;">{item['Rating']}</small>
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
                            "location": item["Location"]
                        }
                        st.success(f"Added {order_kg} kg {item['Crop']} to Cart!")
                        st.rerun()

    # ----------------- SCREEN 2: CART & CHECKOUT -----------------
    elif menu == "🛍️ My Cart & Escrow Checkout":
        st.subheader("🛍️ Your Shopping Cart & Smart Escrow Payout")
        
        if not st.session_state.cart:
            st.info("Your cart is empty! Head over to 'Shop Live Produce' to pick fresh crops.")
        else:
            cart_data = []
            total_bill = 0
            for k, v in list(st.session_state.cart.items()):
                sub = v["qty"] * v["price"]
                total_bill += sub
                cart_data.append({
                    "Crop Produce": v["crop"],
                    "Farmer Name": v["farmer"],
                    "Unit Rate": f"₹{v['price']} / kg",
                    "Weight": f"{v['qty']} kg",
                    "Subtotal": f"₹{sub:,.2f}"
                })

            st.table(pd.DataFrame(cart_data))
            st.markdown(f"### 💳 Total Amount: :green[**₹{total_bill:,.2f}**]")
            st.caption("🔒 Payments are deposited into an autonomous Escrow and transferred to the Farmer only after OTP verification upon delivery.")

            st.markdown("---")
            st.markdown("#### 🚚 Delivery Coordinates")
            b1, b2 = st.columns(2)
            with b1:
                b_name = st.text_input("Buyer / Business Name", value=st.session_state.user_info.get("name", ""))
                b_phone = st.text_input("Mobile Number (for Delivery OTP)", value=st.session_state.user_info.get("contact", ""))
            with b2:
                b_addr = st.text_input("Delivery Address / Mandi Hub", placeholder="e.g. Kankarbagh, Patna")
                slot = st.selectbox("Preferred Time Slot", ["Morning (7 AM - 11 AM)", "Evening (4 PM - 8 PM)"])

            c1, c2 = st.columns(2)
            with c1:
                if st.button("🚀 Pay & Lock Payment in Escrow", use_container_width=True):
                    if b_name and b_phone:
                        for cid, cval in st.session_state.cart.items():
                            st.session_state.orders.append({
                                "Order ID": f"ORD-{len(st.session_state.orders) + 109}",
                                "Crop": cval["crop"],
                                "Farmer": cval["farmer"],
                                "Buyer": f"{b_name} ({b_phone})",
                                "Qty": cval["qty"],
                                "Total (₹)": cval["qty"] * cval["price"],
                                "Status": "Escrow Locked 🔒"
                            })
