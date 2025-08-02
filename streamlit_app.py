import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

# Function to detect obstacles
def find_obstacles(points):
    obstacles = []
    for x, y, z in points:
        distance = math.sqrt(x**2 + y**2)
        if distance < 10:
            obstacles.append((x, y, z))
    return obstacles

# UI Title
st.title("🚗 LIDAR Obstacle Detection")
st.markdown("Upload a CSV file with LIDAR point data in this format: `x,y,z`")

# File uploader
uploaded_file = st.file_uploader("Upload your LIDAR CSV file", type="csv")

# If file is uploaded
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, header=None, names=["x", "y", "z"])
    points = list(df.itertuples(index=False, name=None))

    obstacles = find_obstacles(points)

    st.success(f"✅ Detected {len(obstacles)} obstacle(s) within 10 meters.")
    st.write("### 📍 Obstacle Points")
    st.dataframe(obstacles)

    # Visualization
    x_all = df['x']
    y_all = df['y']
    x_obs = [x for x, y, z in obstacles]
    y_obs = [y for x, y, z in obstacles]

    fig, ax = plt.subplots()
    ax.scatter(x_all, y_all, color='gray', label='All Points')
    ax.scatter(x_obs, y_obs, color='red', label='Obstacles')
    ax.add_patch(plt.Circle((0, 0), 10, fill=False, linestyle='--', edgecolor='blue', label='10m Range'))
    ax.scatter(0, 0, color='blue', label='Robot Origin')
    ax.set_aspect('equal')
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    st.pyplot(fig)
