from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from PIL import Image , ImageOps
from io import BytesIO
from rembg import remove
import os
from django.http import HttpResponse
from django.conf import settings
from removebg.models import Person
from removebg.serializers import PersonSerializaer, ImageSerializer
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET','POST'])
def index(request):
    courses={
        'course_name':'python',
        'learn':['flask','django'],
        'course_provider':'santosh bhosle'
        }
    if request.method == 'POST':
        data = request.data
        print(data)
    return Response(courses)

@api_view(['GET','POST'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.all()
        serializer = PersonSerializaer(objs, many= True)
        return Response(serializer.data)
    
    else:
        data = request.data
        serializer = PersonSerializaer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.error)
    

# class RemoveBackground(APIView):
#     parser_classes = (MultiPartParser,)

#     def post(self, request):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             # Get the uploaded image from the serializer
#             image = serializer.validated_data['image']

#             # Process the image to remove the background
#             processed_image = remove(Image.open(image))

#             # Convert processed image to bytes
#             img_byte_arr = BytesIO()
#             processed_image.save(img_byte_arr, format='PNG')
#             img_byte_arr = img_byte_arr.getvalue()

#             # Return the processed image as a response
#             return Response({'processed_image': img_byte_arr})
#         else:
#             return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser])
def remove_background(request):
    # Log request headers
    print(request.headers)
    if request.method == 'POST' and request.FILES.get('image'):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            # Get the uploaded image from the serializer
            image = serializer.validated_data['image']


            # Save the uploaded image to the 'masked' directory
            # original_dir = os.path.join(settings.BASE_DIR, 'original')
            # if not os.path.exists(original_dir):
            #     os.makedirs(original_dir)

            # image_name = image.name
            # original_image_path = os.path.join(original_dir, image_name)
            # with open(original_image_path, 'wb') as f:
            #     for chunk in image.chunks():
            #         f.write(chunk)

            # getting image details
            pil_image = Image.open(image)
            original_width, original_height = pil_image.size

            # Extract image name and format
            image_name = image.name
            image_format = image_name.split('.')[-1].lower()
            # image_format = image.name.split('.')[-1].lower() 

            # Process the image to remove the  background
            processed_image = remove(Image.open(image))


            # Save the processed image to the 'masked' directory
            # masked_dir = os.path.join(settings.BASE_DIR, 'masked')
            # if not os.path.exists(masked_dir):
            #     os.makedirs(masked_dir)
            # processed_image_name = f"processed_{image_name}"
            # processed_image_path = os.path.join(masked_dir, processed_image_name)
            # processed_image.save(processed_image_path, format='PNG')

            # Convert processed image to bytes
            img_byte_arr = BytesIO()
            processed_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()            

            # Return the processed image as a response
            response = HttpResponse(img_byte_arr, content_type='image/png')
            # Include image name and format in the Content-Disposition header
            response['Content-Disposition'] = f'attachment; filename="{image_name}"'
            # response['Image-Format'] = image_format
            response['Image-Name'] = image_name
            return response
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response({'error': 'Invalid request'}, status=400)


 