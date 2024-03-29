# streamlit run c:/Users/Akash/Desktop/pROJECT bizcard/biz1.py

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
import psycopg2
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re

# set page config
st.set_page_config(page_title="BizCardX",
                   page_icon = '📇',
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This OCR app is created by *By Aakash.K*!"""})
st.markdown("<h1 style='text-align: center;text-decoration: underline; color: light green;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)

# set background 
def setting_bg():
    st.markdown(f""" 
    <style>
        .stApp {{
            background: linear-gradient(to right, #f0aa7f, #f09156);
            background-size: cover;
            transition: background 0.5s ease;
        }}
        h1,h2,h3,h4,h5,h6 {{
            color: #f3f3f3;
            font-family: 'Arial', 'sans-serif';
        }}
        .stTextInput>div>div>input {{
            color: #4e4376;
            background-color: #f3f3f3;
        }}
        .stButton>button:hover {{
            color: #f3f3f3;
            background-color: #2b5876;
        }}
        .stTextInput>div>div>input {{
            color: #4e4376;
            background-color: #f3f3f3;
        }}     
    </style>
    """,unsafe_allow_html=True) 
setting_bg()

# menu
selected = option_menu(None, ["Home","Upload & Extract","Modify"], 
                       icons=["house", "upload", "pencil"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "25px", "text-align": "centre", "margin": "0px", "--hover-color": "#8f8483", "transition": "color 0.3s ease, background-color 0.3s ease"},
                               "icon": {'color': 'green',"font-size": "25px"},
                               "container" : {"max-width": "4000px", "padding": "10px", "border-radius": "10px"},
                               "nav-link-selected": {"background-color": "#9c433d", "color": "white"}})



# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

# Establish a connection to PostgreSQL
conn = psycopg2.connect(
                dbname="BizCardX",
                user="postgres",
                password="yourPassword",
                host="localhost",
                port="5432"
            )
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card_data (
    id SERIAL PRIMARY KEY,
    company_name TEXT,
    card_holder TEXT,
    designation TEXT,
    mobile_number VARCHAR(50),
    email TEXT,
    website TEXT,
    area TEXT,
    city TEXT,
    state TEXT,
    pin_code VARCHAR(10),
    image BYTEA
);""")
conn.commit()

# HOME MENU
if selected == "Home":
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("##  In this streamlit web app you can upload an image of a business card and extract relevant information from it using 'easyOCR'. You can view, modify or delete the extracted data in this app. This app would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.")
    with col2:
        st.image(Image.open(r'C:\Users\Akash\Downloads\ocr1.jpeg'), width = 600)
        st.markdown(
            """
            <div style='text-align: center; font-style: italic; font-size: 18px; color: gray; margin-top: 20px;'>
                Tecchnologies used: Python, Pandas, Postgre SQL, psycopg2 connector-python, Streamlit, easy OCR and Plotly.
            </div>
            """,
            unsafe_allow_html=True
            )

# UPLOAD AND EXTRACT MENU
elif selected == "Upload & Extract":
    col1,col2,col3 = st.columns(3)
    col2.image(Image.open(r'C:\Users\Akash\Downloads\ocr2.jpeg'), width = 400)
    st.markdown("### Upload a Business Card")
    uploaded_card = st.file_uploader("Upload here",label_visibility="collapsed",type=["png","jpeg","jpg"])
        
    if uploaded_card is not None:
            
            def save_card(uploaded_card):
                with open((uploaded_card.name), "wb") as f:
                    f.write(uploaded_card.getbuffer())   
            save_card(uploaded_card)
            
            def image_preview(image,result): 
                for (bbox, text, prob) in result: 
                # unpack the bounding box
                    (tl, tr, br, bl) = bbox
                    tl = (int(tl[0]), int(tl[1]))
                    tr = (int(tr[0]), int(tr[1]))
                    br = (int(br[0]), int(br[1]))
                    bl = (int(bl[0]), int(bl[1]))
                            
                    # Draw a rectangle around the text
                    cv2.rectangle(image, tl, br, (0, 255, 0), 2)

                    # Put the extracted text onto the image
                    cv2.putText(image, text, (tl[0], tl[1] - 10),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)

                 # Configure the plot settings for displaying the image
                plt.rcParams['figure.figsize'] = (16,16)
                plt.axis('off')
                plt.imshow(image)
            
            # DISPLAYING THE UPLOADED CARD
            col1,col2 = st.columns(2,gap="large")
            with col1:                            
                st.markdown("### You have uploaded the card:")
                st.image(uploaded_card)
            # DISPLAYING THE CARD WITH HIGHLIGHTS
            with col2:                
                with st.spinner("Please wait processing image..."):
                    st.set_option('deprecation.showPyplotGlobalUse', False)
                    saved_img = os.getcwd()+ "\\" + uploaded_card.name
                    image = cv2.imread(saved_img)
                    result = reader.readtext(saved_img)
                    st.markdown("### Image Processed and Data Extracted:")
                    st.pyplot(image_preview(image,result))
            
            saved_img = os.getcwd() + "\\"+ uploaded_card.name
            final_result = reader.readtext(saved_img,detail = 0,paragraph=False)
            print(final_result)

            # convert img to binary & upload to sql 
            def img_to_binary(file):
                # Convert image data to binary format
                with open(file, 'rb') as f:
                    binaryData = f.read()
                return binaryData
            
            data = {"company_name" : [],
                    "card_holder" : [],
                    "designation" : [],
                    "mobile_number" :[],
                    "email" : [],
                    "website" : [],
                    "area" : [],
                    "city" : [],
                    "state" : [],
                    "pin_code" : [],
                    "image" : img_to_binary(saved_img)
                }

            def get_data(final_result):
                for ind,i in enumerate(final_result):

                    # To get website
                    if "www" in i.lower() or "www." in i.lower():
                        data["website"].append(i)
                    elif "WWW" in i:
                        data["website"] = result[4] +"." + result[5]

                    # To get email
                    elif "@" in i:
                        data["email"].append(i)

                    # To get mob
                    elif "-"in i or "+" in i:
                        data["mobile_number"].append(i)
                        if len(data["mobile_number"]) ==2:
                            data["mobile_number"] = " & ".join(data["mobile_number"])

                    # To get company name  
                    elif ind == len(final_result)-1:
                        data["company_name"].append(i)

                    # To get card holder
                    elif ind == 0:
                        data["card_holder"].append(i)

                    # To get designation
                    elif ind == 1:
                        data["designation"].append(i)

                    # To get Aarea
                    if re.findall('^[0-9].+, [a-zA-Z]+',i):
                        data["area"].append(i.split(',')[0])
                    elif re.findall('[0-9] [a-zA-Z]+',i):
                        data["area"].append(i)

                    # To get city name
                    match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                    match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                    match3 = re.findall('^[E].*',i)
                    if match1:
                        data["city"].append(match1[0])
                    elif match2:
                        data["city"].append(match2[0])
                    elif match3:
                        data["city"].append(match3[0])

                    # To get STATE
                    state_match = re.findall('[a-zA-Z]{9} +[0-9]',i)
                    if state_match:
                        data["state"].append(i[:9])
                    elif re.findall('^[0-9].+, ([a-zA-Z]+);',i):
                        data["state"].append(i.split()[-1])
                    if len(data["state"])== 2:
                        data["state"].pop(0)

                    # To get PINCODE        
                    if len(i)>=6 and i.isdigit():
                        data["pin_code"].append(i)
                    elif re.findall('[a-zA-Z]{9} +[0-9]',i):
                        data["pin_code"].append(i[10:])
                    else:
                        pass
            get_data(final_result)

            for key, value in data.items():
                print(f"Length of {key}: {len(value)}")

            #FUNCTION TO CREATE DATAFRAME
            def create_df(data):
                df = pd.DataFrame(data)
                return df
            df = create_df(data)
            st.success("#### Data Extracted")
            st.write(df)
        
            if st.button("Upload to Database"):
                for i, row in df.iterrows():
                    # Check if the data already exists in the database
                    cur.execute("SELECT id FROM card_data WHERE company_name = %s AND card_holder = %s", (row['company_name'], row['card_holder']))
                    existing_row = cur.fetchone()
                    if existing_row:
                        st.markdown(
                            "<div style='background-color: black; color: white; padding: 8px; border-radius: 5px;'>Duplicate data !!</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        # Insert new data if it doesn't exist
                        sql = """INSERT INTO card_data(company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, image)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                        cur.execute(sql, tuple(row))
                        conn.commit()
                        st.success("Uploaded to database successfully")


# MODIFY MENU    
elif selected == "Modify":
    col1,col2,col3 = st.columns([3,3,2])
    col2.markdown("## Alter or Delete the data here")
    column1,column2 = st.columns(2,gap="large")

    try:
        with column1:
            cur.execute("SELECT card_holder FROM card_data")
            result = cur.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to update", list(business_cards.keys()))
            st.markdown("#### Update or modify any data below")
            cur.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data WHERE card_holder=%s",
                            (selected_card,))
            result = cur.fetchone()

            # DISPLAYING ALL THE INFORMATIONS
            company_name = st.text_input("Company_Name", result[0])
            card_holder = st.text_input("Card_Holder", result[1])
            designation = st.text_input("Designation", result[2])
            mobile_number = st.text_input("Mobile_Number", result[3])
            email = st.text_input("Email", result[4])
            website = st.text_input("Website", result[5])
            area = st.text_input("Area", result[6])
            city = st.text_input("City", result[7])
            state = st.text_input("State", result[8])
            pin_code = st.text_input("Pin_Code", result[9])

            if st.button("Commit changes to DB"):
                # Update the information for the selected business card in the database
                cur.execute("""UPDATE card_data SET company_name=%s,card_holder=%s,designation=%s,mobile_number=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pin_code=%s
                                    WHERE card_holder=%s""", (company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,selected_card))
                conn.commit()
                st.success("Information updated in database successfully.")

        with column2:
            cur.execute("SELECT card_holder FROM card_data")
            result = cur.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to Delete", list(business_cards.keys()))
            st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
            st.write("#### Proceed to delete this card?")

            if st.button("Yes, Delete !"):
                with st.spinner("Please wait deleting Bussiness Card..."):
                    cur.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
                    conn.commit()
                    st.success("Business card information deleted from database.")
    except:
        st.warning("There is no data available in the database")
    
    if st.button("View updated data"):
        cur.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        updated_df = pd.DataFrame(cur.fetchall(),columns=["Company_Name","Card_Holder","Designation","Mobile_Number","Email","Website","Area","City","State","Pin_Code"])
        st.write(updated_df)
