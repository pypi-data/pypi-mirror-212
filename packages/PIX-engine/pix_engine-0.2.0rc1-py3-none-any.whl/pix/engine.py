import logging
import pyfiglet

# Set up basic configuration
logging.basicConfig(
    format='%(asctime)s | %(name)s - %(levelname)s: %(message)s',
    level=logging.DEBUG,
    filename="pix.log")

# Create a logger
log = logging.getLogger("PIX RUNTIME")


class Data:
    def save(variable, filename):
        with open(filename, 'a') as file:
            file.write(str(variable) + '\n')
            log.debug(f"Data ({variable}) was saved to the file, {filename}")

    def load(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Remove newline characters and create a list of variables
        variables = [line.strip() for line in lines]

        # Create a dictionary to store the variables
        obj = {}

        # Assign the variables to dictionary keys
        for i, variable in enumerate(variables):
            obj[f'var{i}'] = variable
        log.debug(f"All saved wariables from {filename} has been loaded.")
        return obj


class UI:

    def draw(text, font="standard"):
        ascii_text = pyfiglet.figlet_format(text, font=font)
        return ascii_text and log.info(f"Experimental: Draw was successful in converting {text} into ASCII")
        
