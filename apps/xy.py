import leafmap.foliumap as leafmap
import pandas as pd
import streamlit as st

@st.cache
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options



def app():

    st.title("Add Points from XY")
    width = 1000
    height = 600
    sample_url = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/world_cities.csv"
    url = st.sidebar.text_input("Enter URL:", sample_url)
    m = leafmap.Map(locate_control=True, plugin_LatLngPopup=True)

    row1_col1, row1_col2 = st.columns([3, 1.3])
    esa_landcover = "http://srvags.sgc.gov.co/arcgis/services/Atlas_Geologico_Colombiano/Atlas_Geologico_Colombia/MapServer/WMSServer?"
    urls = st.text_input("Enter a WMS URL:", value="https://services.terrascope.be/wms/v2")
    empty = st.empty()
    
    if url:
        options = get_layers(url)

        default = None
        if url == esa_landcover:
            default = "WORLDCOVER_2020_MAP"
        layers = empty.multiselect(
            "Select WMS layers to add to the map:", options, default=default
        )
        add_legend = st.checkbox("Add a legend to the map", value=True)
        if default == "WORLDCOVER_2020_MAP":
            legend = str(leafmap.builtin_legends["ESA_WorldCover"])
        else:
            legend = ""
        if add_legend:
            legend_text = st.text_area(
                "Enter a legend as a dictionary {label: color}",
                value=legend,
                height=200,
            )

    empty = st.empty()
    
        

    with row1_col1:
        if url:
            try:
                df = pd.read_csv(url)

                columns = df.columns.values.tolist()
               

                lon_index = 0
                lat_index = 0

            # for col in columns:
            #     if col.lower() in ["lon", "longitude", "long", "lng"]:
            #         lon_index = columns.index(col)
            #     elif col.lower() in ["lat", "latitude"]:
            #         lat_index = columns.index(col)

            # with row1_col1:
            #     x = st.selectbox("Select longitude column", columns, lon_index)

            # with row1_col2:
            #     y = st.selectbox("Select latitude column", columns, lat_index)

            # with row1_col3:
            #     popups = st.multiselect("Select popup columns", columns, columns)

            # with row1_col4:
            #     heatmap = st.checkbox("Add heatmap")

            # if heatmap:
            #     with row1_col5:
            #         if "pop_max" in columns:
            #             index = columns.index("pop_max")
            #         else:
            #             index = 0
            #         heatmap_col = st.selectbox("Select heatmap column", columns, index)
            #         try:
            #             m.add_heatmap(df, y, x, heatmap_col)
            #         except:
            #             st.error("Please select a numeric column")

            # try:
            #     m.add_points_from_xy(df, x, y, popups)
            # except:
            #     st.error("Please select a numeric column")

            except Exception as e:
                st.error(e)

    m.to_streamlit(width, height)