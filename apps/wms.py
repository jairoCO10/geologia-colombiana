import ast
import streamlit as st
import leafmap.foliumap as leafmap
from PIL import Image
import io


@st.cache
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


def app():
    
    width = 1200
    height = 850
    layers = None

    col1, col2 = st.columns(2)
    with col1:
        esa_landcover = "https://services.terrascope.be/wms/v2"
        url= "http://srvags.sgc.gov.co/arcgis/services/Atlas_Geologico_2015/Atlas_Geologico_Colombiano_2015/MapServer/WMSServer?"
       

    with col2:
        
        empty = st.sidebar.empty()
        if url:
            options = get_layers(url)
            
            default = None
            if url == esa_landcover:
                default = "WORLDCOVER_2020_MAP"
            layers = empty.multiselect(
                "Select WMS layers to add to the map:", options, default=default
            )
            # add_legend = st.checkbox("Add a legend to the map", value=False)
        # if default == "WORLDCOVER_2020_MAP":
        #     legend = str(leafmap.builtin_legends["ESA_WorldCover"])
        # else:
        #     legend = ""
        # if add_legend:
        #     legend_text = st.text_area(
        #         "Enter a legend as a dictionary {label: color}",
        #         value=legend,
        #         height=200,
        #     )

       
    m = leafmap.Map(center=(4.6482837, -74.247892), zoom=6, locate_control=True, plugin_LatLngPopup=True, print= True)

    if layers is not None:
        for layer in layers:
            m.add_wms_layer(
                url, layers=layer, name=layer, attribution=" ", transparent=True
            )
        # if add_legend and legend_text:
        #     legend_dict = ast.literal_eval(legend_text)
        #     m.add_legend(legend_dict=legend_dict)
        
    m.to_streamlit(width, height)
        #st.download_button("hola", m.save("filename.png"))
    st.sidebar.button("Imprimir", m.save("filename.png",))
    st.sidebar.write("la opcion 0 muestra por defecto el mapa geologico de Colombia")
        # def get_image_download_link(img,filename,text):
        #     buffered = BytesIO()
        #     m.save(buffered, format="JPEG")
        #     img_str = base64.b64encode(buffered.getvalue()).decode()
        #     href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
        #     return href
        # result = Image.fromarray(m)
        # st.markdown(get_image_download_link(result, img_file.name,'Download '+img_file.name), unsafe_allow_html=True)
        