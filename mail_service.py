"""
ShopX Automated Email & Notification Dispatcher
Handles real email delivery via:
1. Direct SMTP (Gmail / Custom SMTP with STARTTLS)
2. Google Apps Script Email Relay
3. Local audit log and in-memory outbox for testing / live monitoring
"""

import os
import smtplib
import threading
import json
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL", "shopx.customercare@gmail.com")
ADMIN_BACKUP_EMAIL = os.environ.get("ADMIN_BACKUP_EMAIL", "raghavdeepak664@gmail.com")

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "") or os.environ.get("GMAIL_APP_PASSWORD", "")

GOOGLE_SHEETS_WEBHOOK_URL = os.environ.get(
    "GOOGLE_SHEETS_WEBHOOK_URL",
    "https://script.google.com/macros/s/AKfycbw6ObP-H0k65oxelCijRkuoU96bCSVYZZQo70oqhAGXSaXIDJccHMs24rEo2vaNDfBoyw/exec"
)

OUTBOX_LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "email_outbox.log")
RECENT_NOTIFICATIONS = []
_outbox_lock = threading.Lock()

def record_outbox_event(event_dict):
    """Save dispatched message to memory and append to outbox log."""
    with _outbox_lock:
        RECENT_NOTIFICATIONS.insert(0, event_dict)
        if len(RECENT_NOTIFICATIONS) > 100:
            RECENT_NOTIFICATIONS.pop()
        try:
            with open(OUTBOX_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_dict) + "\n")
        except Exception:
            pass

def send_via_smtp(to_email, subject, body_html, body_text="", reply_to=None):
    """Send real email via authenticated SMTP server."""
    if not SMTP_USER or not SMTP_PASSWORD:
        return False, "SMTP credentials not configured"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"ShopX Official <{SMTP_USER}>"
    msg["To"] = to_email
    if reply_to:
        msg["Reply-To"] = reply_to

    part_text = MIMEText(body_text or "Please enable HTML viewing to read this email.", "plain", "utf-8")
    part_html = MIMEText(body_html, "html", "utf-8")
    msg.attach(part_text)
    msg.attach(part_html)

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=12)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=12)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [to_email], msg.as_string())
        server.quit()
        return True, "Delivered via SMTP"
    except Exception as e:
        return False, f"SMTP Error: {str(e)}"

def relay_via_google_script(to_email, subject, body_html, body_text=""):
    """Relay email notification via deployed Google Apps Script webhook."""
    if not GOOGLE_SHEETS_WEBHOOK_URL:
        return False, "Google webhook URL not configured"

    try:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet_row = [
            now_str,
            "PASSWORD_RESET_OTP" if "Verification Code" in subject else "EMAIL_NOTIFICATION",
            to_email,
            subject,
            (body_text or body_html).strip()[:200]
        ]
        payload = json.dumps({
            "action": "SEND_EMAIL",
            "to": to_email,
            "subject": subject,
            "body": body_text,
            "htmlBody": body_html,
            "timestamp": now_str,
            "row": sheet_row
        }).encode("utf-8")
        req = urllib.request.Request(
            GOOGLE_SHEETS_WEBHOOK_URL,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8", errors="ignore").strip()
            if "Success" in content:
                return True, "Relayed to Google Apps Script (Success)"
            elif "Error" in content:
                return False, f"Google Apps Script Error: {content[:80]}"
            return True, f"Relayed to Google Apps Script ({content[:50]})"
    except Exception as e:
        return False, f"Google relay error: {str(e)}"

def test_email_dispatch(to_email):
    """Synchronously test both direct SMTP and Google Apps Script relay and return full diagnostic status."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"🔐 ShopX Email Delivery Test [{now_str}]"
    test_otp = "123456"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 20px;">
      <div style="max-width: 500px; margin: 0 auto; background: #ffffff; border-radius: 8px; padding: 24px; border: 1px solid #e5e7eb;">
        <h2 style="color: #ff9900; margin-top: 0;">ShopX Email Delivery Test</h2>
        <p>This is a real diagnostic verification email sent to confirm OTP and notifications delivery.</p>
        <div style="background: #fef3c7; border: 2px dashed #f59e0b; padding: 12px; font-size: 24px; font-weight: bold; text-align: center; letter-spacing: 4px; color: #92400e; margin: 16px 0;">{test_otp}</div>
        <p style="font-size: 13px; color: #4b5563;">Verification Code valid for 10 minutes. If you received this, your email delivery pipeline is working 100%.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="font-size: 11px; color: #9ca3af; margin: 0;">ShopX Official Security Service &bull; {SUPPORT_EMAIL}</p>
      </div>
    </body>
    </html>
    """
    text = f"ShopX Email Delivery Test. Verification OTP: {test_otp}."

    # 1. Test Direct SMTP
    smtp_ok, smtp_msg = send_via_smtp(to_email, subject, html, text)
    # 2. Test Google Apps Script Relay
    relay_ok, relay_msg = relay_via_google_script(to_email, subject, html, text)

    return {
        "timestamp": now_str,
        "target_email": to_email,
        "smtp_configured": bool(SMTP_USER and SMTP_PASSWORD),
        "smtp_user": SMTP_USER or "(Not configured on Render)",
        "smtp_success": smtp_ok,
        "smtp_status": smtp_msg,
        "google_sheets_webhook_url": GOOGLE_SHEETS_WEBHOOK_URL,
        "google_relay_success": relay_ok,
        "google_relay_status": relay_msg,
        "overall_status": "DELIVERED" if (smtp_ok or relay_ok) else "FAILED",
        "instructions": (
            "To receive emails into your inbox: "
            "1. In your Google Sheet -> Extensions -> Apps Script (Code.gs), add MailApp.sendEmail(). "
            "2. Or in Render Dashboard -> Environment, add SMTP_USER=shopx.customercare@gmail.com and SMTP_PASSWORD=[16-char App Password]."
        )
    }

def dispatch_email_async(to_email, subject, body_html, body_text="", reply_to=None, metadata=None):
    """Send email asynchronously with immediate outbox recording and automatic fallback."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = {
        "timestamp": timestamp,
        "to": to_email,
        "reply_to": reply_to,
        "subject": subject,
        "body_html": body_html,
        "body_text": body_text,
        "delivered_via": "QUEUED",
        "smtp_status": "Pending",
        "relay_status": "Pending",
        "metadata": metadata or {}
    }
    record_outbox_event(event)

    def _worker():
        smtp_success, smtp_status = send_via_smtp(to_email, subject, body_html, body_text, reply_to)
        
        delivered_via = "SMTP" if smtp_success else "OUTBOX_LOGGER"
        relay_status = "Skipped"

        if not smtp_success:
            # Try Google Apps Script relay
            g_success, g_status = relay_via_google_script(to_email, subject, body_html, body_text)
            if g_success:
                delivered_via = "GOOGLE_APPS_SCRIPT"
            relay_status = g_status

        event["delivered_via"] = delivered_via
        event["smtp_status"] = smtp_status
        event["relay_status"] = relay_status

    t = threading.Thread(target=_worker, daemon=True)
    t.start()

def notify_customer_care_inquiry(name, email, phone, subject, message):
    """
    Format and send customer support inquiry email to shopx.customercare@gmail.com
    and send acknowledgement to customer.
    """
    now_str = datetime.now().strftime("%d %b %Y, %I:%M %p")
    
    # 1. Email to shopx.customercare@gmail.com
    admin_subject = f"🔔 [ShopX Help Request] {subject} - From {name}"
    admin_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 20px; }}
        .card {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #e5e7eb; }}
        .header {{ background: #131921; color: #ffffff; padding: 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 22px; color: #ff9900; }}
        .header p {{ margin: 6px 0 0; font-size: 14px; color: #9ca3af; }}
        .badge {{ display: inline-block; background: #fee2e2; color: #b91c1c; font-weight: 700; font-size: 12px; padding: 4px 10px; border-radius: 9999px; margin-top: 10px; }}
        .content {{ padding: 24px; color: #1f2937; line-height: 1.6; }}
        .field {{ margin-bottom: 16px; border-bottom: 1px solid #f3f4f6; padding-bottom: 12px; }}
        .label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; font-weight: 600; margin-bottom: 4px; }}
        .value {{ font-size: 15px; font-weight: 500; color: #111827; }}
        .msg-box {{ background: #f9fafb; border-left: 4px solid #ff9900; padding: 14px; border-radius: 4px; font-size: 15px; white-space: pre-wrap; }}
        .cta {{ text-align: center; margin-top: 24px; }}
        .btn {{ display: inline-block; background: #ff9900; color: #111827; text-decoration: none; font-weight: 700; padding: 12px 24px; border-radius: 8px; font-size: 14px; }}
        .footer {{ background: #f9fafb; padding: 16px; text-align: center; font-size: 12px; color: #6b7280; border-top: 1px solid #e5e7eb; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h1>ShopX Customer Care Inbox</h1>
          <p>Incoming User Support & Help Ticket</p>
          <span class="badge">URGENT CUSTOMER INQUIRY</span>
        </div>
        <div class="content">
          <div class="field">
            <div class="label">Customer Name</div>
            <div class="value">{name}</div>
          </div>
          <div class="field">
            <div class="label">Customer Email</div>
            <div class="value"><a href="mailto:{email}">{email}</a></div>
          </div>
          <div class="field">
            <div class="label">Customer Mobile</div>
            <div class="value"><a href="tel:{phone}">{phone or 'Not provided'}</a></div>
          </div>
          <div class="field">
            <div class="label">Subject</div>
            <div class="value">{subject}</div>
          </div>
          <div class="field">
            <div class="label">Received At</div>
            <div class="value">{now_str}</div>
          </div>
          <div class="field" style="border-bottom: none;">
            <div class="label">Message / Query</div>
            <div class="msg-box">{message}</div>
          </div>
          <div class="cta">
            <a href="mailto:{email}?subject=Re: [ShopX Support] {subject}" class="btn">✉️ Reply Directly to Customer</a>
          </div>
        </div>
        <div class="footer">
          ShopX Customer Care &bull; Official Support: {SUPPORT_EMAIL} &bull; Recorded to Excel & Google Sheets
        </div>
      </div>
    </body>
    </html>
    """

    admin_text = f"""
    [ShopX Customer Care - New Help Ticket]
    Customer: {name}
    Email: {email}
    Phone: {phone or 'N/A'}
    Subject: {subject}
    Date: {now_str}

    Message:
    {message}

    Reply directly to: {email}
    """

    dispatch_email_async(
        to_email=SUPPORT_EMAIL,
        subject=admin_subject,
        body_html=admin_html,
        body_text=admin_text,
        reply_to=email,
        metadata={"type": "CUSTOMER_CARE_INQUIRY", "customer_name": name, "customer_email": email}
    )

    # Also dispatch to backup admin email if distinct
    if ADMIN_BACKUP_EMAIL and ADMIN_BACKUP_EMAIL.lower() != SUPPORT_EMAIL.lower():
        dispatch_email_async(
            to_email=ADMIN_BACKUP_EMAIL,
            subject=admin_subject,
            body_html=admin_html,
            body_text=admin_text,
            reply_to=email,
            metadata={"type": "CUSTOMER_CARE_INQUIRY_BACKUP"}
        )

    # 2. Automated Confirmation Email to Customer
    if email and "@" in email:
        cust_subject = f"✓ We've received your ShopX request: {subject}"
        cust_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; margin: 0; padding: 20px; }}
            .card {{ max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; }}
            .header {{ background: #131921; color: #ffffff; padding: 20px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 20px; color: #ff9900; }}
            .content {{ padding: 24px; color: #374151; font-size: 15px; line-height: 1.6; }}
            .footer {{ background: #f9fafb; padding: 14px; text-align: center; font-size: 12px; color: #6b7280; }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="header">
              <h1>ShopX Customer Care</h1>
            </div>
            <div class="content">
              <p>Hi <strong>{name}</strong>,</p>
              <p>Thank you for reaching out to us! Your help request regarding <strong>"{subject}"</strong> has been assigned to our customer support team.</p>
              <p>One of our specialists will review your message and reply back to you at <strong>{email}</strong> within 2-4 business hours.</p>
              <p>If you have any additional details or urgent questions, please feel free to reply directly to this email or contact us at <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>.</p>
              <p style="margin-top: 24px;">Warm regards,<br><strong>ShopX Support Team</strong></p>
            </div>
            <div class="footer">
              ShopX &bull; India's Most Trusted Digital Shopping Destination
            </div>
          </div>
        </body>
        </html>
        """
        dispatch_email_async(
            to_email=email,
            subject=cust_subject,
            body_html=cust_html,
            body_text=f"Hi {name}, we received your inquiry regarding '{subject}'. Our team is on it and will reply soon.",
            reply_to=SUPPORT_EMAIL,
            metadata={"type": "CUSTOMER_CONFIRMATION"}
        )

def notify_seller_application(seller_data):
    """
    Format and send seller/reseller inquiry email to shopx.customercare@gmail.com
    and send onboarding welcome email to merchant.
    """
    brand = seller_data.get("brand_name", "N/A")
    owner = seller_data.get("owner_name", "N/A")
    email = seller_data.get("email", "N/A")
    phone = seller_data.get("phone", "N/A")
    category = seller_data.get("category", "General")
    city = seller_data.get("city", "N/A")
    state = seller_data.get("state", "N/A")
    gstin = seller_data.get("gstin", "N/A")
    now_str = datetime.now().strftime("%d %b %Y, %I:%M %p")

    admin_subject = f"🚀 [ShopX Merchant Inquiry] New Seller Application: {brand} ({owner})"
    admin_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; margin: 0; padding: 20px; }}
        .card {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
        .header {{ background: #065f46; color: #ffffff; padding: 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 22px; color: #a7f3d0; }}
        .header p {{ margin: 6px 0 0; font-size: 14px; opacity: 0.9; }}
        .content {{ padding: 24px; color: #1f2937; line-height: 1.6; }}
        .field {{ display: flex; justify-content: space-between; border-bottom: 1px solid #f3f4f6; padding: 10px 0; }}
        .label {{ font-size: 13px; font-weight: 600; color: #6b7280; }}
        .value {{ font-size: 14px; font-weight: 600; color: #111827; }}
        .cta {{ text-align: center; margin-top: 24px; }}
        .btn {{ display: inline-block; background: #059669; color: #ffffff; text-decoration: none; font-weight: 700; padding: 12px 24px; border-radius: 8px; font-size: 14px; }}
        .footer {{ background: #f9fafb; padding: 14px; text-align: center; font-size: 12px; color: #6b7280; border-top: 1px solid #e5e7eb; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h1>New Merchant Registration</h1>
          <p>Application to Sell / Resell on ShopX Marketplace</p>
        </div>
        <div class="content">
          <div class="field"><span class="label">Brand / Business Name</span><span class="value">{brand}</span></div>
          <div class="field"><span class="label">Owner / Contact Person</span><span class="value">{owner}</span></div>
          <div class="field"><span class="label">Email Address</span><span class="value"><a href="mailto:{email}">{email}</a></span></div>
          <div class="field"><span class="label">Mobile Number</span><span class="value"><a href="tel:{phone}">{phone}</a></span></div>
          <div class="field"><span class="label">Product Category</span><span class="value">{category}</span></div>
          <div class="field"><span class="label">City & State</span><span class="value">{city}, {state}</span></div>
          <div class="field"><span class="label">GSTIN / Tax ID</span><span class="value">{gstin}</span></div>
          <div class="field"><span class="label">Submitted At</span><span class="value">{now_str}</span></div>

          <div class="cta">
            <a href="mailto:{email}?subject=ShopX Merchant Onboarding: Next Steps for {brand}" class="btn">✉️ Contact Merchant Directly</a>
          </div>
        </div>
        <div class="footer">
          ShopX Merchant Onboarding &bull; Official Email: {SUPPORT_EMAIL} &bull; Recorded to Excel & Google Sheets
        </div>
      </div>
    </body>
    </html>
    """

    admin_text = f"""
    [ShopX New Seller Application]
    Brand: {brand}
    Owner: {owner}
    Email: {email}
    Phone: {phone}
    Category: {category}
    Location: {city}, {state}
    GSTIN: {gstin}
    Date: {now_str}

    Reply to merchant at: {email}
    """

    dispatch_email_async(
        to_email=SUPPORT_EMAIL,
        subject=admin_subject,
        body_html=admin_html,
        body_text=admin_text,
        reply_to=email,
        metadata={"type": "SELLER_APPLICATION", "brand": brand, "owner": owner}
    )

    if ADMIN_BACKUP_EMAIL and ADMIN_BACKUP_EMAIL.lower() != SUPPORT_EMAIL.lower():
        dispatch_email_async(
            to_email=ADMIN_BACKUP_EMAIL,
            subject=admin_subject,
            body_html=admin_html,
            body_text=admin_text,
            reply_to=email,
            metadata={"type": "SELLER_APPLICATION_BACKUP"}
        )

    # Confirmation to applicant
    if email and "@" in email:
        welcome_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; margin: 0; padding: 20px; }}
            .card {{ max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; }}
            .header {{ background: #131921; color: #ffffff; padding: 20px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 20px; color: #ff9900; }}
            .content {{ padding: 24px; color: #374151; font-size: 15px; line-height: 1.6; }}
            .footer {{ background: #f9fafb; padding: 14px; text-align: center; font-size: 12px; color: #6b7280; }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="header">
              <h1>Welcome to ShopX Merchant Network</h1>
            </div>
            <div class="content">
              <p>Dear <strong>{owner}</strong>,</p>
              <p>Thank you for registering <strong>{brand}</strong> to sell on ShopX! We have received your application and catalog profile under <strong>{category}</strong>.</p>
              <p>Our Seller Onboarding team has logged your credentials and will connect with you at <strong>{phone}</strong> or via this email within 24 hours to guide you through catalog upload and payout setup.</p>
              <p>If you have any questions in the meantime, reach us anytime at <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>.</p>
              <p style="margin-top: 24px;">Best regards,<br><strong>ShopX Merchant Onboarding Team</strong></p>
            </div>
            <div class="footer">
              ShopX Marketplace &bull; {SUPPORT_EMAIL}
            </div>
          </div>
        </body>
        </html>
        """
        dispatch_email_async(
            to_email=email,
            subject=f"✓ Application Received: Start Selling on ShopX with {brand}",
            body_html=welcome_html,
            body_text=f"Dear {owner}, we received your application for {brand} on ShopX. Our seller onboarding team will contact you within 24 hours.",
            reply_to=SUPPORT_EMAIL,
            metadata={"type": "SELLER_WELCOME"}
        )

def notify_password_reset_otp(to_email, otp, user_name="Shopper"):
    """Send 6-digit OTP email for password recovery."""
    if not to_email or "@" not in to_email:
        return

    subject = f"🔐 {otp} is your ShopX Password Reset Verification Code"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; margin: 0; padding: 20px; }}
        .card {{ max-width: 500px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
        .header {{ background: #131921; color: #ffffff; padding: 20px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 20px; color: #ff9900; }}
        .content {{ padding: 24px; color: #374151; font-size: 15px; line-height: 1.6; text-align: center; }}
        .otp-box {{ display: inline-block; background: #fef3c7; border: 2px dashed #f59e0b; padding: 12px 28px; border-radius: 8px; font-size: 28px; font-weight: 800; letter-spacing: 6px; color: #92400e; margin: 18px 0; }}
        .warning {{ font-size: 13px; color: #6b7280; margin-top: 14px; }}
        .footer {{ background: #f9fafb; padding: 14px; text-align: center; font-size: 12px; color: #6b7280; border-top: 1px solid #e5e7eb; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h1>ShopX Security Service</h1>
        </div>
        <div class="content">
          <p>Hi <strong>{user_name}</strong>,</p>
          <p>We received a request to reset your password for your ShopX account. Use the one-time verification code below:</p>
          <div class="otp-box">{otp}</div>
          <p class="warning">⚠️ This code expires in <strong>10 minutes</strong>. Never share this code with anyone. ShopX representatives will never ask for your OTP.</p>
          <p class="warning">If you did not request this, please ignore this email.</p>
        </div>
        <div class="footer">
          ShopX Account Security &bull; {SUPPORT_EMAIL}
        </div>
      </div>
    </body>
    </html>
    """

    text = f"""
    ShopX Password Reset Code: {otp}
    Hi {user_name}, use this code to reset your ShopX password.
    This code is valid for 10 minutes. Do not share it with anyone.
    """

    dispatch_email_async(
        to_email=to_email,
        subject=subject,
        body_html=html,
        body_text=text,
        reply_to=SUPPORT_EMAIL,
        metadata={"type": "PASSWORD_RESET_OTP", "otp": otp, "user": user_name}
    )

def get_recent_outbox(limit=50):
    """Retrieve recent notifications for Admin inbox inspection."""
    with _outbox_lock:
        return RECENT_NOTIFICATIONS[:limit]
