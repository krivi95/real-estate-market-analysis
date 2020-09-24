from enum import Enum


class REGRESSION_SETTINGS(Enum):
    BACKUP_DIRECTORY = r'models/linear_regression_model'
    WEIGHTS = 'weights.txt'
    ENCODER = 'onehotencoder.pickle'
    SCALER = 'standardizer.pickle'

class CLASSIFICATION_SETTINGS(Enum):
    BACKUP_DIRECTORY = r'models/svm_model'
    MODEL = 'svm.pickle'
    ENCODER = 'onehotencoder.pickle'
    SCALER = 'standardizer.pickle'

class ML_MODEL(Enum):
    LINEAR_REGRESSION = 'Multiple linear regression'
    CLASSIFICATION = 'Classification (SVM)'

class CITY_DISTRICT(Enum):
    STARI_GRAD = 'Stari grad'
    ZVEZDARA = 'Zvezdara'
    VRACAR = 'Vracar'
    PALILULA = 'Palilula'
    NOVI_BEOGRAD = 'Novi Beograd'   
    CUKARICA = 'Cukarica' 
    SAVSKI_VENAC = 'Savski Venac'
    ZEMUN = 'Zemun'
    RAKOVICA = 'Rakovica'
    VOZDOVAC = 'Vozdovac'
    MLADENOVAC = 'Mladenovac'
    GROCKA = 'Grocka'
    LAZAREVAC = 'Lazarevac'
    OBRENOVAC = 'Obrenovac'
    SURCIN = 'Surcin'
    BARAJEVO = 'Barajevo'

class HEATING_TYPE(Enum):
    CENTRALNO = 'Centralno'
    ETAZNO = 'Etažno'
    GAS = 'Gas'
    KALJEVA_PEC = 'Kaljeva peć'
    NORVESKI_RADIJATORI = 'Norveški radijatori'
    PODNO = 'Podno'
    STRUJA = 'Struja'
    TA_PEC = 'TA peć'