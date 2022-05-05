class KeyValuePair:
    def __init__(self):
        self.key = None  # string
        self.value = None  # any


class Link:
    def __init__(self):
        self.url = None  # string
        self.text = None  # string


class Log:
    def __init__(self):
        self.timestamp = None  # number
        self.field = []  # array<keyvaluepari>


class Process:
    def __init__(self, process):
        self.servicename = process["serviceName"]
        self.tags = process["tags"]


class SpanReference:
    def __init__(self, ref_data, span):
        self.refType = ref_data["refType"]
        self.span = span
        self.spanID = ref_data["spanID"]
        self.traceID = ref_data["traceID"]


class Span:
    def __init__(self, span_id, span):
        self.spanID = span_id
        self.references = []
        self.traceID = span["traceID"]
        self.processID = span["processID"]
        self.operationName = span["operationName"]
        self.startTime = span["startTime"]
        self.duration = span["duration"]
        self.process = Process()
        self.depth = None
        self.hasChildren = True
        self.relativeStartTime = None
        self.subsidiarilyReferencedBy = []

class Trace:
    def __init__(self):
        self.traceID = None
        self.startTime = None
        self.endTime = None
        self.duration = None
        self.spans = []


data = {
    "data": [
        {
            "traceID": "af66c1b7dd41535b",
            "spans": [
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "af66c1b7dd41535b",
                    "flags": 1,
                    "operationName": "queryInfo",
                    "references": [],
                    "startTime": 1625848106793000,
                    "duration": 8565,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "sampler.type",
                            "type": "string",
                            "value": "const"
                        },
                        {
                            "key": "sampler.param",
                            "type": "bool",
                            "value": True
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/travelservice/trips/left"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "POST"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106793000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity travel.controller.TravelController.queryInfo(travel.entity.TripInfo,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "TravelController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryInfo"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106802000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity travel.controller.TravelController.queryInfo(travel.entity.TripInfo,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p1",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "6886bd87965bb5e1",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "af66c1b7dd41535b"
                        }
                    ],
                    "startTime": 1625848106794000,
                    "duration": 1839,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-ticketinfo-service:15681/api/v1/ticketinfoservice/ticketinfo/Xu%20Zhou"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 15681
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p1",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "5b52eae436dfef71",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "fc8d4109b97c740f"
                        }
                    ],
                    "startTime": 1625848106794000,
                    "duration": 1274,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-basic-service:15680/api/v1/basicservice/basic/Xu%20Zhou"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 15680
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p2",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "fc8d4109b97c740f",
                    "flags": 1,
                    "operationName": "queryForStationId",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "6886bd87965bb5e1"
                        }
                    ],
                    "startTime": 1625848106794000,
                    "duration": 1633,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/ticketinfoservice/ticketinfo/Xu%20Zhou"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106794000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity ticketinfo.controller.TicketInfoController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "TicketInfoController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryForStationId"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106795000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity ticketinfo.controller.TicketInfoController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p2",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "26f2559ec26dd671",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "ef150dcd70ea7c5b"
                        }
                    ],
                    "startTime": 1625848106794000,
                    "duration": 642,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-station-service:12345/api/v1/stationservice/stations/id/Xu%20Zhou"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 12345
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p3",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "ef150dcd70ea7c5b",
                    "flags": 1,
                    "operationName": "queryForStationId",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "5b52eae436dfef71"
                        }
                    ],
                    "startTime": 1625848106794000,
                    "duration": 1153,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/basicservice/basic/Xu%20Zhou"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106794000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity fdse.microservice.controller.BasicController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "BasicController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryForStationId"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106795000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity fdse.microservice.controller.BasicController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p3",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "864e017eedfa163a",
                    "flags": 1,
                    "operationName": "queryForStationId",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "26f2559ec26dd671"
                        }
                    ],
                    "startTime": 1625848106794000,
                    "duration": 491,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/stationservice/stations/id/Xu%20Zhou"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106794000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity fdse.microservice.controller.StationController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "StationController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryForStationId"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106794000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity fdse.microservice.controller.StationController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p4",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "4694776d84c1e38f",
                    "flags": 1,
                    "operationName": "queryForStationId",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "44d86d08f9ba3c5c"
                        }
                    ],
                    "startTime": 1625848106795000,
                    "duration": 1640,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/ticketinfoservice/ticketinfo/Jia%20Xing%20Nan"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106796000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity ticketinfo.controller.TicketInfoController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "TicketInfoController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryForStationId"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106797000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity ticketinfo.controller.TicketInfoController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p2",
                    "warnings": [
                        "clock skew adjustment disabled; not applying calculated delta of 1.0555ms"
                    ]
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "44d86d08f9ba3c5c",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "af66c1b7dd41535b"
                        }
                    ],
                    "startTime": 1625848106796000,
                    "duration": 1751,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-ticketinfo-service:15681/api/v1/ticketinfoservice/ticketinfo/Jia%20Xing%20Nan"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 15681
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p1",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "b69580963f1ea2d7",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "4694776d84c1e38f"
                        }
                    ],
                    "startTime": 1625848106796000,
                    "duration": 1277,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-basic-service:15680/api/v1/basicservice/basic/Jia%20Xing%20Nan"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 15680
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p2",
                    "warnings": [
                        "clock skew adjustment disabled; not applying calculated delta of 1.0555ms"
                    ]
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "d2b58b83ba56daa6",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "5eec1f3b5addb17d"
                        }
                    ],
                    "startTime": 1625848106796000,
                    "duration": 610,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-station-service:12345/api/v1/stationservice/stations/id/Jia%20Xing%20Nan"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 12345
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p3",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "5eec1f3b5addb17d",
                    "flags": 1,
                    "operationName": "queryForStationId",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "b69580963f1ea2d7"
                        }
                    ],
                    "startTime": 1625848106796000,
                    "duration": 1177,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/basicservice/basic/Jia%20Xing%20Nan"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106796000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity fdse.microservice.controller.BasicController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "BasicController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryForStationId"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106797000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity fdse.microservice.controller.BasicController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p3",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "863013301bc8609e",
                    "flags": 1,
                    "operationName": "queryForStationId",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "d2b58b83ba56daa6"
                        }
                    ],
                    "startTime": 1625848106796000,
                    "duration": 474,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/stationservice/stations/id/Jia%20Xing%20Nan"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106796000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity fdse.microservice.controller.StationController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "StationController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryForStationId"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106796000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity fdse.microservice.controller.StationController.queryForStationId(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p4",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "6d8d5de98baefe90",
                    "flags": 1,
                    "operationName": "queryById",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "38beb703d831e2c8"
                        }
                    ],
                    "startTime": 1625848106797000,
                    "duration": 513,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/routeservice/routes/92708982-77af-4318-be25-57ccb0ff69ad"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106797000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "RouteController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryById"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106798000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p5",
                    "warnings": [
                        "clock skew adjustment disabled; not applying calculated delta of 1.067ms"
                    ]
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "38beb703d831e2c8",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "af66c1b7dd41535b"
                        }
                    ],
                    "startTime": 1625848106798000,
                    "duration": 647,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-route-service:11178/api/v1/routeservice/routes/92708982-77af-4318-be25-57ccb0ff69ad"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 11178
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p1",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "943eae6942c4edd9",
                    "flags": 1,
                    "operationName": "queryById",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "337c835ea26a83bd"
                        }
                    ],
                    "startTime": 1625848106798000,
                    "duration": 486,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/routeservice/routes/aefcef3f-3f42-46e8-afd7-6cb2a928bd3d"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106798000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "RouteController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryById"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106799000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p5",
                    "warnings": [
                        "clock skew adjustment disabled; not applying calculated delta of 1.063ms"
                    ]
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "337c835ea26a83bd",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "af66c1b7dd41535b"
                        }
                    ],
                    "startTime": 1625848106799000,
                    "duration": 612,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-route-service:11178/api/v1/routeservice/routes/aefcef3f-3f42-46e8-afd7-6cb2a928bd3d"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 11178
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p1",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "e5744ef17a6cabb6",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "af66c1b7dd41535b"
                        }
                    ],
                    "startTime": 1625848106799000,
                    "duration": 624,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-route-service:11178/api/v1/routeservice/routes/a3f256c1-0e43-4f7d-9c21-121bf258101f"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 11178
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p1",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "75264cad98d9d8b5",
                    "flags": 1,
                    "operationName": "queryById",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "e5744ef17a6cabb6"
                        }
                    ],
                    "startTime": 1625848106799000,
                    "duration": 500,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/routeservice/routes/a3f256c1-0e43-4f7d-9c21-121bf258101f"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106799000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "RouteController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryById"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106799000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p5",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "a516153a43d90998",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "af66c1b7dd41535b"
                        }
                    ],
                    "startTime": 1625848106800000,
                    "duration": 575,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-route-service:11178/api/v1/routeservice/routes/084837bb-53c8-4438-87c8-0321a4d09917"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 11178
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p1",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "08b0c47443f68f9e",
                    "flags": 1,
                    "operationName": "queryById",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "a516153a43d90998"
                        }
                    ],
                    "startTime": 1625848106800000,
                    "duration": 460,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/routeservice/routes/084837bb-53c8-4438-87c8-0321a4d09917"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106800000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "RouteController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryById"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106800000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p5",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "801a5ea3da9796af",
                    "flags": 1,
                    "operationName": "GET",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "af66c1b7dd41535b"
                        }
                    ],
                    "startTime": 1625848106801000,
                    "duration": 565,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-spring-rest-template"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "client"
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-route-service:11178/api/v1/routeservice/routes/f3d4d4ef-693b-4456-8eed-59c0d717dd08"
                        },
                        {
                            "key": "peer.port",
                            "type": "int64",
                            "value": 11178
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [],
                    "processID": "p1",
                    "warnings": None
                },
                {
                    "traceID": "af66c1b7dd41535b",
                    "spanID": "5a57006240df705d",
                    "flags": 1,
                    "operationName": "queryById",
                    "references": [
                        {
                            "refType": "CHILD_OF",
                            "traceID": "af66c1b7dd41535b",
                            "spanID": "801a5ea3da9796af"
                        }
                    ],
                    "startTime": 1625848106801000,
                    "duration": 454,
                    "tags": [
                        {
                            "key": "http.status_code",
                            "type": "int64",
                            "value": 200
                        },
                        {
                            "key": "http.url",
                            "type": "string",
                            "value": "http://ts-travel-service:12346/api/v1/routeservice/routes/f3d4d4ef-693b-4456-8eed-59c0d717dd08"
                        },
                        {
                            "key": "component",
                            "type": "string",
                            "value": "java-web-servlet"
                        },
                        {
                            "key": "span.kind",
                            "type": "string",
                            "value": "server"
                        },
                        {
                            "key": "http.method",
                            "type": "string",
                            "value": "GET"
                        },
                        {
                            "key": "internal.span.format",
                            "type": "string",
                            "value": "proto"
                        }
                    ],
                    "logs": [
                        {
                            "timestamp": 1625848106801000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "preHandle"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                },
                                {
                                    "key": "handler.class_simple_name",
                                    "type": "string",
                                    "value": "RouteController"
                                },
                                {
                                    "key": "handler.method_name",
                                    "type": "string",
                                    "value": "queryById"
                                }
                            ]
                        },
                        {
                            "timestamp": 1625848106801000,
                            "fields": [
                                {
                                    "key": "event",
                                    "type": "string",
                                    "value": "afterCompletion"
                                },
                                {
                                    "key": "handler",
                                    "type": "string",
                                    "value": "public org.springframework.http.HttpEntity route.controller.RouteController.queryById(java.lang.String,org.springframework.http.HttpHeaders)"
                                }
                            ]
                        }
                    ],
                    "processID": "p5",
                    "warnings": None
                }
            ],
            "processes": {
                "p1": {
                    "serviceName": "ts-travel-service",
                    "tags": [
                        {
                            "key": "hostname",
                            "type": "string",
                            "value": "ts-travel-service-859cf49b6c-b4sx9"
                        },
                        {
                            "key": "ip",
                            "type": "string",
                            "value": "10.42.0.23"
                        },
                        {
                            "key": "jaeger.version",
                            "type": "string",
                            "value": "Java-0.30.6"
                        }
                    ]
                },
                "p2": {
                    "serviceName": "ts-ticketinfo-service",
                    "tags": [
                        {
                            "key": "hostname",
                            "type": "string",
                            "value": "ts-ticketinfo-service-6647bf5457-266q9"
                        },
                        {
                            "key": "ip",
                            "type": "string",
                            "value": "10.47.0.28"
                        },
                        {
                            "key": "jaeger.version",
                            "type": "string",
                            "value": "Java-0.30.6"
                        }
                    ]
                },
                "p3": {
                    "serviceName": "ts-basic-service",
                    "tags": [
                        {
                            "key": "hostname",
                            "type": "string",
                            "value": "ts-basic-service-66866df769-zcwld"
                        },
                        {
                            "key": "ip",
                            "type": "string",
                            "value": "10.42.0.17"
                        },
                        {
                            "key": "jaeger.version",
                            "type": "string",
                            "value": "Java-0.30.6"
                        }
                    ]
                },
                "p4": {
                    "serviceName": "ts-station-service",
                    "tags": [
                        {
                            "key": "hostname",
                            "type": "string",
                            "value": "ts-station-service-c9745b857-4dcl4"
                        },
                        {
                            "key": "ip",
                            "type": "string",
                            "value": "10.44.0.22"
                        },
                        {
                            "key": "jaeger.version",
                            "type": "string",
                            "value": "Java-0.30.6"
                        }
                    ]
                },
                "p5": {
                    "serviceName": "ts-route-service",
                    "tags": [
                        {
                            "key": "hostname",
                            "type": "string",
                            "value": "ts-route-service-6bf96b7976-7xnp6"
                        },
                        {
                            "key": "ip",
                            "type": "string",
                            "value": "10.44.0.21"
                        },
                        {
                            "key": "jaeger.version",
                            "type": "string",
                            "value": "Java-0.30.6"
                        }
                    ]
                }
            },
            "warnings": None
        }
    ],
    "total": 0,
    "limit": 0,
    "offset": 0,
    "errors": None
}
