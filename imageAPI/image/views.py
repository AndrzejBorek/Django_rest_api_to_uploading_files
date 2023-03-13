import http
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.exceptions import BadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from psycopg2 import errors


from .models import Image as imageModel
from .s3 import s3


def is_valid_image_file(file):
    return file in ['image/jpeg', 'image/png']


@api_view(['POST'])
@parser_classes([FileUploadParser])
@csrf_exempt
def upload_image(request):
    user_id = request.user.id
    if user_id:
        username = request.user.username
        # Check if the file is a valid image file
        if not is_valid_image_file(request.data['file'].content_type):
            raise BadRequest('Invalid file type. JPG, PNG allowed.')

        filename = request.data['file']
        account_tier = request.user.user_profile.account_tier
        thumbnail_sizes = account_tier.thumbnail_sizes
        original_key = f"{username}/original/org_{filename}"
        try:
            s3.upload_fileobj(request.data['file'], settings.AWS_STORAGE_BUCKET_NAME, original_key,
                              ExtraArgs={'Metadata': {'sizes': f'{thumbnail_sizes}'}})
        except ClientError as e:
            return Response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                            data={"Message": f'Failed to upload the image: {e}'})
        else:
            image_name = f'{request.data["file"].name}_org'
            image_path = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{original_key}'
            try:
                imageModel.objects.create(user=request.user, name=image_name, image_path=image_path)
            except errors.UniqueViolation as e:
                print("CONFLICT")
        return Response(status=http.HTTPStatus.CREATED, data={"Message": "Image uploaded successfully."})
    return Response(status=http.HTTPStatus.BAD_REQUEST)
