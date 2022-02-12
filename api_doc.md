# API Documentation

## Endpoints

https://ecourse.cpe.ku.ac.th/exceed10/api

## Bathroom model structure

```json
{
    "room_number": 1, // int, from 1-3
    "status": false, // boolean, true if occupied, false if not
    "last_update": "2022-02-12 11:47:08.453951", // datetime
    "total_time": 106.768687, // float in second
    "total_session": 5 // int
}
```

## Reset all the data in the database to the default

> POST /bathroom/reset

Reset all the data in the database to the default

The default data is:

```json
{
    "room_number": i,
    "status": false,
    "last_update": current_time,
    "total_time": 0,
    "total_session": 0
}
```

Example response (200):

```json
{
    "message": "Reset all the data in the database to the default successfully"
}
```

## Get all bathroom details

> GET /bathroom/get/all

Example response:

```json
[
    {
        "room_number": 1,
        "status": false,
        "last_update": "2022-02-12 12:22:46.535424",
        "total_time": 65.387313,
        "total_session": 2
    },
    {
        "room_number": 2,
        "status": false,
        "last_update": "2022-02-12 12:23:03.774329",
        "total_time": 80.09358900000001,
        "total_session": 2
    },
    {
        "room_number": 3,
        "status": false,
        "last_update": "2022-02-12 12:23:16.478801",
        "total_time": 90.19993099999999,
        "total_session": 2
    }
]
```

## Get specific detail of the bathroom by number

> GET /bathroom/get/{room_number}

room_number: int, from 1-3

Will return 404 if the target room_number is not found

Example response (200):
```json
{
    "room_number": 1,
    "status": false,
    "last_update": "2022-02-12 12:22:46.535424",
    "total_time": 65.387313,
    "total_session": 2
}
```

Example response (404):
```json
{
    "message": "Target bathroom not found"
}
```

## Calculate the average time from all bathroom

> GET /bathroom/get/average/all

Example response:

```json
{
    "total_time_all_room": 235.680833,
    "total_session_all_room": 6,
    "average_time": 39.28013883333333
}
```

## Calculate the average time from specific room

> GET /bathroom/get/average/{room_number}/

room_number: int, from 1-3

Will return 404 if the target room_number is not found

Example response (200):

```json
{
    "total_time": 65.387313,
    "total_session": 2,
    "average_time": 32.6936565
}
```

Example response (404):
```json
{
    "message": "Target bathroom not found"
}
```

## Put a new status to the target bathroom

> PUT /bathroom/change/{room_number}/{status}

room_number: int, from 1-3
status: boolean, true if occupied, false if not (to not make the conflict between backend and hardware, if conflict occurs, the status will not change and return 400)

Example response (200):

```json
{
    "message": "Update status success"
}
```

Example response (400):

```json
{
    "detail": "Status is same with database"
}
```