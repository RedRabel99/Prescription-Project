from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(title, content, patient_email):
    send_mail(
        title,
        content,
        None,
        patient_email
    )


def get_prescription_email_content(prescription):
    content_string = f"The following prescription has been prescribed for you:\n"
    for segment in prescription.segments.all():
        content_string += f"{segment.drug.name} {segment.drug.form} - {segment.drug.pack}\n" \
                          f"qantity: {segment.count}\n\n"

    content_string += "Visit website for more information"
    return content_string
