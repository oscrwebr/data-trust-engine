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
        print("Invite has been sent and will be logged")
        #await send_invite([invite.email])

    else:
        return is_invite_valid
    
    return True      


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
                <body>
                    <p>Hi !!!
                    <br>Thanks for using fastapi mail, keep using it..!!!</p>
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
    print(message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})