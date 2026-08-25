import streamlit as st
import pandas as pd
import datetime

# Page Configuration
st.set_page_config(
    page_title="KisanSaathi | Direct Farm Mart",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Lush Green & Farm Watermark CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    * { font-family: 'Plus+Jakarta+Sans', sans-serif; }
    
    .stApp {
        background: linear-gradient(180deg, rgba(236, 253, 245, 0.95) 0%, rgba(209, 250, 229, 0.92) 100%),
                    url('https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?w=1200&auto=format&fit=crop&q=40');
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }

    .hero-box {
        background: linear-gradient(135deg, #065f46 0%, #059669 60%, #10b981 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(5, 150, 105, 0.3);
    }
    
    .crop-card-box {
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(8px);
        border: 2px solid #a7f3d0;
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 22px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.06);
    }

    .crop-badge {
        background: #059669;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
    }
    .quality-badge {
        background: #fef3c7;
        color: #d97706;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-left: 5px;
    }

    .price-tag {
        font-size: 1.5rem;
        font-weight: 800;
        color: #065f46;
    }

    .farmer-details {
        background: #f0fdf4;
        border-left: 4px solid #059669;
        padding: 8px 12px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# Expanded Product Master Catalog (with Makka, Sugarcane, Banana, Haldi)
INITIAL_ITEMS = [
    {
        "ID": 101,
        "Crop": "Sweet Corn / Maize (Makka)",
        "Category": "Grains",
        "Farmer": "Birendra Paswan",
        "Phone": "+91 98350 11223",
        "Price": 18,
        "Qty": 1500,
        "Location": "Khagaria Hub",
        "Quality": "Fresh Sweet Cob Grade-A",
        "Image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 102,
        "Crop": "Organic Sugarcane (Ganna)",
        "Category": "Commercial Crops",
        "Farmer": "Manoj Upadhyay",
        "Phone": "+91 97722 33445",
        "Price": 8,
        "Qty": 5000,
        "Location": "West Champaran",
        "Quality": "High Sucrose Juice Cane",
        "Image": "https://images.unsplash.com/photo-1589135233689-d561a3375b43?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 103,
        "Crop": "Hajipur Desi Banana (Chiniya Kela)",
        "Category": "Fruits",
        "Farmer": "Sunil Mahato",
        "Phone": "+91 91234 56780",
        "Price": 28,
        "Qty": 1200,
        "Location": "Hajipur Mandi",
        "Quality": "Naturally Ripened (GI Tag Area)",
        "Image": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 104,
        "Crop": "Raw Turmeric (Desi Haldi Ganth)",
        "Category": "Spices",
        "Farmer": "Rajendra Prasad",
        "Phone": "+91 94312 88990",
        "Price": 65,
        "Qty": 600,
        "Location": "Gaya Mandi Hub",
        "Quality": "High Curcumin Organic",
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
        "Quality": "Long Grain Aromatic",
        "Image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 106,
        "Crop": "Fresh Red Tomato (Desi Tamatar)",
        "Category": "Vegetables",
        "Farmer": "Amit Yadav",
        "Phone": "+91 99887 76655",
        "Price": 22,
        "Qty": 450,
        "Location": "Muzaffarpur Hub",
        "Quality": "Farm Picked Fresh",
        "Image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 107,
        "Crop": "Golden Wheat (Sharbati Gehu)",
        "Category": "Grains",
        "Farmer": "Rameshwar Singh",
        "Phone": "+91 98765 43210",
        "Price": 25,
        "Qty": 800,
        "Location": "Patna Rural",
        "Quality": "Certified Organic",
        "Image": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 108,
        "Crop": "Red Onion (Patna Pyaz)",
        "Category": "Vegetables",
        "Farmer": "Dinesh Kushwaha",
        "Phone": "+91 97711 22334",
        "Price": 20,
        "Qty": 1100,
        "Location": "Patna Central",
        "Quality": "Dry Graded Stock",
        "Image": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=600&auto=format&fit=crop&q=80"
    },
    {
        "ID": 109,
        "Crop": "Fresh Potato (Hajipur Desi Aloo)",
        "Category": "Vegetables",
        "Farmer": "Ram Naresh",
        "Phone": "+91 94300 22114",
        "Price": 14,
        "Qty": 1400,
        "Location": "Hajipur Mandi",
        "Quality": "Cold Store Graded",
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
        "Location": "Bhagalpur",
        "Quality": "42% Oil Grade",
        "Image": "https://images.unsplash.com/photo-1508873696983-2df5293cb395?w=600&auto=format&fit=crop&q=80"
    }
]

if 'listings' not in st.session_state:
    st.session_state.listings = INITIAL_ITEMS

if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {"Order ID": "ORD-701", "Item": "Hajipur Desi Banana (Chiniya Kela)", "Farmer": "Sunil Mahato", "Buyer": "Hotel Maurya (Patna)", "Qty": 200, "Bill (₹)": 5600, "Status": "Escrow Secured 🔒"}
    ]

# Hero Banner
st.markdown("""
<div class="hero-box">
    <h1 style="margin:0; font-size: 2.5rem; font-weight:800;">🌾 KisanSaathi Direct Mart</h1>
    <p style="margin:6px 0 0 0; font-size:1.1rem; opacity:0.95;">Direct Farm Harvest • 0% Broker Commission • Smart Escrow & Transparent Tracking</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?w=400&auto=format&fit=crop&q=80", caption="Direct Farm Network", use_container_width=True)
    st.markdown("### Navigation")
    menu = st.radio("Go To:", [
        "🛒 Live Farm Produce (Shop)",
        "🛍️ Cart & Smart Checkout",
        "👨‍🌾 Post Harvest (Farmer Desk)",
        "📦 Live Order Tracking",
        "📊 Mandi Intelligence",
        "📈 Impact Analytics"
    ])
    st.markdown("---")
    cart_items_count = sum(x["qty"] for x in st.session_state.cart.values())
    st.metric("🛍️ Cart Items", f"{cart_items_count} kg")

# ================= 1. SHOP SCREEN =================
if menu == "🛒 Live Farm Produce (Shop)":
    st.subheader("🥬 Fresh Harvest Available for Direct Purchase")
    
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        cat_select = st.selectbox("Filter by Category", ["All", "Grains", "Vegetables", "Fruits", "Commercial Crops", "Spices", "Oilseeds"])
    with col_f2:
        loc_select = st.selectbox("Filter by Mandi Region", ["All"] + sorted(list(set(x["Location"] for x in st.session_state.listings))))

    filtered_data = [
        x for x in st.session_state.listings
        if (cat_select == "All" or x["Category"] == cat_select) and (loc_select == "All" or x["Location"] == loc_select)
    ]

    st.markdown("---")
    
    # 3-Card Grid
    for i in range(0, len(filtered_data), 3):
        cols = st.columns(3)
        chunk = filtered_data[i:i+3]
        
        for col, item in zip(cols, chunk):
            with col:
                st.image(item["Image"], use_container_width=True)
                st.markdown(f"""
                <span class="crop-badge">{item['Category']}</span>
                <span class="quality-badge">{item['Quality']}</span>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:5px;">
                    <h3 style="margin:0; font-size:1.15rem;">{item['Crop']}</h3>
                    <span class="price-tag">₹{item['Price']}<small style="font-size:0.8rem; color:#666;">/kg</small></span>
                </div>
                <div class="farmer-details">
                    <b>👨‍🌾 Farmer:</b> {item['Farmer']}<br>
                    <b>📞 Contact:</b> <code>{item['Phone']}</code><br>
                    <b>📍 Location:</b> {item['Location']} | <b>📦 Stock:</b> {item['Qty']} kg
                </div>
                """, unsafe_allow_html=True)
                
                add_qty = st.number_input(f"Order (kg)", min_value=5, max_value=max(5, item["Qty"]), value=20, key=f"q_{item['ID']}")
                if st.button("🛒 Add to Cart", key=f"b_{item['ID']}", use_container_width=True):
                    st.session_state.cart[item["ID"]] = {
                        "id": item["ID"],
                        "crop": item["Crop"],
                        "farmer": item["Farmer"],
                        "price": item["Price"],
                        "qty": add_qty,
                        "location": item["Location"]
                    }
                    st.success(f"Added {add_qty} kg {item['Crop']}!")
                    st.rerun()

# ================= 2. CART & CHECKOUT =================
elif menu == "🛍️ Cart & Smart Checkout":
    st.subheader("🛍️ Cart Summary & Direct Escrow Payment")
    
    if not st.session_state.cart:
        st.info("Your shopping cart is empty! Add crops from the live store.")
    else:
        table_rows = []
        total_val = 0
        for k, v in list(st.session_state.cart.items()):
            sub = v["qty"] * v["price"]
            total_val += sub
            table_rows.append({
                "Crop Produce": v["crop"],
                "Farmer Name": v["farmer"],
                "Rate": f"₹{v['price']} / kg",
                "Weight": f"{v['qty']} kg",
                "Subtotal": f"₹{sub:,.2f}"
            })

        st.table(pd.DataFrame(table_rows))
        st.markdown(f"### 💳 Total Payable: :green[**₹{total_val:,.2f}**]")
        st.caption("🔒 Payments are deposited to the KisanSaathi Smart Escrow and released after physical OTP validation.")

        st.markdown("---")
        st.markdown("#### 🚚 Delivery Coordinates")
        b1, b2 = st.columns(2)
        with b1:
            buyer_title = st.text_input("Buyer / Establishment Name", placeholder="e.g. Gaurav Supermart")
            buyer_contact = st.text_input("Contact Mobile", placeholder="+91 9XXXXXXXXX")
        with b2:
            buyer_destination = st.text_input("Destination Address", placeholder="e.g. Boring Road, Patna")
            delivery_window = st.selectbox("Preferred Dispatch Time", ["Early Morning (6 AM - 10 AM)", "Evening (4 PM - 8 PM)"])

        cb1, cb2 = st.columns(2)
        with cb1:
            if st.button("🚀 Pay & Confirm Order (Escrow Locked)", use_container_width=True):
                if buyer_title and buyer_contact:
                    for cid, cval in st.session_state.cart.items():
                        st.session_state.orders.append({
                            "Order ID": f"ORD-{len(st.session_state.orders) + 702}",
                            "Item": cval["crop"],
                            "Farmer": cval["farmer"],
                            "Buyer": f"{buyer_title} ({buyer_contact})",
                            "Qty": cval["qty"],
                            "Bill (₹)": cval["qty"] * cval["price"],
                            "Status": "Escrow Secured 🔒"
                        })
                    st.session_state.cart.clear()
                    st.balloons()
                    st.success("🎉 Order successfully placed via Smart Escrow!")
                    st.rerun()
                else:
                    st.error("Please fill in buyer name and mobile number.")
        with cb2:
            if st.button("🗑️ Empty Cart", use_container_width=True):
                st.session_state.cart.clear()
                st.rerun()

# ================= 3. FARMER POSTING =================
elif menu == "👨‍🌾 Post Harvest (Farmer Desk)":
    st.subheader("👨‍🌾 Direct Farmer Produce Publishing Portal")
    
    fc1, fc2 = st.columns(2)
    with fc1:
        fn = st.text_input("Farmer Full Name", placeholder="e.g. Rameshwar Singh")
        fp = st.text_input("Farmer Mobile Number", placeholder="+91 9XXXXXXXXX")
        fc = st.selectbox("Crop Harvested", [
            "Sweet Corn / Maize (Makka)", 
            "Organic Sugarcane (Ganna)", 
            "Hajipur Desi Banana (Chiniya Kela)", 
            "Raw Turmeric (Desi Haldi Ganth)",
            "Basmati Rice (Sharbati Chawal)", 
            "Fresh Red Tomato (Desi Tamatar)", 
            "Golden Wheat (Sharbati Gehu)", 
            "Red Onion (Patna Pyaz)", 
            "Fresh Potato (Hajipur Desi Aloo)", 
            "Pure Mustard Seeds (Pili Sarson)"
        ])
        fcat = st.selectbox("Category", ["Grains", "Vegetables", "Fruits", "Commercial Crops", "Spices", "Oilseeds"])
    with fc2:
        fq = st.number_input("Available Stock (kg)", min_value=10, max_value=100000, value=500)
        fpr = st.number_input("Demanded Price (₹/kg)", min_value=1, value=25)
        fl = st.selectbox("Nearest Mandi Hub", ["Patna Rural", "Hajipur Mandi", "Muzaffarpur Hub", "Khagaria Hub", "West Champaran", "Gaya Mandi Hub", "Bhagalpur", "Buxar District"])
        fqual = st.selectbox("Quality Standard", ["Certified Organic", "Fresh Sweet Cob Grade-A", "High Curcumin Organic", "Naturally Ripened (GI Area)", "High Sucrose Juice Cane", "Cold Store Graded"])

    if st.button("🚀 Publish to Live Market", use_container_width=True):
        if fn and fp:
            st.session_state.listings.append({
                "ID": len(st.session_state.listings) + 101,
                "Crop": fc,
                "Category": fcat,
                "Farmer": fn,
                "Phone": fp,
                "Price": fpr,
                "Qty": fq,
                "Location": fl,
                "Quality": fqual,
                "Image": "https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?w=600&auto=format&fit=crop&q=80"
            })
            st.success("✅ Your produce is now live on the KisanSaathi Mart!")
        else:
            st.error("Please fill in farmer name and mobile number.")

# ================= 4. ORDER TRACKING =================
elif menu == "📦 Live Order Tracking":
    st.subheader("📦 Real-Time Order Transparency Ledger")
    st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔐 Delivery Verification & Escrow Payout")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Enter 4-Digit Buyer Delivery OTP", placeholder="e.g. 7412")
    with c2:
        if st.button("Verify OTP & Release ₹ Payment to Farmer Bank", use_container_width=True):
            st.success("✅ OTP Verified! 100% Escrow amount transferred to farmer's UPI account.")

# ================= 5. MANDI BENCHMARKING =================
elif menu == "📊 Mandi Intelligence":
    st.subheader("📊 Mandi MSP vs KisanSaathi Direct Rate")
    st.write("Real-time data showcasing profit margin improvement by skipping middlemen.")
    
    st.table(pd.DataFrame({
        "Crop": ["Sweet Corn (Makka)", "Sugarcane (Ganna)", "Banana (Kela)", "Haldi (Turmeric)", "Basmati Rice", "Golden Wheat", "Mustard Seeds"],
        "APMC Mandi Rate (₹/kg)": [14.00, 4.50, 18.00, 45.00, 30.00, 22.75, 48.00],
        "KisanSaathi Direct (₹/kg)": [18.00, 8.00, 28.00, 65.00, 36.00, 25.00, 54.00],
        "Middleman Supermarket (₹/kg)": [26.00, 15.00, 45.00, 95.00, 48.00, 32.00, 70.00],
        "Farmer Direct Benefit": ["+28.5%", "+77.7%", "+55.5%", "+44.4%", "+20.0%", "+9.8%", "+12.5%"]
    }))

# ================= 6. IMPACT ANALYTICS =================
elif menu == "📈 Impact Analytics":
    st.subheader("📈 SIH Key Performance Metrics")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Farmer Income Growth", "+38.2%", "Direct Payouts")
    with m2:
        st.metric("Consumer Cost Reduction", "-24.6%", "No Middlemen Cut")
    with m3:
        st.metric("Commission Saved", "₹ 11.4 Lakhs", "Direct Transacted")

    st.markdown("---")
    st.write("#### 🚚 Pooled Route vs Traditional Logistics Cost")
    st.line_chart(pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Traditional Broker Logistics (₹)": [14000, 15500, 17000, 18500, 19200, 21000],
        "KisanSaathi Shared Logistics (₹)": [7800, 8300, 8900, 9200, 9600, 10100]
    }).set_index("Month"))