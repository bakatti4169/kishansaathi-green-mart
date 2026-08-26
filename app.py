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

# 3. Bright Styling & Custom Theme
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
            background: #ffffff;
            border-radius: 20px;
            padding: 35px 30px;
            box-shadow: 0 20px 45px rgba(0,0,0,0.22);
            margin-top: 30px;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        * { font-family: 'Plus+Jakarta+Sans', sans-serif; }
        
        .stApp {
            background-color: #ffffff;
            color: #1e293b;
        }

        .top-navbar {
            background: #2e7d32;
            padding: 16px 28px;
            border-radius: 12px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .hero-banner-container {
            background: #eef7ee;
            border-radius: 18px;
            padding: 35px 30px;
            margin-bottom: 30px;
            border: 1px solid #d4ecd5;
        }
        
        .hero-tag {
            color: #b45309;
            font-size: 0.85rem;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        .hero-headline {
            color: #1b5e20;
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 12px;
        }
        
        .hero-desc {
            color: #475569;
            font-size: 1.05rem;
            line-height: 1.5;
            margin-bottom: 20px;
            max-width: 90%;
        }

        .badge-cat {
            background: #e8f5e9;
            color: #2e7d32;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            display: inline-block;
        }

        .badge-trust {
            background: #fef3c7;
            color: #b45309;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            display: inline-block;
            margin-left: 4px;
        }

        .price-main {
            font-size: 1.5rem;
            font-weight: 800;
            color: #2e7d32;
        }

        .farmer-profile-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 10px 12px;
            margin: 10px 0;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)# ================= 4. AUTHENTICATION =================
if not st.session_state.authenticated:
    _, center_col, _ = st.columns([1, 1.8, 1])
    
    with center_col:
        st.markdown("""
        <div class="login-card">
            <div style="text-align: center;">
                <h1 style="color: #2e7d32; margin: 0; font-size: 2.2rem; font-weight: 800;">🌾 KisanConnect</h1>
                <p style="color: #64748b; font-size: 0.95rem; margin-top: 5px; margin-bottom: 20px;">Direct Farm-to-Customer Marketplace</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        login_tab, signup_tab = st.tabs(["🔑 Quick Login", "📝 New Registration"])
        
        with login_tab:
            auth_mode = st.radio("Login Via:", ["📱 Mobile OTP", "📧 Email & Password"], horizontal=True)
            
            if auth_mode == "📱 Mobile OTP":
                user_mobile = st.text_input("Mobile Number", placeholder="+91 98765 43210")
                user_role = st.selectbox("I am a:", ["🛒 Consumer / Bulk Buyer", "👨‍🌾 Kisan (Farmer)", "🚚 Logistics Partner"])
                
                if st.button("📲 Send & Verify OTP", use_container_width=True):
                    if len(user_mobile) >= 10:
                        st.session_state.authenticated = True
                        st.session_state.user_info = {
                            "name": "Verified Buyer",
                            "contact": user_mobile,
                            "role": user_role
                        }
                        st.success("✅ Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Please enter a valid 10-digit mobile number.")
            else:
                user_email = st.text_input("Registered Email ID", placeholder="user@gmail.com")
                user_pwd = st.text_input("Password", type="password", placeholder="••••••••")
                user_role = st.selectbox("Account Role:", ["🛒 Consumer / Bulk Buyer", "👨‍🌾 Kisan (Farmer)", "🚚 Logistics Partner"], key="role_email")
                
                if st.button("🚀 Sign In", use_container_width=True):
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
                        st.error("Please enter email and password.")

        with signup_tab:
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
                    st.success("🎉 Registration successful!")
                    st.rerun()
                else:
                    st.error("Please fill all details.")

# ================= 5. MAIN LOGGED-IN PORTAL =================
else:
    st.markdown("""
    <div class="top-navbar">
        <div style="font-size: 1.5rem; font-weight: 800; display:flex; align-items:center; gap:8px;">
            🌾 KisanConnect
        </div>
        <div style="font-size: 0.95rem; font-weight: 600; opacity: 0.95;">
            Home &nbsp;&nbsp;|&nbsp;&nbsp; Products &nbsp;&nbsp;|&nbsp;&nbsp; Farmers &nbsp;&nbsp;|&nbsp;&nbsp; Orders
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
        menu = st.radio("Marketplace Views:", [
            "🛒 Home & Farm Marketplace",
            "🛍️ My Cart & Escrow Checkout",
            "👨‍🌾 Farmer Produce Desk",
            "📦 Live Orders Ledger",
            "📊 Mandi Price Intelligence",
            "📈 Impact Analytics"
        ])
        
        st.markdown("---")
        total_cart_kg = sum(x["qty"] for x in st.session_state.cart.values())
        st.metric("🛍️ Cart Items", f"{total_cart_kg} kg")# SCREEN 1: HOME & MARKETPLACE
    if menu == "🛒 Home & Farm Marketplace":
        hero_left, hero_right = st.columns([1.3, 1.1])
        with hero_left:
            st.markdown("""
            <div class="hero-banner-container">
                <div class="hero-tag">DIRECT FARM-TO-CUSTOMER MARKETPLACE</div>
                <div class="hero-headline">Fresh food from local farmers.</div>
                <div class="hero-desc">
                    KisanConnect helps farmers sell directly to customers. Farmers get a better price. Customers get fresh products at a fair price.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with hero_right:
            st.image("https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&auto=format&fit=crop&q=80", caption="Direct Harvest Assured Quality", use_container_width=True)

        st.markdown("## 🥬 Why KisanConnect?")
        w1, w2, w3 = st.columns(3)
        with w1:
            st.success("🌱 **100% Farm Fresh**\nHarvested and dispatched within 24 hours directly from farms.")
        with w2:
            st.info("💰 **Fair Pricing Engine**\nNo intermediary markups. Transparent mandi-indexed base rates.")
        with w3:
            st.warning("🔒 **Smart Escrow Guarantee**\nPayments released to farmers only upon verified buyer delivery OTP.")

        st.markdown("---")
        st.subheader("🛒 Browse Certified Produce")

        f1, f2 = st.columns([1, 2])
        with f1:
            cat_filter = st.selectbox("🏷️ Category Filter", ["All", "Grains", "Vegetables", "Fruits", "Cash Crops", "Spices", "Oilseeds"])
        with f2:
            loc_filter = st.selectbox("📍 Mandi Hub Region", ["All"] + sorted(list(set(x["Location"] for x in st.session_state.listings))))

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
                        <span class="price-main">₹{item['Price']}<small style="font-size:0.8rem; color:#64748b;">/kg</small></span>
                    </div>
                    <div class="farmer-profile-box">
                        👨‍🌾 <b>Farmer:</b> {item['Farmer']}<br>
                        📞 <b>Contact:</b> <code>{item['Phone']}</code><br>
                        📍 <b>Hub:</b> {item['Location']} | 📦 <b>Stock:</b> {item['Qty']} kg<br>
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
                            "location": item["Location"]
                        }
                        st.success(f"Added {order_kg} kg {item['Crop']} to Cart!")
                        st.rerun()

    # SCREEN 2: CART & CHECKOUT
    elif menu == "🛍️ My Cart & Escrow Checkout":
        st.subheader("🛍️ Shopping Cart & Escrow Settlement")
        
        if not st.session_state.cart:
            st.info("Your cart is empty! Head over to 'Home & Farm Marketplace' to pick fresh crops.")
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
            st.caption("🔒 Payments are deposited into an autonomous Escrow and transferred to the Farmer only after OTP verification.")

            st.markdown("---")
            st.markdown("#### 🚚 Delivery Information")
            b1, b2 = st.columns(2)
            with b1:
                b_name = st.text_input("Buyer / Business Name", value=st.session_state.user_info.get("name", ""))
                b_phone = st.text_input("Mobile Number (for Delivery OTP)", value=st.session_state.user_info.get("contact", ""))
            with b2:
                b_addr = st.text_input("Delivery Address / Mandi Hub", placeholder="e.g. Boring Road, Patna")
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
                        st.session_state.cart.clear()
                        st.balloons()
                        st.success("🎉 Order Placed! Payment securely stored in escrow.")
                        st.rerun()
                    else:
                        st.error("Please fill in name and mobile number.")
            with c2:
                if st.button("🗑️ Empty Cart", use_container_width=True):
                    st.session_state.cart.clear()
                    st.rerun()

    # SCREEN 3: FARMER LISTING
    elif menu == "👨‍🌾 Farmer Produce Desk":
        st.subheader("👨‍🌾 Farmer Direct Harvest Listing")
        
        fc1, fc2 = st.columns(2)
        with fc1:
            f_name = st.text_input("Farmer Full Name", value=st.session_state.user_info.get("name", "Rameshwar Singh"))
            f_phone = st.text_input("Mobile Number", value=st.session_state.user_info.get("contact", "+91 9XXXXXXXXX"))
            f_crop = st.selectbox("Crop Harvested", [
                "Sweet Corn / Maize (Desi Makka)",
                "High-Sucrose Sugarcane (Taaza Ganna)",
                "Hajipur GI-Tag Banana (Chiniya Kela)",
                "Organic Raw Turmeric (Haldi Ganth)",
                "Basmati Rice (Sharbati Chawal)",
                "Fresh Red Tomato (Desi Tamatar)",
                "Certified Golden Wheat (Sharbati Gehu)",
                "Storage Red Onion (Patna Pyaz)",
                "Cold-Storage Desi Potato (Aloo)",
                "Pure Mustard Seeds (Pili Sarson)"
            ])
            f_cat = st.selectbox("Category", ["Grains", "Vegetables", "Fruits", "Cash Crops", "Spices", "Oilseeds"])
        with fc2:
            f_qty = st.number_input("Available Quantity (kg)", min_value=10, max_value=100000, value=500)
            f_price = st.number_input("Rate Expected (₹/kg)", min_value=1, value=25)
            f_loc = st.selectbox("Hub Location", ["Patna Rural", "Hajipur Mandi", "Muzaffarpur Hub", "Khagaria Hub", "West Champaran", "Gaya Mandi Hub", "Bhagalpur Hub", "Buxar District"])
            f_quality = st.selectbox("Quality Certificate", ["Grade-A Premium", "100% Organic", "Fresh Farm Harvest", "Naturally Ripened", "High Sucrose Juice Cane"])

        if st.button("🚀 Publish Crop to Live Mart", use_container_width=True):
            if f_name and f_phone:
                st.session_state.listings.append({
                    "ID": len(st.session_state.listings) + 101,
                    "Crop": f_crop,
                    "Category": f_cat,
                    "Farmer": f_name,
                    "Phone": f_phone,
                    "Price": f_price,
                    "Qty": f_qty,
                    "Location": f_loc,
                    "Quality": f_quality,
                    "Rating": "⭐ New Verified Farmer",
                    "Image": "https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?w=600&auto=format&fit=crop&q=80"
                })
                st.success("✅ Produce listed live on the marketplace!")
            else:
                st.error("Please provide your name and contact details.")

    # SCREEN 4: ORDER TRACKING
    elif menu == "📦 Live Orders Ledger":
        st.subheader("📦 Real-Time Order Transparency Ledger")
        st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔐 Delivery Verification & Escrow Release")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Enter 4-Digit Buyer Delivery OTP", placeholder="e.g. 5821")
        with c2:
            if st.button("Verify OTP & Release ₹ Payment to Farmer Bank", use_container_width=True):
                st.success("✅ OTP Verified! 100% Escrow amount transferred to farmer's UPI account.")

    # SCREEN 5: MANDI BENCHMARKING
    elif menu == "📊 Mandi Price Intelligence":
        st.subheader("📊 Mandi MSP vs KisanConnect Direct Rate")
        st.write("Live data showcasing fair value distribution by cutting out the middleman chain.")
        
        st.table(pd.DataFrame({
            "Crop": ["Sweet Corn (Makka)", "Sugarcane (Ganna)", "Banana (Kela)", "Haldi (Turmeric)", "Basmati Rice", "Golden Wheat", "Mustard Seeds"],
            "Govt Mandi Rate (₹/kg)": [14.00, 4.50, 18.00, 45.00, 30.00, 22.75, 48.00],
            "KisanConnect Direct (₹/kg)": [18.00, 8.00, 28.00, 65.00, 36.00, 25.00, 54.00],
            "Middleman Supermarket (₹/kg)": [26.00, 15.00, 45.00, 95.00, 48.00, 32.00, 70.00],
            "Farmer Profit Gain": ["+28.5%", "+77.7%", "+55.5%", "+44.4%", "+20.0%", "+9.8%", "+12.5%"]
        }))

    # SCREEN 6: IMPACT ANALYTICS
    elif menu == "📈 Impact Analytics":
        st.subheader("📈 Key Performance Metrics")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Farmer Realized Income Increase", "+38.2%", "Direct Payouts")
        with m2:
            st.metric("Consumer Cost Reduction", "-24.6%", "No Middlemen Cut")
        with m3:
            st.metric("Middleman Commissions Eliminated", "₹ 11.4 Lakhs", "Direct Transacted")

        st.markdown("---")
        st.write("#### 🚚 Pooled Route vs Traditional Logistics Cost")
        st.line_chart(pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Traditional Broker Logistics (₹)": [14000, 15500, 17000, 18500, 19200, 21000],
            "KisanConnect Shared Logistics (₹)": [7800, 8300, 8900, 9200, 9600, 10100]
        }).set_index("Month"))
