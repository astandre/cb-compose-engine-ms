import unittest
from kbsbot.compose_engine.compose_utils import *


class TestUtils(unittest.TestCase):

    def test_clean_uri(self):
        uri = clean_uri("http://127.0.0.1/ockb/resources/Course")
        self.assertEqual(uri, "Course")
        uri = clean_uri("http://127.0.0.1/ockb/ontology/endDate")
        self.assertEqual(uri, "endDate")

    def test_build_answer(self):
        # Testing best scenario
        answer_dict = {
            "answer": [
                {
                    "property": "endDate",
                    "value": [
                        "24 Nov 2019"
                    ]
                },
                {
                    "property": "beginDate",
                    "value": [
                        "14 Oct 2019"
                    ]
                }
            ],
            "template": "Las fechas importantes del curso son {%beginDate%} y termina el dia {%endDate%}"
        }
        answer = build_answer(answer_dict, "text")
        self.assertIn(answer_dict["answer"][0]["value"][0], answer["text"])
        self.assertIn(answer_dict["answer"][1]["value"][0], answer["text"])
        # Testing missing property
        answer_dict = {
            "answer": [
                {
                    "property": "beginDate",
                    "value": [
                        "14 Oct 2019"
                    ]
                }
            ],
            "template": "Las fechas importantes del curso son {%beginDate%} y termina el dia {%endDate%}"
        }
        answer = build_answer(answer_dict, "text")
        self.assertIn("{%endDate%}", answer["text"])
        # Testing missing value
        answer_dict = {
            "answer": [
                {
                    "property": "endDate",
                    "value": []
                },
                {
                    "property": "beginDate",
                    "value": [
                        "14 Oct 2019"
                    ]
                }
            ],
            "template": "Las fechas importantes del curso son {%beginDate%} y termina el dia {%endDate%}"
        }
        answer = build_answer(answer_dict, "text")
        self.assertNotIn("24 Nov 2019", answer["text"])

        # Testing list values
        answer_dict = {
            "answer": [
                {
                    "property": "courseName",
                    "value": [
                        "Uso de las tecnologías de la información y la comunicación  ",
                        "Microbiología Ambiental y Agrícola ",
                        "Razonamiento Abstracto  ",
                        "Métodos alternativos de resolución de conflictos ",
                        "Introducción a la Economía ",
                        "Realidad Nacional ",
                        "Economía a tu alcance ",
                        "Orientación Vocacional ",
                        "Producción Audiovisual ",
                    ]
                }
            ],
            "template": "Los cursos de la oferta actual son: {%courseName%}"
        }
        answer = build_answer(answer_dict, "text")

        for value in answer_dict["answer"][0]["value"]:
            self.assertIn(value, answer["text"])

        answer_dict = {"options": {
            "entity": "http://127.0.0.1/ockb/course/ontology/Course",
            "options": [
                {
                    "option": "Desarrollo comunitario ",
                    "payload": "http://127.0.0.1/ockb/resources/CD12"
                },
                {
                    "option": "Fundamentos matemáticos ",
                    "payload": "http://127.0.0.1/ockb/resources/MATHFUND2"
                }
            ]},
            "template": "De que curso quieres conocer"
        }
        answer = build_answer(answer_dict, "options")
        self.assertIn(answer_dict["template"], answer["text"])

    def test_check_requirements(self):
        # Testing best scenario
        requirements = ["http://127.0.0.1/ockb/course/ontology/Course"]
        entities = [{"type": "http://127.0.0.1/ockb/course/ontology/Course",
                     "value": "http://127.0.0.1/ockb/resources/EAIG5"}]
        missing_status, missing = check_requirements(requirements, entities)
        self.assertEqual(missing_status, False)
        # Testing no requirements
        requirements = []
        entities = [{"type": "http://127.0.0.1/ockb/course/ontology/Course",
                     "value": "http://127.0.0.1/ockb/resources/EAIG5"}]
        missing_status, missing = check_requirements(requirements, entities)
        self.assertEqual(missing_status, False)
        # Testing no entities
        requirements = ["http://127.0.0.1/ockb/course/ontology/Course"]
        entities = []
        missing_status, missing = check_requirements(requirements, entities)
        self.assertEqual(missing_status, True)
        # Testing multiple needs
        requirements = ["http://127.0.0.1/ockb/course/ontology/Course", "http://127.0.0.1/ockb/course/ontology/Teacher"]
        entities = [{"type": "http://127.0.0.1/ockb/course/ontology/Course",
                     "value": "http://127.0.0.1/ockb/resources/EAIG5"}]
        missing_status, missing = check_requirements(requirements, entities)
        self.assertEqual(missing_status, True)

    def test_update_entities(self):
        result = update_entities(
            [{'type': 'http://127.0.0.1/ockb/course/ontology/Course',
              'value': 'http://127.0.0.1/ockb/resources/INTRECON2'},
             {'type': 'http://127.0.0.1/ockb/course/ontology/Cosas',
              'value': 'http://127.0.0.1/ockb/resources/INTRECON2'}],
            [{'type': 'http://127.0.0.1/ockb/course/ontology/Course', 'value': 'http://127.0.0.1/ockb/resources/MSPV'}])
        self.assertTrue(len(result) == 2)

        result = update_entities([],
                                 [{'type': 'http://127.0.0.1/ockb/course/ontology/Course',
                                   'value': 'http://127.0.0.1/ockb/resources/MSPV'}])
        self.assertTrue(len(result) == 1)
