from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import ValidationError
import os
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone
# import magic

QUANTITY_UNIT_CHOICES = (
    ("Kg", "kg"),
)

CURRENCY_UNIT_CHOICES = (
    ("Rial", "Rial"),
)

DENSITY_UNIT_CHOICES = (
    ("kg/lit", "kg/lit"),

)

CONCENTRATION_UNIT_CHOICES = (
    ("mg/lit", "mg/lit"),

)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Reusable functions &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

def generate_unique_ids(prefix, k):
    fixed_chars = prefix
    random_chars = str(uuid.uuid4().hex)[:k]
    unique_id = fixed_chars + random_chars
    return unique_id


def json_default():
    return {"en": "English content", "fa": "محتوای فارسی"}


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Validators &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def validate_file_size(fieldfile_obj):
    megabyte_limit = 5
    filesize = fieldfile_obj.file.size
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(_(f"Max file size is {megabyte_limit}MB"))


def validate_image_file_content(file):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/tiff', 'application/postscript', 'image/svg+xml']
    # file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    # if file_mime_type not in valid_mime_types:
    #     raise ValidationError(
    #         _('Unsupported file type. Only JPEG, PNG, GIF, TIFF, EPS, and SVG images are allowed.')
    #     )


def validate_document_file_content(file):
    valid_mime_types = ['application/pdf', 'application/msword',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        'application/vnd.ms-powerpoint',
                        'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/zip',
                        'application/x-rar']
    # file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    # if file_mime_type not in valid_mime_types:
    #     raise ValidationError(
    #         _('Unsupported file type. Only PDF, Word, Excel, PowerPoint, and ZIP files are allowed.')
    #     )


def validate_image_file_extension(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.tif', '.eps', '.svg']
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _('File type not supported. Only JPEG, PNG, GIF, tif, eps, and svg images are allowed.')
        )


def validate_document_file_extension(file):
    valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pps', '.ppsx', '.zip', '.rar']
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _('File type not supported. Only PDF, Word, Excel, PowerPoint, and zip files are allowed.')
        )


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Upload Destinations &&&&&&&&&&&&&&&&&&&&&&&&&&&&&

def earthlytix_uploads_path(instance, filename):
    ext = filename.split('.')[-1]
    random_name = "%s.%s" % (uuid.uuid4(), ext)
    return "SybanUploads/" + random_name


def user_uploads_path(instance, filename):
    ext = filename.split('.')[-1]
    random_name = "%s.%s" % (uuid.uuid4(), ext)
    return "UserUploads/" + random_name


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Reusable Models &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class FacilityType(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)

    def __str__(self):
        return self.ref


class Location(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility_type = models.ForeignKey(FacilityType, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50, blank=True, null=True)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)


class ContactType(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)

    def __str__(self):
        return self.ref


class Contact(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact_type = models.ForeignKey(ContactType, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True)


class MembershipType(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.ref


class ClientStatus(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.ref


# *******
class Language(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    content = models.JSONField(default=json_default)

    def __str__(self):
        return self.ref


class Calendar(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    content = models.JSONField(default=json_default)

    def __str__(self):
        return self.ref


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Client Data &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class Client(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    access_code = models.CharField(max_length=50, null=True, blank=True)
    membership_type = models.ForeignKey(MembershipType, null=True, blank=True, on_delete=models.SET_NULL)
    current_status = models.ForeignKey(ClientStatus, null=True, blank=True, on_delete=models.SET_NULL)

    location = models.ManyToManyField(Location)
    contact = models.ManyToManyField(Contact)

    logo = models.ImageField(upload_to=user_uploads_path, validators=[validate_file_size, validate_image_file_extension,
                                                                      validate_image_file_content], blank=True,
                             null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to=user_uploads_path,
                                      validators=[validate_file_size, validate_image_file_extension,
                                                  validate_image_file_content], blank=True, null=True)
    signature_image = models.ImageField(upload_to=user_uploads_path,
                                        validators=[validate_file_size, validate_image_file_extension,
                                                    validate_image_file_content], blank=True, null=True)
    selected_language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    selected_calender = models.ForeignKey(Calendar, on_delete=models.SET_NULL, blank=True, null=True)
    is_client_admin = models.BooleanField(default=False)

    # Override the groups and user_permissions fields with unique related_names
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Unique related_name for this User model
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permission_set',  # Unique related_name for this User model
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    """
    User already has these fields
        username: A unique string that identifies the user.
        password: A hashed version of the user's password.
        email: The user's email address.
        first_name: The user's first name.
        last_name: The user's last name.
        is_staff: A boolean indicating whether the user can access the admin site.
        is_active: A boolean indicating whether the user account is active.
        date_joined: The date and time the user account was created.
    """

    def __str__(self):
        return self.username


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Base Models &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class ObjectBase(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_last_modified = models.DateTimeField(auto_now=True)
    auther = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_by_the_form_submitter = models.BooleanField(default=False)
    approved_date_time = models.DateTimeField(null=True, blank=True)
    archieved_by_the_form_submitter = models.BooleanField(default=False)
    archieved_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id_code)

    def save(self, *args, **kwargs):
        # Check if this instance has been persisted previously
        if not self._state.adding:
            # It has been saved before; check the original value from _loaded_values

            # For approved status
            original_approved_status = self._state._loaded_values.get("approved_by_the_form_submitter")
            # Only update approved_date_time if original_approved_status is different
            if original_approved_status != self.approved_by_the_form_submitter:
                self.approved_date_time = timezone.now()

            # For archieved status
            original_archieved_status = self._state._loaded_values.get("archieved_by_the_form_submitter")
            # Only update archieved_date_time if original_archieved_status is different
            if original_archieved_status != self.archieved_by_the_form_submitter:
                self.archieved_date_time = timezone.now()
        else:
            # This is a new instance being saved for the first time
            self.approved_date_time = None  # Or set it to any default value you prefer
            self.archieved_date_time = None  # Likewise for archieved_date_time

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# &&&&&&&&&&&&&&&&&&&&&&&&&&&& Department, Roles & Positions &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class Department(ObjectBase):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)


class Role(ObjectBase):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)


class UserPosition(ObjectBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_positions")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& User Files &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class DocumentFile(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_note = models.CharField(max_length=50)
    document = models.FileField(upload_to=user_uploads_path,
                                validators=[validate_file_size, validate_document_file_extension,
                                            validate_document_file_content])


class ImageFile(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_note = models.CharField(max_length=50)
    image = models.ImageField(upload_to=user_uploads_path,
                              validators=[validate_file_size, validate_image_file_extension,
                                          validate_image_file_content])


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Form Templates &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class FormGroup(models.Model):
    ref = models.CharField(max_length=50, primary_key=True)
    name = models.JSONField(default=json_default)
    logo = models.ImageField(upload_to=earthlytix_uploads_path,
                             validators=[validate_file_size, validate_image_file_extension], blank=True, null=True)

    def __str__(self):
        return self.ref


class Form(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    group = models.ForeignKey(FormGroup, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default)
    create_url = models.URLField(blank=True, null=True)
    update_url = models.URLField(blank=True, null=True)
    delete_url = models.URLField(blank=True, null=True)
    list_url = models.URLField(blank=True, null=True)
    pdf_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.group.ref, self.ref)


class Section(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    title = models.JSONField(default=json_default)
    help_text = models.JSONField(default=json_default, blank=True, null=True)
    repeat_enabled = models.BooleanField()

    def __str__(self):
        return '{} - {}'.format(self.form.ref, self.ref)


class StaticChoice(models.Model):
    ref = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.ref


class StaticChoiceOption(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    static_option = models.ForeignKey(StaticChoice, related_name='options', on_delete=models.CASCADE)
    content = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.static_option.ref)


FIELD_TYPE_CHOICES = (
    ("SMALL TEXT BOX", "small text box"),
    ("LARGE TEXT BOX", "large text box"),
    ("NUMERIC POSITIVE INTEGER", "numeric positive integer"),
    ("NUMERIC FLOAT", "numeric float"),
    ("RADIO BUTTON", "radio button"),
    ("CHECKBOX", "checkbox"),
    ("YES OR NO", "yes or no"),
    ("SINGLE SELECT", "single select"),
    ("MULTI SELECT", "multi select"),
    ("EMAIL", "email"),
    ("PASSWORD", "password"),
    ("DATE", "date"),
    ("TIME", "time"),
    ("IMAGE", "image"),
    ("DOCUMENT", "document"),

)


class Field(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.CASCADE)
    order_in_section = models.PositiveSmallIntegerField()
    inquiry = models.JSONField(default=json_default)
    help_text = models.JSONField(default=json_default, blank=True, null=True)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE_CHOICES, default=FIELD_TYPE_CHOICES[0][0])
    choices_static = models.ForeignKey(StaticChoice, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    mandatory = models.BooleanField(default=False)
    default_value = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.section.ref, self.order_in_section)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Content &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class ContentBase(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref = models.CharField(max_length=50)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ref

    class Meta:
        abstract = True


class ContentText(ContentBase):
    name = models.JSONField(default=json_default)
    content = models.JSONField(default=json_default)


class ContentImage(ContentBase):
    image_caption = models.CharField(max_length=50, unique=True)
    content_image = models.ImageField(upload_to=earthlytix_uploads_path, validators=[validate_file_size], blank=True,
                                      null=True)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Contact us &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class ContactUs(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    company = models.CharField(max_length=50, blank=True, null=True)
    product = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& CalendarEvent &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class CalendarEvent(ObjectBase):
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.date, self.title)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Vehicles &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class VehicleType(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)

    def __str__(self):
        return self.ref


class VehicleInfo(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_type = models.ForeignKey(VehicleType, null=True, blank=True, on_delete=models.SET_NULL)
    license_number = models.CharField(max_length=50)
    driver_first_name = models.CharField(max_length=50)
    driver_surname = models.CharField(max_length=50)
    driver_phone = models.CharField(max_length=50, blank=True, null=True)
    is_the_label_attached = models.BooleanField()
    is_the_cargo_specifications_consistent_with_the_bill_of_lading = models.BooleanField()
    amount_of_waste_transported = models.FloatField()
    unit_of_waste_quantity = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES,
                                              default=QUANTITY_UNIT_CHOICES[0][0])


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Various Types &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class AssociateType(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)

    def __str__(self):
        return self.ref


# *******
class ContractType(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)

    def __str__(self):
        return self.ref


# *******
class WasteStorageType(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.ref


# *******
class WasteAnalysisParameter(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.ref


class WasteAnalysisPreparationStandard(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    related_document = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.ref


class WasteAnalysisPreparationMethod(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    related_document = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.ref


class WasteAnalysisStandard(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    related_document = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.ref


class WasteAnalysisMethod(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    related_document = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.ref


###
class LabAnalysisResult(ObjectBase):
    parameter = models.ForeignKey(WasteAnalysisParameter, on_delete=models.SET_NULL, blank=True, null=True)
    value = models.FloatField()
    unit_of_concentration = models.CharField(max_length=50, choices=CONCENTRATION_UNIT_CHOICES,
                                             default=CONCENTRATION_UNIT_CHOICES[0][0])
    detection_limit = models.FloatField(blank=True, null=True)
    analysis_method = models.ForeignKey(WasteAnalysisMethod, on_delete=models.SET_NULL, blank=True, null=True)
    analysis_standard = models.ForeignKey(WasteAnalysisStandard, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class WasteTreatmentMaterial(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.ref


class WasteTreatmentEquipment(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.ref


class WasteTreatmentMethod(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)
    treatment_material = models.ForeignKey(WasteTreatmentMaterial, on_delete=models.SET_NULL, blank=True, null=True)
    treatment_equipment = models.ForeignKey(WasteTreatmentEquipment, on_delete=models.SET_NULL, blank=True, null=True)
    related_document = models.ForeignKey(DocumentFile, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.ref


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Customers, contracts and payments &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class AssociateOfClient(ObjectBase):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.ForeignKey(AssociateType, null=True, blank=True, on_delete=models.SET_NULL)
    reference_code = models.CharField(unique=True, default=generate_unique_ids('A-', 6), editable=False, max_length=50)
    name = models.CharField(max_length=50)
    location = models.ManyToManyField(Location, blank=True)
    contact = models.ManyToManyField(Contact, blank=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.client.name, self.name)


class Contract(ObjectBase):
    associate = models.ForeignKey(AssociateOfClient, null=True, blank=True, on_delete=models.SET_NULL)
    type_of_contract = models.ForeignKey(ContractType, null=True, blank=True, on_delete=models.CASCADE)
    reference_code = models.CharField(unique=True, default=generate_unique_ids('Contract-', 6), editable=False,
                                      max_length=50)
    title = models.CharField(max_length=50)
    duration_in_days = models.IntegerField(blank=True, null=True)
    date_of_signing = models.DateField()
    agreed_start_date = models.DateField()
    commencement_date = models.DateField()
    agreed_end_date = models.DateField()
    actual_end_date = models.DateField()
    total_price = models.FloatField()
    AP_guarantee = models.FloatField(blank=True, null=True)
    performance_bond = models.FloatField(blank=True, null=True)
    has_performance_guarantee = models.BooleanField()
    currency = models.CharField(max_length=50, choices=CURRENCY_UNIT_CHOICES, default=CURRENCY_UNIT_CHOICES[0][0])
    job_description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    attachment = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{} - {}'.format(self.associate.name, self.title)


class Payment(ObjectBase):
    contract = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    currency = models.CharField(max_length=50, choices=CURRENCY_UNIT_CHOICES, default=CURRENCY_UNIT_CHOICES[0][0])
    due_date = models.DateField()
    date_paid = models.DateField()
    reference_number = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.amount, self.currency, self.due_date)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Classification &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class WasteClassificationSystem(models.Model):
    ref = models.CharField(max_length=50, primary_key=True)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.ref


class WasteClass(ObjectBase):
    classification_system = models.ForeignKey(WasteClassificationSystem, on_delete=models.CASCADE)
    class_name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.class_name


class WasteType(ObjectBase):
    name = models.CharField(max_length=50)
    is_hazardous = models.BooleanField()
    waste_class = models.ForeignKey(WasteClass, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.JSONField(default=json_default)
    handling_instructions = models.JSONField(default=json_default, blank=True, null=True)
    regulations_compliance = models.JSONField(default=json_default, blank=True, null=True)
    packaging_requirements = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.name


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Initial Pickup Request &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class WastePickupRequest(ObjectBase):
    name_of_client_company = models.CharField(max_length=50)
    person_requesting_first_name = models.CharField(max_length=50)
    person_requesting_last_name = models.CharField(max_length=50)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, blank=True, null=True)
    pickup_location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    is_based_on_past_contract = models.BooleanField()
    contract_title = models.CharField(max_length=50, blank=True, null=True)


WASTE_STATE_CHOICES = (
    ("Solid Powder", "Solid Powder"),
    ("Solid Non-Powder", "Solid Non-Powder"),
    ("Semi-Solid (Sludge)", "Semi-Solid (Sludge)"),
    ("Liquid", "Liquid"),
    ("Other", "Other"),
)


class WasteExpressedCharacteristic(ObjectBase):
    related_pickup_request = models.ForeignKey(WastePickupRequest, on_delete=models.CASCADE)
    description_of_waste = models.CharField(max_length=50)
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    state = models.CharField(max_length=50, choices=WASTE_STATE_CHOICES, default=WASTE_STATE_CHOICES[0][0])
    density = models.FloatField(null=True, blank=True)
    density_unit = models.CharField(max_length=50, choices=DENSITY_UNIT_CHOICES, default=DENSITY_UNIT_CHOICES[0][0])
    color = models.TextField(null=True, blank=True)
    odor = models.TextField(null=True, blank=True)
    storage_type = models.ForeignKey(WasteStorageType, on_delete=models.SET_NULL, blank=True, null=True)
    number_of_containers = models.IntegerField(null=True, blank=True)
    waste_class = models.ForeignKey(WasteClass, null=True, blank=True, on_delete=models.CASCADE)
    is_MSDS_document_available = models.BooleanField()
    is_process_info_document_available = models.BooleanField()
    is_treatment_info_document_available = models.BooleanField(default=False)
    is_basic_characterization_document_available = models.BooleanField(default=False)
    party_responsible_for_hauling = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    image = models.ForeignKey(ImageFile, null=True, blank=True, on_delete=models.SET_NULL)
    document = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Define waste batch and sub-batch &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class WasteBatch(ObjectBase):
    customer = models.ForeignKey(AssociateOfClient, null=True, blank=True, on_delete=models.SET_NULL)
    contract = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_waste_reference_code = models.CharField(unique=True, default=generate_unique_ids('WB-', 12),
                                                     editable=False, max_length=50)
    related_WasteExpressedCharacteristic = models.ForeignKey(WasteExpressedCharacteristic, null=True, blank=True,
                                                             on_delete=models.SET_NULL)

    waste_class = models.ForeignKey(WasteClass, null=True, blank=True, on_delete=models.SET_NULL)

    description_of_waste = models.CharField(max_length=50)
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    state = models.CharField(max_length=50, choices=WASTE_STATE_CHOICES, default=WASTE_STATE_CHOICES[0][0])
    density = models.FloatField(null=True, blank=True)
    density_unit = models.CharField(max_length=50, choices=DENSITY_UNIT_CHOICES, default=DENSITY_UNIT_CHOICES[0][0])


class WasteSubBatch(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    assigned_waste_reference_code = models.CharField(unique=True, default=generate_unique_ids('SUB-', 8),
                                                     editable=False, max_length=50)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Initial and Secondary Evaluation &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class WasteBatchInitialEvaluation(ObjectBase):
    date_of_initial_evaluation = models.DateField()
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    is_assessment_required = models.BooleanField()
    is_sampling_required = models.BooleanField()
    recommendation = models.TextField(null=True, blank=True)


class WasteBatchSecondaryEvaluation(ObjectBase):
    date_of_secondary_evaluation = models.DateField()
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    is_analysis_required = models.BooleanField()
    analysis_preparation_method = models.CharField(max_length=50, blank=True, null=True)
    suggested_analysis_parameters = models.CharField(max_length=50, blank=True, null=True)
    suggested_disposal_method = models.CharField(max_length=50, blank=True, null=True)
    hauling_responsibility = models.CharField(max_length=50, blank=True, null=True)
    testing_responsibility = models.CharField(max_length=50, blank=True, null=True)
    image = models.ForeignKey(ImageFile, null=True, blank=True, on_delete=models.SET_NULL)
    document = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)
    comments = models.TextField(blank=True, null=True)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Assessment and Sampling &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class WasteAssessment(ObjectBase):
    date_of_assessment = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(AssociateOfClient, null=True, blank=True, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.CASCADE)
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    waste_class = models.ForeignKey(WasteClass, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    density = models.FloatField(null=True, blank=True)
    density_unit = models.CharField(max_length=50, choices=DENSITY_UNIT_CHOICES, default=DENSITY_UNIT_CHOICES[0][0])
    management_price_per_unit_quantity = models.FloatField()
    currency = models.CharField(max_length=50, choices=CURRENCY_UNIT_CHOICES, default=CURRENCY_UNIT_CHOICES[0][0])
    state = models.CharField(max_length=50, choices=WASTE_STATE_CHOICES, default=WASTE_STATE_CHOICES[0][0])
    color = models.CharField(max_length=50, null=True, blank=True)
    odor = models.CharField(max_length=50, null=True, blank=True)
    storage_type = models.ForeignKey(WasteStorageType, on_delete=models.SET_NULL, blank=True, null=True)
    number_of_containers = models.IntegerField()
    is_site_preparation_required = models.BooleanField()
    is_pretreatment_required = models.BooleanField()
    loading_requirements = models.TextField(null=True, blank=True)
    hauling_requirements = models.TextField(null=True, blank=True)
    other_requirements = models.TextField(null=True, blank=True)
    images = models.ForeignKey(ImageFile, null=True, blank=True, on_delete=models.SET_NULL)

    related_miscellaneous_documents = models.ForeignKey(DocumentFile, null=True, blank=True,
                                                        on_delete=models.SET_NULL, )

    number_of_samples = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True, null=True)


class WasteSample(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    date_of_sampling = models.DateField()
    time_of_sampling = models.TimeField(blank=True, null=True)
    where_is_sample_taken_from = models.TextField(blank=True, null=True)
    description_of_sample_preparation = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Cost offer &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


class WasteBatchCostManHour(models.Model):
    stage = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    man_hour_needed = models.FloatField()
    unit_cost = models.FloatField()


class WasteBatchCostEquipment(models.Model):
    stage = models.CharField(max_length=50)
    required_equipment = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    equipment_hour_needed = models.FloatField()
    unit_cost = models.FloatField()


class WasteBatchCostMaterial(models.Model):
    stage = models.CharField(max_length=50)
    required_material = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    amount_of_material_needed = models.FloatField()
    amount_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    unit_cost = models.FloatField()


class WasteBatchCostEstimation(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    currency = models.CharField(max_length=50, choices=CURRENCY_UNIT_CHOICES, default=CURRENCY_UNIT_CHOICES[0][0])
    man_hours = models.ManyToManyField(WasteBatchCostManHour, blank=True)
    equipments = models.ManyToManyField(WasteBatchCostEquipment, blank=True)
    materials = models.ManyToManyField(WasteBatchCostMaterial, blank=True)
    total_cost = models.FloatField()
    comments = models.TextField(blank=True, null=True)
    waste_overhead_coefficient = models.FloatField(default=0.25)
    company_overhead_coefficient = models.FloatField(default=0.25)
    total_offer = models.FloatField()


class WasteAssociatedWithContract(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, on_delete=models.CASCADE)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    hauling_responsibility = models.CharField(max_length=50, blank=True, null=True)
    testing_responsibility = models.CharField(max_length=50, blank=True, null=True)
    management_price_per_unit_quantity = models.FloatField(blank=True, null=True)
    total_batch_management_price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=50, choices=CURRENCY_UNIT_CHOICES, default=CURRENCY_UNIT_CHOICES[0][0])


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Acceptance &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class WasteBatchAcceptanceAtOrigin(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    date_of_acceptance = models.DateField()
    is_waste_compliant_with_the_assessment_form = models.BooleanField()
    will_loading_be_performed = models.BooleanField()
    is_site_preparation_done = models.BooleanField()
    has_waste_preprocessing_been_done = models.BooleanField()
    has_waste_analysis_been_performed = models.BooleanField()
    waste_quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    number_of_containers = models.IntegerField(blank=True, null=True)

    destination = models.CharField(max_length=50, blank=True, null=True)
    distance_to_destination = models.FloatField(blank=True, null=True)
    loading_time_in_hours = models.FloatField(blank=True, null=True)
    is_on_site_compliance_acceptable = models.BooleanField()
    is_mass_compliance_acceptable = models.BooleanField()

    vehicle_info = models.ManyToManyField(VehicleInfo, blank=True)
    images = models.ManyToManyField(ImageFile, blank=True)

    comments = models.TextField(blank=True, null=True)


class WasteBatchAcceptanceAtDestination(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    date_of_acceptance = models.DateField()
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    number_of_containers = models.IntegerField(blank=True, null=True)

    vehicle_info = models.ManyToManyField(VehicleInfo, blank=True)
    is_cargo_specifications_consistent_with_the_evaluation = models.BooleanField()
    is_waste_accepted = models.BooleanField()

    images = models.ManyToManyField(ImageFile, blank=True)

    destination = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste storage &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class WasteBatchStorageEnter(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    date_entered_storage_facility = models.DateField()
    quantity_entered_storage_facility = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    storage_type = models.ForeignKey(WasteStorageType, on_delete=models.SET_NULL, blank=True, null=True)
    occupied_area_square_meters = models.FloatField(blank=True, null=True)
    location_at_facility = models.TextField()
    comments = models.TextField(blank=True, null=True)


class WasteBatchStorageExit(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    date_exited_storage_facility = models.DateField()
    quantity_exited_storage_facility = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    destination = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Treatment &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class WasteBatchTreatment(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    date_waste_entered_treatment_facility = models.DateField()
    waste_quantity_entering_treatment_facility = models.FloatField()
    waste_quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES,
                                           default=QUANTITY_UNIT_CHOICES[0][0])
    treatment_type = models.ForeignKey(WasteTreatmentMethod, null=True, blank=True, on_delete=models.SET_NULL)
    treatment_material_type = models.ForeignKey(WasteTreatmentMaterial, null=True, blank=True,
                                                on_delete=models.SET_NULL)
    treatment_material_quantity_used = models.FloatField()
    treatment_material_quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES,
                                                        default=QUANTITY_UNIT_CHOICES[0][0])
    water_quantity_used = models.FloatField(null=True, blank=True)
    water_quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES,
                                           default=QUANTITY_UNIT_CHOICES[0][0])
    is_leaching_test_required = models.BooleanField()
    leaching_test_document = models.ForeignKey(DocumentFile, on_delete=models.SET_NULL, blank=True, null=True)
    is_leaching_test_results_compliant = models.BooleanField()
    image = models.ForeignKey(ImageFile, null=True, blank=True, on_delete=models.SET_NULL)
    date_exited_treatment_facility = models.DateField(blank=True, null=True)
    destination = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Lab Analysis &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class Lab(ObjectBase):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)


class WasteBatchTCLPTestResult(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, null=True, blank=True, on_delete=models.SET_NULL)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    sampling_date = models.DateField()
    test_date = models.DateField()
    lab = models.ForeignKey(Lab, blank=True, null=True, on_delete=models.SET_NULL)
    analysis_preparation_method = models.ForeignKey(WasteAnalysisPreparationMethod, on_delete=models.SET_NULL,
                                                    blank=True, null=True)
    analysis_result = models.ManyToManyField(LabAnalysisResult)
    test_document = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)
    comments = models.TextField(blank=True, null=True)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Waste Landfill &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class WasteBatchLandfilling(ObjectBase):
    related_waste_batch = models.ForeignKey(WasteBatch, on_delete=models.SET_NULL, null=True, blank=True)
    related_waste_SUB_batch = models.ForeignKey(WasteSubBatch, null=True, blank=True, on_delete=models.SET_NULL)
    date_waste_entered_landfill = models.DateField()
    quantity_entering_landfill = models.FloatField()
    quantity_unit = models.CharField(max_length=50, choices=QUANTITY_UNIT_CHOICES, default=QUANTITY_UNIT_CHOICES[0][0])
    landfilled_location = models.TextField()
    landfilled_elevation_in_m = models.FloatField(blank=True, null=True)
    machinery_type = models.CharField(max_length=50, blank=True, null=True)
    machinery_engagement_in_hr = models.FloatField(blank=True, null=True)
    personnel_engagement_in_hr = models.FloatField(blank=True, null=True)
    date_landfilling_completed = models.DateField(blank=True, null=True)
    disposal_certificate = models.ForeignKey(DocumentFile, null=True, blank=True, on_delete=models.SET_NULL)


class LandfillDailyReport(ObjectBase):
    date_assessed = models.DateField()
    is_banned_waste_control_present = models.BooleanField()
    banned_waste_control_comment = models.TextField(blank=True, null=True)
    daily_cell_area_in_m2 = models.FloatField()
    is_daily_cover_present = models.BooleanField()
    daily_cover_type = models.CharField(max_length=50)
    daily_cover_amount_in_cm = models.FloatField()
    is_daily_cover_suitable = models.BooleanField()
    do_drivers_observe_safe_distance = models.BooleanField()
    is_waste_compaction_being_carried_out = models.BooleanField()
    is_slope_and_drainage_of_working_face_suitable = models.BooleanField()
    do_landfill_personnel_use_protective_equipment = models.BooleanField()


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Customer Evaluation &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
SATISFACTION_LEVEL_CHOICES = (
    ("low", "low"),
    ("medium", "medium"),
    ("high", "high"),
)


class CustomerOfClientEvaluation(models.Model):
    id_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    CustomerOfClient = models.ForeignKey(AssociateOfClient, on_delete=models.CASCADE)
    satisfaction_level = models.CharField(max_length=50, choices=SATISFACTION_LEVEL_CHOICES,
                                          default=SATISFACTION_LEVEL_CHOICES[0][0])
    comment = models.TextField(blank=True, null=True)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& HSE &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class HSEAccidentType(models.Model):
    ref = models.CharField(primary_key=True, max_length=50)
    name = models.JSONField(default=json_default)
    description = models.JSONField(default=json_default, blank=True, null=True)

    def __str__(self):
        return self.ref


HSEAccident_SEVERITY_CHOICES = (
    ("low", "low"),
    ("medium", "medium"),
    ("high", "high"),
)


class HSEAccidentReport(ObjectBase):
    date = models.DateField()
    type = models.ForeignKey(HSEAccidentType, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=50)
    description = models.TextField()
    severity = models.CharField(max_length=50, choices=HSEAccident_SEVERITY_CHOICES,
                                default=HSEAccident_SEVERITY_CHOICES[0][0])
    employees_involved = models.TextField(blank=True, null=True)
