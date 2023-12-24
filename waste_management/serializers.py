from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import (
    User, ObjectBase, FacilityType, Location, ContactType, Contact, MembershipType, ClientStatus, Client,
    Language, Calendar, Department, Role, UserPosition, DocumentFile, ImageFile,
    StaticChoice, StaticChoiceOption, Section, Field, FormGroup, Form,
    ContentText, ContentImage, ContactUs, CalendarEvent,

    VehicleType, VehicleInfo, AssociateType, ContractType, WasteStorageType, WasteAnalysisParameter,
    WasteAnalysisPreparationStandard, WasteAnalysisStandard, WasteAnalysisMethod, LabAnalysisResult,
    WasteTreatmentMaterial, WasteTreatmentEquipment, WasteTreatmentMethod,
    AssociateOfClient, Contract, Payment, WasteClassificationSystem, WasteClass, WasteType, WastePickupRequest,
    WasteExpressedCharacteristic, WasteBatch, WasteSubBatch, WasteBatchInitialEvaluation, WasteBatchSecondaryEvaluation,
    WasteAssessment, WasteSample, WasteBatchCostManHour, WasteBatchCostEquipment, WasteBatchCostMaterial,
    WasteBatchCostEstimation,
    WasteAssociatedWithContract, WasteBatchAcceptanceAtOrigin, WasteBatchAcceptanceAtDestination,
    WasteBatchStorageEnter, WasteBatchStorageExit, WasteBatchTreatment, Lab, WasteBatchTCLPTestResult,
    WasteBatchLandfilling, LandfillDailyReport,
    CustomerOfClientEvaluation, WasteAnalysisPreparationMethod, HSEAccidentType, HSEAccidentReport,
)


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        read_only_fields = ('username', 'first_name', 'last_name')


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Object &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ObjectBaseSerializer(serializers.ModelSerializer):
    auther = UserMinimalSerializer()

    class Meta:
        model = ObjectBase
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Location &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class FacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityType
        fields = ('name',)
        read_only_fields = ('name',)


class LocationSerializer(serializers.ModelSerializer):
    facility_type = FacilityTypeSerializer()

    class Meta:
        model = Location
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Contact &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = ('name',)
        read_only_fields = ('name',)


class ContactSerializer(serializers.ModelSerializer):
    contact_type = ContactTypeSerializer()

    class Meta:
        model = Contact
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Client &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = ('name', 'description')
        read_only_fields = ('name', 'description')


class ClientStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientStatus
        fields = ('name', 'description')
        read_only_fields = ('name', 'description')


class ClientDetailSerializer(serializers.ModelSerializer):
    membership_type = MembershipTypeSerializer()
    current_status = ClientStatusSerializer()
    location = LocationSerializer()
    contact = ContactSerializer()

    class Meta:
        model = Client
        fields = ('name', 'membership_type', 'current_status', 'location', 'contact', 'logo')

        read_only_fields = ('membership_type', 'current_status')


class ClientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id_code', 'name', 'logo')
        read_only_fields = ('id_code', 'name', 'logo')


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Language and Calendar &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& User &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class UserFullDetailSerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer()
    selected_language = LanguageSerializer()
    selected_calender = CalendarSerializer()

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('is_client_admin', 'is_staff', 'is_active', 'date_joined')


class UserDetailSerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer()
    selected_language = LanguageSerializer()
    selected_calender = CalendarSerializer()

    class Meta:
        model = User
        fields = (
        'username', 'first_name', 'last_name', 'date_joined', 'client', 'email', 'phone_number', 'profile_image',
        'signature_image', 'selected_language', 'selected_calender')
        read_only_fields = ('username', 'date_joined', 'client', 'email', 'first_name', 'last_name', 'username')


class UserSummarySerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'client', 'profile_image')
        read_only_fields = ('username', 'first_name', 'last_name', 'client', 'profile_image')


class ChangeUserPasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('The old password is incorrect. Please try again.')
            )
        return value  # This line returns the old password if it's valid

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The new passwords do not match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


# &&&&&&&&&&&&&&&&&&&&&&&&&&&& Department, Roles & Positions &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class DepartmentSerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer()

    class Meta:
        model = Department
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer()

    class Meta:
        model = Role
        fields = '__all__'


class UserPositionSerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer()
    department = DepartmentSerializer()
    role = RoleSerializer()

    class Meta:
        model = UserPosition
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& User Files &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class DocumentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = '__all__'


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Form Templates &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class FormGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormGroup
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    # group = FormGroupSerializer()
    group = serializers.PrimaryKeyRelatedField(queryset=FormGroup.objects.all())

    class Meta:
        model = Form
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())

    class Meta:
        model = Section
        fields = '__all__'


class StaticChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticChoice
        fields = '__all__'


class StaticChoiceOptionSerializer(serializers.ModelSerializer):
    static_option = StaticChoiceSerializer()

    class Meta:
        model = StaticChoiceOption
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    choices_static = serializers.PrimaryKeyRelatedField(
        queryset=StaticChoice.objects.all(),
        required=False,  # Allow this field to be optional
        allow_null=True  # Allow null values
    )

    class Meta:
        model = Field
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Content &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ContentTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentText
        fields = '__all__'


class ContentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentImage
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Contact us &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& CalendarEvent &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Vehicles &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ('name',)
        read_only_fields = ('name',)


class VehicleInfoSerializer(serializers.ModelSerializer):
    vehicle_type = VehicleTypeSerializer()

    class Meta:
        model = VehicleInfo
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Various Types &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class AssociateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociateType
        fields = ('ref', 'name',)
        read_only_fields = ('ref', 'name',)


class ContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractType
        fields = ('ref', 'name',)
        read_only_fields = ('ref', 'name',)


class WasteStorageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteStorageType
        fields = ('name', 'description')
        read_only_fields = ('name', 'description')


class WasteAnalysisParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteAnalysisParameter
        fields = ('ref', 'name', 'description')
        read_only_fields = ('ref', 'name', 'description')


class WasteAnalysisPreparationStandardSerializer(serializers.ModelSerializer):
    related_document = DocumentFileSerializer()

    class Meta:
        model = WasteAnalysisPreparationStandard
        fields = ('ref', 'name', 'description', 'reference', 'related_document')
        read_only_fields = ('ref', 'name', 'description', 'reference', 'related_document')


class WasteAnalysisPreparationMethodSerializer(serializers.ModelSerializer):
    related_document = DocumentFileSerializer()

    class Meta:
        model = WasteAnalysisPreparationMethod
        fields = ('ref', 'name', 'description', 'reference', 'related_document')
        read_only_fields = ('ref', 'name', 'description', 'reference', 'related_document')


class WasteAnalysisStandardSerializer(serializers.ModelSerializer):
    related_document = DocumentFileSerializer()

    class Meta:
        model = WasteAnalysisStandard
        fields = ('ref', 'name', 'description', 'reference', 'related_document')
        read_only_fields = ('ref', 'name', 'description', 'reference', 'related_document')


class WasteAnalysisMethodSerializer(serializers.ModelSerializer):
    related_document = DocumentFileSerializer()

    class Meta:
        model = WasteAnalysisMethod
        fields = ('ref', 'name', 'description', 'reference', 'related_document')
        read_only_fields = ('ref', 'name', 'description', 'reference', 'related_document')


class LabAnalysisResultSerializer(serializers.ModelSerializer):
    parameter = WasteAnalysisParameterSerializer()
    analysis_method = WasteAnalysisMethodSerializer()
    analysis_standard = WasteAnalysisStandardSerializer()

    class Meta:
        model = LabAnalysisResult
        fields = '__all__'


class WasteTreatmentMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTreatmentMaterial
        fields = ('ref', 'name', 'description')
        read_only_fields = ('ref', 'name', 'description')


class WasteTreatmentEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTreatmentEquipment
        fields = ('ref', 'name', 'description')
        read_only_fields = ('ref', 'name', 'description')


class WasteTreatmentMethodSerializer(serializers.ModelSerializer):
    treatment_material = WasteTreatmentMaterialSerializer()
    treatment_equipment = WasteTreatmentEquipmentSerializer()
    related_document = DocumentFileSerializer()

    class Meta:
        model = WasteTreatmentMethod
        fields = '__all__'
        read_only_fields = ('ref',)


####################################################################
class AssociateOfClientDetailSerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer()
    type = AssociateTypeSerializer()
    location = LocationSerializer()
    contact = ContactSerializer()

    class Meta:
        model = AssociateOfClient
        fields = '__all__'


class AssociateOfClientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociateOfClient
        fields = ('name',)
        read_only_fields = ('name',)


class ContractDetailSerializer(serializers.ModelSerializer):
    associate = AssociateOfClientSummarySerializer()
    type_of_contract = ContractTypeSerializer()
    attachment = DocumentFileSerializer()

    class Meta:
        model = Contract
        fields = ('associate', 'type_of_contract', 'reference_code', 'title', 'duration_in_days', 'date_of_signing',
                  'agreed_start_date', 'agreed_end_date',
                  'total_price', 'AP_guarantee', 'performance_bond', 'has_performance_guarantee', 'currency',
                  'job_description', 'notes', 'attachment')


class ContractCommencementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('title', 'commencement_date')
        read_only_fields = ('title',)


class ContractTerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('title', 'actual_end_date')
        read_only_fields = ('title',)


class ContractSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('title',)


class PaymentInstallmentSerializer(serializers.ModelSerializer):
    contract = ContractSummarySerializer()

    class Meta:
        model = Payment
        fields = ('contract', 'amount', 'currency', 'due_date')


class PaymentRecievedSerializer(serializers.ModelSerializer):
    contract = ContractSummarySerializer()

    class Meta:
        model = Payment
        fields = ('contract', 'due_date', 'date_paid', 'reference_number', 'comments')
        read_only_fields = ('contract', 'due_date')


class PaymentSummarySerializer(serializers.ModelSerializer):
    contract = ContractSummarySerializer()

    class Meta:
        model = Payment
        fields = ('contract', 'amount', 'currency', 'due_date', 'date_paid')
        read_only_fields = ('contract', 'amount', 'currency', 'due_date', 'date_paid')


class WasteClassificationSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteClassificationSystem
        fields = ('name', 'description')
        read_only_fields = ('name', 'description')


class WasteClassSerializer(serializers.ModelSerializer):
    classification_system = WasteClassificationSystemSerializer()

    class Meta:
        model = WasteClass
        fields = ('classification_system', 'class_name', 'description')


class WasteTypeSerializer(serializers.ModelSerializer):
    waste_class = WasteClassSerializer()

    class Meta:
        model = WasteType
        fields = '__all__'


class WastePickupRequestSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    pickup_location = LocationSerializer()

    class Meta:
        model = WastePickupRequest
        fields = '__all__'


class WasteExpressedCharacteristicSerializer(serializers.ModelSerializer):
    related_pickup_request = WastePickupRequestSerializer()
    storage_type = WasteStorageTypeSerializer()
    waste_class = WasteClassSerializer()
    MSDS_document = DocumentFileSerializer()
    process_info_document = DocumentFileSerializer()
    treatment_info_document = DocumentFileSerializer()
    basic_characterization_document = DocumentFileSerializer()
    images = ImageFileSerializer()
    other_documents = DocumentFileSerializer()

    class Meta:
        model = WasteExpressedCharacteristic
        fields = '__all__'


class WasteBatchSerializer(serializers.ModelSerializer):
    customer = AssociateOfClientSummarySerializer()
    contract = ContractSummarySerializer()
    related_WasteExpressedCharacteristic = WasteExpressedCharacteristicSerializer()
    waste_class = WasteClassSerializer()

    class Meta:
        model = WasteBatch
        fields = '__all__'


class WasteBatchSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBatch
        fields = ('assigned_waste_reference_code',)


class WasteSubBatchSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()

    class Meta:
        model = WasteSubBatch
        fields = '__all__'


class WasteSubBatchSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteSubBatch
        fields = ('assigned_waste_reference_code',)


class WasteBatchInitialEvaluationSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    recommended_assessor = UserSummarySerializer()

    class Meta:
        model = WasteBatchInitialEvaluation
        fields = '__all__'


class WasteBatchSecondaryEvaluationSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    images = ImageFileSerializer()
    documents = DocumentFileSerializer()

    class Meta:
        model = WasteBatchSecondaryEvaluation
        fields = '__all__'


class WasteAssessmentSerializer(serializers.ModelSerializer):
    customer = AssociateOfClientSummarySerializer()
    contract = ContractSummarySerializer()
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    waste_class = WasteClassSerializer()
    storage_type = WasteStorageTypeSerializer()
    images = ImageFileSerializer()
    related_miscellaneous_documents = DocumentFileSerializer()

    class Meta:
        model = WasteAssessment
        fields = '__all__'


class WasteSampleSerializer(serializers.ModelSerializer):
    related_waste_assessment = WasteAssessmentSerializer()

    class Meta:
        model = WasteSample
        fields = '__all__'


class WasteBatchCostManHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBatchCostManHour
        fields = '__all__'


class WasteBatchCostEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBatchCostEquipment
        fields = '__all__'


class WasteBatchCostMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBatchCostMaterial
        fields = '__all__'


class WasteBatchCostEstimationSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    man_hours = WasteBatchCostManHourSerializer()
    equipments = WasteBatchCostEquipmentSerializer()
    materials = WasteBatchCostMaterialSerializer()

    class Meta:
        model = WasteBatchCostEstimation
        fields = '__all__'


class WasteAssociatedWithContractSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()

    class Meta:
        model = WasteAssociatedWithContract
        fields = '__all__'


class WasteBatchAcceptanceAtOriginSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    vehicle_info = VehicleInfoSerializer()
    images = ImageFileSerializer()
    documents = DocumentFileSerializer()

    class Meta:
        model = WasteBatchAcceptanceAtOrigin
        fields = '__all__'


class WasteBatchAcceptanceAtDestinationSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    vehicle_info = VehicleInfoSerializer()
    hauling_document = DocumentFileSerializer()
    images = ImageFileSerializer()
    scale_print_document = DocumentFileSerializer()

    class Meta:
        model = WasteBatchAcceptanceAtDestination
        fields = '__all__'


class WasteBatchStorageEnterSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    storage_type = WasteStorageTypeSerializer()
    images = ImageFileSerializer()
    documents = DocumentFileSerializer()

    class Meta:
        model = WasteBatchStorageEnter
        fields = '__all__'


class WasteBatchStorageExitSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    wasteBatchStorageEnter = WasteBatchStorageEnterSerializer()
    images = ImageFileSerializer()
    documents = DocumentFileSerializer()

    class Meta:
        model = WasteBatchStorageExit
        fields = '__all__'


class WasteBatchTreatmentSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    treatment_type = WasteTreatmentMethodSerializer()
    treatment_material_type = WasteTreatmentMaterialSerializer()
    images = ImageFileSerializer()
    documents = DocumentFileSerializer()

    class Meta:
        model = WasteBatchTreatment
        fields = '__all__'


class LabSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    contact = ContactSerializer()

    class Meta:
        model = Lab
        fields = '__all__'


class LabSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ('name',)


class WasteBatchTCLPTestResultSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()
    lab = LabSerializer()
    analysis_preparation_method = WasteAnalysisPreparationMethodSerializer()
    analysis_result = LabAnalysisResultSerializer()
    images = ImageFileSerializer()
    documents = DocumentFileSerializer()

    class Meta:
        model = WasteBatchTCLPTestResult
        fields = '__all__'


class WasteBatchLandfillingSerializer(serializers.ModelSerializer):
    related_waste_batch = WasteBatchSerializer()
    related_waste_SUB_batch = WasteSubBatchSerializer()

    class Meta:
        model = WasteBatchLandfilling
        fields = '__all__'


class LandfillDailyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandfillDailyReport
        fields = '__all__'


class CustomerOfClientEvaluationSerializer(serializers.ModelSerializer):
    CustomerOfClient = AssociateOfClientSummarySerializer()

    class Meta:
        model = CustomerOfClientEvaluation
        fields = '__all__'


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& HSE &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class HSEAccidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSEAccidentType
        fields = ('name', 'description')
        read_only_fields = ('name', 'description')


class HSEAccidentReportSerializer(serializers.ModelSerializer):
    type = HSEAccidentTypeSerializer()

    class Meta:
        model = HSEAccidentReport
        fields = '__all__'
