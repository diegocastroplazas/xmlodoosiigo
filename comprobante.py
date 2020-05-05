import io
from bs4 import BeautifulSoup


class Comprobante(object):
    def __init__(self, filename):
        self.fileName = filename
        self.isProcessed = False
        self.leer()
        self.inicializarXML()
        self.inicializarData()
        self.transformar()

    def leer(self):
        f = io.open(self.fileName, encoding='latin-1')
        self.soup = BeautifulSoup(f.read(), "lxml-xml")

    def transformar(self):
        self._seccionCompany()
        self._seccionCustomer()
        self._seccionContact()
        self._seccionRequest()
        self._seccionBilling()

        print(self.out.prettify())

    def inicializarData(self):
        self.config = {
            'TIPO_DOC': {
                'INVOIC': 'F',
                'NC': 'C'
            }
        }

    def inicializarXML(self):
        self.out = BeautifulSoup(features="lxml")

        xmlDataSection = self.out.new_tag("XMLData")
        xmlDataSection.attrs['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
        self.out.append(xmlDataSection)
        
        productSection = self.out.new_tag("Product")
        productSection.attrs["Name"] = "SIIGO"
        productSection.attrs["Version"] = "03"
        self.out.XMLData.append(productSection)

        companySection = self.out.new_tag("CompanyData")
        customerSection = self.out.new_tag("Customer")
        contactSection = self.out.new_tag("Contact")
        requestSection = self.out.new_tag("Request")
        billingSection = self.out.new_tag("Billing")
        
        self.out.XMLData.append(companySection)
        self.out.XMLData.append(customerSection)
        self.out.XMLData.append(contactSection)
        self.out.XMLData.append(requestSection)
        self.out.XMLData.append(billingSection)

        print("XML inicializado")

    def _createTags(self, dicti=dict(), name=""):
        for k, v in dicti.items():
            tag = self.soup.new_tag(k)
            tag.string = v
            self.out.find(name).append(tag)
        

    def _seccionCompany(self):
        COMPANY = {
            "PersonType": self.soup.FACTURA.EMI.EMI_1.string,
            "Name": self.soup.FACTURA.EMI.EMI_6.string,
            "Nit": self.soup.FACTURA.EMI.EMI_2.string,
            "Phone": self.soup.FACTURA.EMI.CDE.CDE_3.string,
            "RegimeType": "2",
            "Address": self.soup.FACTURA.EMI.EMI_10.string,
            "City": self.soup.FACTURA.EMI.EMI_13.string,
            "EconomicActivityCode": "04659",
            "EconomicActivityName": "Comercio al por mayor de otros tipos de maquinaria",
            "EconomicActivityRate": "11.040",
            "EMail": self.soup.FACTURA.EMI.CDE.CDE_4.string,
            "Contact": self.soup.FACTURA.EMI.CDE.CDE_2.string,
        }
        self._createTags(COMPANY, "CompanyData")
        
    def _seccionCustomer(self):
        CUSTOMER = {
            "Code": self.soup.FACTURA.ADQ.ADQ_2.string,
            "CheckDigit": self.soup.FACTURA.ADQ.ADQ_22.string,
            "BranchOffice": "000",
            "IsSocialReason": "",
            "FirstName": self.soup.FACTURA.ADQ.ILA.ILA_1.string,
            "Address": self.soup.FACTURA.ADQ.ADQ_10.string,
            "Phone": "",
            "EMail": self.soup.FACTURA.ADQ.CDA.CDA_4.string,
            "Collector": "1"
        }
        self._createTags(CUSTOMER, "Customer")

    def _seccionContact(self):
        CONTACT = {
            "Code": "",
            "Email": "",
        }
        self._createTags(CONTACT, "Contact")

    def _seccionRequest(self):
        REQUEST = {
            "WithApproval": "FALSE"
        }
        self._createTags(REQUEST, "Request")

    def _seccionBilling(self):
        globalSection = self.out.new_tag("Global")
        detailSection = self.out.new_tag("Detail")
        self.out.find('Billing').append(globalSection)
        self.out.find('Billing').append(detailSection)

        # DATA DEL EMISOR
        GLOBAL_DATA = dict()
        GLOBAL_DATA["0001"] = "CRUTEK S.A.S"
        GLOBAL_DATA["0002"] = self.soup.FACTURA.ENC.ENC_2.string
        GLOBAL_DATA["0003"] = self.soup.FACTURA.EMI.EMI_2.string
        GLOBAL_DATA["0005"] = self.soup.FACTURA.EMI.EMI_10.string
        GLOBAL_DATA["0011"] = self.soup.FACTURA.EMI.CDE.CDE_3.string
        GLOBAL_DATA["0013"] = "Responsables de iva"
        GLOBAL_DATA["0018"] = self.soup.FACTURA.ADQ.ADQ_2.string
        GLOBAL_DATA["1019"] = self.soup.FACTURA.EMI.CDE.CDE_4.string
        GLOBAL_DATA["1189"] = self.soup.FACTURA.DFE.DFE_3.string
        GLOBAL_DATA["1205"] = "1"
        GLOBAL_DATA["1209"] = self.config['TIPO_DOC'][self.soup.FACTURA.ENC.ENC_1.string]
        GLOBAL_DATA["1210"] = self.soup.FACTURA.EMI.EMI_6.string
        GLOBAL_DATA["1232"] = self.soup.FACTURA.DFE.DFE_6.string
        GLOBAL_DATA["1233"] = self.soup.FACTURA.DFE.DFE_2.string
        GLOBAL_DATA["1234"] = self.soup.FACTURA.DFE.DFE_4.string
        GLOBAL_DATA["1264"] = self.soup.FACTURA.DFE.DFE_1.string
        GLOBAL_DATA["1263"] = self.soup.FACTURA.EMI.EMI_6.string
        GLOBAL_DATA["1265"] = "05"
        GLOBAL_DATA["1266"] = self.soup.FACTURA.EMI.TAC.TAC_1.string

        # DATA DEL RECEPTOR
        
        GLOBAL_DATA["0403"] = "Digito verificacion"
        GLOBAL_DATA["1253"] = self.soup.FACTURA.ADQ.TCR.TCR_1.string
        GLOBAL_DATA["1184"] = "Responsabilidad fiscal adquiriente"
        GLOBAL_DATA["1185"] = self.soup.FACTURA.ADQ.ADQ_1.string
        GLOBAL_DATA["1126"] = self.soup.FACTURA.ADQ.ADQ_3.string
        GLOBAL_DATA["0017"] = "Responsabilidad fiscal adquiriente"

        #Aplica unicamente para persona natural

        GLOBAL_DATA["0405"] = self.soup.FACTURA.ADQ.ADQ_3.string
        GLOBAL_DATA["0406"] = self.soup.FACTURA.ADQ.ADQ_9.string
        GLOBAL_DATA["0407"] = self.soup.FACTURA.ADQ.ADQ_9.string
        # -------------------------------------

        GLOBAL_DATA["1268"] = self.soup.FACTURA.ADQ.ADQ_7.string
        GLOBAL_DATA["0025"] = self.soup.FACTURA.ADQ.ADQ_10.string
        GLOBAL_DATA["0402"] = "Colombia"
        GLOBAL_DATA["0028"] = self.soup.FACTURA.ADQ.ADQ_13.string
        GLOBAL_DATA["0822"] = self.soup.FACTURA.ADQ.CDA.CDA_4.string
        GLOBAL_DATA["0089"] = ""
        GLOBAL_DATA["0505"] = self.soup.FACTURA.ADQ.CDA.CDA_2.string

        GLOBAL_DATA["1190"] = "CO"
        GLOBAL_DATA["1211"] = self.soup.FACTURA.IEN.IEN_2.string
        GLOBAL_DATA["1212"] = self.soup.FACTURA.IEN.IEN_12.string
        

        #DATA GENERAL DEL DOCUMENTO

        GLOBAL_DATA["1271"] = "Codigo tipo de factura"
        GLOBAL_DATA["0009"] = "Tipo de documento"
        GLOBAL_DATA["0494"] = "Codigo comprobante contable"
        GLOBAL_DATA["0008"] = self.soup.FACTURA.ENC.ENC_6.string
        GLOBAL_DATA["0071"] = self.soup.FACTURA.DRF.DRF_1.string
        GLOBAL_DATA["0072"] = self.soup.FACTURA.DRF.DRF_2.string
        GLOBAL_DATA["1213"] = self.soup.FACTURA.DRF.DRF_3.string
        GLOBAL_DATA["0494"] = "Codigo comprobante contable"
        GLOBAL_DATA["0073"] = self.soup.FACTURA.ENC.ENC_6.string #Revisar
        GLOBAL_DATA["0074"] = self.soup.FACTURA.DRF.DRF_3.string
        GLOBAL_DATA["0075"] = self.soup.FACTURA.DRF.DRF_6.string
        GLOBAL_DATA["1131"] = self.soup.FACTURA.TIM.IMP.IMP_6.string
        GLOBAL_DATA["1240"] = "COP" # Revisar
        GLOBAL_DATA["1114"] = "Codigo comprobante contable" # Revisar
        GLOBAL_DATA["0022"] = self.soup.FACTURA.ENC.ENC_7.string
        GLOBAL_DATA["1187"] = self.soup.FACTURA.ENC.ENC_9.string
        '''
        GLOBAL_DATA["0068"] = "Codigo comprobante contable"
        GLOBAL_DATA["0069"] = "Codigo comprobante contable"
        GLOBAL_DATA["0070"] = "Codigo comprobante contable"

        GLOBAL_DATA["1196"] = "Codigo comprobante contable"
        GLOBAL_DATA["1197"] = "Codigo comprobante contable"
        GLOBAL_DATA["1198"] = "Codigo comprobante contable"

        GLOBAL_DATA["0088"] = "Codigo comprobante contable" # Revisar
        GLOBAL_DATA["0054"] = "Codigo comprobante contable" # Revisar
        GLOBAL_DATA["1235"] = "Codigo comprobante contable"
        GLOBAL_DATA["1236"] = "Codigo comprobante contable"
        GLOBAL_DATA["0459"] = "Codigo comprobante contable"
        GLOBAL_DATA["1271"] = "Codigo comprobante contable"
        GLOBAL_DATA["1272"] = "Codigo comprobante contable"
        '''
        GLOBAL_DATA["1281"] = self.soup.find("MEP_2").string

        # TOTALES DEL DOCUMENTO

        descuentos = self.soup.find("DSC_3")

        GLOBAL_DATA["0067"] = self.soup.find("TOT_7").string
        GLOBAL_DATA["0053"] = self.soup.find("TOT_1").string
        GLOBAL_DATA["0602"] = self.soup.find("TOT_3").string
        GLOBAL_DATA["0060"] = self.soup.find("TIM_2").string
        GLOBAL_DATA["0416"] = 19
        GLOBAL_DATA["1273"] = self.soup.find("TOT_7").string
        if descuentos != None:
            GLOBAL_DATA["0600"] = self.soup.find("DSC_3").string


        for k, v in GLOBAL_DATA.items():
            dtag = self.out.new_tag("D")
            dtag.attrs["K"] = k
            dtag.string = str(v)
            self.out.find("Global").append(dtag)

        indice = 0
        for detalle in self.soup.find_all("ITE"):
            r_section = self.out.new_tag("R")
            self.out.find("Detail").append(r_section)

            DATA_DETALLE = dict()
            DATA_DETALLE["0490"] = detalle.find("ITE_1").string
            DATA_DETALLE["0031"] = detalle.find("IAE_1").string
            DATA_DETALLE["0035"] = detalle.find("ITE_10").string
            DATA_DETALLE["1282"] = detalle.find("ITE_28").string
            
            DATA_DETALLE["0033"] = detalle.find("ITE_11").string
            DATA_DETALLE["0038"] = detalle.find("ITE_3").string
            DATA_DETALLE["0039"] = detalle.find("ITE_7").string
            DATA_DETALLE["0476"] = detalle.find("ITE_5").string
            DATA_DETALLE["0509"] = detalle.find("ITE_5").string # TO-DO Incluir descuentos
            '''
            DATA_DETALLE["42"] = "Iten"
            DATA_DETALLE["826"] = "Iten"
            DATA_DETALLE["43"] = "Iten"
            DATA_DETALLE["511"] = "Iten"
            DATA_DETALLE["512"] = "Iten"
            '''
            DATA_DETALLE["0527"] = detalle.find("TII_1").string
            DATA_DETALLE["1292"] = detalle.find("IIM_4").string

            '''
            DATA_DETALLE["1201"] = "Iten"
            DATA_DETALLE["1292"] = "Iten"
            DATA_DETALLE["1290"] = "Iten"
            DATA_DETALLE["516"] = "Iten"
            DATA_DETALLE["531"] = "Iten"
            DATA_DETALLE["1288"] = "Iten"
            DATA_DETALLE["1257"] = "Iten"
            DATA_DETALLE["1258"] = "Iten"
            DATA_DETALLE["1259"] = "Iten"
            DATA_DETALLE["1260"] = "Iten"
            DATA_DETALLE["1261"] = "Iten"
            DATA_DETALLE["1262"] = "Iten"
            DATA_DETALLE["1208"] = "Iten"
            '''

            for k, v in DATA_DETALLE.items():
                dtag = self.out.new_tag("D")
                dtag.attrs["K"] = k
                dtag.string = str(v)
                self.out.find_all("R")[indice].append(dtag)

            indice += 1



        
        
        
        






        