import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


st.set_page_config(layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<h1 style="
    padding-top: 5px;
">
</h1>
""", unsafe_allow_html=True)





col_1, col_2 = st.columns(2)

with col_1:
    st.title("Image Classification")

# load model
    model = load_model("model.h5")

    picture = st.camera_input("Ambil Foto")

    if picture is not None:

        # buka dengan PIL
        img = Image.open(picture)

        # convert RGB
        img = img.convert("RGB")

        # resize sesuai input model
        img_resized = img.resize((224, 224), Image.LANCZOS)

        # numpy array
        img_array = np.array(img_resized)

        # tambah batch dimension
        img_array = np.expand_dims(img_array, axis=0)



        c1, c2, c3 = st.columns([1, 2, 1])

        with c2:

            predict = st.button("Predict")

            if predict:

                prediction = model.predict(img_array)

                class_id = np.argmax(prediction)
                confidence = np.max(prediction)

                st.session_state["prediction"] = prediction

                if confidence >= 0.75:
                    st.session_state["predicted_class"] = class_id
                else:
                    st.session_state.pop("predicted_class", None)


                if confidence < 0.75:
                    st.error("Bukan E-Waste")

                else:
                    # label class id
                    if class_id == 0 :
                        st.write('camera')
                    elif class_id ==1 :
                        st.write('crt')
                    elif class_id ==2 :
                        st.write('handphone')
                    elif class_id ==3 :
                        st.write('keyboard')
                    elif class_id ==4 :
                        st.write('kulkas')
                    elif class_id ==5 :
                        st.write('laptop')
                    elif class_id ==6 :
                        st.write('mesin cuci')
                    elif class_id ==7 :
                        st.write('microwave')
                    elif class_id ==8 :
                        st.write('mouse')
                    elif class_id ==9 :
                        st.write('printer')
                    elif class_id ==10 :
                        st.write('pv panel')
                    elif class_id ==11 :
                        st.write('smartwatch')
                    elif class_id ==12 :
                        st.write('monitor flat')

                    st.write("Confidence:", float(confidence))


with col_2:
    import pandas as pd
    import plotly.express as px

    if "prediction" in st.session_state:

        prediction = st.session_state["prediction"]

        class_names = [
            "camera",
            "crt",
            "handphone",
            "keyboard",
            "kulkas",
            "laptop",
            "mesin cuci",
            "microwave",
            "mouse",
            "printer",
            "pv panel",
            "smartwatch",
            "monitor flat"
        ]

        scores = prediction[0] * 100

        df = pd.DataFrame({
            "Class": class_names,
            "Confidence": scores
        })


        df = df.sort_values(by="Confidence", ascending=True)

        fig = px.bar(
            df,
            x="Confidence",
            y="Class",
            orientation="h",
            text="Confidence",
            title="Confidence Score Tiap Class"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Confidence (%)",
            yaxis_title="",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)



# Lokasi Terdekat E-Waste
from geopy.distance import geodesic
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from geopy.geocoders import Nominatim

location = streamlit_geolocation()

if location and location.get("latitude") and location.get("longitude"):

    lat = location["latitude"]
    lon = location["longitude"]

    st.write("Latitude:", lat)
    st.write("Longitude:", lon)

    address = Nominatim(
        user_agent="streamlit-app"
    ).reverse(f"{lat}, {lon}")

    st.write(address.address)

    

    # =====================
    # DATA LOKASI
    # =====================

    lokasi = {
        "ewaste_kecil": {
            "Dropbox Kantor Kelurahan Klitren": (-7.7835717, 110.3788353),
            "Dropbox Dinas Lingkungan Hidup Kota Yogyakarta": (-7.7867645, 110.3805689),
            "Dropbox Kantor Kemantren Danurejan": (-7.7942445, 110.3730066),
            "Dropbox Kantor Kemantren Jetis": (-7.7832220, 110.3625423),
        },
        "ewaste_besar": {
            "Rekosistem": (-7.7832240, 110.3744867)
        },
        "laptop_bekas": {
            "Laptop Bekas": (-7.7869527, 110.3874332)
        }
    }

    # =====================
    # MAPPING BARANG
    # =====================

    kategori_barang = {
        "camera": ["ewaste_kecil"],
        "handphone": ["ewaste_kecil"],
        "mouse": ["ewaste_kecil"],
        "smartwatch": ["ewaste_kecil"],

        "laptop": ["laptop_bekas", "ewaste_besar"],

        "crt": ["ewaste_besar"],
        "keyboard": ["ewaste_besar"],
        "kulkas": ["ewaste_besar"],
        "mesin cuci": ["ewaste_besar"],
        "microwave": ["ewaste_besar"],
        "printer": ["ewaste_besar"],
        "monitor flat": ["ewaste_besar"],
    }

    class_names = [
        "camera","crt","handphone","keyboard",
        "kulkas","laptop","mesin cuci","microwave",
        "mouse","printer","pv panel","smartwatch",
        "monitor flat"
    ]

    if "predicted_class" in st.session_state:

        barang = class_names[
            st.session_state["predicted_class"]
        ]

        st.subheader("♻️ Lokasi E-Waste")

        if barang == "pv panel":
            st.warning("Lokasi PV Panel belum tersedia.")

        else:

            user_location = (lat, lon)

            ditemukan = False
            
            if barang not in kategori_barang:
                st.warning("⚠️ Lokasi tidak ditemukan untuk kategori barang ini.")
            else:
                for kategori in kategori_barang.get(barang, []):

                    for nama, koordinat in lokasi[kategori].items():

                        jarak = geodesic(
                            user_location,
                            koordinat
                        ).km

                        if jarak <= 2:

                            tujuan_lat, tujuan_lon = koordinat

                            url = (
                                f"https://www.google.com/maps/dir/"
                                f"{lat},{lon}/"
                                f"{tujuan_lat},{tujuan_lon}"
                            )

                            st.success(
                                f"{nama} ({jarak:.2f} km)"
                            )

                            # Informasi tambahan berdasarkan kategori
                            if kategori == "ewaste_kecil":

                                st.info("""
                        Jam Operasional : 24 Jam
                                """)

                            elif kategori == "ewaste_besar":

                                st.info("""
                        Jam Operasional : Senin - Jumat
                        08:00 - 17:00 WIB

                        Kontak : xxxx
                                """)

                            elif kategori == "laptop_bekas":

                                st.info("""
                        Jam Operasional : Unknown
                        Kontak : Unknown
                                """)

                            st.markdown(
                                f"🗺️ [Map]({url})"
                            )

                            st.divider()

                            ditemukan = True

                if not ditemukan:
                    st.warning(
                        "Tidak ada lokasi dalam radius 2 km."
                    )

else:

    st.warning(
        "📍 GPS belum aktif atau izin lokasi belum diberikan."
    )