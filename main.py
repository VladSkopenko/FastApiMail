from pathlib import Path

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List


class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME="skopil@meta.ua",
    MAIL_PASSWORD="Mypasswordformeta1",
    MAIL_FROM="skopil@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Vladislav",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

app = FastAPI()


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    message = MessageSchema(
        subject="Privetic",
        recipients=[body.email],
        template_body={"fullname": "Skopenko"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="email.html")

    return {"message": "email has been sent"}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)