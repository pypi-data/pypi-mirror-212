LIN_INSTANCE_TYPES = [
    {
        "cores": 8,
        "memory": 30.0,
        "description": "8 core, 30GB Mem",
        "name": "n1-standard-8",
        "operating_system": "linux",
    },
    {
        "cores": 64,
        "memory": 416.0,
        "description": "64 core, 416GB Mem",
        "name": "n1-highmem-64",
        "operating_system": "linux",
    },
    {
        "cores": 4,
        "memory": 27.0,
        "description": "4 core, 27GB Mem",
        "name": "n1-highmem-4",
        "operating_system": "linux",
    },
    {
        "cores": 32,
        "memory": 208.0,
        "description": "32 core, 208GB Mem",
        "name": "n1-highmem-32",
        "operating_system": "linux",
    },
]

WIN_INSTANCE_TYPES = [
    {
        "cores": 64,
        "memory": 416.0,
        "description": "64 core, 416GB Mem w",
        "name": "n1-highmem-64-w",
        "operating_system": "windows",
    },
    {
        "cores": 4,
        "memory": 26.0,
        "description": "4 core, 26GB Mem w",
        "name": "n1-highmem-4-w",
        "operating_system": "windows",
    },
    {
        "cores": 32,
        "memory": 208.0,
        "description": "32 core, 208GB Mem w",
        "name": "n1-highmem-32-w",
        "operating_system": "windows",
    },
]

ALL_INSTANCE_TYPES = WIN_INSTANCE_TYPES + LIN_INSTANCE_TYPES


CW_INSTANCE_TYPES = [
    {
        "cores": 4,
        "memory": 16,
        "name": "4-16",
        "categories": [{"label": "low", "order": 1}, {"label": "extra", "order": 9}],
        "operating_system": "linux",
        "description": "Desc 4 C 16 M",
    },
    {
        "cores": 8,
        "memory": 16,
        "name": "8-16",
        "categories": [{"label": "low", "order": 1}],
        "operating_system": "linux",
        "description": "Desc 8 C 16 M",
    },
    {
        "cores": 4,
        "memory": 32,
        "name": "4-32",
        "categories": [{"label": "mid", "order": 2}, {"label": "extra", "order": 9}],
        "operating_system": "linux",
        "description": "Desc 4 C 32 M",
    },
    {
        "cores": 8,
        "memory": 32,
        "name": "8-32",
        "categories": [{"label": "mid", "order": 2}],
        "operating_system": "linux",
        "description": "Desc 8 C 32 M",
    },
    {
        "cores": 4,
        "memory": 64,
        "name": "4-32",
        "categories": [{"label": "high", "order": 3}, {"label": "extra", "order": 9}],
        "operating_system": "linux",
        "description": "Desc 4 C 32 M",
    },
    {
        "cores": 8,
        "memory": 64,
        "name": "8-32",
        "categories": [{"label": "high", "order": 3}],
        "operating_system": "linux",
        "description": "Desc 8 C 32 M",
    },
]
