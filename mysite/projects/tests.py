from django.test import TestCase

# Create your tests here.
xpath = "(//div[contains(@data-cel-widget,'MAIN-TEXT_REFORMULATION-50')]//span/div/div/div/div)[1]//a/////@href"
xpath_list = xpath.split('/')
if xpath_list[-1][0] == "@":
    xpath = xpath.removesuffix(xpath_list[-1])
    while xpath[-1] == '/':
        xpath = xpath.removesuffix('/')
print(xpath)