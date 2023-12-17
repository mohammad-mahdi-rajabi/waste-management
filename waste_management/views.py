from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .serializers import (
    FacilityTypeSerializer, LocationSerializer, ContactTypeSerializer, ContactSerializer,
    ClientSummarySerializer, ClientDetailSerializer, UserFullDetailSerializer, UserDetailSerializer, UserSummarySerializer, ChangeUserPasswordSerializer,
    DepartmentSerializer, RoleSerializer, UserPositionSerializer, FormGroupSerializer, FormSerializer, FieldSerializer,
    ContentTextSerializer, ContentImageSerializer,
    LanguageSerializer, CalendarSerializer, CalendarEventSerializer, ContactUsSerializer, SectionSerializer, StaticChoiceSerializer, StaticChoiceOptionSerializer,

    VehicleTypeSerializer, VehicleInfoSerializer, AssociateTypeSerializer, ContractTypeSerializer, WasteStorageTypeSerializer,
    WasteAnalysisParameterSerializer, WasteAnalysisPreparationStandardSerializer, WasteAnalysisPreparationMethodSerializer,
    WasteAnalysisStandardSerializer, WasteAnalysisMethodSerializer, LabAnalysisResultSerializer, WasteTreatmentMaterialSerializer,
    WasteTreatmentEquipmentSerializer, WasteTreatmentMethodSerializer, AssociateOfClientDetailSerializer, AssociateOfClientSummarySerializer,
    ContractDetailSerializer, ContractSummarySerializer, PaymentSummarySerializer, WasteClassificationSystemSerializer,
    WasteClassSerializer, WasteTypeSerializer, WastePickupRequestSerializer, WasteExpressedCharacteristicSerializer,
    WasteBatchSerializer, WasteSubBatchSerializer, WasteBatchInitialEvaluationSerializer,
    WasteBatchSecondaryEvaluationSerializer, WasteAssessmentSerializer, WasteSampleSerializer, WasteBatchCostEstimationSerializer,
    WasteAssociatedWithContractSerializer, WasteBatchAcceptanceAtOriginSerializer,
    WasteBatchAcceptanceAtDestinationSerializer, WasteBatchStorageEnterSerializer, WasteBatchStorageExitSerializer,
    WasteBatchTreatmentSerializer, LabSerializer, WasteBatchTCLPTestResultSerializer, WasteBatchLandfillingSerializer,
    LandfillDailyReportSerializer, CustomerOfClientEvaluationSerializer, HSEAccidentTypeSerializer, HSEAccidentReportSerializer,
    WasteSubBatchSummarySerializer, WasteBatchSummarySerializer, LabSummarySerializer,
    PaymentRecievedSerializer, PaymentInstallmentSerializer, ContractCommencementSerializer, ContractTerminationSerializer,
)

from .models import (
    FacilityType, Location, ContactType, Contact, Client, User, Department, Role, UserPosition, FormGroup, Form, Field,
    ContentText, ContentImage, Language, Calendar, CalendarEvent, Section, StaticChoice, StaticChoiceOption,

    VehicleType, VehicleInfo, AssociateType, ContractType, WasteStorageType, WasteAnalysisParameter, WasteAnalysisPreparationStandard,
    WasteAnalysisPreparationMethod, WasteAnalysisStandard, WasteAnalysisMethod, LabAnalysisResult, WasteTreatmentMaterial,
    WasteTreatmentEquipment, WasteTreatmentMethod, AssociateOfClient, Contract, Payment, WasteClassificationSystem, WasteClass,
    WasteType, WastePickupRequest, WasteExpressedCharacteristic, WasteBatch, WasteSubBatch,  WasteBatchInitialEvaluation,
    WasteBatchSecondaryEvaluation, WasteAssessment, WasteSample, WasteBatchCostEstimation,
    WasteAssociatedWithContract, WasteBatchAcceptanceAtOrigin, WasteBatchAcceptanceAtDestination, WasteBatchStorageEnter,
    WasteBatchStorageExit, WasteBatchTreatment, Lab, WasteBatchTCLPTestResult, WasteBatchLandfilling, LandfillDailyReport, CustomerOfClientEvaluation,
    HSEAccidentType, HSEAccidentReport,
)




# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Permissions &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class OnlySeeDataYouOwn(BasePermission):
    """
    Permission to allow users to access only the data they've created.
    """
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        else:
            return False


class OnlySeeDataFromYourCompany(BasePermission):
    """
    Permission to allow users to access data within their client/company.
    """
    def has_object_permission(self, request, view, obj):
        if obj.author.client== request.user.client:
            return True
        else:
            return False


class ClientAdminPrivilege(BasePermission):
    """
    Permission to grant special privileges to client administrators.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_client_admin == True:
            return True
        else:
            return False


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Authentication &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated, OnlySeeDataYouOwn)
    serializer_class = ChangeUserPasswordSerializer


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Location &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ViewFacilityTypes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer


class ViewUpdateDeleteLocation(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'id_code'


class CreateLocation(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Language and Calendar &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class ViewLanguageTypes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ViewCalendarTypes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Contact &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ViewContactTypes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


class ViewUpdateDeleteContact(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'id_code'


class CreateContact(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Client &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ViewUpdateDetailClient(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany, ClientAdminPrivilege]
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    lookup_field = 'id_code'


class ViewSummaryClient(generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Client.objects.all()
    serializer_class = ClientSummarySerializer
    lookup_field = 'id_code'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& User &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ViewUpdateUserDetail(generics.RetrieveUpdateAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'


class ViewUpdateDeleteUserFullDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany, ClientAdminPrivilege]
    queryset = User.objects.all()
    serializer_class = UserFullDetailSerializer
    lookup_field = 'username'


class CreateUserFullDetail(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany, ClientAdminPrivilege]
    queryset = User.objects.all()
    serializer_class = UserFullDetailSerializer

    def perform_create(self, serializer):
        # Get the authenticated user from the request object
        user = self.request.user

        # Check if the authenticated user is a client admin
        if not user.is_client_admin:
            raise PermissionDenied("You do not have permission to create users.")

        # Set the client field in the serializer's validated data
        # to the client associated with the authenticated user
        serializer.validated_data['client'] = user.client

        # Call super to continue with the object creation
        super().perform_create(serializer)


class ViewSummaryUser(generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = User.objects.all()
    serializer_class = UserSummarySerializer
    lookup_field = 'username'


class ListSummaryUsers(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = User.objects.all()
    serializer_class = UserSummarySerializer
    lookup_field = 'client__id_code'

# &&&&&&&&&&&&&&&&&&&&&&&&&&&& Department, Roles & Positions &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ViewUpdateDeleteDepartment(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany, ClientAdminPrivilege]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'id_code'


class CreateDepartment(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ClientAdminPrivilege]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def perform_create(self, serializer):
        # Get the authenticated user from the request object
        user = self.request.user

        # Check if the authenticated user is a client admin
        if not user.is_client_admin:
            raise PermissionDenied("You do not have permission to create users.")

        # Set the client field in the serializer's validated data
        # to the client associated with the authenticated user
        serializer.validated_data['client'] = user.client

        # Call super to continue with the object creation
        super().perform_create(serializer)


class ListDepartments(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'client__id_code'


#****
class ViewUpdateDeleteRole(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany, ClientAdminPrivilege]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id_code'


class CreateRole(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ClientAdminPrivilege]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def perform_create(self, serializer):
        # Get the authenticated user from the request object
        user = self.request.user

        # Check if the authenticated user is a client admin
        if not user.is_client_admin:
            raise PermissionDenied("You do not have permission to create users.")

        # Set the client field in the serializer's validated data
        # to the client associated with the authenticated user
        serializer.validated_data['client'] = user.client

        # Call super to continue with the object creation
        super().perform_create(serializer)


class ListRoles(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'client__id_code'

#****
class ViewUpdateDeleteUserPosition(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany, ClientAdminPrivilege]
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer
    lookup_field = 'id_code'


class CreateUserPosition(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ClientAdminPrivilege]
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer


class ListUserPositions(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer
    lookup_field = 'client__id_code'


class ViewUserPosition(generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer
    lookup_field = 'user__username'



# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Form Templates &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class FormGroupListView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, ]
    serializer_class = FormGroupSerializer

    def get_queryset(self):
        # Exclude 'system-forms' from the queryset
        return FormGroup.objects.exclude(ref="system-forms")


class CreateFormGroupView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = FormGroup.objects.all()
    serializer_class = FormGroupSerializer



class EditDeleteFormGroupView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = FormGroup.objects.all()
    serializer_class = FormGroupSerializer
    lookup_field = 'id'  # or 'ref' or any other unique field of FormGroup


class CreateFormView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Form.objects.all()
    serializer_class = FormSerializer


class EditDeleteFormView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'ref'  # or another unique field of the Form model


class CreateSectionView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class EditDeleteSectionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    lookup_field = 'ref'  # or another unique field of the Section model


class CreateFieldView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class EditDeleteFieldView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    lookup_field = 'id_code'  # or another unique field of the Field model


class CreateStaticChoiceView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = StaticChoice.objects.all()
    serializer_class = StaticChoiceSerializer


class EditDeleteStaticChoiceView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = StaticChoice.objects.all()
    serializer_class = StaticChoiceSerializer
    lookup_field = 'ref'  # or another unique field of the StaticChoice model


class CreateStaticChoiceOptionView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = StaticChoiceOption.objects.all()
    serializer_class = StaticChoiceOptionSerializer


class EditDeleteStaticChoiceOptionView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = StaticChoiceOption.objects.all()
    serializer_class = StaticChoiceOptionSerializer
    lookup_field = 'id_code'  # or another unique field of the StaticChoiceOption model



class FormListView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated,]
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'group_ref'


class FormTemplateView(generics.RetrieveAPIView):
    queryset = Field.objects.all()
    lookup_field = 'section__form__ref'
    lookup_url_kwarg = 'form_ref'

    def get_static_choice_options(self, field):
        if field.choices_static and field.field_type in ["RADIO BUTTON", "CHECKBOX", "SINGLE SELECT", "MULTI SELECT"]:
            options = StaticChoiceOption.objects.filter(static_option=field.choices_static)
            return StaticChoiceOptionSerializer(options, many=True).data
        return None

    def retrieve(self, request, *args, **kwargs):
        form_ref = self.kwargs[self.lookup_url_kwarg]

        form_instance = Form.objects.filter(ref=form_ref).first()

        if not form_instance:
            raise NotFound(f"Form '{form_ref}' not found.")

        list_of_sections = form_instance.section_set.all()

        sections_with_fields = {}
        for section in list_of_sections:
            fields = Field.objects.filter(section=section)
            field_data = []
            for field in fields:
                serialized_field = FieldSerializer(field).data
                choice_options = self.get_static_choice_options(field)
                if choice_options:
                    serialized_field['choice_options'] = choice_options
                field_data.append(serialized_field)

            sections_with_fields[section.ref] = {
                'section_data': SectionSerializer(section).data,
                'fields': field_data
            }

        return Response(sections_with_fields)





# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Content &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ContentTextDetailView(generics.RetrieveAPIView):
    serializer_class = ContentTextSerializer
    queryset = ContentText.objects.all()
    lookup_field = 'ref'


class ContentImageDetailView(generics.RetrieveAPIView):
    serializer_class = ContentImageSerializer
    queryset = ContentImage.objects.all()
    lookup_field = 'ref'

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Contact us &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ContactUsCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactUsSerializer


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& CalendarEvent &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ViewUpdateDeleteCalendarEvent(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    lookup_field = 'id_code'


class CreateCalendarEvent(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer


class CompanyWideCalendarEventListView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    serializer_class = CalendarEventSerializer

    def get_queryset(self):
        year = self.kwargs['year']  # Assuming the year is passed as a URL parameter
        month = self.kwargs['month']  # Assuming the month is passed as a URL parameter
        queryset = CalendarEvent.objects.filter(date__year=year, date__month=month, is_private=False)
        return queryset


class PersonalCalendarEventListView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    serializer_class = CalendarEventSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        queryset = CalendarEvent.objects.filter(date__year=year, date__month=month)
        return queryset


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Vehicles &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class ViewVehicleTypes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer


class ViewUpdateDeleteVehicleInfo(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = VehicleInfo.objects.all()
    serializer_class = VehicleInfoSerializer
    lookup_field = 'id_code'


class CreateVehicleInfo(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = VehicleInfo.objects.all()
    serializer_class = VehicleInfoSerializer


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Various Types &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class ViewAssociateTypes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = AssociateType.objects.all()
    serializer_class = AssociateTypeSerializer


class ViewContractTypes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = ContractType.objects.all()
    serializer_class = ContractTypeSerializer


class ViewWasteStorageTypes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteStorageType.objects.all()
    serializer_class = WasteStorageTypeSerializer


class ViewWasteAnalysisParameters(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteAnalysisParameter.objects.all()
    serializer_class = WasteAnalysisParameterSerializer


class ViewWasteAnalysisPreparationStandards(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteAnalysisPreparationStandard.objects.all()
    serializer_class = WasteAnalysisPreparationStandardSerializer


class ViewWasteAnalysisPreparationMethods(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteAnalysisPreparationMethod.objects.all()
    serializer_class = WasteAnalysisPreparationMethodSerializer


class ViewWasteAnalysisStandards(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteAnalysisStandard.objects.all()
    serializer_class = WasteAnalysisStandardSerializer


class ViewWasteAnalysisMethods(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteAnalysisMethod.objects.all()
    serializer_class = WasteAnalysisMethodSerializer


class ViewUpdateDeleteLabAnalysisResult(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = LabAnalysisResult.objects.all()
    serializer_class = LabAnalysisResultSerializer
    lookup_field = 'id_code'


class CreateLabAnalysisResult(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = LabAnalysisResult.objects.all()
    serializer_class = LabAnalysisResultSerializer


class ViewWasteTreatmentMaterials(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteTreatmentMaterial.objects.all()
    serializer_class = WasteTreatmentMaterialSerializer


class ViewWasteTreatmentEquipments(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteTreatmentEquipment.objects.all()
    serializer_class = WasteTreatmentEquipmentSerializer


class ViewWasteTreatmentMethods(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteTreatmentMethod.objects.all()
    serializer_class = WasteTreatmentMethodSerializer


class ViewAssociateOfClientSummarys(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset =AssociateOfClient.objects.all()
    serializer_class = AssociateOfClientSummarySerializer
    # lookup_field = 'client__id_code'


class ViewUpdateDeleteAssociateOfClientDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = AssociateOfClient.objects.all()
    serializer_class = AssociateOfClientDetailSerializer
    lookup_field = 'id_code'


class CreateAssociateOfClientDetail(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = AssociateOfClient.objects.all()
    serializer_class = AssociateOfClientDetailSerializer

    def perform_create(self, serializer):
        # Get the authenticated user from the request object
        user = self.request.user

        # Set the client field in the serializer's validated data
        # to the client associated with the authenticated user
        serializer.validated_data['client'] = user.client

        # Call super to continue with the object creation
        super().perform_create(serializer)

class ViewContractSummarys(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Contract.objects.all()
    serializer_class = ContractSummarySerializer
    lookup_field = 'client__id_code'


class ViewUpdateDeleteContractDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = Contract.objects.all()
    serializer_class = ContractDetailSerializer
    lookup_field = 'id_code'


class CreateContractDetail(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = Contract.objects.all()
    serializer_class = ContractDetailSerializer


class ViewUpdateContractCommencement(generics.RetrieveUpdateAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = Contract.objects.all()
    serializer_class = ContractCommencementSerializer
    lookup_field = 'id_code'


class ViewUpdateContractTermination(generics.RetrieveUpdateAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = Contract.objects.all()
    serializer_class = ContractTerminationSerializer
    lookup_field = 'id_code'

#
class ViewPaymentSummarys_by_client(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Payment.objects.all()
    serializer_class = PaymentSummarySerializer
    lookup_field = 'client__id_code'


class ViewPaymentSummarys_by_contract(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Payment.objects.all()
    serializer_class = PaymentSummarySerializer
    lookup_field = 'contract__id_code'




class ViewUpdateDeletePaymentInstallment(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = Payment.objects.all()
    serializer_class = PaymentInstallmentSerializer
    lookup_field = 'id_code'


class CreatePaymentInstallment(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = Payment.objects.all()
    serializer_class = PaymentInstallmentSerializer


class ViewUpdatePaymentRecieved(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = Payment.objects.all()
    serializer_class = PaymentRecievedSerializer
    lookup_field = 'id_code'


#
class ViewWasteClassificationSystems(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteClassificationSystem.objects.all()
    serializer_class = WasteClassificationSystemSerializer


class ViewWasteClasses(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteClass.objects.all()
    serializer_class = WasteClassSerializer
    lookup_field = 'classification_system__ref'



class ViewUpdateDeleteWasteType(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteType.objects.all()
    serializer_class = WasteTypeSerializer
    lookup_field = 'id_code'


class CreateWasteType(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteType.objects.all()
    serializer_class = WasteTypeSerializer

# *****
class ViewUpdateDeleteWastePickupRequest(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WastePickupRequest.objects.all()
    serializer_class = WastePickupRequestSerializer
    lookup_field = 'id_code'


class CreateWastePickupRequest(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = WastePickupRequest.objects.all()
    serializer_class = WastePickupRequestSerializer


class ViewWastePickupRequests(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WastePickupRequest.objects.all()
    serializer_class = WastePickupRequestSerializer


# *****
class ViewUpdateDeleteWasteExpressedCharacteristic(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = WasteExpressedCharacteristic.objects.all()
    serializer_class = WasteExpressedCharacteristicSerializer
    lookup_field = 'id_code'


class CreateWasteExpressedCharacteristic(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = WasteExpressedCharacteristic.objects.all()
    serializer_class = WasteExpressedCharacteristicSerializer


#
class ViewUpdateDeleteWasteBatch(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatch.objects.all()
    serializer_class = WasteBatchSerializer
    lookup_field = 'id_code'


class CreateWasteBatch(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatch.objects.all()
    serializer_class = WasteBatchSerializer


class ViewWasteBatchReferenceCodes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = WasteBatch.objects.all()
    serializer_class = WasteBatchSummarySerializer

#
class ViewUpdateDeleteWasteSubBatch(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteSubBatch.objects.all()
    serializer_class = WasteSubBatchSerializer
    lookup_field = 'id_code'


class CreateWasteSubBatch(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteSubBatch.objects.all()
    serializer_class = WasteSubBatchSerializer


class ViewWasteSubBatchReferenceCodes(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = WasteSubBatch.objects.all()
    serializer_class = WasteSubBatchSummarySerializer
    lookup_field = 'WasteBatch__assigned_waste_reference_code'

#
class ViewUpdateDeleteWasteBatchInitialEvaluation(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchInitialEvaluation.objects.all()
    serializer_class = WasteBatchInitialEvaluationSerializer
    lookup_field = 'id_code'


class CreateWasteBatchInitialEvaluation(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchInitialEvaluation.objects.all()
    serializer_class = WasteBatchInitialEvaluationSerializer



class ViewUpdateDeleteWasteBatchSecondaryEvaluation(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchSecondaryEvaluation.objects.all()
    serializer_class = WasteBatchSecondaryEvaluationSerializer
    lookup_field = 'id_code'


class CreateWasteBatchSecondaryEvaluation(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchSecondaryEvaluation.objects.all()
    serializer_class = WasteBatchSecondaryEvaluationSerializer


class ViewUpdateDeleteWasteAssessment(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteAssessment.objects.all()
    serializer_class = WasteAssessmentSerializer
    lookup_field = 'id_code'


class CreateWasteAssessment(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteAssessment.objects.all()
    serializer_class = WasteAssessmentSerializer


class ViewUpdateDeleteWasteSample(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteSample.objects.all()
    serializer_class = WasteSampleSerializer
    lookup_field = 'id_code'


class CreateWasteSample(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = WasteSample.objects.all()
    serializer_class = WasteSampleSerializer


class ViewUpdateDeleteWasteBatchCostEstimation(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchCostEstimation.objects.all()
    serializer_class = WasteBatchCostEstimationSerializer
    lookup_field = 'id_code'


class CreateWasteBatchCostEstimation(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchCostEstimation.objects.all()
    serializer_class = WasteBatchCostEstimationSerializer


class ViewWasteBatchCostEstimations(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = WasteBatchCostEstimation.objects.all()
    serializer_class = WasteBatchCostEstimationSerializer


#

class ViewUpdateDeleteWasteAssociatedWithContract(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteAssociatedWithContract.objects.all()
    serializer_class = WasteAssociatedWithContractSerializer
    lookup_field = 'id_code'


class CreateWasteAssociatedWithContract(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = WasteAssociatedWithContract.objects.all()
    serializer_class = WasteAssociatedWithContractSerializer


class ViewUpdateDeleteWasteBatchAcceptanceAtOrigin(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchAcceptanceAtOrigin.objects.all()
    serializer_class = WasteBatchAcceptanceAtOriginSerializer
    lookup_field = 'id_code'


class CreateWasteBatchAcceptanceAtOrigin(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchAcceptanceAtOrigin.objects.all()
    serializer_class = WasteBatchAcceptanceAtOriginSerializer


class ViewUpdateDeleteWasteBatchAcceptanceAtDestination(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchAcceptanceAtDestination.objects.all()
    serializer_class = WasteBatchAcceptanceAtDestinationSerializer
    lookup_field = 'id_code'


class CreateWasteBatchAcceptanceAtDestination(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchAcceptanceAtDestination.objects.all()
    serializer_class = WasteBatchAcceptanceAtDestinationSerializer


class ViewUpdateDeleteWasteBatchStorageEnter(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchStorageEnter.objects.all()
    serializer_class = WasteBatchStorageEnterSerializer
    lookup_field = 'id_code'


class CreateWasteBatchStorageEnter(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchStorageEnter.objects.all()
    serializer_class = WasteBatchStorageEnterSerializer


class ViewUpdateDeleteWasteBatchStorageExit(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchStorageExit.objects.all()
    serializer_class = WasteBatchStorageExitSerializer
    lookup_field = 'id_code'


class CreateWasteBatchStorageExit(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchStorageExit.objects.all()
    serializer_class = WasteBatchStorageExitSerializer


class ViewUpdateDeleteWasteBatchTreatment(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchTreatment.objects.all()
    serializer_class = WasteBatchTreatmentSerializer
    lookup_field = 'id_code'


class CreateWasteBatchTreatment(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchTreatment.objects.all()
    serializer_class = WasteBatchTreatmentSerializer


class ViewUpdateDeleteLab(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    lookup_field = 'id_code'


class CreateLab(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class ViewLabSummaries(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = Lab.objects.all()
    serializer_class = LabSummarySerializer


#######################
class ViewUpdateDeleteWasteBatchTCLPTestResult(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchTCLPTestResult.objects.all()
    serializer_class = WasteBatchTCLPTestResultSerializer
    lookup_field = 'id_code'


class CreateWasteBatchTCLPTestResult(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchTCLPTestResult.objects.all()
    serializer_class = WasteBatchTCLPTestResultSerializer


class ViewUpdateDeleteWasteBatchLandfilling(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = WasteBatchLandfilling.objects.all()
    serializer_class = WasteBatchLandfillingSerializer
    lookup_field = 'id_code'


class CreateWasteBatchLandfilling(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = WasteBatchLandfilling.objects.all()
    serializer_class = WasteBatchLandfillingSerializer


class ViewUpdateDeleteLandfillDailyReport(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = LandfillDailyReport.objects.all()
    serializer_class = LandfillDailyReportSerializer
    lookup_field = 'id_code'


class CreateLandfillDailyReport(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = LandfillDailyReport.objects.all()
    serializer_class = LandfillDailyReportSerializer


class CreateCustomerOfClientEvaluation(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = CustomerOfClientEvaluation.objects.all()
    serializer_class = CustomerOfClientEvaluationSerializer

#
class ViewHSEAccidentType(generics.ListAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataFromYourCompany]
    queryset = HSEAccidentType.objects.all()
    serializer_class = HSEAccidentTypeSerializer


class ViewUpdateDeleteHSEAccidentReport(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated, OnlySeeDataYouOwn]
    queryset = HSEAccidentReport.objects.all()
    serializer_class = HSEAccidentReportSerializer
    lookup_field = 'id_code'


class CreateHSEAccidentReport(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated, ]
    queryset = HSEAccidentReport.objects.all()
    serializer_class = HSEAccidentReportSerializer
