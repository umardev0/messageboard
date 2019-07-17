# Message Board Application

Message board application with SOAP web service for creating message written in Java using Spring Boot and REST web service for getting messages list written in Python using Flask.

## Installation
You can use the services of application either by running them in a container or on local machine. Open Terminal and set messageboard as working directory.

### Docker Installation (Preferred)
Make sure you have docker desktop installed and then simply run docker-compose to start the services using following command:
```sh
$ docker-compose -f docker-compose.yml up -d
```
To stop the containers run:
```sh
$ docker-compose down --remove-orphans
```
### Local Installation
Make sure you satisfy following dependencies before running bash.sh script:
  - Java 8
  - Python 3
  - **Redis running at localhost:6379**

Run bash.sh file to start the services. You might need to give bash.sh permissions to use.
```sh
$ chmod +x bash.sh
$ ./bash.sh
```
Wait for success messages to appear before using the services.

**Note:** Everything was tested on macOS Mojave. Make appropriate changes if required to run bash script on windows 10.

## Usage
Once the services are running by either installation method, you can use them by following methods.
### Create Message Service
```sh
http://localhost:7000/createmessage/message.wsdl
```
Create message is a SOAP service and you can either use SoapUI to interact with it by providing the wsdl URL or add a message using provided request.xml by running:
```sh
$ curl --header "content-type: text/xml" -d @request.xml http://localhost:7000/createmessage
```

### List Messages Service
```sh
http://localhost:7001/
```
List messages is a REST service and you can either use Postman to interact with it or retrieve messages by running:
```sh
$ curl http://localhost:7001/v1
$ curl http://localhost:7001/v2?format=json
$ curl http://localhost:7001/v2?format=xml
```

To run tests, change working directory to ListMessages and run:
```sh
$ source venv/bin/activate
$ pytest
```

## Solution Explanation
### Frameworks
I decided to use vanilla flask for my service but we can improve development in flask by using its extended frameworks like flask-restful or conexxion. I decided to use Spring boot for SOAP service as it is also an enterprise grade framework that can scale well.
### URL Validation
URL validation is done by using a URL regex. We can further optimize this regex to satisfy our needs for specific URL patterns.
### Service Versions
List messages service take version as URL parameter. V1 has strict rules and does not allow any query parameter. V2 allows format to be sent as query parameter and returns response in requested format. If requested format is not found, it informs the user. V2 is fault tolerant and in case no query parameter is sent, it responds in JSON as it is set as default parameter.
### Scalability
The services can scale well as demonstrated by the use of containers. We can easily increase service containers to handle the load using Kubernetes. Containerized version of application is using production grade servers so the solution is production ready. As both services are running in their respective containers so they can also scale independantly.
### Extendibility
Code is structured in a way that we can easily add new versions with little change to existing codebase.
### Data Store
Redis is being used as data store for this application. It can be easily replaced with persistent database.