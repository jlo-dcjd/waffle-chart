import streamlit as st
import base64
import random

def generate_waffle_chart(width, height, categories, colors, percentages):
    total_tiles = width * height
    tiles = []
    
    for category, color, percentage in zip(categories, colors, percentages):
        tiles_to_fill = int(total_tiles * percentage / 100)
        tiles.extend([f'<div class="tile" style="background-color: {color};" title="{category}: {percentage}%"></div>'] * tiles_to_fill)
    
    # Fill remaining tiles if any
    remaining_tiles = total_tiles - len(tiles)
    tiles.extend(['<div class="tile" style="background-color: #eee;"></div>'] * remaining_tiles)

    html = f"""
    <div class="waffle-chart" style="display: grid; grid-template-columns: repeat({width}, 1fr); gap: 2px; width: {width * 30}px;">
        {''.join(tiles)}
    </div>
    <style>
        .tile {{
            width: 30px;
            height: 30px;
        }}
    </style>
    """
    return html

def main():
    st.title("Waffle Chart Generator")

    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("Width of the waffle chart", min_value=1, value=10)
    with col2:
        height = st.number_input("Height of the waffle chart", min_value=1, value=10)

    num_categories = st.number_input("Number of categories", min_value=1, max_value=10, value=3)

    categories = []
    colors = []
    percentages = []

    for i in range(num_categories):
        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.text_input(f"Category {i+1} name", value=f"Category {i+1}")
        with col2:
            color = st.color_picker(f"Color for category {i+1}", value="#1E3CC9")
        with col3:
            percentage = st.number_input(f"Percentage for category {i+1}", min_value=0.0, max_value=100.0, value=100.0 / num_categories)
        
        categories.append(category)
        colors.append(color)
        percentages.append(percentage)

    if st.button("Generate Waffle Chart"):
        if sum(percentages) != 100:
            st.error("The sum of percentages must equal 100%")
        else:
            html_chart = generate_waffle_chart(width, height, categories, colors, percentages)
            st.components.v1.html(html_chart, height=(height * 32), width=(width * 32))

            # Generate a legend
            legend_html = "<div style='margin-top: 20px;'>"
            for category, color, percentage in zip(categories, colors, percentages):
                legend_html += f"<div style='display: flex; align-items: center; margin-bottom: 5px;'>"
                legend_html += f"<div style='width: 20px; height: 20px; background-color: {color}; margin-right: 10px;'></div>"
                legend_html += f"<span>{category}: {percentage}%</span>"
                legend_html += "</div>"
            legend_html += "</div>"
            st.components.v1.html(legend_html)

            # Provide download link for the HTML
            html_file = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Waffle Chart</title>
            </head>
            <body>
                {html_chart}
                {legend_html}
            </body>
            </html>
            """
            b64 = base64.b64encode(html_file.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="waffle_chart.html">Download Waffle Chart HTML</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
