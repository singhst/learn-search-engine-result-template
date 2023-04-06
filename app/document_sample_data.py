SAMPLE_DOCUMENTS = [
    {
        "url_id": 1,
        "score": "0.90123",
        "title": "Chicken Vesuvio",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
        "last_modification_date": "xxxx",
        "size_of_page": "111",
        "keywords": [
            {"word": "w1", "frequency": 4},
            {"word": "w2", "frequency": 83},
            {"word": "w3", "frequency": 1},
            {"word": "w4", "frequency": 9},
            {"word": "w5", "frequency": 7},
        ],
        "parent_links": [
            {"url_id": 1, "link": "p_link1"},
            {"url_id": 1, "link": "p_link2"},
        ],
        "child_links": [
            {"url_id": 1, "link": "c_link1"},
            {"url_id": 1, "link": "c_link2"},
            {"url_id": 1, "link": "c_link3"},
            {"url_id": 1, "link": "c_link4"},
            {"url_id": 1, "link": "c_link5"},
        ]
    },
    {
        "url_id": 2,
        "score": "0.88472",
        "title": "Chicken Paprikash",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
        "last_modification_date": "xxxx",
        "size_of_page": "222",
        "keywords": [
            {"word": "w1", "frequency": 3},
            {"word": "w2", "frequency": 8},
            {"word": "w3", "frequency": 54},
            {"word": "w4", "frequency": 93},
            {"word": "w5", "frequency": 238},
        ],
        "parent_links": [
            {"url_id": 2, "link": "p_link1"},
            {"url_id": 2, "link": "p_link2"},
            {"url_id": 2, "link": "p_link3"},
            {"url_id": 2, "link": "p_link4"},
        ],
        "child_links": [
            {"url_id": 2, "link": "c_link1"},
            {"url_id": 2, "link": "c_link2"},
        ]
    },
    {
        "url_id": 3,
        "score": "0.50795",
        "title": "Cauliflower and Tofu Curry Recipe",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
        "last_modification_date": "xxxx",
        "size_of_page": "333",
        "keywords": [
            {"word": "w1", "frequency": 132},
            {"word": "w2", "frequency": 432},
            {"word": "w3", "frequency": 96},
            {"word": "w4", "frequency": 56},
            {"word": "w5", "frequency": 17},
        ],
        "parent_links": [
            {"url_id": 2, "link": "p_link1"},
            {"url_id": 2, "link": "p_link2"},
            {"url_id": 2, "link": "p_link3"},
        ],
        "child_links": [
            {"url_id": 2, "link": "c_link1"},
        ]
    },
]

SAMPLE_DOCUMENTS = [
    {
        "url_id": 1,
        "title": "title1",
        "url": "http://1.com",
        "last_modification_date": "xxxxxxxx 1",
        "size_of_page": 324,
        "keywords": [
            {
                "url_id": 1,
                "term_id": 1,
                "term_freq": 12,
                "term": "keyword1"
            },
            {
                "url_id": 1,
                "term_id": 2,
                "term_freq": 53,
                "term": "keyword2"
            },
            {
                "url_id": 1,
                "term_id": 3,
                "term_freq": 2352,
                "term": "keyword3"
            },
            {
                "url_id": 1,
                "term_id": 4,
                "term_freq": 34,
                "term": "keyword4"
            },
            {
                "url_id": 1,
                "term_id": 5,
                "term_freq": 7,
                "term": "keyword5"
            }
        ],
        "parent_links": [
            {
                "url_id": 3,
                "url": "http://3.com"
            }
        ],
        "child_links": [
            {
                "child_url_id": 2,
                "url": "http://2.com"
            },
            {
                "child_url_id": 3,
                "url": "http://3.com"
            }
        ]
    },
    {
        "url_id": 2,
        "title": "title2",
        "url": "http://2.com",
        "last_modification_date": "xxxxxxxx 2",
        "size_of_page": 91238,
        "keywords": [
            {
                "url_id": 2,
                "term_id": 2,
                "term_freq": 441,
                "term": "keyword2"
            },
            {
                "url_id": 2,
                "term_id": 3,
                "term_freq": 142,
                "term": "keyword3"
            },
            {
                "url_id": 2,
                "term_id": 7,
                "term_freq": 84,
                "term": "keyword7"
            },
            {
                "url_id": 2,
                "term_id": 8,
                "term_freq": 529,
                "term": "keyword8"
            }
        ],
        "parent_links": [
            {
                "url_id": 1,
                "url": "http://1.com"
            },
            {
                "url_id": 2,
                "url": "http://2.com"
            }
        ],
        "child_links": [
            {
                "child_url_id": 2,
                "url": "http://2.com"
            },
            {
                "child_url_id": 3,
                "url": "http://3.com"
            }
        ]
    },
    {
        "url_id": 3,
        "title": "title3",
        "url": "http://3.com",
        "last_modification_date": "xxxxxxxx 3",
        "size_of_page": 47,
        "keywords": [
            {
                "url_id": 3,
                "term_id": 4,
                "term_freq": 4232,
                "term": "keyword4"
            },
            {
                "url_id": 3,
                "term_id": 5,
                "term_freq": 24,
                "term": "keyword5"
            },
            {
                "url_id": 3,
                "term_id": 9,
                "term_freq": 2412,
                "term": "keyword9"
            }
        ],
        "parent_links": [
            {
                "url_id": 1,
                "url": "http://1.com"
            },
            {
                "url_id": 2,
                "url": "http://2.com"
            }
        ],
        "child_links": [
            {
                "child_url_id": 1,
                "url": "http://1.com"
            }
        ]
    }
]