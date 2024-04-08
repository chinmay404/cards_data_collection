import streamlit as st
from PIL import Image
from image_proccess import *
from tempfile import NamedTemporaryFile
def main():
    temp_dir = "temp_files"  # You can customize this directory name
    os.makedirs(temp_dir, exist_ok=True)
    front_image_path = os.path.join(temp_dir, "temp_front_image.jpg")
    back_image_path = os.path.join(temp_dir, "temp_back_image.jpg")
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
            if button:
                with st.sidebar:
                    st.divider()
                    # Create temporary files for uploaded images # Get temporary file path
                    with open(front_image_path, "wb") as temp_front_image:
                        temp_front_image.write(uploaded_front_image.read())

                    with open(back_image_path, "wb") as temp_back_image:
                        temp_back_image.write(uploaded_back_image.read())
                    # Display uploaded images (optional)
                    st.divider()
                    st.image(Image.open(uploaded_front_image), caption="Front Side Of Card")
                    st.write(front_image_path)
                    st.divider()
                    st.image(Image.open(uploaded_back_image), caption="Back Side Of card")
                    st.write(back_image_path)
                    st.divider()
                try:
                    results = process_image(front_image_path, back_image_path)
                    st.write(results)
                    try:
                        st.subheader("Extracted Information:")
                        res_path = os.path.join(temp_dir, 'res.json')
                        with open(res_path, "r") as res:
                            data = json.load(res) 
                        if isinstance(data, dict):
                            for key, value in data.items():
                                st.write(f"- {key.title()}: {value}")
                        else:
                            st.error("Invalid JSON data: Expected a dictionary.")

                    except Exception as e:
                        st.error(f"DISPLAY: {e}")
                except Exception as e:
                    st.error(f"Exception: {e}")

        except Exception as e:
            st.error(f"Error reading uploaded files: {e}")

    else:
        st.error(f"Please upload both front and back images of the visiting card.")

if __name__ == '__main__':
    main()
