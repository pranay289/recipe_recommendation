# Recipe Recommendation System

This project is a Recipe Recommendation System that utilizes a combination of Docker, Python, Flask, and Render. The system recommends recipes based on user preferences and interactions. Below are the key components and tools involved in this example:

* ### Docker
Used for version control and deployment, incorporating a Docker image with Python and a command for running the machine learning (ML) model.

* ### Python 
Employed for scripting and developing the ML model and backend logic.

* ### Flask
Utilized for creating APIs, providing a powerful library for building web applications.

* ### Render
Used to deploy the Docker file, leveraging the Render console for cloud storage and deployment.

Technologies Used
* ### Docker
Ensures consistency across different environments and simplifies deployment.
* ### Python
Used for developing the machine learning model and backend logic.
* ### Flask
Enables the creation of APIs to interact with the machine learning model.
* ### Render
Used for deploying the Docker container in the cloud.

# Getting Started
 ### Prerequisites
Install Docker on your machine.
Have Python installed
Install Flask using pip install Flask.
Installation Steps
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/recipe-recommendation.git
cd recipe-recommendation
Build Docker Image:

bash
Copy code
```

docker build -t recipe-recommendation .

```
Run Docker Container:

bash
Copy code
```

docker run -p 5000:5000 recipe-recommendation

```
Access the API:
Open your web browser and go to `http://localhost:5000.`

```
API Endpoints
Recommend Recipes:
Endpoint: /api/recommend
Method: POST
Input: User preferences (send as JSON)
Output: Recommended recipes (JSON format)
Deploying on Render
Create Render Account:
Sign up for a Render account if you don't have one.
```
## Create a New Web Service:

Set up a new web service on [Render](render.com).
Connect your GitHub repository for automatic deployments.
Configure Environment Variables:

Set environment variables for sensitive information if you have.
## Example: 
API_KEY, SECRET_KEY, etc.
Deploy:

Click the **Deploy** button on Render.
Access the Deployed App:
Once deployed, your app will be accessible via the provided URL.


[Hosted url example](https://recipe-recommendation-flask.onrender.com/alldata)
