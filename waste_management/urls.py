from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth.views import LogoutView


from .views import (
    CreateStaticChoiceView, EditDeleteStaticChoiceView,
    CreateStaticChoiceOptionView, EditDeleteStaticChoiceOptionView,
    ViewFacilityTypes, ViewUpdateDeleteLocation, CreateLocation, ViewContactTypes, ViewUpdateDeleteContact, CreateContact,
    ViewUpdateDetailClient, ViewSummaryClient, ViewUpdateUserDetail, ViewUpdateDeleteUserFullDetail, CreateUserFullDetail,
    ViewSummaryUser, ViewUpdateDeleteDepartment, CreateDepartment, ListDepartments, ViewUpdateDeleteRole, CreateRole, ListRoles,
    ViewUpdateDeleteUserPosition, CreateUserPosition, ListUserPositions, ViewUserPosition, FormGroupListView,
    FormListView, FormTemplateView, ContentImageDetailView, ContentTextDetailView, ContactUsCreateAPIView,
    ViewUpdateDeleteCalendarEvent, CreateCalendarEvent, CompanyWideCalendarEventListView, PersonalCalendarEventListView,
    ListSummaryUsers, ChangePasswordView, ViewLanguageTypes, ViewCalendarTypes, CreateFieldView, EditDeleteFieldView,
    CreateSectionView, EditDeleteSectionView,  CreateFormView, EditDeleteFormView, CreateFormGroupView, EditDeleteFormGroupView,
    ###
    ViewVehicleTypes, ViewUpdateDeleteVehicleInfo, CreateVehicleInfo, ViewAssociateTypes, ViewContractTypes,
    ViewWasteStorageTypes, ViewWasteAnalysisParameters, ViewWasteAnalysisPreparationStandards, ViewWasteAnalysisPreparationMethods,
    ViewWasteAnalysisStandards, ViewWasteAnalysisMethods, ViewUpdateDeleteLabAnalysisResult, CreateLabAnalysisResult,
    ViewWasteTreatmentMaterials, ViewWasteTreatmentEquipments, ViewWasteTreatmentMethods, ViewAssociateOfClientSummarys,
    ViewUpdateDeleteAssociateOfClientDetail, CreateAssociateOfClientDetail, ViewContractSummarys, ViewUpdateDeleteContractDetail,
    CreateContractDetail, ViewPaymentSummarys_by_client, ViewPaymentSummarys_by_contract, ViewUpdateDeletePaymentInstallment, CreatePaymentInstallment, ViewUpdatePaymentRecieved,
    ViewWasteClassificationSystems, ViewUpdateDeleteWasteType, CreateWasteType,
    ViewUpdateDeleteWastePickupRequest, CreateWastePickupRequest, ViewUpdateDeleteWasteExpressedCharacteristic, CreateWasteExpressedCharacteristic,
    ViewUpdateDeleteWasteBatch, CreateWasteBatch, ViewUpdateDeleteWasteBatchInitialEvaluation, CreateWasteBatchInitialEvaluation,
    ViewUpdateDeleteWasteBatchSecondaryEvaluation, CreateWasteBatchSecondaryEvaluation, ViewUpdateDeleteWasteAssessment,
    CreateWasteAssessment, ViewUpdateDeleteWasteSample, CreateWasteSample, ViewUpdateDeleteWasteBatchCostEstimation, CreateWasteBatchCostEstimation,
    ViewUpdateDeleteWasteAssociatedWithContract, CreateWasteAssociatedWithContract,
    ViewUpdateDeleteWasteBatchAcceptanceAtOrigin, CreateWasteBatchAcceptanceAtOrigin, ViewUpdateDeleteWasteBatchAcceptanceAtDestination,
    CreateWasteBatchAcceptanceAtDestination, ViewUpdateDeleteWasteBatchStorageEnter, CreateWasteBatchStorageEnter,
    ViewUpdateDeleteWasteBatchStorageExit, CreateWasteBatchStorageExit, ViewUpdateDeleteWasteBatchTreatment, CreateWasteBatchTreatment,
    ViewUpdateDeleteLab, CreateLab, ViewUpdateDeleteWasteBatchTCLPTestResult, CreateWasteBatchTCLPTestResult, ViewUpdateDeleteWasteBatchLandfilling,
    CreateWasteBatchLandfilling, ViewUpdateDeleteLandfillDailyReport, CreateLandfillDailyReport, CreateCustomerOfClientEvaluation,
    ViewUpdateDeleteWasteSubBatch, CreateWasteSubBatch, ViewHSEAccidentType, ViewUpdateDeleteHSEAccidentReport, CreateHSEAccidentReport,
    ViewUpdateContractCommencement, ViewUpdateContractTermination, ViewWastePickupRequests, ViewWasteBatchReferenceCodes, ViewWasteSubBatchReferenceCodes,
    ViewLabSummaries
)

from .dashboard import (
    accident_report
    )

# /?page=2/ must be included at the end fo all lists.

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', LogoutView.as_view(), name='logout_token'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),

    # signup
    # forgot password

    path('client-detail/<str:id_code>/', ViewUpdateDetailClient.as_view(), name='view-update-client-detail'),
    path('client-summary/<str:id_code>/', ViewSummaryClient.as_view(), name='view-client-summary'),

    path('user-detail/<str:username>/', ViewUpdateUserDetail.as_view(), name='view-update-user-detail'),
    path('user-full-detail/<str:user__username>/', ViewUpdateDeleteUserFullDetail.as_view(), name='view-update-delete-user-full-detail'),
    path('user-full-detail/', CreateUserFullDetail.as_view(), name='create-user-full-detail'),
    path('user-summary/<str:username>/', ViewSummaryUser.as_view(), name='view-summary-user'),
    path('list-users-summary/<str:client__id_code>/', ListSummaryUsers.as_view(), name='list-users-summary'),

    path('language-types/', ViewLanguageTypes.as_view(), name='view-language-types'),
    path('calendar-types/', ViewCalendarTypes.as_view(), name='view-calendar-types'),

    path('facility-types/', ViewFacilityTypes.as_view(), name='view-facility-types'),
    path('location/<str:id_code>/', ViewUpdateDeleteLocation.as_view(), name='view-update-delete-location'),
    path('location/', CreateLocation.as_view(), name='create-location'),

    path('contact-types/', ViewContactTypes.as_view(), name='view-contact-types'),
    path('contact/<str:id_code>/', ViewUpdateDeleteContact.as_view(), name='view-update-delete-contact'),
    path('contact/', CreateContact.as_view(), name='create-contact'),

    path('department/<str:id_code>/', ViewUpdateDeleteDepartment.as_view(), name='view-update-delete-department'),
    path('department/', CreateDepartment.as_view(), name='create-department'),
    path('list-departments/<str:client__id_code>/', ListDepartments.as_view(), name='list-departments'),

    path('role/<str:id_code>/', ViewUpdateDeleteRole.as_view(), name='view-update-delete-role'),
    path('role/', CreateRole.as_view(), name='create-role'),
    path('list-roles/<str:client__id_code>/', ListRoles.as_view(), name='list-roles'),

    path('user-position/<str:id_code>/', ViewUpdateDeleteUserPosition.as_view(), name='view-update-delete-user-position'),
    path('user-position/', CreateUserPosition.as_view(), name='create-user-position'),
    path('list-user-positions/<str:client__id_code>/', ListUserPositions.as_view(), name='list-user-positions'),
    path('user-position-by-username/<str:user__username)/', ViewUserPosition.as_view(), name='view-user-position-by-username'),

    path('list-form-groups/', FormGroupListView.as_view(), name='list-form-groups'),
    path('form-groups/create/', CreateFormGroupView.as_view(), name='create-form-group'),
    path('form-groups/<int:id>/', EditDeleteFormGroupView.as_view(), name='edit-delete-form-group'),

    path('forms/create/', CreateFormView.as_view(), name='create-form'),
    path('forms/<int:id>/', EditDeleteFormView.as_view(), name='edit-delete-form'),

    path('sections/create/', CreateSectionView.as_view(), name='create-section'),
    path('sections/<int:id>/', EditDeleteSectionView.as_view(), name='edit-delete-section'),


    path('fields/create/', CreateFieldView.as_view(), name='create-field'),
    path('fields/<int:id>/', EditDeleteFieldView.as_view(), name='edit-delete-field'),

    path('static-choices/create/', CreateStaticChoiceView.as_view(), name='create-static-choice'),
    path('static-choices/<int:id>/', EditDeleteStaticChoiceView.as_view(), name='edit-delete-static-choice'),

    path('static-choice-options/create/', CreateStaticChoiceOptionView.as_view(), name='create-static-choice-option'),
    path('static-choice-options/<int:id>/', EditDeleteStaticChoiceOptionView.as_view(), name='edit-delete-static-choice-option'),


    path('list-forms/<str:group>/', FormListView.as_view(), name='lis-forms'),
    path('forms/<str:form_ref>/', FormTemplateView.as_view(), name='form_template_view'),

    path('content-image/<str:ref>/', ContentImageDetailView.as_view(), name='view-content-image'),
    path('content-text/<str:ref>/', ContentTextDetailView.as_view(), name='view-content-text'),

    path('contact-us/', ContactUsCreateAPIView.as_view(), name='create-contact-us'),

    path('events/<str:id_code>/', ViewUpdateDeleteCalendarEvent.as_view(), name='view-update-delete-events'),
    path('events/', CreateCalendarEvent.as_view(), name='create-events'),
    path('company-events-list/<int:year>/<int:month>/', CompanyWideCalendarEventListView.as_view(), name='company-events-list'),
    path('personal-events-list/<int:year>/<int:month>/', PersonalCalendarEventListView.as_view(), name='personal-events-list'),

    ####

    path('list-vehicle-types/', ViewVehicleTypes.as_view(), name='list-vehicle-types'),
    path('vehicle-info/<str:id_code>/', ViewUpdateDeleteVehicleInfo.as_view(), name='view-update-delete-vehicle-info'),
    path('vehicle-info/', CreateVehicleInfo.as_view(), name='create-vehicle-info'),

    path('list-associate-types/', ViewAssociateTypes.as_view(), name='list-associate-types'),
    path('list-contract-types/', ViewContractTypes.as_view(), name='list-contract-types'),
    path('list-waste-storage-types/', ViewWasteStorageTypes.as_view(), name='list-waste-storage-types'),
    path('list-waste-analysis-parameters/', ViewWasteAnalysisParameters.as_view(), name='list-waste-analysis-parameters'),
    path('list-waste-analysis-preparation-standards/', ViewWasteAnalysisPreparationStandards.as_view(), name='list-waste-analysis-preparation-standards'),
    path('list-waste-analysis-preparation-methods/', ViewWasteAnalysisPreparationMethods.as_view(), name='list-waste-analysis-preparation-methods'),
    path('list-waste-analysis-standards/', ViewWasteAnalysisStandards.as_view(), name='list-waste-analysis-standards'),
    path('list-waste-analysis-methods/', ViewWasteAnalysisMethods.as_view(), name='list-waste-analysis-methods'),

    path('analysis-result/<str:id_code>/', ViewUpdateDeleteLabAnalysisResult.as_view(), name='view-update-delete-analysis-result'),
    path('analysis-result/', CreateLabAnalysisResult.as_view(), name='create-analysis-result'),

    path('list-waste-treatment-materials/', ViewWasteTreatmentMaterials.as_view(), name='list-waste-treatment-materials'),
    path('list-waste-treatment-equipments/', ViewWasteTreatmentEquipments.as_view(), name='list-waste-treatment-equipments'),
    path('list-waste-treatment-methods/', ViewWasteTreatmentMethods.as_view(), name='list-waste-treatment-methods'),

    path('list-associate-of-client-summarys/', ViewAssociateOfClientSummarys.as_view(), name='list-waste-treatment-methods'),
    path('associate-of-client/<str:id_code>/', ViewUpdateDeleteAssociateOfClientDetail.as_view(), name='view-update-delete-associate-of-client'),
    path('associate-of-client/', CreateAssociateOfClientDetail.as_view(), name='create-associate-of-client'),

    path('list-contract-summarys/<str:id_code>/', ViewContractSummarys.as_view(), name='list-contract-summarys'),
    path('contract/<str:id_code>/', ViewUpdateDeleteContractDetail.as_view(), name='view-update-delete-contract'),
    path('contract/', CreateContractDetail.as_view(), name='create-contract'),

    path('contract-commencement/<str:id_code>/', ViewUpdateContractCommencement.as_view(), name='view-update-contract-commencement'),
    path('contract-termination/<str:id_code>/', ViewUpdateContractTermination.as_view(), name='view-update-contract-termination'),



    path('list-payment-summarys-by-client/<str:id_code>/', ViewPaymentSummarys_by_client.as_view(), name='list-payment-summarys-by-client'),
    path('list-payment-summarys-by-contract/<str:id_code>/', ViewPaymentSummarys_by_contract.as_view(), name='list-payment-summarys-by-contract'),
    path('payment-installment/<str:id_code>/', ViewUpdateDeletePaymentInstallment.as_view(), name='view-update-delete-payment-installment'),
    path('payment-installment/', CreatePaymentInstallment.as_view(), name='create-payment-installment'),
    path('payment-received/<str:id_code>/', ViewUpdatePaymentRecieved.as_view(), name='view-update-payment-received'),

    path('list-waste-classification-systems/', ViewWasteClassificationSystems.as_view(), name='list-waste-classification-systems'),
    path('list-waste-class/<str:classification_system__ref>', ViewWasteClassificationSystems.as_view(), name='list-waste-classification-systems'),

    path('waste-type/<str:id_code>/', ViewUpdateDeleteWasteType.as_view(), name='view-update-delete-waste-type'),
    path('waste-type/', CreateWasteType.as_view(), name='create-waste-type'),

    path('waste-pickup-request/<str:id_code>/', ViewUpdateDeleteWastePickupRequest.as_view(), name='view-update-delete-waste-pickup-request'),
    path('waste-pickup-request/', CreateWastePickupRequest.as_view(), name='create-waste-pickup-request'),
    path('list-waste-pickup-requests/', ViewWastePickupRequests.as_view(), name='list-waste-pickup-requests'),

    path('waste-expressed-characteristic/<str:id_code>/', ViewUpdateDeleteWasteExpressedCharacteristic.as_view(), name='view-update-delete-waste-expressed-characteristic'),
    path('waste-expressed-characteristic/', CreateWasteExpressedCharacteristic.as_view(), name='create-waste-expressed-characteristic'),

    path('waste-batch/<str:id_code>/', ViewUpdateDeleteWasteBatch.as_view(), name='view-update-delete-waste-batch'),
    path('waste-batch/', CreateWasteBatch.as_view(), name='create-waste-batch'),
    path('list-waste-batch-reference-codes/', ViewWasteBatchReferenceCodes.as_view(), name='list-waste-batch-reference-codes'),


    path('waste-sub-batch/<str:id_code>/', ViewUpdateDeleteWasteSubBatch.as_view(), name='view-update-delete-waste-sub-batch'),
    path('waste-sub-batch/', CreateWasteSubBatch.as_view(), name='create-waste-sub-batch'),
    path('list-waste-sub-batch-reference-codes/<str:WasteBatch__assigned_waste_reference_code>', ViewWasteSubBatchReferenceCodes.as_view(), name='list-waste-sub-batch-reference-codes'),

    path('waste-batch-initial-evaluation/<str:id_code>/', ViewUpdateDeleteWasteBatchInitialEvaluation.as_view(), name='view-update-delete-waste-batch-initial-evaluation'),
    path('waste-batch-initial-evaluation/', CreateWasteBatchInitialEvaluation.as_view(), name='create-waste-batch-initial-evaluation'),

    path('waste-batch-secondary-evaluation/<str:id_code>/', ViewUpdateDeleteWasteBatchSecondaryEvaluation.as_view(), name='view-update-delete-waste-batch-secondary-evaluation'),
    path('waste-batch-secondary-evaluation/', CreateWasteBatchSecondaryEvaluation.as_view(), name='create-waste-batch-secondary-evaluation'),

    path('waste-assessment/<str:id_code>/', ViewUpdateDeleteWasteAssessment.as_view(), name='view-update-delete-waste-assessment'),
    path('waste-assessment/', CreateWasteAssessment.as_view(), name='create-waste-assessment'),

    path('waste-sample/<str:id_code>/', ViewUpdateDeleteWasteSample.as_view(), name='view-update-delete-waste-sample'),
    path('waste-sample/', CreateWasteSample.as_view(), name='create-waste-sample'),

    path('waste-batch-cost-estimation/<str:id_code>/', ViewUpdateDeleteWasteBatchCostEstimation.as_view(), name='view-update-delete-waste-batch-cost-estimation'),
    path('waste-batch-cost-estimation/', CreateWasteBatchCostEstimation.as_view(), name='create-waste-batch-cost-estimation'),


    path('waste-associated-with-contract/<str:id_code>/', ViewUpdateDeleteWasteAssociatedWithContract.as_view(), name='view-update-delete-waste-associated-with-contract'),
    path('waste-associated-with-contract/', CreateWasteAssociatedWithContract.as_view(), name='create-waste-associated-with-contract'),

    path('waste-batch-acceptance-at-origin/<str:id_code>/', ViewUpdateDeleteWasteBatchAcceptanceAtOrigin.as_view(), name='view-update-delete-waste-batch-acceptance-at-origin'),
    path('waste-batch-acceptance-at-origin/', CreateWasteBatchAcceptanceAtOrigin.as_view(), name='create-waste-batch-acceptance-at-origin'),

    path('waste-batch-acceptance-at-destination/<str:id_code>/', ViewUpdateDeleteWasteBatchAcceptanceAtDestination.as_view(), name='view-update-delete-waste-batch-acceptance-at-destination'),
    path('waste-batch-acceptance-at-destination/', CreateWasteBatchAcceptanceAtDestination.as_view(), name='create-waste-batch-acceptance-at-destination'),

    path('waste-batch-storage-enter/<str:id_code>/', ViewUpdateDeleteWasteBatchStorageEnter.as_view(), name='view-update-delete-waste-batch-storage-enter'),
    path('waste-batch-storage-enter/', CreateWasteBatchStorageEnter.as_view(), name='create-waste-batch-storage-enter'),

    path('waste-batch-storage-exit/<str:id_code>/', ViewUpdateDeleteWasteBatchStorageExit.as_view(), name='view-update-delete-waste-batch-storage-exit'),
    path('waste-batch-storage-exit/', CreateWasteBatchStorageExit.as_view(), name='create-waste-batch-storage-exit'),

    path('waste-batch-treatment/<str:id_code>/', ViewUpdateDeleteWasteBatchTreatment.as_view(), name='view-update-delete-waste-batch-treatment'),
    path('waste-batch-treatment/', CreateWasteBatchTreatment.as_view(), name='create-waste-batch-treatment'),

    path('lab/<str:id_code>/', ViewUpdateDeleteLab.as_view(), name='view-update-delete-lab'),
    path('lab/', CreateLab.as_view(), name='create-lab'),
    path('list-labs-summaries/', ViewLabSummaries.as_view(), name='list-labs-summaries'),

    path('waste-batch-tclp-test-result/<str:id_code>/', ViewUpdateDeleteWasteBatchTCLPTestResult.as_view(), name='view-update-delete-waste-batch-tclp-test-result'),
    path('waste-batch-tclp-test-result/', CreateWasteBatchTCLPTestResult.as_view(), name='create-waste-batch-tclp-test-result'),

    path('waste-batch-landfilling/<str:id_code>/', ViewUpdateDeleteWasteBatchLandfilling.as_view(), name='view-update-delete-waste-batch-landfilling'),
    path('waste-batch-landfilling/', CreateWasteBatchLandfilling.as_view(), name='create-waste-batch-landfilling'),

    path('landfill-daily-report/<str:id_code>/', ViewUpdateDeleteLandfillDailyReport.as_view(), name='view-update-delete-landfill-daily-report'),
    path('landfill-daily-report/', CreateLandfillDailyReport.as_view(), name='create-landfill-daily-report'),

    path('customer-of-evaluation/', CreateCustomerOfClientEvaluation.as_view(), name='create-customer-of-evaluation'),

    path('list-hse-incident-type/', ViewHSEAccidentType.as_view(), name='list-hse-incident-type'),
    path('hse-accident-report/<str:id_code>/', ViewUpdateDeleteHSEAccidentReport.as_view(), name='view-update-delete-hse-accident-report'),
    path('hse-accident-report/', CreateHSEAccidentReport.as_view(), name='create-hse-accident-report'),


    # DASHBOARDS
    path('accident-report/', accident_report, name='accident_report'),
]

