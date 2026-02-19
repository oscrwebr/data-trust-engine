import os
from dotenv import load_dotenv
from zerobouncesdk import ZeroBounce, ZBException
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse
from .schema import EmailSchema, conf
from datetime import datetime
from typing import List

load_dotenv()

ZEROBOUNCE_API_KEY = os.getenv("ZEROBOUNCE_API_KEY")

#Creating, sending and logging invite
async def create_invite(invite):

    # Validate inputs
    is_invite_valid = await validate_invite(invite.email, invite.expiry_date)
    if(is_invite_valid == True):
    
        #Send invite
        print("Invite email has been sent")
        #await send_invite([invite.email])
        return True 

    else:
        return is_invite_valid
    
         


# Validating the invite
async def validate_invite(email: str, expiry_date: datetime | None):
    
    # Call validate email function
    is_email_valid = await validate_email(email)
    if(is_email_valid == "invalid"):
        return is_email_valid
   
    # Check whether expiry date is not null
    if(expiry_date == None and is_email_valid == "valid"):
        return "expiry"
    
    return True

    
# Using ZeroBounce API to validate email address
async def validate_email(email: str):
    zero_bounce = ZeroBounce(ZEROBOUNCE_API_KEY) 

    # Check whether email is valid
    try:
        response = zero_bounce.validate(email)
        return str(response.status.value)
    except ZBException as e:
        return str(e)
  

#Using FastAPI smtplib to send the email
async def send_invite(email: EmailSchema):
    template = """
            <html>
                <body style="margin:0; padding:0; font-family:Arial, sans-serif; background-color:#f5f5f5;">
                    <table align="center" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; background:#ffffff;">
                    <!-- Header image -->
                    <tr>
                        <td align="center" style="padding:20px 0;">
                        <img 
                            src="http://blogs.cardiff.ac.uk/innovation/wp-content/uploads/sites/561/2023/01/CIH-Logo-Primary-Black.jpg" 
                            alt="Company Logo or Header" 
                            style="max-width:200px; width:100%; height:auto;" />
                        </td>
                    </tr>

                    <!-- Body content -->
                    <tr>
                        <td style="padding:20px;">
                        <p style="font-size:16px; color:#333333;">
                            Hi <strong>[employee_name]</strong>,
                        </p>

                        <p style="font-size:14px; color:#333333;">
                            You have been invited to join our system.
                            Please use the link below to activate your account before the expiry date.  
                            If you have any questions, feel free to reach out.
                        </p>

                        <p style="font-size:14px; color:#333333;">
                            Best regards,<br />
                            <strong>[admin_name]</strong>
                        </p>

                        <p style="font-size:14px; color:#333333; margin-top:25px;">
                            This invite expires on: <strong>[expiry_date]</strong>
                        </p>

                        <!-- Accept invite button -->
                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;">
                            <tr>
                            <td align="center">
                                <a 
                                href="[activation_link]" 
                                target="_blank"
                                style="background-color:#007bff; color:#ffffff; padding:12px 24px; text-decoration:none; font-weight:bold; font-size:16px; border-radius:4px; display:inline-block;">
                                Accept Invite
                                </a>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>

                    <!-- Footer / optional -->
                    <tr>
                        <td style="padding:15px; font-size:12px; color:#777777; text-align:center;">
                        If you didn’t expect this email, you can safely ignore it.
                        </td>
                    </tr>
                    </table>
                </body>
            </html>

            """

    message = MessageSchema(
        subject="[Organisation name] Invite Request",
        recipients=email, 
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})