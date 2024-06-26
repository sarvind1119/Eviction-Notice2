import os
import streamlit as st
import google.generativeai as genai
import pdfkit

# Configure the Google Generative AI SDK
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the model
generation_config = {
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Act as an expert lawyer who specialises in sending out eviction notices to tenants. Following is the format which has to be sent to the tenants. Take the inputs from the user about the details. The inputs from user are enclosed in \"[]\" square brackets. Use the template below and make a custom notice:\n\n\"\"\"\n[Your Name]\n\n[Your Address]\n\n[City, State, ZIP Code]\n\n[Email Address]\n\n[Phone Number]\n\n[Date]\n\n[Tenant]\n\n[Tenant’s Name]\n\n[Tenant’s Address]\n\n[City, State, ZIP Code]\n\nSubject: Eviction Notice\n\nDear [Tenant’s Name],\n\nI hope this letter finds you well. I am writing to officially notify you that your tenancy at [Tenant’s Address] is terminated by the terms of our lease agreement dated [Date of Lease Agreement].\n\nThe grounds for eviction are [Specify grounds, e.g., non-payment of rent, breach of terms, etc.]. As per Section X of the Rent Control Act [mention relevant Act], these grounds warrant termination of the tenancy.\n\nNotice Period: You are hereby given [X] days’ notice to vacate the premises, as required by Section Y of the Rent Control Act. The notice period starts from the date of receipt of this letter.\n\nRent Arrears: Please be advised that the outstanding rent amount of [Specify amount] for the period [Specify period] is due and must be settled before the end of the notice period to avoid further legal action.\n\nProperty Inspection: Prior to vacating the premises, a joint inspection of the property will be conducted on [Specify Date and Time] to assess any damages. Your presence is requested during this inspection.\n\nReturn of Keys: Kindly return all keys, access cards, or any other property belonging to the premises on or before the date of vacating.\n\nFailure to Comply: Failure to vacate the premises within the stipulated notice period will result in legal action, including but not limited to court proceedings for eviction.\n\nShould you have any concerns or queries regarding this notice, please feel free to contact me at [Your Phone Number] or [Your Email Address].\n\nThank you for your understanding and cooperation in this matter.\n\nSincerely,\n\n[Your Full Name]\n\n[Your Signature]\n\n\"\"\"\n",
)

# Streamlit app
st.title("Eviction Notice Generator")

st.header("Enter the following details:")

your_name = st.text_input("Your Name")
your_address = st.text_input("Your Address")
city_state_zip = st.text_input("City, State, ZIP Code")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
date = st.date_input("Date")
tenant_name = st.text_input("Tenant’s Name")
tenant_address = st.text_input("Tenant’s Address")
tenant_city_state_zip = st.text_input("City, State, ZIP Code (Tenant)")
date_of_lease = st.date_input("Date of Lease Agreement")
grounds_for_eviction = st.text_area("Grounds for Eviction")
notice_period = st.number_input("Notice Period (days)", min_value=1)
outstanding_rent = st.text_input("Outstanding Rent Amount")
rent_period = st.text_input("Rent Period")
inspection_date_time = st.text_input("Property Inspection Date and Time")
return_keys_date = st.text_input("Return of Keys Date")
your_full_name = st.text_input("Your Full Name")
your_signature = st.text_input("Your Signature")

if st.button("Generate Eviction Notice"):
    # Form the input string
    input_text = f"""
[Your Name]
{your_name}

[Your Address]
{your_address}

[City, State, ZIP Code]
{city_state_zip}

[Email Address]
{email}

[Phone Number]
{phone}

[Date]
{date}

[Tenant]
[Tenant’s Name]
{tenant_name}

[Tenant’s Address]
{tenant_address}

[City, State, ZIP Code]
{tenant_city_state_zip}

Subject: Eviction Notice

Dear {tenant_name},

I hope this letter finds you well. I am writing to officially notify you that your tenancy at {tenant_address} is terminated by the terms of our lease agreement dated {date_of_lease}.

The grounds for eviction are {grounds_for_eviction}. As per Section X of the Rent Control Act [mention relevant Act], these grounds warrant termination of the tenancy.

Notice Period: You are hereby given {notice_period} days’ notice to vacate the premises, as required by Section Y of the Rent Control Act. The notice period starts from the date of receipt of this letter.

Rent Arrears: Please be advised that the outstanding rent amount of {outstanding_rent} for the period {rent_period} is due and must be settled before the end of the notice period to avoid further legal action.

Property Inspection: Prior to vacating the premises, a joint inspection of the property will be conducted on {inspection_date_time} to assess any damages. Your presence is requested during this inspection.

Return of Keys: Kindly return all keys, access cards, or any other property belonging to the premises on or before {return_keys_date}.

Failure to Comply: Failure to vacate the premises within the stipulated notice period will result in legal action, including but not limited to court proceedings for eviction.

Should you have any concerns or queries regarding this notice, please feel free to contact me at {phone} or {email}.

Thank you for your understanding and cooperation in this matter.

Sincerely,

{your_full_name}

{your_signature}
"""

    # Create chat session and send the message
    chat_session = model.start_chat(
        history=[]
    )

    response = chat_session.send_message(input_text)

    # Format the output with a letterhead and the required styling
    letterhead_html = f"""
    <div style="text-align: right;">
        <strong style="color: black;">xyz</strong><strong style="color: red;"> lawfirm</strong>
    </div>
    <h2 style="text-align: center;">Eviction Notice</h2>
    <pre>{response.text}</pre>
    """

    # Save the HTML content to a file
    with open("eviction_notice.html", "w") as file:
        file.write(letterhead_html)

    # Convert the HTML file to a PDF
    pdfkit.from_file("eviction_notice.html", "eviction_notice.pdf")

    # Display the response
    st.subheader("Generated Eviction Notice")
    st.markdown(letterhead_html, unsafe_allow_html=True)

    # Provide a link to download the PDF
    st.download_button(
        label="Download Eviction Notice as PDF",
        data=open("eviction_notice.pdf", "rb").read(),
        file_name="eviction_notice.pdf",
        mime="application/pdf"
    )
