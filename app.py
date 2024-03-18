from application import app
from application.routes import *
import warnings




if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=UserWarning)
    app.run(debug=True)
 