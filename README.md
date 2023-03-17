Image uploading REST API.

Project is a REST API that allows users to upload and retrieve images.
Users can upload an image file, which is then stored on an Amazon S3 bucket.
Based on user account tier, application also generates thumbnails of the uploaded image at different sizes and stores
them on different S3 bucket. Generating thumbnails is done with AWS lambda. Admin can create custom account tiers with
several possible options.

The application provides REST APIs that allow users to upload an image and retrieve a list of uploaded images.
The APIs are secured using JSON Web Tokens (JWT), and only authenticated users can upload or retrieve images.

1. Prerequisites.
    - Docker - To download Docker: _https://docs.docker.com/get-docker/_
    - AWS Console Account - To register and login in AWS: _https://aws.amazon.com/console/_
    - Git - To download Git: _https://git-scm.com/downloads_

2. Setup.
    - All configuration files (AWS policies, request templates) are located in **config_files** directory.
    - Clone this repository to your local machine.
    - Create a new IAM user on your AWS account to use for this app. Make a note of the access key ID and secret access
      key for this user. Application users will upload their images on behalf of this IAM user, so user has to have
      certain permissions. For this sample project
      IAM User will have AmazonS3FullAccess policy. In larger project this IAM user could be app backend hosted on AWS,
      so users
      would send requests to backend which would authorize them, and then if they are allowed to some actions, backend
      would
      send request to AWS. This approach reduces users direct access to resources.
        - How to create IAM user: _https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html_
        - How to add policy to IAM
          user: _https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html_
    - Create AWS lambda for creating thumbnail. How to create lambda to make images
      thumbnail: _https://docs.aws.amazon.com/lambda/latest/dg/with-s3-tutorial.html#with-s3-tutorial-configure-event-source_
    - Add policy to buckets to be able to see uploaded images.
    - Copy the contents of **.env.example** to a new file called **.env** in the root directory of the project. Edit the
      file to include your AWS credentials and PostgresSQL database credentials.
    - From the root directory of the project, run the following command to build and start the app:
      **docker-compose up -d --build**
    - The app will now be running locally at _http://localhost:8000_.

3. Usage.
    - Log in to the Django admin panel at http://localhost:8000/admin/login/?next=/admin/.
    - You will need to use the admin credentials you set in your .env file.
    - Create a new user from the admin panel.
    - Using a RESTful API client like Postman, send a **POST** request to _http://localhost:8000/api/token/_ with the
      username and password of the user you just created in the request body. This will return an access token.
      With the access token, you can now send a **POST** request to http://localhost:8000/api/images/ to upload an image
      to your S3 bucket. Name of uploaded file is taken from Content-Disposition header, from filename.
4. Endpoints.
    - _http://localhost:8000/token/_ [**POST**] returns access and refresh token if user credentials are correct.
    - _http://localhost:8000/image/upload_ [**POST**] uploads image. In postman, file has to be uploaded with binary
      type.
      In request headers user has to add key: \
      _**Content-Disposition**_ with value: **_: attachment; filename=<name of uploaded file>_**
    - _http://localhost:8000/image/all_ [**GET**] Returns all images of user sending request.
    - _http://localhost:8000/image/expiring/?image=image_name&expire_time=expire_time_ [POST] Based on user account tier
      and its permissions, returns link with expiring time set by user.
5. TODO
    - Unfortunately, I was not able to write quite important test, which kinda is crucial to all tests. It's sense was
      to test uploading file by user. I added comment in code **/imageAPI/image/tests.py**. Feel free to give me
      feedback or advices. It will be handled in the future. Also I will be changing way of uploading the images, so that user won't have to add Conten
      t-Disposition header by hand.
