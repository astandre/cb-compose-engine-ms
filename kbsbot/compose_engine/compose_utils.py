import re


def clean_uri(uri):
    """
    This method removes the url part of the URI in order to obtain just the property or class

    :param uri: An uri to be cleaned

    :return: The name of the property or the class
    """

    if uri.find('#') != -1:
        special_char = '#'
    else:
        special_char = '/'
    index = uri.rfind(special_char)
    return uri[index + 1:len(uri)]


def check_requirements(requirements, entities):
    """
      This method compares the existing entities and the entities required to complete an intent.

      :param requirements: The list of the entities needed

      :param entities: The list of current entities

      :return: If entities are missing, a list of this missing entities
    """
    missing = requirements
    missing_status = True
    if len(requirements) > len(entities):
        return missing_status, missing
    else:
        for entity in entities:
            for i, needed_entity in enumerate(requirements):
                if entity["type"] == needed_entity:
                    del missing[i]
                    break

        if len(missing) == 0:
            missing_status = False
        return missing_status, missing


def build_answer(raw_answer, answer_type):
    """
    This method builds the answer, depending of the type of answer.

    :param raw_answer: A dict containing the template of the answer, and the different part of tha answer

    :param answer_type: The type of answer to be constructed

    :return: the raw text of the final answer
    """
    final_answer = None
    if answer_type == "text":
        final_answer = raw_answer["template"]
        re_template = re.compile(r"{%[a-zA-Z]*%}")
        found = re_template.findall(final_answer)
        for aux in found:
            simple_aux = aux.replace("{%", "")
            simple_aux = simple_aux.replace("%}", "")
            for answ in raw_answer["answer"]:
                if answ["property"] == simple_aux:
                    answer_aux = ""
                    for i, part in enumerate(answ["value"]):
                        if i + 1 < len(answ["value"]):
                            answer_aux += " " + part + ","
                        else:
                            answer_aux += " " + part
                    final_answer = final_answer.replace(aux, answer_aux)
                    break
    elif answer_type == "options":
        final_answer = "De que quieres conocer?"
        # TODO get template of requirments

    return final_answer


def update_entities(current_entities, new_entities):
    """
    This method updates the current list of entities, by looking for the same type of entity.

    Parameters:
     :param current_entities: Current list of entities

     :param new_entities: New list of entities

     :return: Current list of entities updated

    """
    if len(current_entities) == 0:
        current_entities = new_entities
    else:
        for i, c_entity in enumerate(current_entities):
            for n_entity in new_entities:
                if c_entity["type"] == n_entity["type"]:
                    current_entities[i] = n_entity
                    break
    return current_entities
