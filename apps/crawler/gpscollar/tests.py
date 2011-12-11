from django.test import TestCase
from apps.crawler.gpscollar.collar import *
from django.core.exceptions import ObjectDoesNotExist
from sys import *

class CollarTestCases(TestCase):
    fixtures = ['GSM0001.json']
    existingCollarID = '1'
    existingSampleData = {'ID': '30812', 'fileName': 'sample_data/GSM30812.TXT'}
    nonExistentCollarID = '999999999'
    testCollarParser = None
    badFileNames = ['badFile0009.TXT','bad/GS0009.TXT', 'GSMM0009.TXT','GSM0009.TX', 'GSM0009T.XT','GSM0009A.TXT']

    def setUp(self):
        self.testCollarParser = self.getTestCollarParser()

    def test_setting_filename_at_init(self):
        someFileName = self.createFileNameFromCollarID(self.nonExistentCollarID)
        testCollarParser = CollarParser(someFileName)
        self.assertEquals(testCollarParser.filePath, someFileName)

    def test_collarExists_true(self):
        existingCollarID = self.existingCollarID
        self.assertIsNotNone(self.getCollarFromDB(existingCollarID))
        testCollarParser = CollarParser(self.createFileNameFromCollarID(existingCollarID))
        self.assertTrue(testCollarParser.collarExists())

    def test_collarExists_false(self):
        self.assertIsNone(self.getCollarFromDB(self.testCollarParser.collarID))
        self.assertFalse(self.testCollarParser.collarExists())

    def test_collarExists_createCollar(self):
        self.assertIsNone(self.getCollarFromDB(self.testCollarParser.collarID))
        self.testCollarParser.createCollar()
        self.assertTrue(self.testCollarParser.collarExists())

    def test_stringToBool_true(self):
        string = "Yes"
        testCollarParser = self.getTestCollarParser()
        self.assertTrue(testCollarParser.stringToBool(string))

    def test_stringToBool_false(self):
        string = "No"
        testCollarParser = self.getTestCollarParser()
        self.assertFalse(testCollarParser.stringToBool(string))

    def test_stringToBool_badInput(self):
        badInputs = 'yes', 'y', 'n', 'no', 'abba', 'blahblah', '0', 0, 1, '1'
        testCollarParser = self.getTestCollarParser()
        for badInput in badInputs:
            self.assertRaises(ValueError, testCollarParser.stringToBool, badInput)

    def test_extractCollarIDFromFilename(self):
        collarID = '5555'
        testCollarParser = CollarParser(self.createFileNameFromCollarID(collarID))
        extractedCollarID = testCollarParser.extractCollarIDFromFilename()
        self.assertEquals(extractedCollarID, collarID)

    def test_createCollar(self):
        nonExistentCollarID = self.nonExistentCollarID
        self.assertIsNone(self.getCollarFromDB(nonExistentCollarID))
        testCollarParser = CollarParser(self.createFileNameFromCollarID(nonExistentCollarID))
        testCollarParser.createCollar()
        self.assertIsNotNone(self.getCollarFromDB(nonExistentCollarID))

    def test_createCollar_badFileNames(self):
        for badFileName in self.badFileNames:
            print "bad_filename: ", badFileName
            self.assertRaises(ValueError, CollarParser, str(badFileName))

    def test_fileReaderWithBadFile(self):
        badFilename = self.createFileNameFromCollarID(self.nonExistentCollarID)
        noFileIOError = IOError(2, 'No such file or directory')
        testCollarParser = CollarParser(badFilename)
        self.assertEquals(testCollarParser.fileReader().args[1],noFileIOError.args[1])

    def test_generateDateTimeFromList_validInput(self):
        validDateString = "28.2.2011"
        validTimeString = "0:0:0"
        testCollarParser = self.getTestCollarParser()
        for validDateString in self.getValidDateStrings():
            testCollarParser.generateDateTimeFromList(validDateString, validTimeString)
        for validTimeString in self.getValidTimeStrings():
            testCollarParser.generateDateTimeFromList(validDateString, validTimeString)


    def test_generateDateTimeFromList_badDate(self):
        testCollarParser = self.getTestCollarParser()
        for badDate in self.getBadDateStrings():
            self.assertRaises(ValueError, testCollarParser.generateDateTimeFromList, badDate, self.getValidTimeStrings()[0])

    def test_generateDateTimeFromList_badTime(self):
        testCollarParser = self.getTestCollarParser()
        for badTime in self.getBadTimeStrings():
            self.assertRaises(ValueError, testCollarParser.generateDateTimeFromList, self.getValidDateStrings()[0], badTime)

    def test_CollarData_clean_duplicate(self):
        duplicateCollarId = '30812'
        duplicateGMTDATETIME = ('12.01.2011', '03:28:34')
        duplicateLocation = Point(float(35.7894160), float(-78.6726674))
        testCollarParser = self.getTestCollarParser()
        testCollarParser.createCollarData('1 12.01.2011 03:28:34 11.01.2011 23:28:34 1017383 -5078894 3709330 35.7894160 -78.6726674 114.28 3.0 3D Yes 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3.44 3.68 12')
        testCollar = Collar()
        testCollar.collarID = duplicateCollarId
        testCollar.save()
        testCollarData = CollarData()
        testCollarData.collar = testCollar
        testCollarData.GMT_DATETIME = testCollarParser.generateDateTimeFromList(duplicateGMTDATETIME[0], duplicateGMTDATETIME[1])
        testCollarData.LMT_DATETIME = testCollarData.GMT_DATETIME
        testCollarData.LOCATION = duplicateLocation
        testCollarData.save()
        testCollarData.clean()

    def test_CollarData_clean_noDuplicates(self):
        duplicateCollarId = '30812'
        nonDuplicateCollarId = '1'
        duplicateGMTDATETIME = ('12.01.2011', '03:28:34')
        nonDuplicateGMTDATETIME = ('5.01.2009', '11:20:35')
        duplicateLocation = Point(float(35.7894160), float(-78.6726674))
        nonDuplicateLocation1 = Point(float(35.7894161), float(-78.6726674))
        nonDuplicateLocation2 = Point(float(35.7894160), float(-78.6726675))
        nonDuplicateLocation3 = Point(float(-35.7894160), float(-78.6726674))
        nonDuplicateLocation4 = Point(float(35.7894160), float(78.6726674))
        testCollarParser = self.getTestCollarParser()
        testCollar = Collar()
        testCollar.collarID = duplicateCollarId
        testCollar.save()
        testCollarData = CollarData()
        testCollarData.collar = testCollar
        testCollarData.GMT_DATETIME = testCollarParser.generateDateTimeFromList(duplicateGMTDATETIME[0], duplicateGMTDATETIME[1])
        testCollarData.LMT_DATETIME = testCollarData.GMT_DATETIME
        testCollarData.LOCATION = duplicateLocation
        testCollarData.save()
        testCollarData.clean()


    def getTestCollarParser(self):
        return CollarParser(self.existingSampleData['fileName'])

    def getValidDateStrings(self):
        return '28.2.2011', '1.1.2000', '31.1.2010', '31.12.2010', '1.1.1990'

    def getValidTimeStrings(self):
        return '0:0:0', '23:59:59', '0:59:59', '23:0:0'

    def getBadDateStrings(self):
        return (None, "-1.1.2011", "29.2.2011", "31.4.2011", "0.1.2011", "a.1.2011", "1a.1.2011", "one.1.2011", ".1.2011", "1 .1.2011",
            "1.-1.2011", "1.0.2011", "1.13.2011", "1.1a.2011", "1.a.2011", "1.one.2011", "1..2011", "1. 1.2011",
            "1.1.-1", "1.1.2025", "1.1.500", "1.1.0", "1.1.2011a", "1.1.201a", "1.1.a", "1.1.twozerooneone", "1.1.", "1.1. 2011",
            "1.1.2011.", ".1.1.2011", "1 1 2011", "1 1.2011", "1,1.2011", "1:1.2011", "1,1,2011", "1:1:2011")

    def getBadTimeStrings(self):
        return (None, "-1:1:1", "24:1:1", "1a:1:1", "a:1:1", ":1:1", "1 :1:1",
            "1:-1:1" "1:60:1", "1:1a:1", "1:a:1", "1::1", "1:1 :1",
            "1:1:-1", "1:1:60", "1:1:1a", "1:1:a", "1:1:", "1:1:1 ",
            "1:1:1:", ":1:1:1", "1 1 1", "1 1:1", "1,1:1", "1.1:1", "1,1,1", "1.1.1")

    def getCollarFromDB(self, collarID):
        try:
            return Collar.objects.get(collarID=collarID)
        except ObjectDoesNotExist:
            return None

    def createFileNameFromCollarID(self, collarID):
        return 'some/path/GSM{0}.TXT'.format(collarID)
