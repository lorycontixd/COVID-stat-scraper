import subprocess
import mylogger as ml

class Utility():
    def __init__(self):
        self.l = ml.Logger()

    @staticmethod
    def validate_driver(driver:str):
        valid = ["chrome","safari","firefow","opera","edge"]
        if driver.lower() not in valid:
            raise ValueError(f"Driver {driver} not supported or doesn't exist.")
        
    @staticmethod
    def RepresentsInt(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def RepresentFloat(s):
        try: 
            float(s)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def check_chromedriver(logger=None):
        result = subprocess.run(["which","chromedriver"],capture_output=True)
        out = result.stdout.decode("utf-8")
        if len(out)<=0:
            if logger is not None:
                logger.warning("No version of chromedriver was detected ---> Installing...")
            subprocess.run(["pip","install","chromedriver"])

            result = subprocess.run(["which","chromedriver"],capture_output=True)
            out = result.stdout.decode("utf-8")

        else:
            if logger is not None:
                logger.info(f"Chromedriver version detected at path:\t{out}")

        return out