import streamlit as st
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import threading

# Email configuration
def send_email(recipient, subject, body, sender_email, sender_password):
    try:
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject

        # Add body to email
        message.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

# Function to run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# Streamlit app
st.title("Email Scheduler")

# Email configuration inputs
sender_email = st.text_input("Sender Email (Gmail)")
sender_password = st.text_input("Email Password", type="password")
recipient = st.text_input("Recipient Email")
subject = st.text_input("Email Subject")
body = st.text_area("Email Body")

# Schedule settings
schedule_date = st.date_input("Select Date")
schedule_time = st.time_input("Select Time")

if st.button("Schedule Email"):
    if sender_email and sender_password and recipient and subject and body:
        # Combine date and time
        schedule_datetime = datetime.combine(schedule_date, schedule_time)
        
        # Schedule the email
        def scheduled_job():
            success = send_email(recipient, subject, body, sender_email, sender_password)
            if success:
                st.success(f"Email sent successfully at {datetime.now()}")
            else:
                st.error("Failed to send email")
        
        # Schedule the job
        schedule.every().day.at(schedule_time.strftime("%H:%M")).do(scheduled_job)
        
        # Start the scheduler in a separate thread
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.start()
        
        st.success(f"Email scheduled for {schedule_datetime}")
    else:
        st.error("Please fill in all fields")

# Display scheduled emails (you might want to store these in a database in a real application)
if st.checkbox("Show scheduled emails"):
    st.write("Scheduled jobs:")
    for job in schedule.get_jobs():
        st.write(f"- Next run at: {job.next_run}")