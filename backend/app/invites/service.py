import os
from dotenv import load_dotenv
from zerobouncesdk import ZeroBounce, ZBException

load_dotenv()

ZEROBOUNCE_API_KEY = os.getenv("ZEROBOUNCE_API_KEY")

async def create_invite(invite):

    # Check whether expiry date is not null
    if(invite.expiry_date == None):
        return "expiry"
    
    # Validate email address
    return await validate_email(invite.email)

    # send email
    # log the invite request?
    return

# Using ZeroBounce API to validate email address
async def validate_email(email: str):
    zero_bounce = ZeroBounce(ZEROBOUNCE_API_KEY) 

    try:
        response = zero_bounce.validate(email)
        return str(response.status.value)
    except ZBException as e:
        return str(e)

