import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(page_title="Outfit Recommendation", layout="wide")
st.title("Content-Based Outfit Recommendation (Gender Aware)")

# -----------------------------
# 1. Genre & Color Definitions
# -----------------------------

GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]

COLOR_RGB = {
    "Black": (30, 30, 30), "White": (240, 240, 240), "Gray": (160, 160, 160),
    "Navy": (40, 60, 100), "Brown": (120, 80, 50), "Beige": (210, 200, 170),
    "Green": (60, 120, 80), "Red": (160, 50, 50)
}

# -----------------------------
# 2. User Input
# -----------------------------

st.header("1️⃣ Basic Information")
# 性別の選択を追加
gender = st.radio("Select Gender", ["Men", "Women", "Unisex"], horizontal=True)

st.header("2️⃣ Rate Your Style Preference (0–5)")
genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.header("3️⃣ Rate Your Color Preference (0–5)")
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}

# -----------------------------
# 3. Content-Based Completion
# -----------------------------

def complete_scores(scores: dict):
    avg = sum(scores.values()) / len(scores) if sum(scores.values()) > 0 else 2.5
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# -----------------------------
# 4. Outfit Library (Gender Specific Items)
# -----------------------------

# 性別ごとにアイテムを定義
OUTFIT_LIBRARY = {
    "Men": {
        "Streetwear": {"inner": ["Graphic Tee"], "outer": ["Hoodie"], "bottom": ["Cargo Pants"]},
        "Casual": {"inner": ["Oxford Shirt"], "outer": ["Cardigan"], "bottom": ["Chinos"]},
        "Formal": {"inner": ["Dress Shirt"], "outer": ["Blazer"], "bottom": ["Slacks"]},
    },
    "Women": {
        "Streetwear": {"inner": ["Crop Top"], "outer": ["Oversized Hoodie"], "bottom": ["Wide Cargo"]},
        "Casual": {"inner": ["Blouse"], "outer": ["Knit Cardigan"], "bottom": ["Skirt", "Tapered Pants"]},
        "Formal": {"inner": ["Silk Top"], "outer": ["Tailored Jacket"], "bottom": ["Pencil Skirt", "Slacks"]},
    }
}

# Unisex用のフォールバック（デフォルト）
DEFAULT_LIBRARY = {
    "inner": ["T-Shirt"], "outer": ["Jacket"], "bottom": ["Pants"]
}

def get_parts(genre, gender):
    # 性別専用のライブラリがあれば取得、なければデフォルト
    lib = OUTFIT_LIBRARY.get(gender, OUTFIT_LIBRARY["Men"]) # Default to Men if not found
    return lib.get(genre, OUTFIT_LIBRARY["Men"]["Casual"])

# -----------------------------
# 5. Outfit Generator
# -----------------------------

def generate_outfit(genre, color, gender):
    parts = get_parts(genre, gender)
    return {
        "Genre": genre,
        "Gender": gender,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}",
        "Bottom": f"{color} {random.choice(parts['bottom'])}"
    }

# -----------------------------
# 6. Image Generator (Gender Silhouette)
# -----------------------------

def generate_image(outfit):
    base_color = COLOR_RGB[outfit["Color Theme"]]
    gender_type = outfit["Gender"]

    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    skin = (220, 200, 180)
    shadow = tuple(max(0, c - 30) for c in base_color)
    inner_color = tuple(min(255, c + 35) for c in base_color)
    bottom_color = tuple(max(0, c - 50) for c in base_color)

    # Head & Neck
    d.ellipse([105, 20, 155, 70], fill=skin, outline="black")
    d.rectangle([120, 70, 140, 95], fill=skin)

    # Shoulder Width Adjustment based on gender
    sw = 20 if gender_type == "Women" else 0 # Shoulder width offset

    # Outer (Silhouette change)
    d.polygon(
        [(70 + sw, 100), (190 - sw, 100), (215, 270), (45, 270)],
        fill=base_color, outline="black"
    )

    # Inner
    d.rectangle([95, 120, 165, 250], fill=inner_color, outline="black")

    # Bottom (Skirt vs Pants logic)
    if "Skirt" in outfit["Bottom"]:
        # Draw Skirt
        d.polygon([(90, 270), (170, 270), (200, 380), (60, 380)], fill=bottom_color, outline="black")
    else:
        # Draw Legs (Pants)
        d.rectangle([95, 270, 125, 400], fill=bottom_color, outline="black")
        d.rectangle([135, 270, 165, 400], fill=bottom_color, outline="black")

    # Shoes
    d.rectangle([90, 400, 130, 420], fill=(40, 40, 40))
    d.rectangle([130, 400, 170, 420], fill=(40, 40, 40))

    return img

# -----------------------------
# 7. Recommendation Engine
# -----------------------------

st.header("👕 Recommended Outfits")

used_colors = []
for i, genre in enumerate(top_genres):
    color = random.choice([c for c in top_colors if c not in used_colors]) if len(used_colors) < len(top_colors) else random.choice(top_colors)
    used_colors.append(color)

    outfit = generate_outfit(genre, color, gender)
    img = generate_image(outfit)

    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.image(img, caption=f"{gender}'s {genre}")
    with col2:
        st.subheader(f"Outfit {i+1}")
        st.write(f"**Gender Style:** {outfit['Gender']}")
        st.write(f"**Genre:** {outfit['Genre']}")
        st.write(f"👕 Inner: {outfit['Inner']}")
        st.write(f"🧥 Outer: {outfit['Outer']}")
        st.write(f"👖 Bottom: {outfit['Bottom']}")
