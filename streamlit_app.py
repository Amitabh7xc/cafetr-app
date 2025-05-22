import streamlit as st
import pandas as pd
from datetime import datetime
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Cafeteria Management System",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Theme and Styles ---
st.markdown("""
    <style>
    body, .main, .block-container {background-color: #f8f5f2;}
    .main-title {font-size: 2.5rem; font-weight: 700; color: #6f4e37;}
    .menu-card {background: #fff; border-radius: 14px; padding: 1.2em; margin-bottom: 1.2em; box-shadow: 0 2px 8px #e0e0e0;}
    .menu-card img {border-radius: 10px;}
    .stButton>button {background-color: #6f4e37; color: #fff; border-radius: 8px;}
    .stButton>button:hover {background-color: #a67c52;}
    .metric-label {color: #6f4e37;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">☕ Cafeteria Management System</div>', unsafe_allow_html=True)
st.markdown("---")

# --- Helper Functions ---
def initialize_data():
    """Initializes sample menu and order data if not already in session state."""
    if 'menu_items' not in st.session_state:
        st.session_state.menu_items = pd.DataFrame({
            'Item ID': [1, 2, 3, 4, 5, 6, 7, 8],
            'Name': ['Coffee', 'Tea', 'Sandwich', 'Salad', 'Pizza Slice', 'Burger', 'Fries', 'Juice'],
            'Category': ['Beverage', 'Beverage', 'Snack', 'Meal', 'Meal', 'Meal', 'Side', 'Beverage'],
            'Price': [50.00, 40.00, 120.00, 150.00, 100.00, 180.00, 70.00, 60.00],
            'Available': [True, True, True, True, True, False, True, True],
            'Image': [
                "https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=400&q=80", # Coffee
                "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=400&q=80", # Tea
                "https://images.unsplash.com/photo-1464306076886-debca5e8a6b0?auto=format&fit=crop&w=400&q=80", # Sandwich
                "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?auto=format&fit=crop&w=400&q=80", # Salad
                "https://images.unsplash.com/photo-1548365328-8b849e6c7b8b?auto=format&fit=crop&w=400&q=80", # Pizza Slice
                "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=400&q=80", # Burger
                "https://images.unsplash.com/photo-1506089676908-3592f7389d4d?auto=format&fit=crop&w=400&q=80", # Fries
                "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80", # Juice
            ]
        })

    if 'orders' not in st.session_state:
        st.session_state.orders = pd.DataFrame(columns=['Order ID', 'Timestamp', 'Items', 'Total Amount', 'Status'])

    if 'order_id_counter' not in st.session_state:
        st.session_state.order_id_counter = 1

    if 'cart' not in st.session_state:
        st.session_state.cart = []

def get_available_menu():
    """Returns the currently available menu items."""
    return st.session_state.menu_items[st.session_state.menu_items['Available'] == True]

def clear_cart():
    st.session_state.cart = []

def remove_cart_item(index):
    del st.session_state.cart[index]

def update_cart_quantity(index, new_quantity):
    st.session_state.cart[index]['Quantity'] = new_quantity
    st.session_state.cart[index]['Subtotal'] = st.session_state.cart[index]['Price'] * new_quantity

def format_currency(amount):
    return f"₹{amount:,.2f}"

# --- Main Application ---
initialize_data()

# --- Sidebar Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["View Menu & Order", "View Orders", "Manage Menu"])
st.sidebar.markdown("---")
st.sidebar.success("Welcome to the Cafeteria Management System!")

# --- Random Food Video ---
if page == "View Menu & Order":
    st.video("https://www.youtube.com/watch?v=4aZr5hZXP_s")  # Random food video

# --- Page 1: View Menu & Order ---
if page == "View Menu & Order":
    st.header("🍽️ Menu")

    available_menu_df = get_available_menu()

    if available_menu_df.empty:
        st.warning("No items are currently available on the menu.")
    else:
        st.subheader("Today's Specials")
        menu_cols = st.columns(2)
        for idx, row in available_menu_df.iterrows():
            with menu_cols[idx % 2]:
                st.markdown(
                    f"""
                    <div class="menu-card">
                        <img src="{row['Image']}" alt="{row['Name']}" style="width:100%;max-height:180px;object-fit:cover;">
                        <h4 style="margin-bottom:0.2em;">{row['Name']}</h4>
                        <span style="color:#888;">{row['Category']}</span><br>
                        <b style="color:#6f4e37;">{format_currency(row['Price'])}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.subheader("Place Your Order")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            selected_item_name = st.selectbox("Select Item", options=available_menu_df['Name'])
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
        with col3:
            st.write("")  # for alignment
            st.write("")  # for alignment
            if st.button("Add to Cart", use_container_width=True):
                if selected_item_name:
                    item_details = available_menu_df[available_menu_df['Name'] == selected_item_name].iloc[0]
                    st.session_state.cart.append({
                        'Item ID': item_details['Item ID'],
                        'Name': selected_item_name,
                        'Price': item_details['Price'],
                        'Quantity': quantity,
                        'Subtotal': item_details['Price'] * quantity,
                        'Image': item_details['Image']
                    })
                    st.success(f"Added {quantity} x {selected_item_name} to cart!")

        st.markdown("---")
        st.subheader("Your Cart 🛒")
        if not st.session_state.cart:
            st.info("Your cart is empty. Add items from the menu above.")
        else:
            cart_df = pd.DataFrame(st.session_state.cart)
            cart_cols = st.columns([3, 1, 1, 1, 1])
            with cart_cols[0]:
                st.markdown("**Item**")
            with cart_cols[1]:
                st.markdown("**Qty**")
            with cart_cols[2]:
                st.markdown("**Price**")
            with cart_cols[3]:
                st.markdown("**Subtotal**")
            with cart_cols[4]:
                st.markdown("**Remove**")
            for i, row in cart_df.iterrows():
                with cart_cols[0]:
                    st.image(row['Image'], width=60)
                    st.write(row['Name'])
                with cart_cols[1]:
                    new_quantity = st.number_input(
                        "Qty", min_value=1, value=row['Quantity'], step=1, key=f"qty_{i}"
                    )
                    if new_quantity != row['Quantity']:
                        update_cart_quantity(i, new_quantity)
                with cart_cols[2]:
                    st.write(format_currency(row['Price']))
                with cart_cols[3]:
                    st.write(format_currency(row['Subtotal']))
                with cart_cols[4]:
                    if st.button("❌", key=f"remove_{i}"):
                        remove_cart_item(i)
                        st.experimental_rerun()

            total_cart_amount = cart_df['Subtotal'].sum()
            total_items = sum(item['Quantity'] for item in st.session_state.cart)
            st.metric("Total Items", total_items)
            st.metric("Total Cart Amount", format_currency(total_cart_amount))

            col_cart1, col_cart2 = st.columns([1, 1])
            with col_cart1:
                if st.button("Clear Cart", use_container_width=True, key="clear_cart"):
                    clear_cart()
                    st.experimental_rerun()
            with col_cart2:
                if st.button("Place Order", type="primary", use_container_width=True):
                    if st.session_state.cart:
                        order_id = st.session_state.order_id_counter
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        items_ordered = cart_df.to_dict('records')  # More detailed storage
                        new_order = pd.DataFrame([{
                            'Order ID': order_id,
                            'Timestamp': timestamp,
                            'Items': items_ordered,
                            'Total Amount': total_cart_amount,
                            'Status': 'Pending'
                        }])
                        st.session_state.orders = pd.concat([st.session_state.orders, new_order], ignore_index=True)
                        st.session_state.order_id_counter += 1
                        st.session_state.cart = []  # Clear cart after placing order
                        st.success(f"Order #{order_id} placed successfully!")
                        st.balloons()
                    else:
                        st.warning("Your cart is empty. Cannot place an empty order.")
