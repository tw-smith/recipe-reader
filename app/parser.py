import re

from google.cloud import vision
import io
import os
from fractions import Fraction
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './plenary-office-350505-6c86322600bb.json'

START_WORDS = ['ingredients', 'ingredient']
STOP_WORDS = ["method", "MЕТНOD", 'methods']
UNIT_STRINGS = ["tsp", "tbsp", "ml", "l", "g", "kg"]
SIZE_STRINGS = ["large", "medium", "small"]
EXCLUDE_STRINGS = ["chopped", "diced", "sliced", "grated"]


class VisionParser:
    # TODO: fucntionality to parse images and pdf
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self.ingredient_list = []
        self.ingredient_dict = []
        self.response = None

    def detect_text(self, file_path):
        with io.open(file_path, 'rb') as f:
            content = f.read()
        image = vision.Image(content=content)
        self.response = self.client.document_text_detection(image=image, image_context={"language_hints": ["en"]})

    def parse_text(self):
        doc = self.response.full_text_annotation
        breaks = vision.TextAnnotation.DetectedBreak.BreakType
        p_string = ""
        stop_found = False
        start_found = False

        for page in doc.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            p_string += symbol.text
                            if symbol.property.detected_break.type == breaks.SPACE:
                                p_string += " "
                            if symbol.property.detected_break.type == breaks.LINE_BREAK or symbol.property.detected_break.type == breaks.EOL_SURE_SPACE:
                                self.ingredient_list.append(p_string)
                                p_string = ""

        for count, entry in enumerate(self.ingredient_list):
            for stopword in STOP_WORDS:
                if stopword in entry.lower():
                    stop_index = count
                    stop_found = True
                    break
            for startword in START_WORDS:
                if startword in entry.lower():
                    start_index = count + 1
                    start_found = True
                    break

        # If we have found start and stop keywords, use those indices. Otherwise just parse all text
        if start_found and stop_found:
            self.ingredient_list = self.ingredient_list[start_index:stop_index]
        else:
            pass

    def find_ingredients(self):
        unit_str = []
        size_str = []
        for count, entry in enumerate(self.ingredient_list):
            # REMOVE THINGS LIKE "DICED" OR "FINELY CHOPPED"
            # These often come after a comma, so throw away anything after a comma TODO: and hypen? and open bracket?
            entry = entry.split(", ")
            self.ingredient_list[count] = entry[0]

            # Remove any words in the blacklist
            for word in EXCLUDE_STRINGS:
                self.ingredient_list[count] = re.sub(word, "", self.ingredient_list[count])

            # LOOK FOR SIZES
            for size in SIZE_STRINGS:
                size_str = re.findall(size, self.ingredient_list[count])
                if size_str:
                    self.ingredient_list[count] = re.sub(size, "", self.ingredient_list[count])
                    break

            # LOOK FOR UNITS
            for unit in UNIT_STRINGS:
                if unit in ["g", "kg", "l", "ml"]:
                    regex = "(?<=[0-9])" + unit  # Seems to be reasonable to assume that these units won't have preceding space (avoids chop off of first letter of following word)
                else:
                    regex = "(?<=[0-9]) ?" + unit
                unit_str = re.findall(regex, self.ingredient_list[count])
                if unit_str:
                    self.ingredient_list[count] = re.sub(regex, "", self.ingredient_list[count])
                    break

            # LOOK FOR QUANTITY VALUES
            # Check for fractions
            regex = "[0-9]/[0-9]"
            if re.findall(regex, self.ingredient_list[count]):
                quant_str = re.findall(regex, self.ingredient_list[count])
                quant_str[0] = str(float(Fraction(quant_str[0])))
            else:
                regex = "[0-9]+"
                quant_str = re.findall(regex, self.ingredient_list[count])
            self.ingredient_list[count] = re.sub(regex, "", self.ingredient_list[count])

            ing_string = self.ingredient_list[count].strip()  # anything left is probably the ingredient

            tmp_dict = {
                "quant": "".join(quant_str),
                "unit": "".join(unit_str),
                "size": "".join(size_str),
                "ingredient": ing_string,
            }
            self.ingredient_dict.append(tmp_dict)

    def return_for_flask(self):
        return self.ingredient_dict

    def write_ingredients(self):
        with open("./output/convert.txt", "w") as convert_file:
            for entry in self.ingredient_dict:
                for key, value in entry.items():
                    convert_file.write('%s:%s\n' % (key, value))
                convert_file.write('\n\n')
