import streamlit as st
import pandas as pd

import base64
from pathlib import Path

import streamlit as st
from openai import OpenAI, OpenAIError

st.set_page_config(
    page_title="FlorAI | Love Like a Bouquet",
    page_icon="‧₊˚❀༉‧₊˚.",
    layout="wide",
    initial_sidebar_state="collapsed"
)
import streamlit.components.v1 as components

# JavaScript hover listener to trigger Streamlit's sidebar drawer
components.html("""
<script>
const doc = window.parent.document;

function setupSidebarHover() {
    const expandBtn = doc.querySelector('button[data-testid="stSidebarExpandButton"]') || 
                      doc.querySelector('button[aria-label="Open sidebar"]');
    const collapseBtn = doc.querySelector('button[data-testid="stSidebarCollapseButton"]') || 
                        doc.querySelector('button[aria-label="Close sidebar"]');
    const sidebar = doc.querySelector('[data-testid="stSidebar"]');

    if (expandBtn && !expandBtn.dataset.hoverAttached) {
        expandBtn.dataset.hoverAttached = "true";
        // When mouse hovers over ☰ MENU -> open drawer
        expandBtn.addEventListener('mouseenter', () => {
            expandBtn.click();
        });
    }

    if (sidebar && !sidebar.dataset.hoverAttached) {
        sidebar.dataset.hoverAttached = "true";
        // When mouse leaves the drawer -> close drawer
        sidebar.addEventListener('mouseleave', () => {
            const currentCollapseBtn = doc.querySelector('button[data-testid="stSidebarCollapseButton"]') || 
                                       doc.querySelector('button[aria-label="Close sidebar"]');
            if (currentCollapseBtn) {
                currentCollapseBtn.click();
            }
        });
    }
}

// Run polling loop to hook onto elements once Streamlit finishes rendering
setInterval(setupSidebarHover, 400);
</script>
""", height=0, width=0)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

/* Base Palette & Typography */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    background-color: #FAF5F2 !important;
    color: #2F2A28 !important;
}

h1, h2, h3, .serif-font {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-weight: 300 !important;
    letter-spacing: 0.12em !important;
    color: #1A1817 !important;
}

p, span, label {
    font-weight: 300 !important;
    letter-spacing: 0.02em !important;
    color: #554D4A;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #ECE7E1 !important;
    padding-top: 1.2rem !important;
    max-width: 320px !important;
    box-shadow: 4px 0 25px rgba(0,0,0,0.05) !important;
}

/* Navigation Row Buttons */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #1A1817 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    text-align: left !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    padding: 1rem 0.6rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #F5F1ED !important;
    border-radius: 0px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #FAF8F5 !important;
    color: #8C7B75 !important;
    border-color: #F5F1ED !important;
}

/* 1. CLOSED STATE: 3-Line Hamburger + MENU Button */
button[data-testid="stSidebarExpandButton"],
button[aria-label="Open sidebar"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.55rem !important;
    padding: 0.5rem !important;
    visibility: visible !important;
}

button[data-testid="stSidebarExpandButton"] svg,
button[aria-label="Open sidebar"] svg {
    display: none !important;
}

button[data-testid="stSidebarExpandButton"]::before,
button[aria-label="Open sidebar"]::before {
    content: "☰" !important;
    font-size: 1.2rem !important;
    font-weight: 400 !important;
    line-height: 1 !important;
    color: #1A1817 !important;
}

button[data-testid="stSidebarExpandButton"]::after,
button[aria-label="Open sidebar"]::after {
    content: "MENU" !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    color: #1A1817 !important;
}

/* 2. OPEN STATE: Circled ✕ + CLOSE Button */
button[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.55rem !important;
    padding: 0.5rem !important;
    visibility: visible !important;
}

button[data-testid="stSidebarCollapseButton"] svg,
button[aria-label="Close sidebar"] svg {
    display: none !important;
}

button[data-testid="stSidebarCollapseButton"]::before,
button[aria-label="Close sidebar"]::before {
    content: "✕" !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 24px !important;
    height: 24px !important;
    border-radius: 50% !important;
    border: 1px solid #D6D0C9 !important;
    font-size: 0.65rem !important;
    font-weight: 400 !important;
    color: #1A1817 !important;
}

button[data-testid="stSidebarCollapseButton"]::after,
button[aria-label="Close sidebar"]::after {
    content: "CLOSE" !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    color: #1A1817 !important;
}

/* Product Card & App Buttons */
.editorial-card {
    background-color: #FFFDFD !important;
    border: 1px solid #EFE4E5 !important;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 20px rgba(186, 163, 165, 0.06);
}

.main .stButton > button {
    background-color: #2C2626 !important;
    color: #FAF5F2 !important;
    border-radius: 0px !important;
    border: 1px solid #2C2626 !important;
    padding: 0.65rem 1.8rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    transition: all 0.25s ease;
}

.main .stButton > button:hover {
    background-color: #FAF5F2 !important;
    color: #2C2626 !important;
    border-color: #2C2626 !important;
}

/* 1. Style the sidebar drawer */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #ECE7E1 !important;
    padding-top: 1.5rem !important;
    max-width: 320px !important;
    box-shadow: 6px 0 25px rgba(0,0,0,0.06) !important;
}

/* 2. Hide the double arrow « completely */
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarExpandButton"] svg,
button[aria-label="Close sidebar"] svg,
button[aria-label="Open sidebar"] svg {
    display: none !important;
}

/* 3. Style the toggle button when closed (☰ MENU) */
button[data-testid="stSidebarExpandButton"],
button[aria-label="Open sidebar"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.55rem !important;
    padding: 0.5rem 0.8rem !important;
}

button[data-testid="stSidebarExpandButton"]::before,
button[aria-label="Open sidebar"]::before {
    content: "☰" !important;
    font-size: 1.15rem !important;
    line-height: 1 !important;
    color: #1A1817 !important;
}

button[data-testid="stSidebarExpandButton"]::after,
button[aria-label="Open sidebar"]::after {
    content: "MENU" !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    color: #1A1817 !important;
}

/* 4. Style the toggle button when open (Circled ✕ CLOSE) */
button[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.55rem !important;
    padding: 0.5rem 0.8rem !important;
}

button[data-testid="stSidebarCollapseButton"]::before,
button[aria-label="Close sidebar"]::before {
    content: "✕" !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 24px !important;
    height: 24px !important;
    border-radius: 50% !important;
    border: 1px solid #D6D0C9 !important;
    font-size: 0.65rem !important;
    color: #1A1817 !important;
}

button[data-testid="stSidebarCollapseButton"]::after,
button[aria-label="Close sidebar"]::after {
    content: "CLOSE" !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    color: #1A1817 !important;
}

/* 5. Navigation buttons inside sidebar */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #1A1817 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    text-align: left !important;
    display: flex !important;
    justify-content: space-between !important;
    width: 100% !important;
    padding: 1rem 0.6rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #F5F1ED !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #FAF8F5 !important;
    color: #8C7B75 !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# ----------------- MASTER BOTANICAL DATA (BY SEASONS & IMAGES) -----------------
SEASONAL_COLLECTIONS = {
    "Spring": {
        "Nº 01 • Pastel Lilac Veil": {
            "meaning": "Purity, Grace & Reverence",
            "stems": ["Blush Pompon Dahlia", "White Calla Lily", "Dusty Lavender Garden Rose", "Ivory Astilbe Plumes"],
            "price": 145,
            "image": "https://images.unsplash.com/photo-1526047932273-341f2a7631f9?auto=format&fit=crop&w=800&q=80",
            "tagline": "Pale blush pompon dahlias, ivory calla lilies, and dusty lavender roses framed in airy astilbe."
        },
        "Nº 02 • Ethereal Mauve": {
            "meaning": "Delicate Affection & Lasting Devotion",
            "stems": ["Double Lilac-Pink Peony Tulips", "Pale Lilac Alstroemeria", "Nigella Pod Accents"],
            "price": 125,
            "image": "https://images.unsplash.com/photo-1582794543139-8ac9cb0f7b11?auto=format&fit=crop&w=800&q=80",
            "tagline": "Reflexed peony tulips and sheer Alstroemeria balanced with dark sculptural seed pods."
        }
    },
    "Summer": {
        "Nº 03 • Citrus Sunrise": {
            "meaning": "Radiant Joy, Passion & Honor",
            "stems": ["Peach Pompon Dahlia", "Lemon Yellow Phalaenopsis", "Golden Oncidium Orchid", "Gloriosa Flame Lily", "Mini Sunflower", "White Snowberry"],
            "price": 175,
            "image": "https://images.unsplash.com/photo-1561181286-d3fee7d55364?auto=format&fit=crop&w=800&q=80",
            "tagline": "Dynamic sunset tones combining golden dancing orchids, reflexed gloriosa, and soft peach dahlias."
        },
        "Nº 04 • Modern Ikebana Duo": {
            "meaning": "Patience, Peace & Hospitality",
            "stems": ["Lilac & Green Anthuriums", "Feverfew Daisy Florets"],
            "price": 95,
            "image": "https://images.unsplash.com/photo-1508610048659-a06b669e3321?auto=format&fit=crop&w=800&q=80",
            "tagline": "Architectural clean lines featuring heart-shaped anthuriums paired with delicate wild feverfew."
        }
    },
    "Autumn": {
        "Nº 05 • Sculptural Flora": {
            "meaning": "Strength, Faith & Enduring Devotion",
            "stems": ["Bicolor Pink-Blush Anthurium", "Crimson Matsumoto Aster", "Upright Sansevieria Leaf"],
            "price": 135,
            "image": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&q=80",
            "tagline": "Minimalist Japanese-inspired placement with high-contrast magenta spadices and structural foliage."
        }
    },
    "Winter": {
        "Nº 06 • High-Contrast Monochrome": {
            "meaning": "Avant-Garde Luxury & Mystery",
            "stems": ["White Anthurium", "Cascade Phalaenopsis Orchid", "Dyed Jet-Black Roses", "Pure White Roses", "Burgundy Sharry Baby Oncidium", "White Delphinium"],
            "price": 245,
            "image": "https://images.unsplash.com/photo-1509722747041-616f39b57569?auto=format&fit=crop&w=800&q=80",
            "tagline": "Drama and editorial contrast: dyed black roses anchored by cascading white moth orchids and rich chocolate oncidium."
        }
    }
}

TIERS = {
    "The Petite Vessel ($95)": {"price": 95, "stem_count": 10, "vessel": "matte bisque ceramic cylinder"},
    "The Signature Compote ($165)": {"price": 165, "stem_count": 18, "vessel": "fluted stoneware compote pedestal"},
    "The Gallery Urn ($285)": {"price": 285, "stem_count": 30, "vessel": "raw unglazed footed ceramic urn"}
}

# ----------------- BRAND HEADER -----------------
st.markdown(
"""<div style="margin-bottom: 1.5rem;">
<div style="background-color: #F8ECEB; border-bottom: 1px solid #EFE4E5; padding: 0.38rem 1rem; text-align: center;">
<p style="margin: 0; font-size: 0.68rem; letter-spacing: 0.04em; color: #332D2C; font-weight: 300;">Enjoy 20% off your first floral order</p>
</div>
<div style="text-align: center; line-height: 1; padding: 1.4rem 0 0.8rem 0; border-bottom: 1px solid #ECE3E3;">
<span style="font-family: 'Fraunces', 'Cormorant Garamond', serif; font-size: 1.45rem; letter-spacing: 0.05em; font-weight: 400; text-transform: lowercase; color: #1A1817;">florai</span><br>
<span style="font-size: 0.48rem; letter-spacing: 0.28em; text-transform: uppercase; color: #7B6E6E; font-weight: 400;">Los Angeles </span>
</div>
</div>""",
    unsafe_allow_html=True
)
# ----------------- SESSION STATE NAVIGATION -----------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "SIGNATURE COLLECTION"

# ----------------- SLIDE-OUT LEFT DRAWER -----------------
with st.sidebar:
    # 1. Signature Collection
    if st.button("SIGNATURE COLLECTION        ›", key="nav_btn_collection"):
        st.session_state.current_page = "SIGNATURE COLLECTION"
        st.rerun()

    # 2. Custom Floral Design
    if st.button("CUSTOM FLORAL DESIGN        ›", key="nav_btn_custom"):
        st.session_state.current_page = "CUSTOM FLORAL DESIGN"
        st.rerun()

    # 3. Lookbook
    if st.button("LOOKBOOK                 ›", key="nav_btn_lookbook"):
        st.session_state.current_page = "LOOKBOOK"
        st.rerun()

   # ----------------- FOOTER & SOCIAL MEDIA ICONS -----------------
    social_footer_html = """<div style="margin-top: 2.5rem; padding-top: 1.2rem; border-top: 1px solid #F2EEEA;">
<p style="font-size: 0.72rem; color: #8F857D; letter-spacing: 0.08em; line-height: 1.8; margin-bottom: 1.2rem;">
❀ Complimentary LA Delivery ($150+)<br>
❀ Inquiry: <a href="mailto:atelier@florai.com" style="color: #6E6360; text-decoration: none;">atelier@florai.com</a>
</p>
<p style="font-size: 0.65rem; letter-spacing: 0.22em; text-transform: uppercase; color: #A69E97; margin-bottom: 0.6rem;">
Follow US
</p>
<div style="display: flex; gap: 1.2rem; align-items: center;">
<!-- Instagram -->
<a href="https://instagram.com" target="_blank" title="Instagram" style="color: #2F2A28; text-decoration: none;">
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
<line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
</svg>
</a>
<!-- Email -->
<a href="mailto:atelier@florai.com" title="Email Atelier" style="color: #2F2A28; text-decoration: none;">
<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
<polyline points="22,6 12,13 2,6"></polyline>
</svg>
</a>
</div>
</div>"""

    st.markdown(social_footer_html, unsafe_allow_html=True)


# ======================================================
# PAGE 1: SIGNATURE COLLECTION
# ======================================================
if st.session_state.current_page == "SIGNATURE COLLECTION":
    st.markdown("<p style='text-align: center; font-size: 0.78rem; letter-spacing: 0.25em; text-transform: uppercase; color: #8F857D; margin: 1.5rem 0 2rem 0;'>Select Your Curated Seasonal Arrangement</p>", unsafe_allow_html=True)

    col_products, col_cart = st.columns([2, 1], gap="medium")

    with col_products:
        selected_season = st.selectbox("Filter by Season:", list(SEASONAL_COLLECTIONS.keys()))
        season_items = SEASONAL_COLLECTIONS[selected_season]

        for item_name, item_details in season_items.items():
            st.markdown(f"""
            <div class="editorial-card">
                <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #F2EEEA; padding-bottom: 0.8rem; margin-bottom: 1rem;">
                    <span style="font-family: Cormorant Garamond, serif; font-size: 1.35rem; letter-spacing: 0.05em;">{item_name}</span>
                    <span style="font-family: Cormorant Garamond, serif; font-size: 1.25rem;">${item_details['price']}</span>
                </div>
                <p style="font-size: 0.82rem; color: #7A726D; margin-bottom: 0.6rem;">{item_details['tagline']}</p>
                <p style="font-size: 0.75rem; color: #8F857D; font-style: italic; margin-bottom: 0.8rem;">花語寓意: {item_details['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Add to Bag • ${item_details['price']}", key=f"btn_prod_{item_name}"):
                st.session_state.cart.append({
                    "name": item_name,
                    "season": selected_season,
                    "price": item_details["price"]
                })
                st.rerun()
            st.write("")

    with col_cart:
        st.markdown("""
        <div style="background-color: #FFFFFF; border: 1px solid #EFEAE6; padding: 1.5rem 1.5rem 0.5rem 1.5rem;">
            <p style="font-size: 0.72rem; letter-spacing: 0.25em; text-transform: uppercase; color: #8F857D; text-align: center;">Shopping Bag</p>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.cart:
            st.markdown("<p style='text-align: center; font-size: 0.82rem; color: #A69E97; padding: 2rem 0;'>Your shopping bag is empty.</p>", unsafe_allow_html=True)
        else:
            total_sum = 0
            for idx, cart_item in enumerate(st.session_state.cart):
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F5F1ED; padding: 0.8rem 0;">
                    <div>
                        <span style="font-size: 0.82rem; font-weight: 400;">{cart_item['name']}</span><br>
                        <span style="font-size: 0.7rem; color: #9E948C;">{cart_item.get('season', 'Bespoke Studio')}</span>
                    </div>
                    <span style="font-family: Cormorant Garamond, serif; font-size: 1rem;">${cart_item['price']}</span>
                </div>
                """, unsafe_allow_html=True)
                total_sum += cart_item["price"]

            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 1.2rem 0 1rem 0; border-top: 1.5px solid #1A1817; margin-top: 1rem;">
                <span style="font-size: 0.8rem; letter-spacing: 0.15em; text-transform: uppercase;">Estimated Total</span>
                <span style="font-family: Cormorant Garamond, serif; font-size: 1.4rem; font-weight: 500;">${total_sum}</span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Proceed to Checkout", use_container_width=True):
                st.success("Your floral commission request has been received.")
            if st.button("Empty Bag", use_container_width=True):
                st.session_state.cart = []
                st.rerun()


# ======================================================
# PAGE 2: CUSTOM FLORAL DESIGN
# ======================================================
elif st.session_state.current_page == "CUSTOM FLORAL DESIGN":
    IMAGE_DIR = Path(__file__).resolve().parent / "images"
    FLORIST_CHOICE = "Let Florist Decide"

    flowers = {
        "Dahlia": {
            "image": "Dahlia.jpg",
            "meaning": "Admiration & Lasting Commitment",
            
        },
        "Calla Lily": {
            "image": "Calla Lily.jpg",
            "meaning": "Elegance, Respect & Devotion",
        },
        "Anthurium": {
            "image": "anthurium.jpg",
            "meaning": "Welcome & Warmth",
        },
        "Phalaenopsis Orchid": {
            "image": "Phalaenopsis Orchid.jpg",
            "meaning": "Admiration & Refined Beauty",
        },
        "Oncidium Orchid (文心蘭 / 跳舞蘭)": {
            "image": "oncidium.jpg",
            "meaning": "Joy & Celebration",
        },
        "Double Peony Tulip (重瓣鬱金香)": {
            "image": "double_tulip.jpg",
            "meaning": "Love & Affection",
        },
        "Gloriosa Lily": {
            "image": "Gloriosa Lily.jpg",
            "meaning": "Passion & Admiration",
        },
        "Garden Rose": {
            "image": "Garden Rose.jpg",
            "meaning": (
                "Classic: Love & Romance\n\n"
                "Lavender: Love at First Sight\n\n"
                "Black: Farewell & Remembrance"
            ),
        },
        "Chamomile": {
            "image": "Chamomile.jpg",
            "meaning": "Encouragement & Comfort",
        },
        "Alstroemeria (水仙百合 / 六出花)": {
            "image": "alstroemeria.jpg",
            "meaning": "Friendship & Support",
        },
        "Astilbe": {
            "image": "Astilbe.jpg",
            "meaning": "Patience & Dedication",
        },
        FLORIST_CHOICE: {
            "image": None,
            "meaning": "讓花藝師依照你的心意、色調與季節挑選花材。",
        },
    }

    color_options = [
        "Soft Pastels: Blush Pink, Pale Lavender, Baby Blue, Butter Yellow",
        "Warm Tones: Peach, Terracotta, Ochre, Golden Sunrise",
        "Cool Tones: Mauve, Dusty Lavender, Soft Plum, Powder Blue",
        "Neutral: Cream, Bone White, Fresh Apple Green",
        "High Contrast: Monochrome Black, Pure White, Deep Charcoal",
        FLORIST_CHOICE,
    ]

    sentiment_options = [
        FLORIST_CHOICE,
        "Love & Romance｜blush pink, burgundy",
        "Friendship & Companionship｜Yellow, peach, cream",
        "Gratitude & Appreciation｜Dusty pink, mauve, ivory",
        "Congratulations & Success｜Purple, golden yellow, white",
        "Joy & Celebration｜Bright yellow, coral, orange",
        "Good Luck & Prosperity｜Red, golden yellow, orange",
        "Thinking of You｜Blush pink, lavender, cream",
    ]

    # --------------------------------------------------
    # 2. Session state and reusable photo display
    # --------------------------------------------------
    st.session_state.setdefault("cart", [])

    def show_flower_photo(flower_name, width=160):
        """Display a reference photo, if one is available."""
        filename = flowers[flower_name]["image"]

        if filename is None:
            return

        image_path = IMAGE_DIR / filename

        if image_path.is_file():
            st.image(str(image_path), width=width)
        else:
            st.caption(f"Photo coming soon｜{flower_name.split(' (')[0]}")

    # --------------------------------------------------
    # 3. Page layout
    # --------------------------------------------------
    st.markdown(
        """
        <p style="
            text-align: center;
            font-size: 0.78rem;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: #8F857D;
            margin: 1.5rem 0 2rem;
        ">
            Custom Floral Consultation & AI Render
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_studio_cfg, col_studio_preview = st.columns(
        [1, 1],
        gap="large",
    )

    # --------------------------------------------------
    # 4. Design settings
    # --------------------------------------------------
    with col_studio_cfg:
        st.subheader("1. Design Specifications")

        color_tone = st.selectbox(
            "Flower Color Tone",
            options=color_options,
            key="custom_color_tone",
        )

        specific_flower = st.selectbox(
            "Flower Variety",
            options=list(flowers),
            key="custom_flower",
        )

        # Photo and meaning of the selected flower.
        selected_flower = flowers[specific_flower]

        with st.container(border=True):
            if specific_flower == FLORIST_CHOICE:
                st.write("**Florist’s Selection**")
                st.write(selected_flower["meaning"])
            else:
                photo_col, meaning_col = st.columns([1, 2])

                with photo_col:
                    show_flower_photo(specific_flower)

                with meaning_col:
                    st.write(f"**{specific_flower}**")
                    st.write(selected_flower["meaning"])

        # Browse every flower before making a selection.
        with st.expander("View All Flower Photos"):
            gallery_columns = st.columns(2)

            flower_names = [
                name for name in flowers
                if name != FLORIST_CHOICE
            ]

            for index, flower_name in enumerate(flower_names):
                with gallery_columns[index % 2]:
                    show_flower_photo(flower_name, width=130)
                    st.write(f"**{flower_name}**")

        st.caption(
            "Photos are visual references; colors and varieties may vary. "
        )

        flower_meaning = st.selectbox(
            "Your Message",
            options=sentiment_options,
            key="custom_sentiment",
            help="Choose the message you want to express with this bouquet.",
        )

        tier_choice = st.selectbox(
            "Arrangement Tier",
            options=list(TIERS),
            key="custom_tier",
        )
        selected_tier = TIERS[tier_choice]
        try:
            openai_api_key = st.secrets.get("OPENAI_API_KEY", "")
        except FileNotFoundError:
            openai_api_key = ""

        st.divider()

        generate_bespoke = st.button(
            "✨ Visualize Bespoke Concept",
            use_container_width=True,
            key="generate_custom_concept",
        )

    # --------------------------------------------------
    # 5. Generate and display the bouquet concept
    # --------------------------------------------------
    with col_studio_preview:
        st.subheader("2. Atelier Rendering")

        if generate_bespoke:
            if not openai_api_key.strip():
                st.error("error")

            else:
                # Explicit checks handle "Let Florist Decide" correctly.
                tone_desc = (
                    "a delicate, harmonious, high-end palette"
                    if color_tone == FLORIST_CHOICE
                    else color_tone
                )

                flower_desc = (
                    "a curated selection of seasonal flowers"
                    if specific_flower == FLORIST_CHOICE
                    else f"prominently featuring {specific_flower}"
                )

                meaning_desc = (
                    "understated elegance and poetic warmth"
                    if flower_meaning == FLORIST_CHOICE
                    else flower_meaning
                )

                prompt = (
                    "An editorial studio photograph of an exquisite "
                    "custom floral arrangement inspired by romantic art cinema. "
                    "Soft natural window daylight, a neutral plaster wall, "
                    "and gentle shadows. "
                    f"Vessel: {selected_tier['vessel']}. "
                    f"Color palette: {tone_desc}. "
                    f"Floral composition: {flower_desc}. "
                    f"Emotional mood: {meaning_desc}. "
                    f"Approximately {stem_count} stems, arranged in an organic, "
                    "asymmetrical ikebana-inspired composition with loose "
                    "movement, delicate tendrils, beautiful negative space, "
                    "and realistic botanical textures. "
                    "No text, labels, or watermarks."
                )

                with st.spinner("Creating your custom floral concept..."):
                    try:
                        with OpenAI(
                            api_key=openai_api_key.strip()
                        ) as client:
                            response = client.images.generate(
                                model="gpt-image-1",
                                prompt=prompt,
                                size="1024x1024",
                                quality="medium",
                                n=1,
                            )

                        if (
                            not response.data
                            or not response.data[0].b64_json
                        ):
                            st.error("No image was returned. Please try again.")

                        else:
                            # Store image bytes so the preview survives reruns.
                            image_bytes = base64.b64decode(
                                response.data[0].b64_json
                            )

                            st.session_state["bespoke_image"] = image_bytes
                            st.session_state["bespoke_meta"] = {
                                "name": f"Bespoke: {tier_choice.split(' (')[0]}",
                                "season": (
                                    f"{color_tone.split(':')[0]} • "
                                    f"{specific_flower.split(' (')[0]}"
                                ),
                                "price": retail_price,
                            }

                    except OpenAIError as error:
                        st.error(f"Image generation failed: {error}")

        # This preview represents the last successfully generated design.
        if st.session_state.get("bespoke_image") is not None:
            st.image(
                st.session_state["bespoke_image"],
                use_container_width=True,
            )

            concept = st.session_state["bespoke_meta"]
            st.caption(
                f"{concept['name']} • {concept['season']} • "
                f"${concept['price']:,.2f}"
            )

            if st.button(
                "Add Custom Concept to Bag",
                use_container_width=True,
                key="add_custom_concept",
            ):
                st.session_state.cart.append(concept.copy())
                st.success("Your custom concept has been added to your bag.")

        else:
            st.markdown(
                """
                <div style="
                    border: 1px dashed #DDD5CD;
                    padding: 4rem 2rem;
                    text-align: center;
                    background-color: #FCFBFA;
                ">
                    <p style="
                        font-size: 0.8rem;
                        color: #A69E97;
                        text-transform: uppercase;
                        letter-spacing: 0.15em;
                    ">
                        Your bespoke visual concept will render here
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ======================================================
# PAGE 3: LOOKBOOK
# ======================================================
elif st.session_state.current_page == "LOOKBOOK":
    st.markdown("<p style='text-align: center; font-style: italic; font-size: 1.05rem; margin: 1.5rem 0 2.5rem 0; font-family: Cormorant Garamond, serif;'>“Like a blooming love story, each season weaves its own poetry into botanical form.”</p>", unsafe_allow_html=True)

    for season, items in SEASONAL_COLLECTIONS.items():
        st.markdown(f"<h2 style='text-align: center; margin: 2rem 0 1rem 0; font-size: 1.3rem; border-bottom: 1px solid #EFEAE6; padding-bottom: 0.4rem;'>{season}</h2>", unsafe_allow_html=True)
        cols = st.columns(len(items))
        for idx, (title, item) in enumerate(items.items()):
            with cols[idx]:
                st.image(item["image"], use_container_width=True)
                st.markdown(f"<h3 style='margin-top: 1rem; font-size: 1.1rem;'>{title}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 0.82rem; line-height: 1.5; color: #6E6762;'>{item['tagline']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 0.75rem; color: #8F857D; font-style: italic;'><strong>寓意：</strong>{item['meaning']}</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: #9E948C; margin-top: 0.6rem;'>Floral Stems</p>", unsafe_allow_html=True)
                for stem in item["stems"]:
                    st.markdown(f"<span style='font-size: 0.76rem; color: #3B3633;'>— {stem}</span><br>", unsafe_allow_html=True)
                st.write("")