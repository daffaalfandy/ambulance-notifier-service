# RESTful API Documentation

## User

### User Registration

> Endpoint: /api/user
> Method: POST

```
Request:
    Header\['Content-Type'] = application/json
    Body: {
        "email": "email",
        "password": "password",
        "fullname": "fullname"
    }
Response: {
    "result": {
        "email": "email",
        "fullname": "fullname",
        "id_user": int,
        "password": null
    },
    "success": 1
}
```

### User Login

> Endpoint: /api/user/login
> Method: POST

```
Case 1:
    Request:
        Header\['Content-Type'] = application/json
        Body: {
            "email": "email",
            "password": "password",
        }
    Response: {
        "msg": "Login Successful",
        "success": 1,
        "user": {
            "email": "email",
            "fullname": "fullname"
        }
    }
Case 2:
    Request:
        Header\['Content-Type'] = application/json
        Body: {
            "email": "email",
        }
    Response: {
        "msg": "Missing email!",
        "success": 0
    }
Case 3:
    Request:
        Header\['Content-Type'] = application/json
        Body: {
            "password": "password",
        }
    Response: {
        "msg": "Missing password!",
        "success": 0
    }
Case 4:
    Request:
        Header\['Content-Type'] = application/json
        Body: {
            "email": "wrong email",
            "password": "password",
        }
    Response: {
        "msg": "Email not found!",
        "success": 0
    }
Case 5:
    Request:
        Header\['Content-Type'] = application/json
        Body: {
            "email": "email",
            "password": "wrong password",
        }
    Response: {
        "msg": "Wrong password!",
        "success": 0
    }
```

## Ambulance

### Get Ambulance by ID

> Endpoint: /api/ambulance/(id)
> Method: GET

```
Response: {
    "id_ambulance": 2,
    "license_plate": "AB 4321 DC",
    "origin": "Jl. Monjali, ",
    "status": 0,
    "type": "APV2"
}
```

### Update Status Ambulance by ID

> Endpoint: /api/ambulance/(id)
> Method: PUT

```
Request:
    Header\['Content-Type'] = application/json
    Body: {
        "status": int(0 or 1)
    }
Response: {
    "id_ambulance": 2,
    "license_plate": "AB 4321 DC",
    "origin": "Jl. Monjali, ",
    "status": 0,
    "type": "APV2"
}
```

## Ambulance Location

### Using socketio for connection

Endpoint: /socket.io
When connected to this, listening on 'status', if connected msg will be {'status': 'Connected', 'success': 1}  
For ambulance driver, please emit on 'ambulance_location' with data required  
For common user, please listening on 'broadcast_ambulance_location', message will be same as data provided from ambulance driver

## Running machine learning.

For running machine learning, please emit on 'predict' with empty payload, and listen to 'predict_result'
