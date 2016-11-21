Test Task "Resizing Image" on 21.11.16


Create a service to change the image size by two times.

Service should include:

• REST API server with two endpoints:
    ◦ for sending image to service
    ◦ for getting converted image

• Web page with table: image id, time of getting , time of end converting job.
* Table should update on-line through WebSocket.

Images should convert in the background.

You should use: django, django rest api, celery.

The project should contain:

• Deployment Guide
• API Guide
• Functional tests for WebSocket and API.

The project should be on github.