# BizCardX-Extracting-Business-Card-Data-with-OCR
The BizCardX project is a Streamlit-based OCR (Optical Character Recognition) application designed to extract information from uploaded business card images. It employs Python libraries such as easyOCR, Pandas, Psycopg2 for PostgreSQL integration, and matplotlib for image visualization.
The app aims to facilitate the extraction, storage, and management of business card data in a database.

1. Streamlit Setup and UI Customization:
Configures Streamlit's page layout, background, and menu items.
Provides a user-friendly interface using HTML/CSS for styling.

2. Option Menu and Database Initialization:
Creates an option menu with different functionalities: Home, Upload & Extract, Modify.
Initializes a PostgreSQL database named "BizCardX" and sets up a table called "card_data" to store extracted business card information.

3. Upload & Extract Functionality:
Allows users to upload business card images and displays them.
Processes the uploaded image using easyOCR to extract text.
Converts the image to binary format for storage in the database.
Parses the extracted text to categorize and store information like company name, cardholder, contact details, etc., in a DataFrame.
Provides an option to upload the extracted data to the database and prevents duplicate entries.

4. Modify Functionality:
Enables users to modify or delete existing entries in the database.
Displays the extracted data and allows users to edit specific fields.
Offers the ability to delete a selected business card entry from the database.
Provides an option to view the updated data in the database.

5. Overall Functionality:
Implements error handling for database interactions and UI components.
Displays visual elements like images and interactive widgets using Streamlit.
Offers a comprehensive user interface for managing business card data.
