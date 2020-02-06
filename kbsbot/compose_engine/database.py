from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Agent(db.Model):
    """Agent

    An Agent refers to the main o domain or purpose of the chatbot.

    Attributes:
        :param @id: Id to populate the database.

        :param @name: This name must be unique to identify the Agent.

        :param @about: A description of the purpose of the chatbot.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    about = db.Column(db.String(140), nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"


class Interaction(db.Model):
    """Interaction

    And interaction refers to a message that has not been classified.

    Attributes:
        :param @id: Id to populate the database.

        :param @message: A message not found by model

        :param @classified: If the message has been classified
    """
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300), nullable=False)
    classified = db.Column(db.Boolean, nullable=False, default=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'),
                         nullable=False)
    agent = db.relationship('Agent', backref=db.backref('interactions', lazy=True))

    def __repr__(self):
        return f"<Messsage {self.message}>"


def add_unclassified_message(agent, message):
    """
    This method adds a new unclassified message to the database.

    Parameters:
        :param agent: An agent that has the corresponding message

        :param message: A message to be stored

    """
    new_message = Interaction(message=message, agent=agent)
    db.session.add(new_message)
    db.session.commit()


def get_all_unclassified_messages(agent):
    """
    This method returns all of unclassified messages of an agent.

     Parameters:
        :param agent: An agent to retrieve all unclassified messages
    """
    final_interactions = []
    interactions = Interaction.query.filter_by(classified=False, agent=agent).all()
    for inter_aux in interactions:
        final_interactions.append({"message_id": inter_aux.id, "message": inter_aux.message})
    return final_interactions


def update_message_state(message_id):
    """
    This method changes the message status when it is classified.

      Parameters:
        :param message_id: the id of the message to be updated
    """
    message = Interaction.query.filter_by(id=message_id).first()
    message.classified = True
    db.session.add(message)
    db.session.commit()
    return message


def init_database():
    """
    This function is used to initially populate the database
    """
    exists = Agent.query.all()
    if exists is None or len(exists) == 0:
        agent = Agent(name='OpenCampus',
                      about="Este es el chabot de Open Campus capaz de resolver dudas sobre los diferentes cursos de la oferta actual de Open Campus")
        db.session.add(agent)
        db.session.commit()
