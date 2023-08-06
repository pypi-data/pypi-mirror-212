m1 = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type" : "object",
    "properties" : {
        "version" : {"type" : "integer"},
        "reference" : {"type" : "string"},
        "doi": {"type": "string"},
        "name": {"type": "string"},
        "potential" : {
            "type" : "array",
            "items": {"type": "object",
                      "properties": {
                          "type": {"type": "string"},
                          "parameters": {"type": "object"},
                      },
                      "required": ["type", "parameters"]
            }
        },
        "cutoff" : {
            "type" : "array",
            "items" : {"type": "object",
                      "properties": {
                          "type": {"type": "string"},
                          "parameters": {"type": "object"},
                      },
                      "required": ["type", "parameters"]
            }
        },
        "notes": {"type": "string"}
    },
    "required": ["potential", "cutoff"]
}

m2 = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type" : "object",
    "properties" : {
        "version" : {"type" : "integer"},
        "reference" : {"type" : "string"},
        "doi": {"type": "string"},
        "name": {"type": "string"},
        "notes": {"type": "string"},
        "potential" : {
            "type" : "array",
            "items": {"type": "object",
                      "properties": {
                          "type": {"type": "string"},
                          "parameters": {"type": "object"},
                          "cutoff": {"type": "object"}
                      },
                      "required": ["type", "parameters", "cutoff"]
            }
        },
    },
    "required": ["potential"]
}
