from beginai.exec.embeddings.worker import BeginWorker
from beginai.orchapi.api import OrchAPI


class BeginWorkerMock(BeginWorker):

    def __init__(self, app_id, license_key):
        super().__init__(app_id, license_key)
        self.orchapi = _FakeOrchAPI()

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_embeddings(self):
        return self.orchapi.embeddings


class _FakeOrchAPI(OrchAPI):

    def fetch_instructions(self):
        instructions_id = 1
        version_number = 0
        instructions_list = {
            "instructions": {
                "objects": {
                    "user": [
                        {
                            "instruct": "Age",
                            "complexity": 1,
                            "params": {},
                            "f_id": "dateOfBirth",
                        },
                        {
                            "_chains": [
                                [
                                    {
                                        "instruct": "Age",
                                        "complexity": 1,
                                        "params": {

                                        },
                                        "order": 1
                                    },
                                    {
                                        "instruct": "Slice",
                                        "complexity": 1,
                                        "params": {
                                            "minv": 10,
                                            "maxv": 100,
                                            "num_slices": 10,
                                            "skip_masking": False
                                        },
                                        "order": 2
                                    }
                                ]
                            ],
                            "f_id": "dateOfBirth",
                        },
                        {
                            "instruct": "Slice",
                            "complexity": 1,
                            "params": {
                                "minv": 0,
                                "maxv": 255,
                                "num_slices": 10,
                                "skip_masking": False
                            },
                            "f_id": "numberField",
                        },
                        {
                            "instruct": "Length",
                            "complexity": 1,
                            "params": {

                            },
                            "f_id": "textField",
                        }
                    ],
                    "product": [{
                        "instruct": "Length",
                        "complexity": 1,
                        "params": {

                        },
                        "f_id": "description",
                    },
                        {
                            "instruct": "Slice",
                            "complexity": 1,
                            "params": {
                                "minv": 0,
                                "maxv": 255,
                                "num_slices": 10,
                                "skip_masking": False
                            },
                            "f_id": "randomNumber",
                    },
                        {
                            "instruct": "Age",
                            "complexity": 1,
                            "params": {

                            },
                            "f_id": "publishedDate",
                    },
                        {
                            "instruct": "Slice",
                            "complexity": 1,
                            "params": {
                                "minv": 0,
                                "maxv": 255,
                                "num_slices": 10,
                                "skip_masking": True
                            },
                            "f_id": "randomnumberskippingmask",
                    }
                    ],
                },
                "interactions": {
                    "noembedding": {
                        "actions": ["just_action"],
                        "instructions": {}
                    },
                    "user": {
                        "actions": ["followed", "report", "dosomething"],
                        "instructions": {
                            "followed": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ],
                            "report": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ]
                        }
                    },
                    "product": {
                        "actions": ["like", "dislike", "comment"],
                        "instructions": {
                            "like": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ],
                            "dislike": [
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ],
                            "comment": [
                                {
                                    "instruct": "Length",
                                    "complexity": 1,
                                    "params": {},
                                    "f_id": "commentLength",
                                },
                                {
                                    "instruct": "Age",
                                    "complexity": 1,
                                    "params": {
                                    },
                                    "f_id": "date",
                                }
                            ]
                        }}
                },
            },
            "tokenize": {
                "user": [
                    "name",
                    "lastName"
                ],
                "product": [
                    "gender",
                    "name"
                ]
            },
            "labels": {
                "user": ["fake", "not_fake"],
                "product": ["fiction", "comedy", "mystery"]
            },
            "identifiers": {
                "user": ["user_specific_id", "another_user_specific_id"],
                "product": ['product_specific_id']
            },
            "embedding_template": {
                "objects": {
                    "user": ["dateOfBirth", "chain_instruction__Age__user__dateOfBirth", "chain_instruction__Slice__user__dateOfBirth", "numberField", "textField"],
                    "product": ["description", "randomNumber", "publishedDate", "randomnumberskippingmask"]
                },
                "interactions": {
                    "user": {
                        "followed": ["date"],
                        "report": ["date"]
                    },
                    "product": {
                        "like": ["date"],
                        "dislike": ["date"],
                        "comment": ["date", "commentLength"]
                    }
                }
            }
        }
        return instructions_id, version_number, instructions_list

    def submit_embeddings(self, embeddings, instruction_id, version_number):
        self.embeddings = embeddings
