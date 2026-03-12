import os

from dotenv import load_dotenv
from .schema import conf
from zerobouncesdk import ZeroBounce, ZBException
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.invites.models import Invite
from app.authentication.models import User
from app.workspaces import repository
import base64


load_dotenv()

ZEROBOUNCE_API_KEY = os.getenv("ZEROBOUNCE_API_KEY")

#Creating, sending and logging invite
async def create_invite(invite):

    # Validate inputs
    is_invite_valid = validate_invite(invite.email, invite.expiry_date)
    if(is_invite_valid == True):
    
        return True 

    else:
        return is_invite_valid
    

# Validating the invite
def validate_invite(email: str, expiry_date: datetime | None):

    if email is None:
        return "invalid"
    
    # Call validate email function
    is_email_valid = validate_email(email)
    if (is_email_valid == "invalid"):
        return "invalid"
    
    # Check for existing but untrustworthy email
    if (is_email_valid == "do_not_mail"):
        return "trust"
   
    # Check whether expiry date is not null
    if(expiry_date == None and is_email_valid == "valid"):
        return "expiry"
    
    return True

    
# Using ZeroBounce API to validate email address
def validate_email(email: str):
    zero_bounce = ZeroBounce(ZEROBOUNCE_API_KEY) 

    # Check whether email is valid
    try:
        response = zero_bounce.validate(email)
        return str(response.status.value)
    except ZBException as e:
        return str(e)
  

#Using FastAPI smtplib to send the email
async def send_invite_service(db: Session, email: str, expiry: str, token: str, user: User):
    workspace = repository.get_workspace_by_user_id(db, user.user_id)
    image_base64 = base64.b64encode(workspace.image).decode("utf-8")
    template = f"""
            <html>
                <body style="margin:0; padding:0; font-family:Arial, sans-serif; background-color:#f5f5f5;">
                    <table align="center" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; background:#ffffff;">
                    <!-- Header image -->
                    <tr>
                        <td align="center" style="padding:20px 0;">
                        <img 
                            src="data:image/png;base64,{image_base64}"
                            alt="Company Logo or Header" 
                            style="max-width:200px; width:100%; height:auto;" />
                        </td>
                    </tr>

                    <!-- Body content -->
                    <tr>
                        <td style="padding:20px;">
                        <p style="font-size:14px; color:#333333;">
                            Hi there,
                        </p>

                        <p style="font-size:14px; color:#333333;">
                            You have been invited to join our workspace.
                            Please use the link below to activate your account before the expiry date.  
                            If you have any questions, feel free to reach out.
                        </p>

                        <p style="font-size:14px; color:#333333;">
                            Best regards,<br />
                            <strong>{user.firstname} {user.surname}</strong>
                        </p>

                        <p style="font-size:14px; color:#333333; margin-top:25px;">
                            This invite expires on the <strong>{expiry}</strong> at <strong>23:59</strong>.
                        </p>

                        <!-- Accept invite button -->
                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;">
                            <tr>
                            <td align="center">
                                <a 
                                href="http://localhost:8000/invite/invite-processing?token={token}"
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
        subject=f"{workspace.name} Invite Request",
        recipients=[email], 
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

def check_invite(invite:Invite, db: Session):

    # Check invite expiry date
    if(invite.expiry_date < date.today()):
        db.commit()
        return "expired"

    db.commit()
    return True