# Starting up

cd into the project folder and run the following:
uvicorn main:app --reload 

![image](https://user-images.githubusercontent.com/73429081/221334014-87ba2de6-859f-4b4f-b05d-706459cfdeba.png)


# Making use of Swagger UI

access the swagger url with:
http://127.0.0.1:8000/docs#/

![image](https://user-images.githubusercontent.com/73429081/221334131-1ef08025-a965-4817-9d25-c5d26044d61b.png)

# Register a user 

Click the Try it out button for the register POST request  
Enter your values  
Press Execute

![image](https://user-images.githubusercontent.com/73429081/221334219-f6347676-8eb9-4945-b49e-98c113b2c88d.png)

Successful Response should look like:  

![image](https://user-images.githubusercontent.com/73429081/221334771-ec195fc4-2b70-4782-8c3a-d9611969bc6a.png)

# Login with user

Enter your email in the username field  
Enter your password  
Press Execute

![image](https://user-images.githubusercontent.com/73429081/221335139-c2007d51-9c25-4f17-bf67-20fdc6e9edff.png)

A successful response should give a JWT token that can be used to authenticate subsequent requests

![image](https://user-images.githubusercontent.com/73429081/221335255-48fad6b5-313e-4919-a4b1-e6e2cae6d956.png)

# Get user own info 

I would be using POSTMAN for subsequent requests to make use of the token from login for authentication

![image](https://user-images.githubusercontent.com/73429081/221335395-c4e4f205-feac-496b-9b1d-68d7f607aab8.png)

Select the Authorization tab  
Select Bearer Token  
Copy paste the token string gotten from login  
Press send

![image](https://user-images.githubusercontent.com/73429081/221335495-98429862-e396-473a-b9a5-0b60d9b7531a.png)

A successful response should display the user's own information

![image](https://user-images.githubusercontent.com/73429081/221335983-dbae9c05-0872-4f2b-888e-41e5ae4fe4b4.png)

# Update user own info 

Use the same steps for authorization using the token  
For the request body update the fields you want to change  
Select JSON  
Click Send 

![image](https://user-images.githubusercontent.com/73429081/221336953-ad545cda-3b4b-4948-9dc4-c4383896e251.png)
![image](https://user-images.githubusercontent.com/73429081/221337522-800aa963-c7b4-4f7a-a582-5a5daba0891b.png)

The updated fields of user:  

![image](https://user-images.githubusercontent.com/73429081/221338094-57e49ba5-86f9-4af3-a98e-72249c8e8263.png)

# Delete user 

Use the same steps for authorization using the token  
Click Send 

![image](https://user-images.githubusercontent.com/73429081/221338221-06cb0f38-7f32-49ae-8f7e-d8f1e3fc5d9b.png)

A successful response should look like:

![image](https://user-images.githubusercontent.com/73429081/221338244-e5e0ce5c-4720-41a7-bd0e-236ff07f9247.png)

Trying to get the info from the same user would now return a 400 Bad Request Response

![image](https://user-images.githubusercontent.com/73429081/221338402-8b544397-0dc5-4977-9311-7643bf8b0c67.png)
![image](https://user-images.githubusercontent.com/73429081/221338450-36439a05-dfe9-4740-a9f3-ed5e6d294984.png)

# Ending
  
I did try to deploy it on render.com but faced technical limitations

![image](https://user-images.githubusercontent.com/73429081/221338592-f5f154b7-c6bc-4d76-bf4c-a509916831cd.png)

Nevertheless, thank you for taking the time to read this

