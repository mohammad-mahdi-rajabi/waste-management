from django.contrib import admin
from .models import (FacilityType, Location, ContactType, Contact, MembershipType, ClientStatus, Language,
                    Calendar, Client, User, ObjectBase, Department, Role, UserPosition, DocumentFile, ImageFile,
                    FormGroup, Form, Section, StaticChoice, StaticChoiceOption, Field, ContentText, ContentImage,
                    ContactUs, CalendarEvent, VehicleType, VehicleInfo, AssociateType, ContractType, WasteStorageType,
                    WasteAnalysisParameter, WasteAnalysisPreparationStandard, WasteAnalysisPreparationMethod,
                    WasteAnalysisStandard, WasteAnalysisMethod,
                    LabAnalysisResult, WasteTreatmentMaterial, WasteTreatmentEquipment, WasteTreatmentMethod,
                    AssociateOfClient, Contract, Payment, WasteClassificationSystem, WasteClass, WasteType,
                    WastePickupRequest, WasteExpressedCharacteristic, WasteBatch, WasteSubBatch,
                    WasteBatchInitialEvaluation, WasteBatchSecondaryEvaluation, WasteAssessment, WasteSample,
                    WasteBatchCostManHour, WasteBatchCostEquipment, WasteBatchCostMaterial, WasteBatchCostEstimation,
                    WasteAssociatedWithContract, WasteBatchAcceptanceAtOrigin, WasteBatchAcceptanceAtDestination,
                    WasteBatchStorageEnter, WasteBatchStorageExit, WasteBatchTreatment, Lab, WasteBatchTCLPTestResult,
                    WasteBatchLandfilling, LandfillDailyReport, CustomerOfClientEvaluation, HSEAccidentType, HSEAccidentReport
)

# Register your models here.

admin.site.register(FacilityType)
admin.site.register(Location)
admin.site.register(ContactType)
admin.site.register(Contact)
admin.site.register(MembershipType)
admin.site.register(ClientStatus)
admin.site.register(Language)
admin.site.register(Calendar)
admin.site.register(Client)
admin.site.register(User)
# admin.site.register(ObjectBase)  # This is an abstract model and shouldn't be registered
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(UserPosition)
admin.site.register(DocumentFile)
admin.site.register(ImageFile)
admin.site.register(FormGroup)
admin.site.register(Form)
admin.site.register(Section)
admin.site.register(StaticChoice)
admin.site.register(StaticChoiceOption)
admin.site.register(Field)
admin.site.register(ContentText)
admin.site.register(ContentImage)
admin.site.register(ContactUs)
admin.site.register(CalendarEvent)
admin.site.register(VehicleType)
admin.site.register(VehicleInfo)
admin.site.register(AssociateType)
admin.site.register(ContractType)
admin.site.register(WasteStorageType)
admin.site.register(WasteAnalysisParameter)
admin.site.register(WasteAnalysisPreparationStandard)
admin.site.register(WasteAnalysisPreparationMethod)
admin.site.register(WasteAnalysisStandard)
admin.site.register(WasteAnalysisMethod)


admin.site.register(LabAnalysisResult)
admin.site.register(WasteTreatmentMaterial)
admin.site.register(WasteTreatmentEquipment)
admin.site.register(WasteTreatmentMethod)
admin.site.register(AssociateOfClient)
admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(WasteClassificationSystem)
admin.site.register(WasteClass)
admin.site.register(WasteType)
admin.site.register(WastePickupRequest)
admin.site.register(WasteExpressedCharacteristic)
admin.site.register(WasteBatch)
admin.site.register(WasteSubBatch)
admin.site.register(WasteBatchInitialEvaluation)
admin.site.register(WasteBatchSecondaryEvaluation)
admin.site.register(WasteAssessment)
admin.site.register(WasteSample)
admin.site.register(WasteBatchCostManHour)
admin.site.register(WasteBatchCostEquipment)
admin.site.register(WasteBatchCostMaterial)
admin.site.register(WasteBatchCostEstimation)
admin.site.register(WasteAssociatedWithContract)
admin.site.register(WasteBatchAcceptanceAtOrigin)
admin.site.register(WasteBatchAcceptanceAtDestination)
admin.site.register(WasteBatchStorageEnter)
admin.site.register(WasteBatchStorageExit)
admin.site.register(WasteBatchTreatment)
admin.site.register(Lab)
admin.site.register(WasteBatchTCLPTestResult)
admin.site.register(WasteBatchLandfilling)
admin.site.register(LandfillDailyReport)
admin.site.register(CustomerOfClientEvaluation)
admin.site.register(HSEAccidentType)
admin.site.register(HSEAccidentReport)


