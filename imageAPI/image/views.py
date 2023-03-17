import http

from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from .models import Image as imageModel, Image, ImageSerializer
from .s3 import s3_client

EXPIRING_TIME_LOWER_LIMIT = 30
EXPIRING_TIME_UPPER_LIMIT = 30000


def is_valid_image_file(file):
    return file in ['image/jpeg', 'image/png']


@api_view(['POST'])
@parser_classes([FileUploadParser])
@csrf_exempt
@login_required
def upload_image(request):
    username = request.user.username
    file = request.data.get('file')
    if not file or not is_valid_image_file(file.content_type):
        return Response(status=http.HTTPStatus.BAD_REQUEST,
                        data={"message": "Invalid file type or missing file. JPG, PNG allowed."})

    account_tier = request.user.user_profile.account_tier
    thumbnail_sizes = account_tier.thumbnail_sizes if account_tier else []

    original_key = f"{username}/{file}"
    original_image_path = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{original_key}'
    try:
        s3_client.upload_fileobj(request.data['file'], settings.AWS_STORAGE_BUCKET_NAME, original_key,
                                 ExtraArgs={'Metadata': {'sizes': f'{thumbnail_sizes}'}})
    except ClientError as e:
        return Response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                        data={"Message": f'Failed to upload the image: {e}'})

    image_paths = []
    for thumbnail_size in thumbnail_sizes:
        image_paths.append(
            f'https://{settings.AWS_STORAGE_RESIZED_BUCKET_NAME}.s3.amazonaws.com/{username}/{thumbnail_size}{file}')

    if account_tier and account_tier.link_to_original:
        image_paths.append(original_image_path)

    try:
        imageModel.objects.create(user=request.user, name=file, image_paths=image_paths,
                                  thumbnail_sizes=thumbnail_sizes)
    except ValidationError as e:
        return Response(status=http.HTTPStatus.CONFLICT, data={"message": e})

    return Response(status=http.HTTPStatus.CREATED, data={"Data": image_paths})


@api_view(['GET'])
@csrf_exempt
@login_required
def get_user_images(request):
    user_images = Image.objects.filter(user=request.user)
    serializer = ImageSerializer(user_images, many=True)
    names = [image['name'] for image in serializer.data]
    return Response(status=http.HTTPStatus.OK, data=names)


@api_view(['GET'])
@csrf_exempt
@login_required
def get_expiring_link(request):
    user = request.user
    image = request.GET.get('image')
    expire_time = int(request.GET.get('expire_time'))
    if not (image or expire_time):
        return Response(status=http.HTTPStatus.BAD_REQUEST,
                        data={"message": "'image' and 'expiring_time' arguments are obligatory."})
    if EXPIRING_TIME_LOWER_LIMIT > expire_time or expire_time > EXPIRING_TIME_UPPER_LIMIT:
        return Response(status=http.HTTPStatus.BAD_REQUEST,
                        data={"message": "Expiring time must be between 30 and 30000."})
    try:
        Image.objects.get(name=f"{image}.jpg", user=user)
    except Image.DoesNotExist:
        return Response(status=http.HTTPStatus.NOT_FOUND, data={"message": "Image does not exist."})
    if user.user_profile.account_tier.expiring_links:
        img_path = f"{user}/{image}.jpg"
        try:
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': img_path
                },
                ExpiresIn=expire_time
            )
            return Response(status=http.HTTPStatus.OK, data={"expiring_url": url})
        except ClientError as e:
            return Response(status=http.HTTPStatus.BAD_REQUEST, data={"message": f'Failed to upload the image: {e}'})
    return Response(status=http.HTTPStatus.FORBIDDEN,
                    data={"message": {"User does not have privilege to perform this action."}})
