import streamlit as st
from PIL import Image
from image_proccess import *
def main():
    st.set_page_config(page_title="Visiting Card Data Collection")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header("Visiting Card Info")
    st.divider()

    with st.sidebar:
        uploaded_front_image = st.file_uploader("Upload Front Image", accept_multiple_files=False, type=["jpg", "png", "jpeg"])
        uploaded_back_image = st.file_uploader("Upload Back Image", accept_multiple_files=False, type=["jpg", "png", "jpeg"])
        button = st.button("Process")

    if uploaded_front_image and uploaded_back_image:  # Check both images are uploaded
        try:
            front_image = Image.open(uploaded_front_image)
            back_image = Image.open(uploaded_back_image)

            if button:
                with st.sidebar:
                    st.divider()
                    st.image(front_image, caption="Front Side Of Card")
                    st.divider()
                    st.image(back_image, caption="Back Side Of card")
                    st.divider()
                process_image(uploaded_front_image,uploaded_back_image)

        except Exception as e:
            st.error(f"Error reading uploaded files: {e}")

    else:
        st.error(f"Please upload both front and back images of the visiting card.")

if __name__ == '__main__':
    main()
