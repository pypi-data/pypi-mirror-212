from freezegun import freeze_time
from .mock_service import BeginWorkerMock
import json

APP_ID = 1
LICENSE_KEY = 10


@freeze_time("2021-05-16")
def test_learn_from_data():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user": {
            "111": {
                "dateofbirth": "09-12-1989",
                "userlocation": {
                    "latitude": 36.8507689,
                    "longitude": -76.2858726
                },
                "numberfield": 10,
                "textfield": "Hello!",
                "user_specific_id": 100
            },
            "222": {
                "dateofbirth": "09-12-1990",
                "userlocation": {
                    "latitude": 36.8507689,
                    "longitude": -76.2858726
                },
                "numberfield": 120,
                "textfield": "Hellooooooo!",
                "user_specific_id": 200
            }
        },
        "interactions": {
            "111": {
                "noembedding": {
                    "20": {
                        "just_action": {
                            "created_at": 1234
                        },
                        "no_existing": {}
                    }
                },
                "product": {
                    "10": {
                        "dislike": {
                            "date": "08-12-1994",
                            "created_at": 1234
                        },
                        "like": {
                            "date": "10-12-1994",
                        },
                    },
                    "20": {
                        "like": {
                            "date": "08-03-1991"
                        }
                    },
                    "30": {
                        "comment": {
                            "commentLength": 12093
                        }
                    }
                }
            }
        },
        "product": {
            "10": {
                "description": "....the description...",
                "randomnumber": 100.0,
                "publisheddate": "09-12-1999",
                "randomnumberskippingmask": 100.0,
                "product_specific_id": 10
            },
            "20": {
                "description": "hi!",
                "randomnumber": 100.0,
                "publisheddate": "09-12-1991",
                "randomnumberskippingmask": 100.0,
                "product_specific_id": 20
            },
            "30": {
                "description": "hi!!",
                "randomnumber": 100.0,
                "publisheddate": "09-12-1991",
                "randomnumberskippingmask": 100.0,
                "product_specific_id": 30
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "user": {
            "111": {
                "embedding": [31.0, 3.0, 1.0, 6.0],
                "labels": [],
                "tokens": {
                    "input_ids": [],
                    "attention_mask": [],
                    "len_": 0
                },
                "identifiers": {
                    "user_specific_id": 100,
                    "another_user_specific_id": ""
                },
                "created_at": None
            },
            "222": {
                "embedding": [30.0, 3.0, 5.0, 12.0],
                "labels": [],
                "tokens": {
                    "input_ids": [],
                    "attention_mask": [],
                    "len_": 0
                },
                "identifiers": {
                    "user_specific_id": 200,
                    "another_user_specific_id": ""
                },
                "created_at": None
            }
        },
        "interactions": {
            "111": {
                "interactions": {
                    "noembedding": {
                        "20": {
                            "just_action": {
                                "embedding": None,
                                "created_at": 1234
                            }
                        }
                    },
                    "product": {
                        "10": {
                            "dislike": {
                                "embedding": [26.0],
                                "created_at": 1234
                            },
                            "like": {
                                "embedding": [26.0],
                                "created_at": None
                            }
                        },
                        "20": {
                            "like": {
                                "embedding": [30.0],
                                "created_at": None
                            }
                        },
                        "30": {
                            "comment": {
                                "embedding": [0.00011, 0.00011],
                                "created_at": None
                            }
                        }
                    }
                }
            }
        },
        "product": {
            "10": {
                "embedding": [22.0, 4.0, 21.0, 100.0],
                "labels": [],
                "tokens": {
                    "input_ids": [],
                    "attention_mask": [],
                    "len_": 0
                },
                "identifiers": {
                    "product_specific_id": 10
                },
                "created_at": None
            },
            "20": {
                "embedding": [3.0, 4.0, 29.0, 100.0],
                "labels": [],
                "tokens": {
                    "input_ids": [],
                    "attention_mask": [],
                    "len_": 0
                },
                "identifiers": {
                    "product_specific_id": 20
                },
                "created_at": None
            },
            "30": {
                "embedding": [4.0, 4.0, 29.0, 100.0],
                "labels": [],
                "tokens": {
                    "input_ids": [],
                    "attention_mask": [],
                    "len_": 0
                },
                "identifiers": {
                    "product_specific_id": 30
                },
                "created_at": None
            }
        }
    }
    assert json.dumps(result, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


@freeze_time("2021-05-16")
def test_learn_from_data_with_different_types_of_interaction():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user": {
            "111": {
                "dateofbirth": "09-12-1989",
                "userlocation": {
                    "latitude": 36.8507689,
                    "longitude": -76.2858726
                },
                "numberfield": 10,
                "textfield": "Hellooooooo!"
            }
        },
        "interactions": {
            "111": {
                "product": {
                    "10": {
                        "dislike": {
                            "date": "08-12-1994",
                        },
                        "like": {
                            "date": "10-12-1994",
                        },
                    },
                    "20": {
                        "like": {
                            "date": "08-03-1991"
                        }
                    },
                    "30": {
                        "comment": {
                            "commentLength": 12093
                        }
                    }
                },
                "user": {
                    "1234": {
                        "report": {
                            "date": "02-01-2020"
                        },
                        "dosomething": {
                            "created_at": 1234
                        }
                    }
                }
            }
        },
        "product": {
            "10": {
                "description": "....the description...",
                "randomnumber": 100.0,
                "publisheddate": "09-12-1990",
                "randomnumberskippingmask": 100.0
            },
            "20": {
                "description": "hi!",
                "randomnumber": 50.0,
                "publisheddate": "09-12-1991",
                "randomnumberskippingmask": 50.0
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "user": {
            "111": {
                "embedding": [31.0, 3.0, 1.0, 12.0],
                "labels": [],
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "identifiers": {
                    "user_specific_id": "",
                    "another_user_specific_id": ""
                },
                "created_at": None
            }
        },
        "interactions": {
            "111": {
                "interactions": {
                    "product": {
                        "10": {
                            "dislike": {
                                "embedding": [26.0],
                                "created_at": None
                            },
                            "like": {
                                "embedding": [26.0],
                                "created_at": None
                            }
                        },
                        "20": {
                            "like": {
                                "embedding": [30.0],
                                "created_at": None
                            }
                        },
                        "30": {
                            "comment": {
                                "embedding": [0.00011, 0.00011],
                                "created_at": None
                            }
                        }
                    },
                    "user": {
                        "1234": {
                            "report": {
                                "embedding": [1.0],
                                "created_at": None
                            },
                            "dosomething": {
                                "embedding": None,
                                "created_at": 1234
                            },
                        },
                    }
                }
            }
        },

        "product": {
            "10": {
                "embedding": [22.0, 4.0, 30.0, 100.0],
                "labels": [],
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "identifiers": {
                    "product_specific_id": ""
                },
                "created_at": None
            },
            "20": {
                "embedding": [3.0, 2.0, 29.0, 50.0],
                "labels": [],
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "identifiers": {
                    "product_specific_id": ""
                },
                "created_at": None
            }
        }
    }
    assert expected == result


@freeze_time("2022-05-16")
def test_learn_from_data_remove_empty_objects():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user": {
            "111": {}
        },
        "product": {
            "10": {
                "description": "....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991",
                "randomnumberskippingmask": 10.0
            },
            "20": {
                "description": "hi!",
                "randomnumber": 1,
                "publisheddate": "09-12-1993",
                "randomnumberskippingmask": 1.0
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "product": {
            "10": {
                "embedding": [22.0, 1.0, 30.0, 10.0],
                "labels": [],
                "identifiers": {
                    "product_specific_id": ""
                },
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "created_at": None
            },
            "20": {
                "embedding": [3.0, 1.0, 28.0, 1.0],
                "labels": [],
                "identifiers": {
                    "product_specific_id": ""
                },
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "created_at": None
            }
        }
    }
    assert expected == result


@freeze_time("2022-05-16")
def test_learn_from_returns_no_value_when_property_doesnt_exist():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "product": {
            "10": {
                "description": "....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991",
                "randomnumberskippingmask": 10.0
            },
            "20": {
                "description_doesnt_exist": "hi!",
                "randomnumber1": 1,
                "publisheddate": "09-12-1993",
                "randomnumberskippingmask": 1.0
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "product": {
            "10": {
                "embedding": [22.0, 1.0, 30.0, 10.0],
                "labels": [],
                "identifiers": {
                    "product_specific_id": ""
                },
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "created_at": None
            },
            "20": {
                "embedding": [0.00011, 0.00011, 28.0, 1.0],
                "labels": [],
                "identifiers": {
                    "product_specific_id": ""
                },
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "created_at": None
            }
        }
    }
    assert expected == result


@freeze_time("2022-05-16")
def test_learn_from_returns_removes_object_not_defined_in_schema():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "objectnotinschema": {
            "2": {
                "description": "blah"
            }
        },
        "product": {
            "10": {
                "description": "....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991",
                "randomnumberskippingmask": 10.0
            },
            "20": {
                "description_doesnt_exist": "hi!",
                "randomnumber1": 1,
                "publisheddate": "09-12-1993",
                "randomnumberskippingmask": 1.0
            }
        },
        "interactions": {
            "111": {
                "product": {
                    "10": {
                        "like": {
                            "date":  "08-12-1994",
                        },
                        "comment": {
                            "date": "08-12-1995"
                        }
                    },
                    "20": {
                        "dislike": {
                            "date": "08-12-1998"
                        },
                        "like": {
                            "date": "08-12-1999"
                        }
                    }
                },
                "objectnotinschema": {
                    "2": {
                        "report": {
                            "date": "08-12-1994"
                        }
                    }
                },
                "user": {
                    "1234": {
                        "followed": {
                            "date": "08-12-2001"
                        }
                    }
                }
            },
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "product": {
            "10": {
                "embedding": [22.0, 1.0, 30.0, 10.0],
                "labels": [],
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "identifiers": {
                    "product_specific_id": ""
                },
                "created_at": None
            },
            "20": {
                "embedding": [0.00011, 0.00011, 28.0, 1.0],
                "labels": [],
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "identifiers": {
                    "product_specific_id": ""
                },
                "created_at": None
            }
        },
        "interactions": {
            "111": {
                "interactions": {
                    "product": {
                        "10": {
                            "like": {
                                "embedding": [27.0],
                                "created_at": None
                            },
                            "comment": {
                                "embedding": [26.0, 0.00011],
                                "created_at": None
                            }
                        },
                        "20": {
                            "dislike": {
                                "embedding": [23.0],
                                "created_at": None
                            },
                            "like": {
                                "embedding": [22.0],
                                "created_at": None
                            }
                        },
                    },
                    "user": {
                        "1234": {
                            "followed": {
                                "embedding": [20.0],
                                "created_at": None
                            }
                        }
                    }
                }
            }
        }
    }
    assert expected == result


@freeze_time("2021-05-16")
def test_learn_from_data_with_labels():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user": {
            "111": {
                "dateofbirth": "09-12-1989",
                "userlocation": {
                    "latitude": 36.8507689,
                    "longitude": -76.2858726
                },
                "numberfield": 10,
                "textfield": "Hellooooooo!",
                "labels": ["fake"]
            }
        },
        "product": {
            "10": {
                "description": "....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991",
                "randomnumberskippingmask": 10.0,
                "labels": ["comedy"]
            },
            "20": {
                "description": "hi!",
                "randomnumber": 1,
                "publisheddate": "09-12-1993",
                "randomnumberskippingmask": 1.0,
                "labels": ["mystery"]
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "user": {
            "111": {
                "embedding": [31.0, 3.0, 1.0, 12.0],
                "labels": ["fake"],
                "identifiers": {
                    "user_specific_id": "",
                    "another_user_specific_id": ""
                },
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "created_at": None
            }
        },
        "product": {
            "10": {
                "embedding": [22.0, 1.0, 29.0, 10.0],
                "labels": ["comedy"],
                "identifiers": {
                    "product_specific_id": ""
                },
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "created_at": None
            },
            "20": {
                "embedding": [3.0, 1.0, 27.0, 1.0],
                "labels": ["mystery"],
                "identifiers": {
                    "product_specific_id": ""
                },
                "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
                "created_at": None
            }
        }
    }
    assert expected == result


@freeze_time("2021-05-16")
def test_learn_from_data_with_tokens():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.set_data({
        "user": {
            "111": {
                "dateofbirth": "09-12-1989",
                "userlocation": {
                    "latitude": 36.8507689,
                    "longitude": -76.2858726
                },
                "numberfield": 10,
                "textfield": "Hellooooooo!",
                "labels": ["fake"],
                "name": "Jane",
                "lastName": "Doe"
            }
        },
        "product": {
            "10": {
                "description": "....the description...",
                "randomnumber": 10.0,
                "publisheddate": "09-12-1991",
                "labels": ["comedy"],
                "gender": "fiction",
                "randomnumberskippingmask": 10.0
            },
            "20": {
                "description": "hi!",
                "randomnumber": 1,
                "publisheddate": "09-12-1993",
                "labels": ["mystery"],
                "gender": "romance",
                "randomnumberskippingmask": 1.0
            }
        }
    })

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = {
        "user": {
            "111": {
                "embedding": [31.0, 3.0, 1.0, 12.0],
                "labels": ["fake"],
                "identifiers": {
                    "user_specific_id": "",
                    "another_user_specific_id": ""
                },
                "tokens": {"input_ids": [101, 4869, 3527, 2063, 102, 0, 0], "attention_mask": [1, 1, 1, 1, 1, 0, 0], "len_": 5},
                "created_at": None
            }
        },
        "product": {
            "10": {
                "embedding": [22.0, 1.0, 29.0, 10.0],
                "labels": ["comedy"],
                "identifiers": {
                    "product_specific_id": ""
                },
                "tokens": {"input_ids": [101, 4349, 102, 0, 0, 0, 0], "attention_mask": [1, 1, 1, 0, 0, 0, 0], "len_": 3},
                "created_at": None
            },
            "20": {
                "embedding": [3.0, 1.0, 27.0, 1.0],
                "labels": ["mystery"],
                "identifiers": {
                    "product_specific_id": ""
                },
                "tokens": {"input_ids": [101, 7472, 102, 0, 0, 0, 0], "attention_mask": [1, 1, 1, 0, 0, 0, 0], "len_": 3},
                "created_at": None
            }
        }
    }
    assert expected == result
