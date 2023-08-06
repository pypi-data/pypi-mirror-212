from enum import Enum



class ExerciseRelationKind(Enum):
    SUBSCRIBER = "subscriber"
    CREATOR = "creator"


class ROLE(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    USER = "user"


class ExerciseKind(Enum):
    PRIVATE_ROOM = "Salon privé"
    TRAINING = "Exercice d'entrainement"
    COMPETITION = "Compétition"

class ProgramingLanguage(Enum):
    PYTHON = "Python"

class SubmissionKind(Enum):
    SOLVE = "solve"
    TEMPLATE = "template"