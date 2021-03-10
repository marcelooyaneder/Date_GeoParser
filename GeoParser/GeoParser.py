import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from ast import literal_eval
import math
import utm
import requests
import json
import pandas as pd
import numpy as np


driver = webdriver.Chrome(executable_path=r'C:\Users\marcelo\Documents\chromedriver_win32\chromedriver.exe')
driver.get("https://georeferencing.org/georefcalculator/gci3/source/gci3.html")


class SeleniumGeoref:

    #Controlled vocabulary     
    COORD_SYSTEM_DIC={   
        "decimal degrees": 0,
        "degrees minutes seconds": 2,
        "degrees decimal minutes": 1
    }
    PRECISION_DD={
        0.1:1, #0.1
        0.01:2, #0.01
        0.001:3, #0.001
        0.0001:4, #0.0001
        0.00001:5, #0.00001
    }
    PRECISION_DDM={
        0.1:5, #0.1
        0.01:6, #0.01
        0.001:7, #0.001
    }
    PRECISION_DMS={
        0.1:9, #0.1
        0.01:10, #0.01
    }
    DistUnits={
        "km":0,
        "m":1,
        "mi":2,
        "yds":3,
        "ft":4,
        "nm":5,
    }
    COORDINATE_SOURCE={
        "gazetteer":0,
        "Google Earth/Maps <=2008":1,
        "Google Earth/Maps >2008":2,
        "GPS":3,
        "locality description":4,
        "USGS map: 1:250000":5,
        "USGS map: 1:100000":6,
        "USGS map: 1:63360":7,
        "USGS map: 1:62500":8,
        "USGS map: 1:25000":9,
        "USGS map: 1:24000":10,
        "USGS map: 1:12000":11,
        "USGS map: 1:10000":12,
        "USGS map: 1:4800":13,
        "USGS map: 1:2400":14,
        "USGS map: 1:1200":15,
        "NTS map (A): 1:250000":16,
        "NTS map (B): 1:250000":17,
        "NTS map (C): 1:250000":18,
        "NTS map (A): 1:50000":19,
        "NTS map (B): 1:50000":20,
        "NTS map (C): 1:50000":21,
        "other map: 1:3000000":22,
        "other map: 1:2500000":23,
        "other map: 1:1000000":24,
        "other map: 1:500000":25,
        "other map: 1:250000":26,
        "other map: 1:200000":27,
        "other map: 1:180000":28,
        "other map: 1:150000":29,
        "other map: 1:125000":30,
        "other map: 1:100000":31,
        "other map: 1:80000":32,
        "other map: 1:62500":33,
        "other map: 1:60000":34,
        "other map: 1:50000":35,
        "other map: 1:40000":36,
        "other map: 1:32500":37,
        "other map: 1:25000":38,
        "other map: 1:20000":39,
        "other map: 1:10000":40,
    }
    DATUMS_LIST=["(WGS84) World Geodetic System 1984" ,
    "Abidjan 1987" ,
    "Accra" ,
    "Aden 1925" ,
    "Adindan" ,
    "Afgooye" ,
    "Ain el Abd 1970" ,
    "Airy 1830 ellipsoid" ,
    "Airy Modified 1849 ellipsoid" ,
    "Alaska (NAD27)" ,
    "Alaska/Canada (NAD27)" ,
    "Albanian 1987" ,
    "American Samoa 1962" ,
    "Amersfoort" ,
    "Ammassalik 1958" ,
    "Anguilla 1957" ,
    "Anna 1 Astro 1965" ,
    "Antigua Island Astro 1943" ,
    "Aratu" ,
    "Arc 1950 mean" ,
    "Arc 1960 mean" ,
    "Ascension Island 1958" ,
    "Astro Beacon \"E\" 1945" ,
    "Astro DOS 71/4" ,
    "Astro Tern Island (FRIG) 1961" ,
    "Astronomic Station No. 1 1951" ,
    "Astronomic Station No. 2 1951, Truk Island" ,
    "Astronomic Station Ponape 1951" ,
    "Astronomical Station 1952" ,
    "Australian Antarctic Datum 1998" ,
    "(AGD66) Australian Geodetic Datum 1966" ,
    "(AGD84) Australian Geodetic Datum 1984" ,
    "Australian National ellipsoid" ,
    "Autonomous Regions of Portugal 2008" ,
    "Average Terrestrial System 1977 ellipsoid" ,
    "Ayabelle Lighthouse" ,
    "Azores Central Islands 1948" ,
    "Azores Central Islands 1995" ,
    "Azores Occidental Islands 1939" ,
    "Azores Oriental Islands 1940" ,
    "Azores Oriental Islands 1995" ,
    "Bahamas (NAD27)" ,
    "Barbados 1938" ,
    "Batavia" ,
    "Beduaram" ,
    "Beijing 1954" ,
    "Bekaa Valley 1920 (IGN)" ,
    "Bellevue (IGN)" ,
    "Bermuda 1957" ,
    "Bermuda 2000" ,
    "Bessel 1841 ellipsoid (Namibia)" ,
    "Bessel 1841 ellipsoid (non-Namibia)" ,
    "Bessel Modified ellipsoid" ,
    "Bhutan National Geodetic Datum" ,
    "Bioko" ,
    "Bissau" ,
    "Bogota 1975" ,
    "Bukit Rimpah" ,
    "Bulgaria Geodetic System 2005" ,
    "Cadastre 1997" ,
    "Camacupa" ,
    "Camp Area Astro" ,
    "Campo Inchauspe" ,
    "Canada Mean (NAD27)" ,
    "Canal Zone (NAD27)" ,
    "Canton Astro 1966" ,
    "Cape" ,
    "Cape Canaveral mean" ,
    "Caribbean (NAD27)" ,
    "Carthage" ,
    "Cayman Islands Geodetic Datum 2011" ,
    "Central America (NAD27)" ,
    "Centre Spatial Guyanais 1967" ,
    "CH1903" ,
    "CH1903+" ,
    "Chatham Island Astro 1971" ,
    "Chatham Islands Datum 1979" ,
    "Chua Astro" ,
    "Clarke 1858 ellipsoid" ,
    "Clarke 1866 ellipsoid" ,
    "Clarke 1880 ellipsoid" ,
    "Clarke 1880 (Benoit) ellipsoid" ,
    "Clarke 1880 (international foot) ellipsoid" ,
    "Co-Ordinate System 1937 of Estonia" ,
    "Cocos Islands 1965" ,
    "Combani 1950" ,
    "Conakry 1905" ,
    "Congo 1960 Pointe Noire" ,
    "Corrego Alegre 1961" ,
    "Corrego Alegre 1970-72" ,
    "Costa Rica 2005" ,
    "Cuba (NAD27)" ,
    "Croatian Terrestrial Reference System" ,
    "Cyprus" ,
    "Cyprus Geodetic Reference System 1993" ,
    "Dabola 1981" ,
    "Danish 1876" ,
    "Datum 73" ,
    "Datum Geodesi Nasional 1995" ,
    "Dealul Piscului 1930" ,
    "Deception Island" ,
    "Deir ez Zor" ,
    "Deutsches Hauptdreiecksnetz" ,
    "Diego Garcia 1969" ,
    "Djakarta (Batavia)" ,
    "DOS 1968" ,
    "Dominica 1945" ,
    "Douala 1948" ,
    "Easter Island 1967" ,
    "Egypt 1907" ,
    "Egypt Gulf of Suez S-650 TL" ,
    "Estonia 1992" ,
    "Estonia 1997" ,
    "European 1950" ,
    "European 1950 mean" ,
    "European Datum 1950(1977)" ,
    "European 1979 mean" ,
    "European Datum 1987" ,
    "European Libyan Datum 1979" ,
    "European Terrestrial Reference System 1989" ,
    "Everest ellipsoid (Brunei, Sabah, Sarawak)" ,
    "Everest ellipsoid (W. Malaysia, Singapore 1948)" ,
    "Everest 1830 (1937 Adjustment) ellipsoid India" ,
    "Everest India 1856 ellipsoid" ,
    "Everest 1830 (1962 Definition) ellipsoid India" ,
    "Everest 1830 (1975 Definition) ellipsoid India" ,
    "Everest Pakistan ellipsoid" ,
    "Everest W. Malaysia 1969 ellipsoid" ,
    "Fahud" ,
    "Fatu Iva 72" ,
    "Fehmarnbelt Datum 2010" ,
    "Fiji 1956" ,
    "Fiji Geodetic Datum 1986" ,
    "Final Datum 1958" ,
    "Finnish Nautical Chart" ,
    "Fort Marigot" ,
    "Fort Thomas 1955" ,
    "Gambia" ,
    "Gan 1970" ,
    "Gandajika Base" ,
    "Gan 1970" ,
    "Geocentric Datum Brunei Darussalam 2009" ,
    "Geocentric Datum of Australia 1994" ,
    "Geocentric Datum of Australia 2020" ,
    "Geocentric Datum of Korea" ,
    "Geodetic Datum of 1965" ,
    "Geodetic Datum 1949" ,
    "Geodetic Reference System 1967 ellipsoid" ,
    "Geodetic Reference System 1967 Modified ellipsoid" ,
    "Geodetic Reference System 1980 ellipsoid" ,
    "Ghana" ,
    "Graciosa Base SW 1948" ,
    "Grand Cayman Geodetic Datum 1959" ,
    "Grand Comoros" ,
    "Greek Geodetic Reference System 1987" ,
    "Greenland (NAD27)" ,
    "Greenland 1996" ,
    "Grenada 1953" ,
    "Guadeloupe 1948" ,
    "Guam 1963" ,
    "Gulshan 303" ,
    "Gunung Segara" ,
    "Gunung Serindung 1962" ,
    "GUX 1 Astro" ,
    "Hanoi 1972" ,
    "Hartebeesthoek94" ,
    "Helle 1954" ,
    "Helmert 1906 ellipsoid" ,
    "Herat North" ,
    "Hito XVIII 1963" ,
    "Hjorsey 1955" ,
    "Hong Kong 1963(67)" ,
    "Hong Kong 1980" ,
    "Hong Kong Geodetic" ,
    "Hough 1960 ellipsoid" ,
    "Hu-Tzu-Shan 1950" ,
    "Hungarian Datum 1909" ,
    "Hungarian Datum 1972" ,
    "IGN 1962 Kerguelen" ,
    "IGN53 Mare" ,
    "IGN56 Lifou" ,
    "IGN63 Hiva Oa" ,
    "IGN72 Grande Terre" ,
    "IGN72 Nuku Hiva" ,
    "Indian" ,
    "Indian 1954" ,
    "Indian 1960" ,
    "Indian 1975" ,
    "Indonesian 1974 ellipsoid" ,
    "Indonesian Datum 1974" ,
    "Institut Geographique du Congo Belge 1955" ,
    "International 1924 ellipsoid" ,
    "Iran" ,
    "Iraqi Geospatial Reference System" ,
    "Iraq-Kuwait Boundary Datum 1992" ,
    "Ireland 1965" ,
    "IRENET95" ,
    "Islands Net 1993" ,
    "Islands Net 2004" ,
    "Israel 1993" ,
    "Istituto Geografico Militaire 1995" ,
    "ISTS 061 Astro 1968" ,
    "ISTS 073 Astro 1969" ,
    "Iwo Jima 1945" ,
    "Jamaica 1969" ,
    "Jamaica 2001" ,
    "Japanese Geodetic Datum 2000" ,
    "Johnston Island 1961" ,
    "Jouik 1961" ,
    "Kalianpur 1937" ,
    "Kalianpur 1962" ,
    "Kalianpur 1975" ,
    "Kandawala" ,
    "Kapingamarangi Astronomic Station No. 3 1951" ,
    "Karbala 1979" ,
    "Kartastokoordinaattijarjestelma (1966)" ,
    "Katanga 1955" ,
    "Kerguelen Island 1949" ,
    "Kertau 1948" ,
    "Kertau 1968" ,
    "Korean Datum 1985" ,
    "Korean Geodetic System 1995" ,
    "Kosovo Reference System 2001" ,
    "Krassowsky 1940 ellipsoid" ,
    "Kusaie Astro 1951" ,
    "Kuwait Oil Company" ,
    "Kuwait Utility" ,
    "L.C. 5 Astro 1961" ,
    "La Canoa" ,
    "La Reunion" ,
    "Lao National Datum 1997" ,
    "Latvia 1992" ,
    "Le Pouce 1934" ,
    "Leigon" ,
    "Lemuta" ,
    "Liberia 1964" ,
    "Libyan Geodetic Datum 2006" ,
    "Lisbon 1890" ,
    "Lisbon 1937" ,
    "Lithuania 1994 (ETRS89)" ,
    "Locodjo 1965" ,
    "Luxembourg 1930" ,
    "Luzon 1911" ,
    "Macao 1920" ,
    "Macao Geodetic Datum 2008" ,
    "Mahe 1971" ,
    "Makassar" ,
    "Malongo 1987" ,
    "Manoca 1962" ,
    "Marco Astro" ,
    "Marco Geocentrico Nacional de Referencia" ,
    "Marco Geodesico Nacional de Bolivia" ,
    "Marcus Island 1952" ,
    "Marshall Islands 1960" ,
    "Martinique 1938" ,
    "Masirah Is. (Nahrwan)" ,
    "Massawa" ,
    "Maupiti 83" ,
    "Mauritania 1999" ,
    "Merchich" ,
    "Mexico (NAD27)" ,
    "Mexico ITRF2008" ,
    "Mexico ITRF92" ,
    "MGI 1901" ,
    "Midway Astro 1961" ,
    "Militar-Geographische Institut" ,
    "Mindanao" ,
    "Minna" ,
    "Modified Fischer 1960 ellipsoid" ,
    "MOLDREF99" ,
    "MOMRA Terrestrial Reference Frame 2000" ,
    "Monte Mario" ,
    "Montjong Lowe" ,
    "Montserrat Island Astro 1958" ,
    "Moorea 87" ,
    "MOP78" ,
    "Moznet (ITRF94)" ,
    "M'Poraloko" ,
    "Nahrwan" ,
    "Nahrwan 1934" ,
    "Nahrwan 1967" ,
    "Nakhl-e Ghanem" ,
    "Naparima 1955" ,
    "Naparima 1972" ,
    "Naparima, BWI" ,
    "National Geodetic Network" ,
    "NEA74 Noumea" ,
    "Nepal 1981" ,
    "New Zealand Geodetic Datum 1949" ,
    "New Zealand Geodetic Datum 2000" ,
    "NGO 1948" ,
    "(NAD83) North American Datum 1983" ,
    "NAD83 (High Accuracy Reference Network)" ,
    "NAD83 (National Spatial Reference System 2007)" ,
    "NAD83 Canadian Spatial Reference System" ,
    "(NAD27) North American 1927 mean" ,
    "North American Datum 1927" ,
    "North American Datum 1927 (1976)" ,
    "North American Datum 1927 (CGQ77)" ,
    "Nord Sahara 1959" ,
    "Nouakchott 1965" ,
    "Nouvelle Triangulation Francaise" ,
    "Observatorio Meteorologico 1939" ,
    "Observatorio 1966" ,
    "Ocotepeque 1935" ,
    "Old Egyptian 1907" ,
    "Old Hawaiian mean" ,
    "Old Hawaiian Kauai" ,
    "Old Hawaiian Maui" ,
    "Old Hawaiian Oahu" ,
    "Old Trinidad 1903" ,
    "Oman" ,
    "Oman National Geodetic Datum 2014" ,
    "Ordnance Survey of Great Britain 1936" ,
    "Ordnance Survey of Northern Ireland 1952" ,
    "Padang 1884" ,
    "Palestine 1923" ,
    "Pampa del Castillo" ,
    "Papua New Guinea Geodetic Datum 1994" ,
    "Parametry Zemli 1990" ,
    "PDO Survey Datum 1993" ,
    "Peru96" ,
    "Petrels 1972" ,
    "Philippine Reference System 1992" ,
    "Phoenix Islands 1966" ,
    "Pico de las Nieves 1984" ,
    "Pitcairn 2006" ,
    "Pitcairn Astro 1967" ,
    "Point 58" ,
    "Point Noire 1958" ,
    "Pointe Geologie Perroud 1950" ,
    "Porto Santo 1936" ,
    "Porto Santo 1995" ,
    "Posiciones Geodesicas Argentinas 1994" ,
    "Posiciones Geodesicas Argentinas 1998" ,
    "Posiciones Geodesicas Argentinas 2007" ,
    "Potsdam Datum/83" ,
    "Potsdam Rauenberg DHDN" ,
    "Provisional South American 1956" ,
    "Provisional South Chilean 1963" ,
    "Puerto Rico" ,
    "Pulkovo 1942" ,
    "Pulkovo 1942(58)" ,
    "Pulkovo 1942(83)" ,
    "Pulkovo 1995" ,
    "PZ-90" ,
    "Qatar 1974" ,
    "Qatar National Datum 1995" ,
    "Qornoq 1927" ,
    "Rassadiran" ,
    "Rauenberg Datum/83" ,
    "Red Geodesica de Canarias 1995" ,
    "Red Geodesica Venezolana" ,
    "Reseau de Reference des Antilles Francaises 1991" ,
    "Reseau Geodesique de la Polynesie Francaise" ,
    "Reseau Geodesique de la RDC 2005" ,
    "Reseau Geodesique de la Reunion 1992" ,
    "Reseau Geodesique de Mayotte 2004" ,
    "Reseau Geodesique de Nouvelle Caledonie 91-93" ,
    "Reseau Geodesique de Saint Pierre et Miquelon 2006" ,
    "Reseau Geodesique des Antilles Francaises 2009" ,
    "Reseau Geodesique Francais 1993" ,
    "Reseau Geodesique Francais Guyane 1995" ,
    "Reseau National Belge 1972" ,
    "Rete Dinamica Nazionale 2008" ,
    "Reunion 1947" ,
    "Reykjavik 1900" ,
    "Rikets koordinatsystem 1990" ,
    "Rome 1940" ,
    "Ross Sea Region Geodetic Datum 2000" ,
    "S-42" ,
    "S-JTSK" ,
    "Saint Pierre et Miquelon 1950" ,
    "Santo (DOS) 1965" ,
    "Sao Braz" ,
    "Sapper Hill 1943" ,
    "Schwarzeck" ,
    "Scoresbysund 1952" ,
    "Selvagem Grande 1938" ,
    "Serbian Reference Network 1998" ,
    "Serbian Spatial Reference System 2000" ,
    "Sicily" ,
    "Sierra Leone 1960" ,
    "Sierra Leone 1968" ,
    "SIRGAS_ES2007.8" ,
    "SIRGAS-Chile" ,
    "SIRGAS-ROU98" ,
    "Sistema de Referencia Geocentrico para America del Sur 1995" ,
    "Sistema de Referencia Geocentrico para las Americas 2000" ,
    "Sistema Geodesico Nacional de Panama MACARIO SOLIS" ,
    "Sister Islands Geodetic Datum 1961" ,
    "Slovenia Geodetic Datum 1996" ,
    "Solomon 1968" ,
    "South American 1969 ellipsoid" ,
    "South American Datum 1969" ,
    "South American Datum 1969(96)" ,
    "South Asia" ,
    "South East Island 1943" ,
    "South Georgia 1968" ,
    "South Yemen" ,
    "Southeast Base" ,
    "Sri Lanka Datum 1999" ,
    "St. George Island" ,
    "St. Helena Geodetic Datum 2015" ,
    "St. Helena Tritan" ,
    "St. Kitts 1955" ,
    "St. Lawrence Island" ,
    "St. Lucia 1955" ,
    "St. Paul Island" ,
    "St. Vincent 1945" ,
    "ST71 Belep" ,
    "ST84 Ile des Pins" ,
    "ST87 Ouvea" ,
    "SVY21" ,
    "SWEREF99" ,
    "Swiss Terrestrial Reference Frame 1995" ,
    "System of the Unified Trigonometrical Cadastral Ne" ,
    "Tahaa 54" ,
    "Tahiti 52" ,
    "Tahiti 79" ,
    "Taiwan Datum 1997" ,
    "Tananarive Observatory 1925" ,
    "Tern Island 1961" ,
    "Tete" ,
    "Timbalai 1948" ,
    "TM65" ,
    "Tokyo" ,
    "Trinidad 1903" ,
    "Tristan Astro 1968" ,
    "Turkish National Reference Frame" ,
    "Ukraine 2000" ,
    "United Arab Emirates (Nahrwan)" ,
    "Vanua Levu 1915" ,
    "Vietnam 2000" ,
    "Viti Levu 1912" ,
    "Viti Levu 1916" ,
    "Voirol 1874" ,
    "Voirol 1875" ,
    "Voirol 1960" ,
    "(WGS66) World Geodetic System 1966" ,
    "(WGS66) World Geodetic System 1966 ellipsoid" ,
    "(WGS72) World Geodetic System 1972" ,
    "(WGS72) World Geodetic System 1972 ellipsoid" ,
    "(WGS72) Transit Broadcast Ephemeris" ,
    "Wake Island Astro 1952" ,
    "Wake-Eniwetok 1960" ,
    "War Office ellipsoid" ,
    "Yacare" ,
    "Yemen National Geodetic Network 1996" ,
    "Yoff" ,
    "Zanderij"]
    
    #Constant
    DEG_PATTERN=r"(.*?)\°"
    MIN_PATTERN=r"\°(.*?)\'"
    SEC_PATTER=r"\'(.*?)\""
    
    #driver elements
    ButtonCalculate=driver.find_element_by_id("ButtonCalculate")
    ChoiceModel= driver.find_element_by_id("ChoiceModel")
    ChoiceCoordSource=driver.find_element_by_id("ChoiceCoordSource")
    ChoiceCoordSystem=driver.find_element_by_id("ChoiceCoordSystem")
    ChoiceDatum=driver.find_element_by_id("ChoiceDatum")
    ChoiceLatPrecision=driver.find_element_by_id("ChoiceLatPrecision")
    txtT7Lat_DegMM=driver.find_element_by_id("txtT7Lat_DegMM")
    txtT7Lat_MinMM=driver.find_element_by_id("txtT7Lat_MinMM")
    txtT7Long_DegMM=driver.find_element_by_id("txtT7Long_DegMM")
    txtT7Long_MinMM=driver.find_element_by_id("txtT7Long_MinMM")
    txtT2Dec_Lat=driver.find_element_by_id("txtT2Dec_Lat")
    txtT2Dec_Long=driver.find_element_by_id("txtT2Dec_Long")
    textFieldMeasurementError=driver.find_element_by_id("TextFieldMeasurementError")
    ChoiceDistUnits=driver.find_element_by_id("ChoiceDistUnits")
    ChoiceLongDirMM=driver.find_element_by_id("ChoiceLongDirMM")
    ChoiceLatDirMM=driver.find_element_by_id("ChoiceLatDirMM")
    txtT7Lat_DegDMS=driver.find_element_by_id("txtT7Lat_DegDMS")
    txtT7Lat_MinDMS=driver.find_element_by_id("txtT7Lat_MinDMS")
    txtT7Lat_Sec=driver.find_element_by_id("txtT7Lat_Sec")
    ChoiceLatDirDMS=driver.find_element_by_id("ChoiceLatDirDMS")
    txtT7Long_DegDMS=driver.find_element_by_id("txtT7Long_DegDMS")
    txtT7Long_MinDMS=driver.find_element_by_id("txtT7Long_MinDMS")
    txtT7Long_Sec=driver.find_element_by_id("txtT7Long_Sec")
    ChoiceLongDirDMS=driver.find_element_by_id("ChoiceLongDirDMS")
    TextFieldExtent=driver.find_element_by_id("TextFieldExtent")
    TextFieldCalcDecLat=driver.find_element_by_id("TextFieldCalcDecLat")
    TextFieldCalcDecLong=driver.find_element_by_id("TextFieldCalcDecLong")
    TextFieldCalcErrorDist=driver.find_element_by_id("TextFieldCalcErrorDist")
    TextFieldCalcDatum=driver.find_element_by_id("TextFieldCalcDatum")
    TextFieldCalcPrecision=driver.find_element_by_id("TextFieldCalcPrecision")
    TextFieldCalcDate=driver.find_element_by_id("TextFieldCalcDate")
    TextFieldCalcGeoreferencer=driver.find_element_by_id("TextFieldCalcGeoreferencer")
    TextFieldCalcChoiceProtocol=driver.find_element_by_id("ChoiceProtocol")
    
    

    def __init__(self,CoordSystem,verbatimLatitude,verbatimLongitude,dynamicProperties,verbatimSRS):
        self.CoordSystem=CoordSystem    
        self.verbatimLatitude=verbatimLatitude
        self.verbatimLongitude=verbatimLongitude
        self.dynamicProperties=dynamicProperties
        self.verbatimSRS=verbatimSRS
        
    
    def dynamicpropertiesreader(self):
        #{"textFieldMeasurementError": integer, "ChoiceDistUnits": "string", "ChoiceCoordSource": "string", "TextFieldExtent": float}
        if type(literal_eval(self.dynamicProperties)) is dict:
            properties=literal_eval(self.dynamicProperties)
        elif type(literal_eval(self.dynamicProperties)) is tuple:
            for elements in literal_eval(self.dynamicProperties):
                if "geoParser" in elements:
                    properties=elements
        SeleniumGeoref.textFieldMeasurementError.clear()
        SeleniumGeoref.textFieldMeasurementError.send_keys(properties["textFieldMeasurementError"])
        ChoiceDistUnitsIndex=SeleniumGeoref.DistUnits[properties["ChoiceDistUnits"]]
        Select(SeleniumGeoref.ChoiceDistUnits).select_by_index(ChoiceDistUnitsIndex)
        if properties["ChoiceCoordSource"] in SeleniumGeoref.COORDINATE_SOURCE:
            ChoiceCoordSourceIndex=SeleniumGeoref.COORDINATE_SOURCE[properties["ChoiceCoordSource"]]
            Select(SeleniumGeoref.ChoiceCoordSource).select_by_index(ChoiceCoordSourceIndex)
        else: 
            Select(SeleniumGeoref.ChoiceCoordSource).select_by_index(4)
        if "TextFieldExtent" in self.dynamicProperties:
            SeleniumGeoref.TextFieldExtent.clear()
            SeleniumGeoref.TextFieldExtent.send_keys(properties["TextFieldExtent"])
        
            
    def verbatimSRSreader(self):
        if self.verbatimSRS in SeleniumGeoref.DATUMS_LIST:
            verbatimSRSIndex=SeleniumGeoref.DATUMS_LIST.index(self.verbatimSRS)
            Select(SeleniumGeoref.ChoiceDatum).select_by_index(verbatimSRSIndex+1)
        elif self.verbatimSRS == "unknown":
            Select(SeleniumGeoref.ChoiceDatum).select_by_index(0)
        else: 
            Select(SeleniumGeoref.ChoiceDatum).select_by_index(0)
        
        
    def precisionselect(self):
        if self.CoordSystem == "decimal degrees":
            if isinstance(literal_eval(str(self.verbatimLatitude)), int): Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(0) #nearest degree
            elif abs(float("0."+str(self.verbatimLatitude).split(".")[1]))==0.25: #1/4 degree
                Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(7)
            elif abs(float("0."+str(self.verbatimLatitude).split(".")[1]))==0.5: #1/2 degree
                Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(6)
            elif pow(10,-len(str(self.verbatimLatitude).split(".")[1])) in SeleniumGeoref.PRECISION_DD:
                Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(SeleniumGeoref.PRECISION_DD[pow(10,-len(self.verbatimLatitude.split(".")[1]))])
            else:
                Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(8) #0.0000001 or more
        if self.CoordSystem == "degrees decimal minutes":
            try:
                minute=re.search(SeleniumGeoref.MIN_PATTERN, self.verbatimLatitude).group(1).replace(" ","")
                if float(minute)==0: 
                    degree=re.search(SeleniumGeoref.DEG_PATTERN, self.verbatimLatitude).group(1).replace(" ","")
                    if isinstance(literal_eval(degree), int): Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(0) #nearest degree
                    elif abs(float("0."+degree.split(".")[1]))==0.5: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(1)#nearest 30 minutes
                    elif abs(float("0."+degree.split(".")[1]))==0.16: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(2)#nearest 10 minutes
                    elif abs(float("0."+degree.split(".")[1]))==0.083: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(3)#nearest 5 minutes
                    else: Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(0) #nearest degree
                elif isinstance(literal_eval(minute), int): #nearest minute
                    Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(4) 
                elif pow(10,-len(minute.split(".")[1])) in SeleniumGeoref.PRECISION_DDM:
                    Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(SeleniumGeoref.PRECISION_DDM[pow(10,-len(minute.split(".")[1]))])
                else: Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(8)
            except:
                degree=re.search(SeleniumGeoref.DEG_PATTERN, self.verbatimLatitude).group(1).replace(" ","")
                if isinstance(literal_eval(degree), int): Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(0) #nearest degree
                elif abs(float("0."+degree.split(".")[1]))==0.5: 
                    Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(1)#nearest 30 minutes
                elif abs(float("0."+degree.split(".")[1]))==0.16: 
                    Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(2)#nearest 10 minutes
                elif abs(float("0."+degree.split(".")[1]))==0.083: 
                    Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(3)#nearest 5 minutes
                else: Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(0) #nearest degree
        if self.CoordSystem=="degrees minutes seconds":
            try:
                seconds=re.search(SeleniumGeoref.SEC_PATTER, self.verbatimLatitude).group(1).replace(" ","")
                minute=re.search(SeleniumGeoref.MIN_PATTERN, self.verbatimLatitude).group(1).replace(" ","")
                degree=re.search(SeleniumGeoref.DEG_PATTERN, self.verbatimLatitude).group(1).replace(" ","")
                if float(seconds)==0:
                    if isinstance(literal_eval(minute), int): 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(4) #nearest minute
                    elif abs(float("0."+minute.split(".")[1]))==0.5: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(5)#nearest 30 seconds
                    elif abs(float("0."+minute.split(".")[1]))==0.16: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(6)#nearest 10 seconds
                    elif abs(float("0."+minute.split(".")[1]))==0.083: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(7)#nearest 5 seconds
                    else: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(4) #nearest minute
                if float(minute)==0: 
                    if isinstance(literal_eval(degree), int): Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(0) #nearest degree
                    elif abs(float("0."+degree.split(".")[1]))==0.5: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(1)#nearest 30 minutes
                    elif abs(float("0."+degree.split(".")[1]))==0.16: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(2)#nearest 10 minutes
                    elif abs(float("0."+degree.split(".")[1]))==0.083: 
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(3)#nearest 5 minutes
                    else: Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(0) #nearest degree
                elif float(seconds)!=0 and len(seconds.split(".")[1])>=1:
                    if len(seconds.split(".")[1])<=2 and pow(10,-len(seconds.split(".")[1])) in SeleniumGeoref.PRECISION_DDM:
                        Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(SeleniumGeoref.PRECISION_DMS[pow(10,-len(seconds.split(".")[1]))])
                    else: Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(11) #exact
                elif isinstance(literal_eval(minute), int): #nearest minute
                    Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(4) 
            except: Select(SeleniumGeoref.ChoiceLatPrecision).select_by_index(0)


    def coordinatesonly(self):
        Select(SeleniumGeoref.ChoiceModel).select_by_index(1)
        if self.CoordSystem == "decimal degrees":
            Select(SeleniumGeoref.ChoiceCoordSystem).select_by_index(SeleniumGeoref.COORD_SYSTEM_DIC[self.CoordSystem])
            #clear fields
            SeleniumGeoref.txtT2Dec_Lat.clear()
            SeleniumGeoref.txtT2Dec_Long.clear()
            #send keys to fields
            SeleniumGeoref.txtT2Dec_Lat.send_keys(str(self.verbatimLatitude))
            SeleniumGeoref.txtT2Dec_Long.send_keys(str(self.verbatimLongitude))
            #Precision check
            SeleniumGeoref.precisionselect(self)
            #check dynamicProperties
            SeleniumGeoref.dynamicpropertiesreader(self)
            #check Datum
            SeleniumGeoref.verbatimSRSreader(self)
            #results
            SeleniumGeoref.getresults(self)
            
        elif self.CoordSystem == "degrees minutes seconds":
            Select(SeleniumGeoref.ChoiceCoordSystem).select_by_index(SeleniumGeoref.COORD_SYSTEM_DIC[self.CoordSystem])
            #clear fields
            SeleniumGeoref.txtT7Lat_DegDMS.clear()
            SeleniumGeoref.txtT7Lat_MinDMS.clear()
            SeleniumGeoref.txtT7Lat_Sec.clear()
            SeleniumGeoref.txtT7Long_DegDMS.clear()
            SeleniumGeoref.txtT7Long_MinDMS.clear()
            SeleniumGeoref.txtT7Long_Sec.clear()
            #send keys to fields
            SeleniumGeoref.txtT7Lat_DegDMS.send_keys(re.search(SeleniumGeoref.DEG_PATTERN, self.verbatimLatitude).group(1).replace(" ",""))
            SeleniumGeoref.txtT7Lat_MinDMS.send_keys(re.search(SeleniumGeoref.MIN_PATTERN, self.verbatimLatitude).group(1).replace(" ",""))
            SeleniumGeoref.txtT7Lat_Sec.send_keys(re.search(SeleniumGeoref.SEC_PATTER, self.verbatimLatitude).group(1).replace(" ",""))
            SeleniumGeoref.txtT7Long_DegDMS.send_keys(re.search(SeleniumGeoref.DEG_PATTERN, self.verbatimLongitude).group(1).replace(" ",""))
            SeleniumGeoref.txtT7Long_MinDMS.send_keys(re.search(SeleniumGeoref.MIN_PATTERN, self.verbatimLongitude).group(1).replace(" ",""))
            SeleniumGeoref.txtT7Long_Sec.send_keys(re.search(SeleniumGeoref.SEC_PATTER, self.verbatimLongitude).group(1).replace(" ",""))
            #select index
            if "N" in self.verbatimLatitude.upper():
                Select(SeleniumGeoref.ChoiceLatDirDMS).select_by_index(0)
            else: Select(SeleniumGeoref.ChoiceLatDirDMS).select_by_index(1)
            if "E" not in self.verbatimLongitude.upper():
                Select(SeleniumGeoref.ChoiceLongDirDMS).select_by_index(0)
            else: Select(SeleniumGeoref.ChoiceLongDirDMS).select_by_index(1)
            #Precision check
            SeleniumGeoref.precisionselect(self) 
            #check dynamicProperties
            SeleniumGeoref.dynamicpropertiesreader(self)
            #check Datum
            SeleniumGeoref.verbatimSRSreader(self)
            #results
            SeleniumGeoref.getresults(self)
            
        elif self.CoordSystem == "degrees decimal minutes":
            Select(SeleniumGeoref.ChoiceCoordSystem).select_by_index(SeleniumGeoref.COORD_SYSTEM_DIC[self.CoordSystem])
            #clear fields
            SeleniumGeoref.txtT7Lat_DegMM.clear()
            SeleniumGeoref.txtT7Lat_MinMM.clear()
            SeleniumGeoref.txtT7Long_DegMM.clear()
            SeleniumGeoref.txtT7Long_MinMM.clear()
            #send keys to fields
            SeleniumGeoref.txtT7Lat_DegMM.send_keys(re.search(SeleniumGeoref.DEG_PATTERN, self.verbatimLatitude).group(1).replace(" ",""))
            SeleniumGeoref.txtT7Lat_MinMM.send_keys(re.search(SeleniumGeoref.MIN_PATTERN, self.verbatimLatitude).group(1).replace(" ",""))
            SeleniumGeoref.txtT7Long_DegMM.send_keys(re.search(SeleniumGeoref.DEG_PATTERN, self.verbatimLongitude).group(1).replace(" ",""))
            SeleniumGeoref.txtT7Long_MinMM.send_keys(re.search(SeleniumGeoref.MIN_PATTERN, self.verbatimLongitude).group(1).replace(" ",""))
            #select index
            if "N" in self.verbatimLatitude.upper():
                Select(SeleniumGeoref.ChoiceLatDirMM).select_by_index(0)
            else: Select(SeleniumGeoref.ChoiceLatDirMM).select_by_index(1)
            if "E" not in self.verbatimLongitude.upper():
                Select(SeleniumGeoref.ChoiceLongDirMM).select_by_index(0)
            else: Select(SeleniumGeoref.ChoiceLongDirMM).select_by_index(1)
            #Precision Check 
            SeleniumGeoref.precisionselect(self)
            #check dynamicProperties
            SeleniumGeoref.dynamicpropertiesreader(self)
            #check Datum
            SeleniumGeoref.verbatimSRSreader(self)
            #results
            SeleniumGeoref.getresults(self)
    
    def getresults(self):
        SeleniumGeoref.ButtonCalculate.click()
        resultDict={}
        resultDict["decimalLatitude"]=SeleniumGeoref.TextFieldCalcDecLat.text
        resultDict["decimalLongitude"]=SeleniumGeoref.TextFieldCalcDecLong.text
        resultDict["coordinateUncertaintyInMeters"]=SeleniumGeoref.TextFieldCalcErrorDist.text
        resultDict["geodeticDatum"]=SeleniumGeoref.TextFieldCalcDatum.text
        resultDict["coordinatePrecision"]=SeleniumGeoref.TextFieldCalcPrecision.text
        resultDict["georeferencerDate"]=SeleniumGeoref.TextFieldCalcDate.text
        print(resultDict)
    
    def geographicfeature(self):
        Select(SeleniumGeoref.ChoiceModel).select_by_index(1)
        Select(SeleniumGeoref.ChoiceCoordSystem).select_by_index(0)



class db_prep:
    def __init__(self,data):
        self.data=data
    
    def verbatimCoordinates_dms_sep(self,index):
        """
        split verbatimCoordinates data and fill verbatimLatitude & verbatimLongitude
        """
        for Coordinate in self.data.loc[index,"verbatimCoordinates"].split(","):
            if "N" in Coordinate.upper(): 
                self.data.loc[index,"verbatimLatitude"]=Coordinate
            elif "S" in Coordinate.upper(): 
                self.data.loc[index,"verbatimLatitude"]=Coordinate
            elif "E" in Coordinate.upper(): 
                self.data.loc[index,"verbatimLongitude"]=Coordinate
            elif "W" or "O" in Coordinate.upper(): 
                self.data.loc[index,"verbatimLongitude"]=Coordinate

    
    def verbatimCoordinates_utm_sep(self,index):
        Coordinate= self.data.loc[index,"verbatimCoordinates"].split(" ")
        for elements in Coordinate:
            if "N" or "S" in elements.upper(): timezone_index=Coordinate.index(elements)
        Coordinate_indexes=list(range(0,len(Coordinate)))
        Coordinate_indexes.remove(timezone_index)
        if int(Coordinate[Coordinate_indexes[0]]) > int(Coordinate[Coordinate_indexes[1]]):
            self.data.loc[index,"verbatimLatitude"]=Coordinate[Coordinate_indexes[1]]
            self.data.loc[index,"verbatimLongitude"]=Coordinate[Coordinate_indexes[0]]
        else:
            self.data.loc[index,"verbatimLatitude"]=Coordinate[0]
            self.data.loc[index,"verbatimLongitude"]=Coordinate[1]
    
    def verb_lat_long_autocomplete(self):
        """
        check existence of verbatimLatitude & verbatimLongitude:
            -Exist: fill verbatimLatitude & verbatimLongitude from verbatimCoordinates data
            -Absence: create and fill verbatimLatitude & verbatimLongitude from verbatimCoordinates data
        """
        if set(['verbatimLatitude', 'verbatimLongitude']).issubset(set(self.data.columns.to_list())) is False:
            verb_coord_position=self.data.columns.to_list().index("verbatimCoordinates")+1
            self.data.insert(verb_coord_position,"verbatimLatitude",np.nan)
            self.data.insert(verb_coord_position+1,"verbatimLongitude",np.nan)
            for index in self.data.index:
                if pd.isna(self.data.loc[index,"verbatimCoordinates"]):
                    pass
                elif isinstance(self.data.loc[index,"verbatimLongitude"],str)==False and isinstance(self.data.loc[index,"verbatimLatitude"],str)==False:  #cambio
                    if (pd.isna(self.data.loc[index,"verbatimLongitude"])) or (pd.isna(self.data.loc[index,"verbatimLatitude"])): #cambio
                        if self.data.loc[index,"verbatimCoordinateSystem"]=="UTM":
                            db_prep.verbatimCoordinates_utm_sep(self,index)
                        elif self.data.loc[index,"verbatimCoordinateSystem"]=="degrees minutes seconds" or self.data.loc[index,"verbatimCoordinateSystem"]=="degrees decimal minutes":
                            db_prep.verbatimCoordinates_dms_sep(self,index)
                        else:
                            pass                    
        if set(['verbatimLatitude', 'verbatimLongitude']).issubset(set(self.data.columns.to_list())) is True:
            for index in self.data.index:
                if pd.isna(self.data.loc[index,"verbatimCoordinates"]):
                    pass
                elif isinstance(self.data.loc[index,"verbatimLongitude"],str)==False and isinstance(self.data.loc[index,"verbatimLatitude"],str)==False:  #cambio
                    if (pd.isna(self.data.loc[index,"verbatimLongitude"])) or (pd.isna(self.data.loc[index,"verbatimLatitude"])): #cambio
                        if self.data.loc[index,"verbatimCoordinateSystem"]=="UTM":
                            self.verbatimCoordinates_utm_sep(index)
                        elif self.data.loc[index,"verbatimCoordinateSystem"]=="degrees minutes seconds" or self.data.loc[index,"verbatimCoordinateSystem"]=="degrees decimal minutes":
                            self.verbatimCoordinates_dms_sep(index)
                        else:
                            pass
                     
    def verbatimCoordinates_autocomplete(self):
        """
        Check the existence of verbatimCoordinates:
            - Exist: check if verbatimLatitude & verbatimLongitude exist and then fill verbatimCoordinates
            - Absence: create verbatimCoordinates then check if verbatimLatitude & verbatimLongitude exist and then fill verbatimCoordinates
        """
        if "verbatimCoordinates" not in self.data.columns:
            if "verbatimLatitude" and "verbatimLongitude" in self.data.columns:
                self.data["verbatimCoordinates"]=np.nan
                for index in self.data.index:
                    if (pd.isna(self.data.loc[index,"verbatimLatitude"]),pd.isna(self.data.loc[index,"verbatimLongitude"])) == (False,False) :
                        lat,lon=self.data.loc[index,"verbatimLatitude"],self.data.loc[index,"verbatimLongitude"]
                        self.data.loc[index,"verbatimCoordinates"]=f"{lat}, {lon}"
                    else :pass 
        if "verbatimCoordinates" in self.data.columns:
            for index in self.data.index:
                if pd.isna(self.data.loc[index,"verbatimCoordinates"]):
                    if (pd.isna(self.data.loc[index,"verbatimLatitude"]),pd.isna(self.data.loc[index,"verbatimLongitude"])) == (False,False):
                        lat,lon=self.data.loc[index,"verbatimLatitude"],self.data.loc[index,"verbatimLongitude"]
                        self.data.loc[index,"verbatimCoordinates"]=f"{lat}, {lon}"
                    else: pass
                      
    def verbatimCoordinateSystem_autocomplete(self): #work in progress
        """
        fill verbatimCoordinateSystem field based on verbatimCoordinates data
        """
        minutes="'"
        seconds='"'
        for index in self.data.index:
            if pd.isna(self.data.loc[index,"verbatimCoordinates"]) is False:
                try:
                    if "°" or "d" in self.data.loc[index,"verbatimCoordinates"]: 
                        if minutes and seconds in self.data.loc[index,"verbatimCoordinates"]: 
                            self.data.loc[index,"verbatimCoordinateSystem"]="degrees minutes seconds"
                        elif minutes in self.data.loc[index,"verbatimCoordinates"]: 
                            self.data.loc[index,"verbatimCoordinateSystem"]="degrees decimal minutes"
                    elif "." in self.data.loc[index,"verbatimCoordinates"]: 
                        self.data.loc[index,"verbatimCoordinateSystem"]="decimal degrees"
                    else: 
                        self.data.loc[index,"verbatimCoordinateSystem"]="UTM"
                except: pass
    
    def coordinatePrecision_autocomplete(self):
        """
        fill coordinatePrecision based on verbatimLatitude & verbatimLongitude (preference) else decimalLatitude & decimalLongitude information
        """
        for index in self.data.index:
            if (self.data.loc[index,"verbatimLatitude"] or self.data.loc[index,"verbatiLongitude"]) is np.nan or self.data.loc[index,"verbatimCoordinateSystem"]=="decimal degrees":
                if (self.data.loc[index,"decimalLatitude"] or self.data.loc[index,"decimalLongitude"]) is not np.nan:
                    try:
                        lat=self.data.loc[index,"decimalLatitude"].split(".")
                        lon=self.data.loc[index,"decimalLongitude"].split(".")
                        self.data.loc[index,"coordinatePrecision"]="0."+"0"*(min(len(lat[1]),len(lon[1]))-1)+"1"
                    except: pass
            elif self.data.loc[index,"verbatimCoordinateSystem"]=="degrees minutes seconds":
                try:
                    lat=self.data.loc[index,"verbatimLatitude"]
                    lon=self.data.loc[index,"verbatimLongitude"]
                    srch="'(.+?)\""
                    m_lat=re.search(srch, lat)
                    m_lon=re.search(srch, lon)
                    found_lat=m_lat.group(1)
                    found_lon=m_lon.group(1)
                    if "." in found_lat: 
                        pres=1/pow(10,len(found_lat.split(".")[1]))
                        coordP_lat=pres/3600.
                    else: coordP_lat=1/3600.
                    if "." in found_lon:
                        pres=1/pow(10,len(found_lon.split(".")[1]))
                        coordP_lon=pres/3600.
                    else: coordP_lon=1/3600.
                    self.data.loc[index,"coordinatePrecision"]='{:.7f}'.format(min(coordP_lon,coordP_lat))
                except: pass
            elif self.data.loc[index,"verbatimCoordinateSystem"]=="degrees decimal minutes":
                try:
                    lat=self.data.loc[index,"verbatimLatitude"]
                    lon=self.data.loc[index,"verbatimLongitude"]
                    srch="°(.+?)\'"
                    m_lat=re.search(srch, lat)
                    m_lon=re.search(srch, lon)
                    found_lat=m_lat.group(1)
                    found_lon=m_lon.group(1)
                    if "." in found_lat: 
                        pres=1/pow(10,len(found_lat.split(".")[1]))
                        coordP_lat=pres/60.
                    else: coordP_lat=1/60.
                    if "." in found_lon:
                        pres=1/pow(10,len(found_lon.split(".")[1]))
                        coordP_lon=pres/60.
                    else: coordP_lon=1/60.
                    self.data.loc[index,"coordinatePrecision"]='{:.7f}'.format(min(coordP_lon,coordP_lat))
                except: pass
            else: 
                try:
                    lat=self.data.loc[index,"decimalLatitude"].split(".")
                    lon=self.data.loc[index,"decimalLongitude"].split(".")
                    self.data.loc[index,"coordinatePrecision"]="0."+"0"*(min(len(lat[1]),len(lon[1]))-1)+"1"
                except: pass
        
   
class coord_transform:
    def __init__(self,data):
        self.data=data
    
    def utm_to_dg(self):
        for index in self.data.index:
            if self.data.loc[index,"verbatimCoordinates"] is not np.nan and self.data.loc[index,"verbatimCoordinateSystem"]=="UTM":
                coordinate= self.data.loc[index,"verbatimCoordinates"].split(" ")
                for elements in coordinate:
                    if "N" in elements.upper(): 
                        zone_index=coordinate.index(elements)
                        Global="North"
                    elif "S" in elements.upper():
                        zone_index=coordinate.index(elements)
                        Global="South"
                if Global=="South":
                    lat,lon=utm.to_latlon(self.data.loc[index,"verbatimLatitude"], self.data.loc[index,"verbatimLongitude"], int(coordinate[zone_index].upper().replace("S","")), northern=False)
                elif Global=="North":
                    lat,lon=utm.to_latlon(self.data.loc[index,"verbatimLatitude"], self.data.loc[index,"verbatimLongitude"], int(coordinate[zone_index].upper().replace("N","")), northern=True)
                self.data.loc[index,"decimalLatitude"]="{0:.7f}".format(lat)
                self.data.loc[index,"decimalLongitude"]="{0:.7f}".format(lon)
                #self.data.loc[index,"georeferenceSources"]="GeoParser Marcelo Oyaneder"
    
    def dms_to_dg(self):
        """
        fill decimalLatitude & decimalLongitude based on verbatimLatitude & verbatimLongitude transformation
        fill geodeticDatum based on verbatimSRS info
        """
        for index in self.data.index:
            if (self.data.loc[index,"verbatimCoordinateSystem"]=="degrees minutes seconds" or self.data.loc[index,"verbatimCoordinateSystem"]=="degrees decimal minutes") and pd.isna(self.data.loc[index,"verbatimCoordinates"]) is False:
                try: 
                    location= self.data.loc[index,"verbatimCoordinates"]
                    if "O" in location.upper():
                        location=location.replace("O","W")
                    response=requests.get(f"http://data.canadensys.net/tools/coordinates.json?data=35|{location}&idprovided=TRUE").json()
                    lon,lat=response["features"][0]["geometry"]["coordinates"]
                    self.data.loc[index,"decimalLatitude"]="{0:.7f}".format(lat)
                    self.data.loc[index,"decimalLongitude"]="{0:.7f}".format(lon)
                except:
                    self.data.loc[index,"decimalLatitude"]="Error"
                    self.data.loc[index,"decimalLongitude"]="Error"
    
    def geodeticDatum_autocomplete(self): 
        """
        fill geodeticDatum based on info from verbatimSRS 
        if decimalLatitude or decimalLongitude doesnt exist value is na 
        """
        for index in self.data.index:
            if (pd.isna(self.data.loc[index,"decimalLatitude"]) is False) and (pd.isna(self.data.loc[index,"decimalLongitude"]) is False):
                if pd.isna(self.data.loc[index,"geodeticDatum"]):
                    if pd.isna(self.data.loc[index,"verbatimSRS"]):
                        self.data.loc[index,"geodeticDatum"]="unknown"
                    else:
                        self.data.loc[index,"geodeticDatum"]=self.data.loc[index,"verbatimSRS"]
                else: pass
    
    def continent_autocomplete(self):
        """
        fill continent based on country data
        """
        country_data=pd.read_csv("https://raw.githubusercontent.com/VertNet/DwCVocabs/master/vocabs/countryCode_country_continent_merged.csv")
        country_data.set_index("country",inplace=True)
        country_data_dict=country_data.to_dict()
        if set(['country']).issubset(set(self.data.columns.to_list())) is True:
            if set(['continent']).issubset(set(self.data.columns.to_list())) is True:
                for index in self.data.index:
                    if self.data.loc[index,"country"] in country_data_dict["continent"].keys() and pd.isna(self.data.loc[index,"continent"]):
                        self.data.loc[index,"continent"]=country_data_dict["continent"][self.data.loc[index,"country"]]
                    else: pass        
            elif set(['continent']).issubset(set(self.data.columns.to_list())) is False:
                self.data.insert(self.data.columns.to_list().index("country")-1,"continent",np.nan) #en que lugar lo coloco
                for index in self.data.index:
                    if self.data.loc[index,"country"] in country_data_dict["continent"].keys():
                        self.data.loc[index,"continent"]=country_data_dict["continent"][self.data.loc[index,"country"]]
                    else: pass  
        else: pass 
    
    def location_autocomplete(self): #include country, country_code, stateProvince, county, municipality 
        """
        fill country, countryCode, stateProvince, county, municipality based on lat,lon info using gbif API 
        lacking develop about marine regions         
        """
        for index in self.data.index:
            try:
                lat=self.data.loc[index,"decimalLatitude"]
                lon=self.data.loc[index,"decimalLongitude"]
                result=requests.get(f"https://api.gbif-uat.org/v1/geocode/reverse?lat={lat}&lng={lon}").json()
                for elements in result:
                    if elements["source"]=="http://gadm.org/":
                        if elements["type"]=="GADM0":
                            self.data.loc[index,"country"]=elements["title"]
                            self.data.loc[index,"countryCode"]=elements["isoCountryCode2Digit"]
                        elif elements["type"]=="GADM1": self.data.loc[index,"stateProvince"]=elements["title"]
                        elif elements["type"]=="GADM2": self.data.loc[index,"county"]=elements["title"]
                        elif elements["type"]=="GADM3": self.data.loc[index,"municipality"]=elements["title"]
            except: 
                pass
        
    def higherGeography_autocomplete(self): 
        """
        fill higherGeography 
        """
        dwc_labels=["continent","waterBody","country","countryCode","stateProvince","county","municipality","islandGroup","island"]
        dwc_labels_selected=[i for i in dwc_labels if i in self.data.columns]
        try:
            for index in self.data.index:
                higherGeography_list=[]
                if pd.isna(self.data.loc[index,"higherGeography"]) is True:
                    for elements in dwc_labels_selected:
                        if isinstance(self.data.loc[index,elements], str): higherGeography_list.append(self.data.loc[index,elements])
                higherGeography_str=" | ".join(higherGeography_list)
                if higherGeography_str=="":
                    self.data.loc[index,"higherGeography"]=np.nan
                else:
                    self.data.loc[index,"higherGeography"]=higherGeography_str         
        except KeyError:
            self.data["higherGeography"]=np.nan
            for index in self.data.index:
                higherGeography_list=[]
                if pd.isna(self.data.loc[index,"higherGeography"]) is True:
                    for elements in dwc_labels_selected:
                        if isinstance(self.data.loc[index,elements], str): higherGeography_list.append(self.data.loc[index,elements])
                higherGeography_str=" | ".join(higherGeography_list)
                if higherGeography_str == "":
                    self.data.loc[index,"higherGeography"]=np.nan
                else:
                    self.data.loc[index,"higherGeography"]=higherGeography_str      