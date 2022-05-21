from parser import VisionParser

parser = VisionParser()

parser.detect_text(file_path='./images/recipe_screenshot.png')
parser.parse_text()
parser.find_ingredients()
parser.write_ingredients()

print(parser.ingredient_list)
print(parser.ingredient_dict)


