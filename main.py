import streamlit as st
from PIL import Image
from image_proccess import *
from tempfile import NamedTemporaryFile
from wite_db import write_to_db as wdb
from wite_db import fetch_data





# @st.cache_data
# def initialize_session_state():
#   if "conversation" not in st.session_state:
#     st.session_state.conversation = None
#   return st.session_state



def main():
    # st.session_state = initialize_session_state()
    temp_dir = "temp_files" 
    os.makedirs(temp_dir, exist_ok=True)
    front_image_path = os.path.join(temp_dir, "temp_front_image.jpg")
    back_image_path = os.path.join(temp_dir, "temp_back_image.jpg")
    st.set_page_config(page_title="Visiting Card Data Collection")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header("Visiting Card Info")
    st.divider()
    
    
    fetched_data = None
    with st.sidebar:
        api_key = st.text_input("Enter your API key:", type="password") 
        uploaded_front_image = st.file_uploader("Upload Front Image", accept_multiple_files=False, type=["jpg", "png", "jpeg"]) or None
        uploaded_back_image = st.file_uploader("Upload Back Image (Optional)", accept_multiple_files=False, type=["jpg", "png", "jpeg"]) or None
        button = st.button("Process")
        on = st.toggle('Show reposne')
        if st.button("Show Database Entries"):
            fetched_data = fetch_data()
    if fetched_data:
        st.subheader("Data from Database:")
        st.dataframe(fetched_data)


    if uploaded_front_image or uploaded_back_image:  
        try:
            if button:
                with st.sidebar:
                    st.divider()
                    if uploaded_front_image:
                        with open(front_image_path, "wb") as temp_front_image:
                            temp_front_image.write(uploaded_front_image.read())
                    if uploaded_back_image:
                        with open(back_image_path, "wb") as temp_back_image:
                            temp_back_image.write(uploaded_back_image.read())

                    st.divider()
                    if uploaded_front_image:
                        st.image(Image.open(uploaded_front_image), caption="Front Side Of Card")
                        st.write(front_image_path)
                        st.divider()
                    if uploaded_back_image:
                        st.image(Image.open(uploaded_back_image), caption="Back Side Of card")
                        st.write(back_image_path)
                    st.divider()
                try:
                    if uploaded_front_image and uploaded_back_image:
                        results = process_image(front_image_path, back_image_path,api_key)
                    elif uploaded_front_image:
                        st.warning("Limited information available. Backside can provide additional details.")
                        results = process_image_one_side_only(front_image_path,api_key) 
                    elif uploaded_back_image:
                        st.warning("Limited information available. Frontside might contain crucial details.")
                        results = process_image_one_side_only(back_image_path,api_key)
                    try:
                        if on:
                            st.write(results)
                        st.subheader("Extracted Information:")
                        res_path = os.path.join(temp_dir, 'res.json')
                        with open(res_path, "r") as res:
                            data = json.load(res) 
                        if isinstance(data, dict):
                            for key, value in data.items():
                                edited_value = st.text_input(f"{key.title()}:", value)
                                data[key] = edited_value
                            save_button = st.button("Save to Database")
                            # csv = convert_to_csv(data)
                            # st.download_button(
                            #         label="Download data as CSV",
                            #         data=csv,
                            #         file_name='card_info.csv',
                            #         mime='text/csv',
                            #     )
                            if save_button:
                                try:
                                    write_to_db(data)
                                except Exception as e:
                                    st.error(f"Database error: {e}")
                        else:
                            st.error("Invalid JSON data: Expected a dictionary.")

                    except Exception as e:
                        st.error(f"DISPLAY: {e}")
                except Exception as e:
                    st.error(f"Exception: {e}")

        except Exception as e:
            st.error(f"Error reading uploaded files: {e}")

    else:
        st.subheader("Add Gemini API Key")
        st.markdown('Adding Feature to \n1 . export data to csv \n2 . make API call \n3 . Bulk Upload for cards.')
        st.error(f"Please upload both front and back images of the visiting card.")

def write_to_db(data):
    try:
        with open('config.json') as f:
            config = json.load(f)

        conn = psycopg2.connect(**config['database'])
        cur = conn.cursor()
        sql = f"""INSERT INTO {config['table']['name']} (
            name, company_name, job_title, website, email, phone_number,
            office_phone_number, address, additional_info
        ) VALUES (
            %(name)s, %(company_name)s, %(job_title)s, %(website)s, %(email)s, %(phone_number)s,
            %(office_phone_number)s, %(address)s, %(additional_info)s
        )"""
        cur.execute(sql, data)
        conn.commit()
        

    except Exception as e:
        st.error(f"Databse error : {e}")
        print("Error:", e)

    finally:
        st.success('Added To database succesfully', icon="✅")
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()




if __name__ == '__main__':
    main()
