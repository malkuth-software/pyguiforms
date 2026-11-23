# Generated from gui_forms manifests/abi/gf_abi.json by `python3 tools/abi_python.py python`.
# Do not edit. The 1:1 layer: names, layouts and slot types exactly as the C header has them.

import ctypes

ABI_MAJOR = 1
ABI_MINOR = 6

# Scalar typedefs.
gf_status = ctypes.c_int32
gf_table_id = ctypes.c_uint32
gf_object = ctypes.c_uint64
gf_splashscreen = ctypes.c_uint64
gf_object_state = ctypes.c_uint32
gf_value_kind = ctypes.c_uint32
gf_font_role = ctypes.c_uint32
gf_event_field_flags = ctypes.c_uint32
gf_subscription = ctypes.c_uint64
gf_create_flags = ctypes.c_uint32
gf_run_flags = ctypes.c_uint32
gf_owned_window_flags = ctypes.c_uint32
gf_dialog_result_code = ctypes.c_uint32
gf_window_property_flags = ctypes.c_uint32
gf_window_band_full_screen = ctypes.c_uint32
gf_window_band_flags = ctypes.c_uint32
gf_window_band_state = ctypes.c_uint32
gf_window_band_role = ctypes.c_uint32
gf_window_band_appearance_flags = ctypes.c_uint32
gf_window_band_texture = ctypes.c_uint32
gf_window_band_status = ctypes.c_uint32
gf_window_corner_preference = ctypes.c_uint32
gf_window_shaping_flags = ctypes.c_uint32
gf_mdi_layout = ctypes.c_uint32
gf_schema_kind = ctypes.c_uint32
gf_schema_vocabulary = ctypes.c_uint32
gf_schema_property_flags = ctypes.c_uint32
gf_schema_serialization = ctypes.c_uint32
gf_schema_parameter_kind = ctypes.c_uint32
gf_schema_primitive_list = ctypes.c_uint32
gf_schema_effect_time_model = ctypes.c_uint32
gf_schema_effect_input = ctypes.c_uint32
gf_schema_effect_flags = ctypes.c_uint32
gf_theme_outcome = ctypes.c_uint32
gf_user_theme_policy = ctypes.c_uint32
gf_theme_request_outcome = ctypes.c_uint32
gf_theme_severity = ctypes.c_uint32
gf_theme_diagnostic_text = ctypes.c_uint32
gf_host_capability = ctypes.c_uint64
gf_window_corner_shape = ctypes.c_uint32
gf_transient_surface_kind = ctypes.c_uint32
gf_pointer_cursor = ctypes.c_uint32
gf_dialog_kind = ctypes.c_uint32
gf_message_buttons = ctypes.c_uint32
gf_message_icon = ctypes.c_uint32
gf_dialog_choice = ctypes.c_uint32
gf_dialog_flags = ctypes.c_uint32
gf_dialog_outcome = ctypes.c_uint32
gf_shadow_frame_kind = ctypes.c_uint32
gf_shadow_frame_flags = ctypes.c_uint32
gf_failure_detail_flags = ctypes.c_uint32
gf_scroll_orientation = ctypes.c_uint32
gf_relative_pointer_mode = ctypes.c_uint32
gf_relative_pointer_result = ctypes.c_uint32
gf_relative_pointer_end = ctypes.c_uint32
gf_effect_mask_mode = ctypes.c_uint32
gf_effect_mask_composite = ctypes.c_uint32
gf_text_ink_role = ctypes.c_uint32
gf_text_underline = ctypes.c_uint32
gf_text_decoration_fields = ctypes.c_uint32
gf_anchored_overlay_flags = ctypes.c_uint32
gf_tool_tips_setting = ctypes.c_uint32
gf_custom_base = ctypes.c_uint32
gf_custom_control_flags = ctypes.c_uint32
gf_custom_property_flags = ctypes.c_uint32
gf_source_update_mode = ctypes.c_uint32
gf_control_update_mode = ctypes.c_uint32
gf_binding_sort_direction = ctypes.c_uint32
gf_binding_predicate_operator = ctypes.c_uint32
gf_binding_notification_kind = ctypes.c_uint32
gf_binding_provider_flags = ctypes.c_uint32
gf_subsurface_state = ctypes.c_uint32
gf_theme_base = ctypes.c_uint32
gf_presentation_source = ctypes.c_uint32
gf_application_state = ctypes.c_uint32
gf_rule_trigger_kind = ctypes.c_uint32
gf_rule_condition_kind = ctypes.c_uint32
gf_rule_action_kind = ctypes.c_uint32
gf_rule_flags = ctypes.c_uint32
gf_rule_state = ctypes.c_uint32
gf_rule_token = ctypes.c_uint64
gf_data_grid_column_kind = ctypes.c_uint32
gf_dock_panel_kind = ctypes.c_uint32
gf_dock_placement = ctypes.c_uint32
gf_dock_side = ctypes.c_uint32
gf_dock_node_kind = ctypes.c_uint32
gf_dock_allowed = ctypes.c_uint32
gf_dock_option_flags = ctypes.c_uint32
gf_dock_window_visibility = ctypes.c_uint32
gf_dock_edit_kind = ctypes.c_uint32
gf_dock_document_presentation = ctypes.c_uint32
gf_dock_frame_state = ctypes.c_uint32
gf_dock_frame_arrangement = ctypes.c_uint32
gf_dock_refusal = ctypes.c_uint32
gf_help_navigator = ctypes.c_uint32
gf_locale_field = ctypes.c_uint32
gf_locale_origin = ctypes.c_uint32
gf_content_sink = ctypes.c_uint64
gf_content_status = ctypes.c_uint32
gf_content_publish_result = ctypes.c_uint32
gf_content_semantics_result = ctypes.c_uint32
gf_content_layout_result = ctypes.c_uint32
gf_content_pixel_format = ctypes.c_uint32
gf_hosted_support = ctypes.c_uint32
gf_list_view_alignment = ctypes.c_uint32
gf_list_view_sort_order = ctypes.c_uint32
gf_paint_endpoint = ctypes.c_uint64
gf_paint_write_lease = ctypes.c_uint64
gf_class_id = ctypes.c_uint32

# Constants.
GF_ABI_MAJOR = 1
GF_ABI_MINOR = 6
GF_STATUS_OK = 0
GF_STATUS_INVALID_ARGUMENT = 1
GF_STATUS_STALE_HANDLE = 2
GF_STATUS_WRONG_HANDLE_KIND = 3
GF_STATUS_WRONG_THREAD = 4
GF_STATUS_DISPOSED = 5
GF_STATUS_BUFFER_TOO_SMALL = 6
GF_STATUS_UNSUPPORTED_VERSION = 7
GF_STATUS_INTERNAL = 8
GF_STATUS_OUT_OF_MEMORY = 9
GF_STATUS_UNSUPPORTED_CAPABILITY = 10
GF_STATUS_NOT_FOUND = 11
GF_STATUS_INVALID_STATE = 12
GF_STATUS_LIMIT_EXCEEDED = 13
GF_STATUS_CANCELLED = 14
GF_STATUS_REMOVED = 15
GF_STATUS_NATIVE_EXCEPTION = 16
GF_TABLE_RUNTIME = 1
GF_TABLE_OBJECTS = 2
GF_TABLE_PROPERTIES = 3
GF_TABLE_EVENTS = 4
GF_TABLE_DISPATCH = 5
GF_TABLE_WINDOWS = 6
GF_TABLE_SCHEMA = 7
GF_TABLE_THEMES = 8
GF_TABLE_HOST = 9
GF_TABLE_DIAGNOSTICS = 10
GF_TABLE_CONTROLS = 11
GF_TABLE_TEXT_EDITING = 12
GF_TABLE_OVERLAYS = 13
GF_TABLE_PROPERTY_GRID = 14
GF_TABLE_CUSTOM_CONTROLS = 15
GF_TABLE_BINDINGS = 16
GF_TABLE_SUBSURFACES = 17
GF_TABLE_APPLICATION = 18
GF_TABLE_RULES = 19
GF_TABLE_DATA_GRID = 20
GF_TABLE_DOCKING = 21
GF_TABLE_FONTS = 22
GF_TABLE_HELP = 23
GF_TABLE_CLASSES = 24
GF_TABLE_CONTENT = 25
GF_TABLE_LIST_VIEW = 26
GF_TABLE_WINDOWS_PAINT_ENDPOINT = 256
GF_ABI_ENTRY_SLOT = 4294967295
GF_SPLASHSCREEN_MAXIMUM_STATUS_BYTES = 512
GF_SPLASHSCREEN_MINIMUM_EXTENT = 160
GF_SPLASHSCREEN_MAXIMUM_EXTENT = 1600
GF_OBJECT_STATE_ALIVE = 0
GF_OBJECT_STATE_DISPOSING = 1
GF_OBJECT_STATE_DISPOSED = 2
GF_VALUE_KIND_NULL = 0
GF_VALUE_KIND_BOOLEAN = 1
GF_VALUE_KIND_SIGNED = 2
GF_VALUE_KIND_UNSIGNED = 3
GF_VALUE_KIND_NUMBER = 4
GF_VALUE_KIND_TEXT = 5
GF_VALUE_KIND_POINT = 6
GF_VALUE_KIND_SIZE = 7
GF_VALUE_KIND_RECTANGLE = 8
GF_VALUE_KIND_INSETS = 9
GF_VALUE_KIND_COLOR = 10
GF_VALUE_KIND_FONT = 11
GF_VALUE_KIND_IMAGE = 12
GF_VALUE_KIND_ENUMERATION = 13
GF_VALUE_KIND_OBJECT = 14
GF_VALUE_KIND_COLLECTION = 15
GF_FONT_ROLE_CONTROL = 0
GF_FONT_ROLE_CONTENT = 1
GF_FONT_ROLE_MONOSPACE = 2
GF_EVENT_FIELD_WRITABLE = 1
GF_EVENT_FIELD_OPTIONAL = 2
GF_EVENT_FIELD_ANY_KIND = 4
GF_CREATE_FLAGS_COMBINABLE = 1
GF_CREATE_MAXIMUM_CHOICES = 256
GF_CREATE_MAXIMUM_NAME_BYTES = 256
GF_PROPERTY_MAXIMUM_ELEMENTS_PER_CALL = 65536
GF_RUN_FLAGS_NONE = 0
GF_OWNED_WINDOW_FLAGS_NONE = 0
GF_OWNED_WINDOW_TOOL = 1
GF_DIALOG_RESULT_NONE = 0
GF_DIALOG_RESULT_OK = 1
GF_DIALOG_RESULT_CANCEL = 2
GF_DIALOG_RESULT_ABORT = 3
GF_DIALOG_RESULT_RETRY = 4
GF_DIALOG_RESULT_IGNORE = 5
GF_DIALOG_RESULT_YES = 6
GF_DIALOG_RESULT_NO = 7
GF_DIALOG_RESULT_TRY_AGAIN = 10
GF_DIALOG_RESULT_CONTINUE = 11
GF_WINDOW_PROPERTY_TEXT = 1
GF_WINDOW_PROPERTY_ICON = 2
GF_WINDOW_PROPERTY_FORM_BORDER_STYLE = 4
GF_WINDOW_PROPERTY_MINIMIZE_BOX = 8
GF_WINDOW_PROPERTY_MAXIMIZE_BOX = 16
GF_WINDOW_PROPERTY_CONTROL_BOX = 32
GF_WINDOW_PROPERTY_WINDOW_STATE = 64
GF_WINDOW_PROPERTY_TOP_MOST = 128
GF_WINDOW_PROPERTY_OPACITY = 256
GF_WINDOW_PROPERTY_START_POSITION = 512
GF_WINDOW_PROPERTY_SHOW_IN_TASKBAR = 1024
GF_WINDOW_PROPERTY_MINIMUM_SIZE = 2048
GF_WINDOW_BAND_FULL_SCREEN_STAYS = 0
GF_WINDOW_BAND_FULL_SCREEN_HIDES = 1
GF_WINDOW_BAND_PER_EDGE = 1
GF_WINDOW_BAND_STATE_REST = 0
GF_WINDOW_BAND_STATE_LIT = 1
GF_WINDOW_BAND_STATE_FLASHING = 2
GF_WINDOW_BAND_STATE_CYCLING = 3
GF_WINDOW_BAND_ROLE_THEME = 0
GF_WINDOW_BAND_ROLE_FOCUS = 1
GF_WINDOW_BAND_ROLE_ACCENT = 2
GF_WINDOW_BAND_ROLE_ACCENT_LIGHT = 3
GF_WINDOW_BAND_ROLE_TEXT = 4
GF_WINDOW_BAND_ROLE_BORDER = 5
GF_WINDOW_BAND_REST_COLOUR = 1
GF_WINDOW_BAND_LIT_COLOUR = 2
GF_WINDOW_BAND_TEXTURE_NONE = 0
GF_WINDOW_BAND_TEXTURE_PROCEDURAL = 1
GF_WINDOW_BAND_TEXTURE_FINISH = 2
GF_PROCEDURAL_PATTERN_FELT = 0
GF_PROCEDURAL_PATTERN_WOOD_GRAIN = 1
GF_PROCEDURAL_PATTERN_PAPER_FIBRE = 2
GF_PROCEDURAL_PATTERN_PINSTRIPE = 3
GF_PROCEDURAL_PATTERN_BRUSHED_METAL = 4
GF_PROCEDURAL_PATTERN_FRESCO = 5
GF_PROCEDURAL_PATTERN_CHECKER = 6
GF_PROCEDURAL_PATTERN_HATCH = 7
GF_PROCEDURAL_PATTERN_CARBON_FIBRE = 8
GF_HATCH_STYLE_HORIZONTAL = 0
GF_HATCH_STYLE_VERTICAL = 1
GF_HATCH_STYLE_FORWARD_DIAGONAL = 2
GF_HATCH_STYLE_BACKWARD_DIAGONAL = 3
GF_HATCH_STYLE_CROSS = 4
GF_HATCH_STYLE_DIAGONAL_CROSS = 5
GF_FINISH_DUSTY_MATTE = 0
GF_FINISH_ORANGE_PEEL = 1
GF_FINISH_HAMMERTONE = 2
GF_FINISH_WRINKLE = 3
GF_FINISH_BEAD_BLAST = 4
GF_FINISH_SAND_CAST = 5
GF_FINISH_FLAT = 6
GF_FINISH_CLOTH_WEAVE = 7
GF_WINDOW_BAND_DECLARED = 1
GF_WINDOW_BAND_RESERVED = 2
GF_WINDOW_BAND_FLASHING = 4
GF_WINDOW_BAND_CYCLING = 8
GF_WINDOW_BAND_TEXTURED = 16
GF_WINDOW_CORNER_PREFERENCE_SYSTEM = 0
GF_WINDOW_CORNER_PREFERENCE_SQUARE = 1
GF_WINDOW_CORNER_PREFERENCE_ROUND = 2
GF_WINDOW_SHAPING_HOST_ATTACHED = 1
GF_WINDOW_SHAPING_CORNERS_REPORTED = 2
GF_WINDOW_SHAPING_STATE_REPORTED = 4
GF_WINDOW_SHAPING_NATIVE_BORDER = 8
GF_WINDOW_SHAPING_FULL_SCREEN = 16
GF_WINDOW_SHAPING_COMPLIED = 32
GF_MDI_LAYOUT_CASCADE = 0
GF_MDI_LAYOUT_TILE_HORIZONTAL = 1
GF_MDI_LAYOUT_TILE_VERTICAL = 2
GF_MDI_LAYOUT_ARRANGE_ICONS = 3
GF_SCHEMA_KIND_CONTROL = 0
GF_SCHEMA_KIND_COMPONENT = 1
GF_SCHEMA_KIND_SERVICE = 2
GF_SCHEMA_KIND_DEFINED_CONTROL = 3
GF_SCHEMA_VOCABULARY_PART_ROLES = 0
GF_SCHEMA_VOCABULARY_STATES = 1
GF_SCHEMA_VOCABULARY_CUSTOM_STATES = 2
GF_SCHEMA_VOCABULARY_MARKS = 3
GF_SCHEMA_VOCABULARY_ENGINE_INPUTS = 4
GF_SCHEMA_VOCABULARY_VALUES = 5
GF_SCHEMA_VOCABULARY_FAMILIES = 6
GF_SCHEMA_VOCABULARY_SEMANTIC_ROLES = 7
GF_SCHEMA_VOCABULARY_SEMANTIC_ACTIONS = 8
GF_SCHEMA_VOCABULARY_SEMANTIC_STATES = 9
GF_SCHEMA_VOCABULARY_SEMANTIC_FIELDS = 10
GF_SCHEMA_VOCABULARY_CASCADE_LEVELS = 11
GF_SCHEMA_VOCABULARY_EXPRESSION_OPERATIONS = 12
GF_SCHEMA_VOCABULARY_ENGINE_PROPERTIES = 13
GF_SCHEMA_NONE = 18446744073709551615
GF_SCHEMA_PROPERTY_FLAGS_READABLE = 1
GF_SCHEMA_PROPERTY_FLAGS_WRITABLE = 2
GF_SCHEMA_PROPERTY_FLAGS_BINDABLE = 4
GF_SCHEMA_PROPERTY_FLAGS_NULLABLE = 8
GF_SCHEMA_SERIALIZATION_HIDDEN = 0
GF_SCHEMA_SERIALIZATION_VISIBLE = 1
GF_SCHEMA_SERIALIZATION_CONTENT = 2
GF_SCHEMA_PARAMETER_KIND_NUMBER = 0
GF_SCHEMA_PARAMETER_KIND_CHOICE = 1
GF_SCHEMA_PARAMETER_KIND_COLOR = 2
GF_SCHEMA_PRIMITIVE_LIST_ROLES = 0
GF_SCHEMA_PRIMITIVE_LIST_STATES_READ = 1
GF_SCHEMA_PRIMITIVE_LIST_INPUTS_READ = 2
GF_SCHEMA_EFFECT_TIME_MODEL_STATIC_POSE = 0
GF_SCHEMA_EFFECT_TIME_MODEL_TRANSITION = 1
GF_SCHEMA_EFFECT_TIME_MODEL_AMBIENT = 2
GF_SCHEMA_EFFECT_INPUT_NONE = 0
GF_SCHEMA_EFFECT_INPUT_POINTER = 1
GF_SCHEMA_EFFECT_INPUT_POINTER_AND_KEYS = 2
GF_SCHEMA_EFFECT_FLAGS_VERIFIED = 1
GF_SCHEMA_EFFECT_FLAGS_SETUP_ON_GEOMETRY = 2
GF_THEME_PACKAGE_MAXIMUM_FILES = 256
GF_THEME_PACKAGE_MAXIMUM_BYTES = 16777216
GF_THEME_MAXIMUM_PUBLISHED_VALUES = 256
GF_THEME_OUTCOME_APPLIED = 0
GF_THEME_OUTCOME_REFUSED = 1
GF_USER_THEME_POLICY_LAYERED = 0
GF_USER_THEME_POLICY_REPLACES_PROGRAM_SHEET = 1
GF_USER_THEME_POLICY_REFUSED = 2
GF_THEME_REQUEST_NONE = 0
GF_THEME_REQUEST_PENDING = 1
GF_THEME_REQUEST_BUILT_IN = 2
GF_THEME_REQUEST_APPLIED = 3
GF_THEME_REQUEST_IGNORED_BY_POLICY = 4
GF_THEME_REQUEST_UNKNOWN_NAME = 5
GF_THEME_REQUEST_REFUSED = 6
GF_THEME_REQUEST_UNREADABLE = 7
GF_THEME_REQUEST_MALFORMED = 8
GF_THEME_SEVERITY_ERROR = 0
GF_THEME_SEVERITY_WARNING = 1
GF_THEME_DIAGNOSTIC_TEXT_CODE = 0
GF_THEME_DIAGNOSTIC_TEXT_NAME = 1
GF_THEME_DIAGNOSTIC_TEXT_FILE = 2
GF_THEME_DIAGNOSTIC_TEXT_RULE = 3
GF_THEME_DIAGNOSTIC_TEXT_PROPERTY = 4
GF_THEME_DIAGNOSTIC_TEXT_DETAIL = 5
GF_HOST_CAPABILITY_LIFECYCLE = 1
GF_HOST_CAPABILITY_SCALE_NOTIFICATIONS = 2
GF_HOST_CAPABILITY_MONITOR_GEOMETRY = 4
GF_HOST_CAPABILITY_OCCLUSION = 8
GF_HOST_CAPABILITY_SCHEDULED_WAKE = 16
GF_HOST_CAPABILITY_POINTER_INPUT = 32
GF_HOST_CAPABILITY_KEYBOARD_INPUT = 64
GF_HOST_CAPABILITY_TEXT_COMPOSITION = 128
GF_HOST_CAPABILITY_POINTER_CAPTURE = 256
GF_HOST_CAPABILITY_CURSOR = 512
GF_HOST_CAPABILITY_CLIPBOARD = 1024
GF_HOST_CAPABILITY_TYPED_DRAG_DESTINATION = 2048
GF_HOST_CAPABILITY_DIALOGS = 4096
GF_HOST_CAPABILITY_MENUS = 8192
GF_HOST_CAPABILITY_FONT_DISCOVERY = 16384
GF_HOST_CAPABILITY_ACCESSIBILITY = 32768
GF_HOST_CAPABILITY_TYPED_DRAG_SOURCE = 65536
GF_HOST_CAPABILITY_SOUND_CUES = 131072
GF_HOST_CAPABILITY_CLIPBOARD_IMAGES = 262144
GF_HOST_CAPABILITY_FRAME_CAPTURE = 524288
GF_HOST_CAPABILITY_NOTIFICATION_AREA = 1048576
GF_HOST_CAPABILITY_NOTIFICATION_AREA_MESSAGES = 2097152
GF_HOST_CAPABILITY_NOTIFICATION_AREA_MENUS = 4194304
GF_HOST_CAPABILITY_RUNTIME_WINDOWS = 8388608
GF_HOST_CAPABILITY_WINDOW_FRAMES = 16777216
GF_HOST_CAPABILITY_SCREEN_POINTER = 33554432
GF_HOST_CAPABILITY_WINDOW_AT_POINT = 67108864
GF_HOST_CAPABILITY_WINDOW_ORDERING = 134217728
GF_HOST_CAPABILITY_TRANSPARENT_WINDOWS = 268435456
GF_HOST_CAPABILITY_WINDOW_BACKDROPS = 536870912
GF_HOST_CAPABILITY_COMPOSITOR_NOTIFICATIONS = 1073741824
GF_HOST_CAPABILITY_PRESENTATION_PREFERENCES = 2147483648
GF_HOST_CAPABILITY_WINDOWS_PAINT_ENDPOINT = 4294967296
GF_HOST_CAPABILITY_TRANSIENT_SURFACES = 8589934592
GF_HOST_CAPABILITY_WINDOW_CORNERS = 17179869184
GF_HOST_CAPABILITY_WINDOW_STATE_REPORTS = 34359738368
GF_HOST_CAPABILITY_HOSTED_CONTENT = 68719476736
GF_HOST_CAPABILITY_RELATIVE_POINTER = 137438953472
GF_HOST_CAPABILITY_RAW_POINTER_MOTION = 274877906944
GF_HOST_CAPABILITY_POINTER_CONFINEMENT = 549755813888
GF_HOST_CAPABILITY_POINTER_WARP = 1099511627776
GF_HOST_CAPABILITY_OPEN_URL = 2199023255552
GF_HOST_CAPABILITY_DIRECT_BUFFERS = 8796093022208
GF_HOST_CAPABILITY_HOST_SCROLL = 17592186044416
GF_HOST_CAPABILITY_REFERENCE_PRESENTATION = 35184372088832
GF_WINDOW_CORNER_SHAPE_SQUARE = 1
GF_WINDOW_CORNER_SHAPE_ROUNDED = 2
GF_TRANSIENT_SURFACE_TOOLTIP = 1
GF_TRANSIENT_SURFACE_SPLASHSCREEN = 2
GF_TRANSIENT_SURFACE_POPUP = 4
GF_TRANSIENT_SURFACE_TRANSLUCENT = 8
GF_TRANSIENT_SURFACE_OPAQUE = 16
GF_POINTER_CURSOR_ARROW = 0
GF_POINTER_CURSOR_TEXT = 1
GF_POINTER_CURSOR_HAND = 2
GF_POINTER_CURSOR_CROSSHAIR = 3
GF_POINTER_CURSOR_RESIZE_HORIZONTAL = 4
GF_POINTER_CURSOR_RESIZE_VERTICAL = 5
GF_POINTER_CURSOR_WAIT = 6
GF_POINTER_CURSOR_FORBIDDEN = 7
GF_POINTER_CURSOR_RESIZE_DIAGONAL_DOWN = 8
GF_POINTER_CURSOR_RESIZE_DIAGONAL_UP = 9
GF_POINTER_CURSOR_HELP = 10
GF_DIALOG_KIND_MESSAGE = 0
GF_DIALOG_KIND_OPEN_FILE = 1
GF_DIALOG_KIND_SAVE_FILE = 2
GF_DIALOG_KIND_FOLDER = 3
GF_DIALOG_KIND_COLOR = 4
GF_MESSAGE_BUTTONS_OK = 0
GF_MESSAGE_BUTTONS_OK_CANCEL = 1
GF_MESSAGE_BUTTONS_YES_NO = 2
GF_MESSAGE_BUTTONS_YES_NO_CANCEL = 3
GF_MESSAGE_BUTTONS_RETRY_CANCEL = 4
GF_MESSAGE_ICON_NONE = 0
GF_MESSAGE_ICON_INFORMATION = 1
GF_MESSAGE_ICON_WARNING = 2
GF_MESSAGE_ICON_ERROR = 3
GF_MESSAGE_ICON_QUESTION = 4
GF_DIALOG_CHOICE_NONE = 0
GF_DIALOG_CHOICE_OK = 1
GF_DIALOG_CHOICE_CANCEL = 2
GF_DIALOG_CHOICE_YES = 3
GF_DIALOG_CHOICE_NO = 4
GF_DIALOG_CHOICE_RETRY = 5
GF_DIALOG_FLAGS_NONE = 0
GF_DIALOG_FLAGS_ALLOW_MULTIPLE = 1
GF_DIALOG_FLAGS_CONFIRM_OVERWRITE = 2
GF_DIALOG_FLAGS_ALLOW_ALPHA = 4
GF_DIALOG_FLAGS_ALLOW_MISSING_FILE = 8
GF_DIALOG_FLAGS_REQUIRE_EXISTING_FILE = 16
GF_DIALOG_FLAGS_ALLOW_MISSING_FOLDER = 32
GF_DIALOG_FLAGS_CREATE_PROMPT = 64
GF_DIALOG_OUTCOME_ACCEPTED = 0
GF_DIALOG_OUTCOME_CANCELLED = 1
GF_DIALOG_NO_FILTER = 18446744073709551615
GF_SHADOW_FRAME_KIND_LIBRARY_CALL = 1
GF_SHADOW_FRAME_KIND_INPUT_DISPATCH = 2
GF_SHADOW_FRAME_KIND_EVENT_CALLBACK = 3
GF_SHADOW_FRAME_KIND_LAYOUT_PASS = 4
GF_SHADOW_FRAME_KIND_PAINT_PASS = 5
GF_SHADOW_FRAME_KIND_POSTED_CALLBACK = 6
GF_SHADOW_FRAME_KIND_GATE = 7
GF_SHADOW_FRAME_SUBJECT_TRUNCATED = 1
GF_SHADOW_FRAME_NAME_TRUNCATED = 2
GF_SHADOW_FRAME_SUBJECT_CAPACITY = 48
GF_SHADOW_FRAME_NAME_CAPACITY = 32
GF_SHADOW_STACK_CAPACITY = 64
GF_FAILURE_SITE_CAPACITY = 64
GF_FAILURE_MESSAGE_CAPACITY = 512
GF_FAILURE_TYPE_CAPACITY = 256
GF_FAILURE_TRACE_CAPACITY = 32
GF_FAILURE_DETAIL_FLAGS_NONE = 0
GF_FAILURE_DETAIL_FLAGS_FRAMES_LOST_AT_PARK = 1
GF_SCROLL_ORIENTATION_HORIZONTAL = 0
GF_SCROLL_ORIENTATION_VERTICAL = 1
GF_RELATIVE_POINTER_MODE_FREE = 0
GF_RELATIVE_POINTER_MODE_CONFINED = 1
GF_RELATIVE_POINTER_MODE_LOCKED = 2
GF_RELATIVE_POINTER_RESULT_GRANTED = 0
GF_RELATIVE_POINTER_RESULT_DEGRADED = 1
GF_RELATIVE_POINTER_RESULT_DETACHED = 2
GF_RELATIVE_POINTER_RESULT_NOT_ACTIVE = 3
GF_RELATIVE_POINTER_RESULT_NO_PRESS = 4
GF_RELATIVE_POINTER_RESULT_INVALID_REQUEST = 5
GF_RELATIVE_POINTER_END_RELEASED = 0
GF_RELATIVE_POINTER_END_ESCAPE = 1
GF_RELATIVE_POINTER_END_FOCUS_LOST = 2
GF_RELATIVE_POINTER_END_DEACTIVATED = 3
GF_RELATIVE_POINTER_END_MODAL = 4
GF_RELATIVE_POINTER_END_DETACHED = 5
GF_RELATIVE_POINTER_END_PRESS_RELEASED = 6
GF_RELATIVE_POINTER_END_SUPERSEDED = 7
GF_EFFECT_MASK_MODE_ALPHA = 0
GF_EFFECT_MASK_MODE_LUMINANCE = 1
GF_EFFECT_MASK_MODE_INVERSE_ALPHA = 2
GF_EFFECT_MASK_MODE_INVERSE_LUMINANCE = 3
GF_EFFECT_MASK_COMPOSITE_ADD = 0
GF_EFFECT_MASK_COMPOSITE_SUBTRACT = 1
GF_EFFECT_MASK_COMPOSITE_INTERSECT = 2
GF_EFFECT_MASK_COMPOSITE_EXCLUDE = 3
GF_CONTENT_EFFECT_MAXIMUM_MASKS = 4
GF_CONTENT_EFFECT_MAXIMUM_BLUR = 16
GF_TEXT_INK_ROLE_TEXT = 0
GF_TEXT_INK_ROLE_MUTED = 1
GF_TEXT_INK_ROLE_LINK = 2
GF_TEXT_INK_ROLE_VISITED_LINK = 3
GF_TEXT_INK_ROLE_NOTICE = 4
GF_TEXT_UNDERLINE_NONE = 0
GF_TEXT_UNDERLINE_SINGLE = 1
GF_TEXT_UNDERLINE_SQUIGGLE = 2
GF_TEXT_DECORATION_INK = 1
GF_TEXT_DECORATION_FOREGROUND = 2
GF_TEXT_DECORATION_WEIGHT = 4
GF_TEXT_DECORATION_ITALIC = 8
GF_TEXT_DECORATION_UNDERLINE = 16
GF_TEXT_DECORATION_UNDERLINE_COLOR = 32
GF_TEXT_DECORATION_BACKGROUND = 64
GF_ANCHORED_OVERLAY_FLAGS_NONE = 0
GF_ANCHORED_OVERLAY_ABOVE = 1
GF_ANCHORED_OVERLAY_ALIGN_END = 2
GF_ANCHORED_OVERLAY_NO_FLIP = 4
GF_ANCHORED_OVERLAY_KEEP_ON_CLICK_AWAY = 8
GF_ANCHORED_OVERLAY_KEEP_ON_ESCAPE = 16
GF_ANCHORED_OVERLAY_TAKE_FOCUS = 32
GF_TOOL_TIPS_FOLLOW = 0
GF_TOOL_TIPS_SHOWN = 1
GF_TOOL_TIPS_HIDDEN = 2
GF_CUSTOM_BASE_SCROLLABLE_CONTROL = 0
GF_CUSTOM_BASE_USER_CONTROL = 1
GF_CUSTOM_CONTROL_FOCUSABLE = 1
GF_CUSTOM_PROPERTY_READ_ONLY = 1
GF_CUSTOM_PROPERTY_COMBINABLE = 2
GF_CUSTOM_PROPERTY_CHANGE_NOTIFICATIONS = 4
GF_CUSTOM_MAXIMUM_PROPERTIES = 256
GF_COMPOSITE_MAXIMUM_CHILD_TYPES = 64
GF_SOURCE_UPDATE_ON_VALIDATION = 0
GF_SOURCE_UPDATE_ON_PROPERTY_CHANGED = 1
GF_SOURCE_UPDATE_NEVER = 2
GF_CONTROL_UPDATE_ON_PROPERTY_CHANGED = 0
GF_CONTROL_UPDATE_NEVER = 1
GF_BINDING_MAXIMUM_FIELDS = 1024
GF_BINDING_MAXIMUM_RECORDS_PER_CALL = 65536
GF_BINDING_HIDDEN_POSITION = 18446744073709551615
GF_BINDING_WHOLE_ROW = 18446744073709551615
GF_BINDING_SORT_ASCENDING = 0
GF_BINDING_SORT_DESCENDING = 1
GF_BINDING_PREDICATE_EQUAL = 0
GF_BINDING_PREDICATE_NOT_EQUAL = 1
GF_BINDING_PREDICATE_LESS = 2
GF_BINDING_PREDICATE_LESS_OR_EQUAL = 3
GF_BINDING_PREDICATE_GREATER = 4
GF_BINDING_PREDICATE_GREATER_OR_EQUAL = 5
GF_BINDING_PREDICATE_CONTAINS = 6
GF_BINDING_PREDICATE_STARTS_WITH = 7
GF_BINDING_PREDICATE_IS_NULL = 8
GF_BINDING_PREDICATE_IS_NOT_NULL = 9
GF_BINDING_NOTIFY_RESET = 0
GF_BINDING_NOTIFY_INSERTED = 1
GF_BINDING_NOTIFY_REMOVED = 2
GF_BINDING_NOTIFY_MOVED = 3
GF_BINDING_NOTIFY_CHANGED = 4
GF_BINDING_PROVIDER_SORTS = 1
GF_BINDING_PROVIDER_FILTERS = 2
GF_BINDING_PROVIDER_INSERTS = 4
GF_BINDING_PROVIDER_REMOVES = 8
GF_SUBSURFACE_STATE_STOPPED = 0
GF_SUBSURFACE_STATE_STARTING = 1
GF_SUBSURFACE_STATE_RUNNING = 2
GF_SUBSURFACE_STATE_FAILED = 3
GF_THEME_BASE_DEFAULT = 0
GF_THEME_BASE_WINDOWS_PROFESSIONAL = 1
GF_THEME_BASE_GUI_FORMS = 2
GF_PRESENTATION_SOURCE_HOST = 0
GF_PRESENTATION_SOURCE_DEFAULTS = 1
GF_APPLICATION_MAXIMUM_THEME_PACKAGES = 16
GF_APPLICATION_STATE_NONE = 0
GF_APPLICATION_STATE_CURRENT = 1
GF_RULE_TRIGGER_KEY_PRESSED = 1
GF_RULE_TRIGGER_KEY_RELEASED = 2
GF_RULE_TRIGGER_KEY_REPEAT = 3
GF_RULE_TRIGGER_MOUSE_DOWN = 4
GF_RULE_TRIGGER_MOUSE_UP = 5
GF_RULE_TRIGGER_CLICK = 6
GF_RULE_TRIGGER_MOUSE_CLICK = 7
GF_RULE_TRIGGER_DOUBLE_CLICK = 8
GF_RULE_TRIGGER_MOUSE_DOUBLE_CLICK = 9
GF_RULE_TRIGGER_CONTEXT_MENU_REQUESTED = 10
GF_RULE_TRIGGER_MOUSE_ENTER = 11
GF_RULE_TRIGGER_MOUSE_HOVER = 12
GF_RULE_TRIGGER_MOUSE_LEAVE = 13
GF_RULE_TRIGGER_MOUSE_CAPTURE_CHANGED = 14
GF_RULE_TRIGGER_FOCUS_GAINED = 15
GF_RULE_TRIGGER_FOCUS_LOST = 16
GF_RULE_TRIGGER_INTERACTION = 17
GF_RULE_TRIGGER_COMMAND_EXECUTED = 18
GF_RULE_CONDITION_KEY_DOWN = 1
GF_RULE_CONDITION_MODIFIERS = 2
GF_RULE_CONDITION_HOVERING = 3
GF_RULE_CONDITION_PRESSED = 4
GF_RULE_CONDITION_FOCUSED = 5
GF_RULE_CONDITION_FOCUS_WITHIN = 6
GF_RULE_CONDITION_ENABLED = 7
GF_RULE_CONDITION_VISIBLE = 8
GF_RULE_CONDITION_WINDOW_ACTIVE = 9
GF_RULE_CONDITION_DRAGGING = 12
GF_RULE_CONDITION_DROP_CANDIDATE = 13
GF_RULE_MODIFIER_SHIFT = 1
GF_RULE_MODIFIER_CONTROL = 2
GF_RULE_MODIFIER_ALT = 4
GF_RULE_MODIFIER_META = 8
GF_RULE_ACTION_CALLBACK = 1
GF_RULE_ACTION_INVOKE = 2
GF_RULE_ACTION_SET = 3
GF_RULE_ACTION_TOGGLE = 4
GF_RULE_ACTION_FOCUS = 5
GF_RULE_ACTION_BEGIN_KEYBOARD_DRAG = 6
GF_RULE_FLAGS_CONSUME = 1
GF_RULE_STATE_ARMED = 1
GF_RULE_STATE_REVOKED = 2
GF_RULE_STATE_STALE = 3
GF_DATA_GRID_COLUMN_KIND_TEXT = 0
GF_DATA_GRID_COLUMN_KIND_CHECK_BOX = 1
GF_DATA_GRID_COLUMN_KIND_COMBO_BOX = 2
GF_DATA_GRID_COLUMN_KIND_BUTTON = 3
GF_DATA_GRID_COLUMN_KIND_IMAGE = 4
GF_DATA_GRID_COLUMN_KIND_LINK = 5
GF_DATA_GRID_MAXIMUM_ROWS_PER_CALL = 65536
GF_DATA_GRID_MAXIMUM_COLUMN_ITEMS = 4096
GF_DOCK_PANEL_KIND_TOOL = 0
GF_DOCK_PANEL_KIND_DOCUMENT = 1
GF_DOCK_PLACEMENT_DOCKED = 0
GF_DOCK_PLACEMENT_FLOATING = 1
GF_DOCK_PLACEMENT_AUTO_HIDDEN = 2
GF_DOCK_PLACEMENT_HIDDEN = 3
GF_DOCK_PLACEMENT_ABSENT = 4
GF_DOCK_SIDE_LEFT = 0
GF_DOCK_SIDE_TOP = 1
GF_DOCK_SIDE_RIGHT = 2
GF_DOCK_SIDE_BOTTOM = 3
GF_DOCK_SIDE_NONE = 4
GF_DOCK_NODE_KIND_SPLIT = 0
GF_DOCK_NODE_KIND_TOOL_STACK = 1
GF_DOCK_NODE_KIND_DOCUMENT_STACK = 2
GF_DOCK_NODE_KIND_DOCUMENT_AREA = 3
GF_DOCK_NODE_KIND_NONE = 4
GF_DOCK_ALLOWED_DOCKED = 1
GF_DOCK_ALLOWED_DOCUMENT_AREA = 2
GF_DOCK_ALLOWED_FLOATING = 4
GF_DOCK_ALLOWED_AUTO_HIDDEN = 8
GF_DOCK_ALLOWED_TABBED = 16
GF_DOCK_ALLOWED_HIDDEN = 32
GF_DOCK_ALLOWED_CLOSED = 64
GF_DOCK_ALLOWED_SIDE_LEFT = 128
GF_DOCK_ALLOWED_SIDE_TOP = 256
GF_DOCK_ALLOWED_SIDE_RIGHT = 512
GF_DOCK_ALLOWED_SIDE_BOTTOM = 1024
GF_DOCK_ALLOWED_ALL = 2047
GF_DOCK_ALLOWED_CLOSE_BUTTON_HIDDEN = 2048
GF_DOCK_OPTION_FLOATS_SHOWN_WHILE_INACTIVE = 1
GF_DOCK_OPTION_DOCUMENT_TABS_HIDDEN = 2
GF_DOCK_OPTION_AUTO_HIDE_NO_HOVER = 4
GF_DOCK_OPTION_AREA_BACKGROUND = 8
GF_DOCK_OPTION_ALL = 15
GF_DOCK_WINDOW_VISIBILITY_WORKSPACE = 0
GF_DOCK_WINDOW_VISIBILITY_SHOWN = 1
GF_DOCK_WINDOW_VISIBILITY_POLICY = 2
GF_DOCK_EDIT_DOCK_INTO = 0
GF_DOCK_EDIT_DOCK_BESIDE = 1
GF_DOCK_EDIT_DOCK_AT_EDGE = 2
GF_DOCK_EDIT_FLOAT = 3
GF_DOCK_EDIT_AUTO_HIDE = 4
GF_DOCK_EDIT_UNPIN = 5
GF_DOCK_EDIT_HIDE = 6
GF_DOCK_EDIT_SHOW = 7
GF_DOCK_EDIT_CLOSE = 8
GF_DOCK_EDIT_MOVE = 9
GF_DOCK_EDIT_SELECT = 10
GF_DOCK_EDIT_SET_RATIO = 11
GF_DOCK_EDIT_SET_FLOATING_FRAME = 12
GF_DOCK_EDIT_SET_DOCUMENT_PRESENTATION = 13
GF_DOCK_EDIT_SET_FRAME_BOUNDS = 14
GF_DOCK_EDIT_SET_FRAME_STATE = 15
GF_DOCK_EDIT_SET_FRAME_ICON_SLOT = 16
GF_DOCK_DOCUMENT_PRESENTATION_TABS = 0
GF_DOCK_DOCUMENT_PRESENTATION_FRAMES = 1
GF_DOCK_FRAME_STATE_NORMAL = 0
GF_DOCK_FRAME_STATE_MINIMIZED = 1
GF_DOCK_FRAME_STATE_MAXIMIZED = 2
GF_DOCK_FRAME_ARRANGEMENT_CASCADE = 0
GF_DOCK_FRAME_ARRANGEMENT_TILE_HORIZONTAL = 1
GF_DOCK_FRAME_ARRANGEMENT_TILE_VERTICAL = 2
GF_DOCK_FRAME_ARRANGEMENT_ARRANGE_ICONS = 3
GF_DOCK_REFUSAL_NONE = 0
GF_DOCK_REFUSAL_UNKNOWN_PANEL = 1
GF_DOCK_REFUSAL_UNKNOWN_NODE = 2
GF_DOCK_REFUSAL_UNKNOWN_SITE = 3
GF_DOCK_REFUSAL_NOT_A_STACK = 4
GF_DOCK_REFUSAL_NOT_A_SPLIT = 5
GF_DOCK_REFUSAL_NOT_AUTO_HIDDEN = 6
GF_DOCK_REFUSAL_TARGET_IS_SUBJECT = 7
GF_DOCK_REFUSAL_INVALID_RATIO = 8
GF_DOCK_REFUSAL_INVALID_FRAME = 9
GF_DOCK_REFUSAL_INVALID_EXTENT = 10
GF_DOCK_REFUSAL_FLOATING_SITE_LIMIT = 11
GF_DOCK_REFUSAL_IDENTITIES_EXHAUSTED = 12
GF_DOCK_REFUSAL_NOT_ROOT_LEVEL = 13
GF_DOCK_REFUSAL_NOT_IN_MAIN_SITE = 14
GF_DOCK_REFUSAL_ALREADY_PLACED = 15
GF_DOCK_REFUSAL_NOT_PLACED = 16
GF_DOCK_REFUSAL_INVARIANT_VIOLATED = 17
GF_DOCK_REFUSAL_PLACEMENT_NOT_ALLOWED = 18
GF_DOCK_REFUSAL_TABBING_NOT_ALLOWED = 19
GF_DOCK_REFUSAL_KIND_MISMATCH = 20
GF_DOCK_REFUSAL_GROUP_NOT_ADMITTED = 21
GF_DOCK_REFUSAL_SITE_REFUSES_KIND = 22
GF_DOCK_REFUSAL_SITE_REFUSES_GROUP = 23
GF_DOCK_REFUSAL_USER_DOCKING_LOCKED = 24
GF_APP_FONT_MAXIMUM_FACES = 4
GF_APP_FONT_MAXIMUM_BYTES = 67108864
GF_HELP_NAVIGATOR_CONTENTS = 0
GF_HELP_NAVIGATOR_INDEX = 1
GF_HELP_NAVIGATOR_SEARCH = 2
GF_LOCALE_FIELD_TEXT = 0
GF_LOCALE_FIELD_TOOL_TIP = 1
GF_LOCALE_FIELD_ACCESS_KEY = 2
GF_LOCALE_FIELD_TITLE = 3
GF_LOCALE_FIELD_PLACEHOLDER = 4
GF_LOCALE_FIELD_HEADER = 5
GF_LOCALE_FIELD_ACCESSIBLE_NAME = 6
GF_LOCALE_FIELD_ACCESSIBLE_DESCRIPTION = 7
GF_LOCALE_FIELD_HELP_LINE = 8
GF_LOCALE_FIELD_HELP = 9
GF_LOCALE_FIELD_KEYWORDS = 10
GF_LOCALE_ORIGIN_NONE = 0
GF_LOCALE_ORIGIN_BUILT_IN = 1
GF_LOCALE_ORIGIN_PROGRAM = 2
GF_LOCALE_ORIGIN_TRANSLATION = 3
GF_LOCALE_ORIGIN_USER = 4
GF_CONTENT_STATUS_DISCONNECTED = 0
GF_CONTENT_STATUS_WAITING = 1
GF_CONTENT_STATUS_LIVE = 2
GF_CONTENT_STATUS_STALE = 3
GF_CONTENT_STATUS_TERMINATING = 4
GF_CONTENT_STATUS_ENDED = 5
GF_CONTENT_STATUS_ABANDONED = 6
GF_CONTENT_STATUS_FAILED = 7
GF_CONTENT_PUBLISH_PUBLISHED = 0
GF_CONTENT_PUBLISH_DROPPED_BUSY = 1
GF_CONTENT_PUBLISH_REVOKED = 2
GF_CONTENT_PUBLISH_REFUSED_EMPTY = 3
GF_CONTENT_PUBLISH_REFUSED_TOO_LARGE = 4
GF_CONTENT_PUBLISH_REFUSED_ROW_BYTES = 5
GF_CONTENT_PUBLISH_REFUSED_EXTENT = 6
GF_CONTENT_PUBLISH_REFUSED_FORMAT = 7
GF_CONTENT_PUBLISH_REFUSED_DAMAGE = 8
GF_CONTENT_PUBLISH_FAILED_ALLOCATION = 9
GF_CONTENT_SEMANTICS_PUBLISHED = 0
GF_CONTENT_SEMANTICS_REVOKED = 1
GF_CONTENT_SEMANTICS_REFUSED_INVALID_UTF8 = 2
GF_CONTENT_SEMANTICS_REFUSED_TOO_LONG = 3
GF_CONTENT_LAYOUT_ACCEPTED = 0
GF_CONTENT_LAYOUT_STALE_REVISION = 1
GF_CONTENT_LAYOUT_REFUSED_TOO_LARGE = 2
GF_CONTENT_LAYOUT_REFUSED_RANGE = 3
GF_CONTENT_LAYOUT_REFUSED_BOUNDARY = 4
GF_CONTENT_LAYOUT_REFUSED_CLUSTER = 5
GF_CONTENT_LAYOUT_REFUSED_GEOMETRY = 6
GF_CONTENT_LAYOUT_REFUSED_CARET = 7
GF_CONTENT_PIXEL_FORMAT_BGRA32_PREMULTIPLIED_SRGB = 0
GF_HOSTED_SUPPORT_AVAILABLE = 0
GF_HOSTED_SUPPORT_NOT_REPORTED = 1
GF_CONTENT_MAXIMUM_FRAME_EXTENT = 16384
GF_CONTENT_MAXIMUM_FRAME_BYTES = 268435456
GF_CONTENT_MAXIMUM_SEMANTIC_TEXT_BYTES = 1048576
GF_CONTENT_MAXIMUM_LAYOUT_ENTRIES = 1000000
GF_CONTENT_MAXIMUM_TERMINATION_GRACE_MS = 10000
GF_CONTENT_MAXIMUM_WAIT_MS = 3600000
GF_CONTENT_MAXIMUM_SINKS = 65536
GF_HOSTED_MAXIMUM_ARGUMENTS = 4096
GF_LIST_VIEW_ALIGNMENT_LEFT = 0
GF_LIST_VIEW_ALIGNMENT_CENTER = 1
GF_LIST_VIEW_ALIGNMENT_RIGHT = 2
GF_LIST_VIEW_SORT_ORDER_NONE = 0
GF_LIST_VIEW_SORT_ORDER_ASCENDING = 1
GF_LIST_VIEW_SORT_ORDER_DESCENDING = 2
GF_LIST_VIEW_MAXIMUM_COLUMNS = 64
GF_LIST_VIEW_MAXIMUM_ITEMS = 10000000
GF_LIST_VIEW_MAXIMUM_GROUPS = 4096
GF_LIST_VIEW_MAXIMUM_SUB_ITEMS = 64
GF_PAINT_ENDPOINT_MAXIMUM_SIDE = 32768
GF_CLASS_COMPONENT = 1
GF_CLASS_CONTROL = 2
GF_CLASS_BUTTON_BASE = 3
GF_CLASS_BUTTON = 4
GF_CLASS_LINK_LABEL = 5
GF_CLASS_LABEL = 6
GF_CLASS_SCROLLABLE_CONTROL = 7
GF_CLASS_PANEL = 8
GF_CLASS_PICTURE_BOX = 9
GF_CLASS_RANGE_CONTROL = 10
GF_CLASS_PROGRESS_BAR = 11
GF_CLASS_SWEEP_SCOPE = 12
GF_CLASS_LIST_CONTROL = 13
GF_CLASS_LIST_BOX = 14
GF_CLASS_CHECK_BOX = 15
GF_CLASS_RADIO_BUTTON = 16
GF_CLASS_TRACK_BAR = 17
GF_CLASS_GROUP_BOX = 18
GF_CLASS_MATERIAL_PANEL = 19
GF_CLASS_CARD = 20
GF_CLASS_CONTAINER_CONTROL = 21
GF_CLASS_USER_CONTROL = 22
GF_CLASS_PAGE_STRIP = 23
GF_CLASS_PAGE_VIEW = 24
GF_CLASS_NAVIGATION_PANE = 25
GF_CLASS_DOCK_SITE = 26
GF_CLASS_DOCK_NAVIGATOR = 27
GF_CLASS_SCALED_PANEL = 28
GF_CLASS_SCROLL_BAR = 29
GF_CLASS_TOOL_STRIP = 30
GF_CLASS_GAUGE_BASE = 31
GF_CLASS_DIAL = 32
GF_CLASS_RASTER_CANVAS = 33
GF_CLASS_TEXT_BOX_BASE = 34
GF_CLASS_UP_DOWN_BASE = 35
GF_CLASS_MASKED_TEXT_BOX = 36
GF_CLASS_COMBO_BOX = 37
GF_CLASS_DATA_GRID_VIEW = 38
GF_CLASS_NUMERIC_UP_DOWN = 39
GF_CLASS_DATE_TIME_PICKER = 40
GF_CLASS_NODE_CANVAS = 41

# Records and tables, declared first so that fields and slots may name any of them.


class gf_utf8_view(ctypes.Structure):
    """gf_utf8_view (record, 16 bytes)."""


class gf_abi_version_info(ctypes.Structure):
    """gf_abi_version_info (extensible, 24 bytes)."""


class gf_error_detail(ctypes.Structure):
    """gf_error_detail (extensible, 24 bytes)."""


class gf_splashscreen_options(ctypes.Structure):
    """gf_splashscreen_options (extensible, 48 bytes)."""


class gf_runtime_table(ctypes.Structure):
    """gf_runtime_table (table, 64 bytes)."""


class gf_logical_point(ctypes.Structure):
    """gf_logical_point (record, 16 bytes)."""


class gf_logical_size(ctypes.Structure):
    """gf_logical_size (record, 16 bytes)."""


class gf_logical_rect(ctypes.Structure):
    """gf_logical_rect (record, 32 bytes)."""


class gf_logical_insets(ctypes.Structure):
    """gf_logical_insets (record, 32 bytes)."""


class gf_font(ctypes.Structure):
    """gf_font (record, 32 bytes)."""


class gf_value(ctypes.Structure):
    """gf_value (extensible, 200 bytes)."""


class gf_event_field(ctypes.Structure):
    """gf_event_field (record, 32 bytes)."""


class gf_event(ctypes.Structure):
    """gf_event (extensible, 56 bytes)."""


class gf_callback(ctypes.Structure):
    """gf_callback (extensible, 32 bytes)."""


class gf_create_choice(ctypes.Structure):
    """gf_create_choice (record, 24 bytes)."""


class gf_create_arguments(ctypes.Structure):
    """gf_create_arguments (extensible, 56 bytes)."""


class gf_objects_table(ctypes.Structure):
    """gf_objects_table (table, 112 bytes)."""


class gf_properties_table(ctypes.Structure):
    """gf_properties_table (table, 64 bytes)."""


class gf_events_table(ctypes.Structure):
    """gf_events_table (table, 48 bytes)."""


class gf_dispatch_table(ctypes.Structure):
    """gf_dispatch_table (table, 24 bytes)."""


class gf_schema_interaction(ctypes.Structure):
    """gf_schema_interaction (extensible, 40 bytes)."""


class gf_run_options(ctypes.Structure):
    """gf_run_options (extensible, 80 bytes)."""


class gf_owned_window_options(ctypes.Structure):
    """gf_owned_window_options (extensible, 72 bytes)."""


class gf_window_band_options(ctypes.Structure):
    """gf_window_band_options (extensible, 56 bytes)."""


class gf_window_band_appearance(ctypes.Structure):
    """gf_window_band_appearance (extensible, 80 bytes)."""


class gf_window_band_report(ctypes.Structure):
    """gf_window_band_report (extensible, 72 bytes)."""


class gf_window_shaping(ctypes.Structure):
    """gf_window_shaping (extensible, 32 bytes)."""


class gf_windows_table(ctypes.Structure):
    """gf_windows_table (table, 256 bytes)."""


class gf_schema_type(ctypes.Structure):
    """gf_schema_type (extensible, 88 bytes)."""


class gf_schema_item_system(ctypes.Structure):
    """gf_schema_item_system (extensible, 48 bytes)."""


class gf_schema_part(ctypes.Structure):
    """gf_schema_part (extensible, 64 bytes)."""


class gf_schema_property(ctypes.Structure):
    """gf_schema_property (extensible, 72 bytes)."""


class gf_schema_choice(ctypes.Structure):
    """gf_schema_choice (extensible, 32 bytes)."""


class gf_schema_engine(ctypes.Structure):
    """gf_schema_engine (extensible, 96 bytes)."""


class gf_schema_primitive(ctypes.Structure):
    """gf_schema_primitive (extensible, 104 bytes)."""


class gf_schema_parameter(ctypes.Structure):
    """gf_schema_parameter (extensible, 64 bytes)."""


class gf_schema_effect(ctypes.Structure):
    """gf_schema_effect (extensible, 112 bytes)."""


class gf_schema_composite(ctypes.Structure):
    """gf_schema_composite (extensible, 128 bytes)."""


class gf_schema_table(ctypes.Structure):
    """gf_schema_table (table, 256 bytes)."""


class gf_bytes_view(ctypes.Structure):
    """gf_bytes_view (record, 16 bytes)."""


class gf_theme_file(ctypes.Structure):
    """gf_theme_file (record, 32 bytes)."""


class gf_theme_package(ctypes.Structure):
    """gf_theme_package (extensible, 40 bytes)."""


class gf_theme_report(ctypes.Structure):
    """gf_theme_report (extensible, 16 bytes)."""


class gf_theme_diagnostic(ctypes.Structure):
    """gf_theme_diagnostic (extensible, 16 bytes)."""


class gf_themes_table(ctypes.Structure):
    """gf_themes_table (table, 136 bytes)."""


class gf_host_capabilities(ctypes.Structure):
    """gf_host_capabilities (extensible, 32 bytes)."""


class gf_file_filter(ctypes.Structure):
    """gf_file_filter (record, 32 bytes)."""


class gf_dialog_request(ctypes.Structure):
    """gf_dialog_request (extensible, 144 bytes)."""


class gf_dialog_result(ctypes.Structure):
    """gf_dialog_result (extensible, 32 bytes)."""


class gf_host_table(ctypes.Structure):
    """gf_host_table (table, 64 bytes)."""


class gf_shadow_frame(ctypes.Structure):
    """gf_shadow_frame (record, 112 bytes)."""


class gf_shadow_stack_info(ctypes.Structure):
    """gf_shadow_stack_info (extensible, 24 bytes)."""


class gf_failure_snapshot(ctypes.Structure):
    """gf_failure_snapshot (extensible, 104 bytes)."""


class gf_failure_detail(ctypes.Structure):
    """gf_failure_detail (extensible, 544 bytes)."""


class gf_diagnostics_table(ctypes.Structure):
    """gf_diagnostics_table (table, 96 bytes)."""


class gf_layout_transaction(ctypes.Structure):
    """gf_layout_transaction (extensible, 32 bytes)."""


class gf_scroll_axis(ctypes.Structure):
    """gf_scroll_axis (record, 48 bytes)."""


class gf_scroll_snapshot(ctypes.Structure):
    """gf_scroll_snapshot (extensible, 248 bytes)."""


class gf_relative_pointer_request(ctypes.Structure):
    """gf_relative_pointer_request (extensible, 24 bytes)."""


class gf_relative_pointer_grant(ctypes.Structure):
    """gf_relative_pointer_grant (extensible, 24 bytes)."""


class gf_relative_pointer_state(ctypes.Structure):
    """gf_relative_pointer_state (extensible, 96 bytes)."""


class gf_effect_mask_layer(ctypes.Structure):
    """gf_effect_mask_layer (extensible, 56 bytes)."""


class gf_content_effect(ctypes.Structure):
    """gf_content_effect (extensible, 1216 bytes)."""


class gf_controls_table(ctypes.Structure):
    """gf_controls_table (table, 160 bytes)."""


class gf_text_decoration(ctypes.Structure):
    """gf_text_decoration (record, 56 bytes)."""


class gf_text_editing_table(ctypes.Structure):
    """gf_text_editing_table (table, 120 bytes)."""


class gf_anchored_overlay_options(ctypes.Structure):
    """gf_anchored_overlay_options (extensible, 40 bytes)."""


class gf_overlays_table(ctypes.Structure):
    """gf_overlays_table (table, 80 bytes)."""


class gf_property_grid_table(ctypes.Structure):
    """gf_property_grid_table (table, 48 bytes)."""


class gf_custom_property(ctypes.Structure):
    """gf_custom_property (record, 96 bytes)."""


class gf_paint_target(ctypes.Structure):
    """gf_paint_target (extensible, 72 bytes)."""


class gf_custom_semantics(ctypes.Structure):
    """gf_custom_semantics (extensible, 56 bytes)."""


class gf_custom_control_callbacks(ctypes.Structure):
    """gf_custom_control_callbacks (extensible, 48 bytes)."""


class gf_custom_layout_callbacks(ctypes.Structure):
    """gf_custom_layout_callbacks (extensible, 32 bytes)."""


class gf_custom_control_spec(ctypes.Structure):
    """gf_custom_control_spec (extensible, 88 bytes)."""


class gf_composite_spec(ctypes.Structure):
    """gf_composite_spec (extensible, 56 bytes)."""


class gf_custom_controls_table(ctypes.Structure):
    """gf_custom_controls_table (table, 56 bytes)."""


class gf_binding_arguments(ctypes.Structure):
    """gf_binding_arguments (extensible, 96 bytes)."""


class gf_binding_field(ctypes.Structure):
    """gf_binding_field (record, 24 bytes)."""


class gf_binding_record(ctypes.Structure):
    """gf_binding_record (extensible, 40 bytes)."""


class gf_binding_column(ctypes.Structure):
    """gf_binding_column (extensible, 32 bytes)."""


class gf_binding_sort_key(ctypes.Structure):
    """gf_binding_sort_key (extensible, 24 bytes)."""


class gf_binding_predicate(ctypes.Structure):
    """gf_binding_predicate (extensible, 32 bytes)."""


class gf_binding_provider_callbacks(ctypes.Structure):
    """gf_binding_provider_callbacks (extensible, 96 bytes)."""


class gf_bindings_table(ctypes.Structure):
    """gf_bindings_table (table, 160 bytes)."""


class gf_subsurface_content(ctypes.Structure):
    """gf_subsurface_content (extensible, 40 bytes)."""


class gf_subsurfaces_table(ctypes.Structure):
    """gf_subsurfaces_table (table, 48 bytes)."""


class gf_application_config(ctypes.Structure):
    """gf_application_config (extensible, 32 bytes)."""


class gf_program_identity(ctypes.Structure):
    """gf_program_identity (extensible, 104 bytes)."""


class gf_application_table(ctypes.Structure):
    """gf_application_table (table, 40 bytes)."""


class gf_rule_condition(ctypes.Structure):
    """gf_rule_condition (extensible, 32 bytes)."""


class gf_rule_action(ctypes.Structure):
    """gf_rule_action (extensible, 48 bytes)."""


class gf_rule(ctypes.Structure):
    """gf_rule (extensible, 72 bytes)."""


class gf_rules_table(ctypes.Structure):
    """gf_rules_table (table, 32 bytes)."""


class gf_data_grid_column(ctypes.Structure):
    """gf_data_grid_column (extensible, 104 bytes)."""


class gf_data_grid_row(ctypes.Structure):
    """gf_data_grid_row (extensible, 56 bytes)."""


class gf_data_grid_cell(ctypes.Structure):
    """gf_data_grid_cell (record, 16 bytes)."""


class gf_data_grid_table(ctypes.Structure):
    """gf_data_grid_table (table, 272 bytes)."""


class gf_dock_panel(ctypes.Structure):
    """gf_dock_panel (extensible, 136 bytes)."""


class gf_dock_edit(ctypes.Structure):
    """gf_dock_edit (extensible, 112 bytes)."""


class gf_dock_location(ctypes.Structure):
    """gf_dock_location (extensible, 40 bytes)."""


class gf_dock_options(ctypes.Structure):
    """gf_dock_options (extensible, 16 bytes)."""


class gf_dock_frame_memory(ctypes.Structure):
    """gf_dock_frame_memory (extensible, 56 bytes)."""


class gf_docking_table(ctypes.Structure):
    """gf_docking_table (table, 208 bytes)."""


class gf_app_font_face(ctypes.Structure):
    """gf_app_font_face (extensible, 32 bytes)."""


class gf_fonts_table(ctypes.Structure):
    """gf_fonts_table (table, 40 bytes)."""


class gf_help_table(ctypes.Structure):
    """gf_help_table (table, 128 bytes)."""


class gf_content_pixel_rect(ctypes.Structure):
    """gf_content_pixel_rect (record, 16 bytes)."""


class gf_content_frame(ctypes.Structure):
    """gf_content_frame (extensible, 64 bytes)."""


class gf_content_request(ctypes.Structure):
    """gf_content_request (extensible, 32 bytes)."""


class gf_content_semantics(ctypes.Structure):
    """gf_content_semantics (extensible, 56 bytes)."""


class gf_content_statistics(ctypes.Structure):
    """gf_content_statistics (extensible, 80 bytes)."""


class gf_content_program(ctypes.Structure):
    """gf_content_program (extensible, 40 bytes)."""


class gf_hosted_options(ctypes.Structure):
    """gf_hosted_options (extensible, 64 bytes)."""


class gf_hosted_input_report(ctypes.Structure):
    """gf_hosted_input_report (extensible, 16 bytes)."""


class gf_content_text_line(ctypes.Structure):
    """gf_content_text_line (record, 48 bytes)."""


class gf_content_text_cluster(ctypes.Structure):
    """gf_content_text_cluster (record, 56 bytes)."""


class gf_content_caret_stop(ctypes.Structure):
    """gf_content_caret_stop (record, 40 bytes)."""


class gf_content_layout_transform(ctypes.Structure):
    """gf_content_layout_transform (record, 48 bytes)."""


class gf_content_quad(ctypes.Structure):
    """gf_content_quad (record, 64 bytes)."""


class gf_content_text_layout(ctypes.Structure):
    """gf_content_text_layout (extensible, 120 bytes)."""


class gf_content_table(ctypes.Structure):
    """gf_content_table (table, 368 bytes)."""


class gf_list_view_column(ctypes.Structure):
    """gf_list_view_column (extensible, 48 bytes)."""


class gf_list_view_item(ctypes.Structure):
    """gf_list_view_item (extensible, 88 bytes)."""


class gf_list_view_group(ctypes.Structure):
    """gf_list_view_group (extensible, 40 bytes)."""


class gf_list_view_table(ctypes.Structure):
    """gf_list_view_table (table, 184 bytes)."""


class gf_windows_paint_endpoint_table(ctypes.Structure):
    """gf_windows_paint_endpoint_table (table, 104 bytes)."""


class gf_segment_header(ctypes.Structure):
    """gf_segment_header (extensible, 8 bytes)."""


class gf_class_header(ctypes.Structure):
    """gf_class_header (extensible, 24 bytes)."""


class gf_control_hooks(ctypes.Structure):
    """gf_control_hooks (segment, 352 bytes)."""


class gf_masked_text_box_hooks(ctypes.Structure):
    """gf_masked_text_box_hooks (segment, 16 bytes)."""


class gf_picture_box_hooks(ctypes.Structure):
    """gf_picture_box_hooks (segment, 16 bytes)."""


class gf_combo_box_hooks(ctypes.Structure):
    """gf_combo_box_hooks (segment, 16 bytes)."""


class gf_data_grid_view_hooks(ctypes.Structure):
    """gf_data_grid_view_hooks (segment, 184 bytes)."""


class gf_check_box_hooks(ctypes.Structure):
    """gf_check_box_hooks (segment, 32 bytes)."""


class gf_radio_button_hooks(ctypes.Structure):
    """gf_radio_button_hooks (segment, 16 bytes)."""


class gf_range_control_hooks(ctypes.Structure):
    """gf_range_control_hooks (segment, 16 bytes)."""


class gf_numeric_up_down_hooks(ctypes.Structure):
    """gf_numeric_up_down_hooks (segment, 16 bytes)."""


class gf_date_time_picker_hooks(ctypes.Structure):
    """gf_date_time_picker_hooks (segment, 24 bytes)."""


class gf_node_canvas_hooks(ctypes.Structure):
    """gf_node_canvas_hooks (segment, 56 bytes)."""


class gf_button_base_class(ctypes.Structure):
    """gf_button_base_class (class, 32 bytes)."""


class gf_button_class(ctypes.Structure):
    """gf_button_class (class, 32 bytes)."""


class gf_link_label_class(ctypes.Structure):
    """gf_link_label_class (class, 32 bytes)."""


class gf_label_class(ctypes.Structure):
    """gf_label_class (class, 32 bytes)."""


class gf_picture_box_class(ctypes.Structure):
    """gf_picture_box_class (class, 40 bytes)."""


class gf_progress_bar_class(ctypes.Structure):
    """gf_progress_bar_class (class, 40 bytes)."""


class gf_sweep_scope_class(ctypes.Structure):
    """gf_sweep_scope_class (class, 40 bytes)."""


class gf_list_box_class(ctypes.Structure):
    """gf_list_box_class (class, 32 bytes)."""


class gf_check_box_class(ctypes.Structure):
    """gf_check_box_class (class, 40 bytes)."""


class gf_radio_button_class(ctypes.Structure):
    """gf_radio_button_class (class, 40 bytes)."""


class gf_range_control_class(ctypes.Structure):
    """gf_range_control_class (class, 40 bytes)."""


class gf_track_bar_class(ctypes.Structure):
    """gf_track_bar_class (class, 40 bytes)."""


class gf_panel_class(ctypes.Structure):
    """gf_panel_class (class, 32 bytes)."""


class gf_group_box_class(ctypes.Structure):
    """gf_group_box_class (class, 32 bytes)."""


class gf_material_panel_class(ctypes.Structure):
    """gf_material_panel_class (class, 32 bytes)."""


class gf_card_class(ctypes.Structure):
    """gf_card_class (class, 32 bytes)."""


class gf_container_control_class(ctypes.Structure):
    """gf_container_control_class (class, 32 bytes)."""


class gf_user_control_class(ctypes.Structure):
    """gf_user_control_class (class, 32 bytes)."""


class gf_page_strip_class(ctypes.Structure):
    """gf_page_strip_class (class, 32 bytes)."""


class gf_page_view_class(ctypes.Structure):
    """gf_page_view_class (class, 32 bytes)."""


class gf_navigation_pane_class(ctypes.Structure):
    """gf_navigation_pane_class (class, 32 bytes)."""


class gf_dock_site_class(ctypes.Structure):
    """gf_dock_site_class (class, 32 bytes)."""


class gf_dock_navigator_class(ctypes.Structure):
    """gf_dock_navigator_class (class, 32 bytes)."""


class gf_scaled_panel_class(ctypes.Structure):
    """gf_scaled_panel_class (class, 32 bytes)."""


class gf_scrollable_control_class(ctypes.Structure):
    """gf_scrollable_control_class (class, 32 bytes)."""


class gf_scroll_bar_class(ctypes.Structure):
    """gf_scroll_bar_class (class, 40 bytes)."""


class gf_tool_strip_class(ctypes.Structure):
    """gf_tool_strip_class (class, 32 bytes)."""


class gf_gauge_base_class(ctypes.Structure):
    """gf_gauge_base_class (class, 40 bytes)."""


class gf_dial_class(ctypes.Structure):
    """gf_dial_class (class, 40 bytes)."""


class gf_raster_canvas_class(ctypes.Structure):
    """gf_raster_canvas_class (class, 32 bytes)."""


class gf_text_box_base_class(ctypes.Structure):
    """gf_text_box_base_class (class, 32 bytes)."""


class gf_list_control_class(ctypes.Structure):
    """gf_list_control_class (class, 32 bytes)."""


class gf_up_down_base_class(ctypes.Structure):
    """gf_up_down_base_class (class, 32 bytes)."""


class gf_node_canvas_class(ctypes.Structure):
    """gf_node_canvas_class (class, 40 bytes)."""


class gf_classes_table(ctypes.Structure):
    """gf_classes_table (table, 24 bytes)."""


# Callback typedefs.
gf_base_raiser = ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_event))
gf_hook_entry = ctypes.CFUNCTYPE(None, ctypes.c_void_p, gf_object, ctypes.POINTER(gf_event), gf_base_raiser)

# Fields, in C order.
gf_utf8_view._fields_ = [
    ("data", ctypes.POINTER(ctypes.c_char)),
    ("size", ctypes.c_uint64),
]
gf_abi_version_info._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_major", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("library_major", ctypes.c_uint32),
    ("library_minor", ctypes.c_uint32),
    ("library_patch", ctypes.c_uint32),
]
gf_error_detail._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("status", gf_status),
    ("table_id", gf_table_id),
    ("slot_index", ctypes.c_uint32),
    ("message_size", ctypes.c_uint64),
]
gf_splashscreen_options._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("show_progress", ctypes.c_uint32),
    ("artwork", ctypes.POINTER(ctypes.c_uint8)),
    ("artwork_size", ctypes.c_uint64),
    ("status", gf_utf8_view),
    ("progress", ctypes.c_double),
]
gf_runtime_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("version", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_abi_version_info))),
    ("error_detail", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_error_detail), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("clear_error", ctypes.CFUNCTYPE(gf_status)),
    ("splashscreen_show", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_splashscreen_options), ctypes.POINTER(gf_splashscreen))),
    ("splashscreen_set_status", ctypes.CFUNCTYPE(gf_status, gf_splashscreen, gf_utf8_view)),
    ("splashscreen_set_progress", ctypes.CFUNCTYPE(gf_status, gf_splashscreen, ctypes.c_uint32, ctypes.c_double)),
    ("splashscreen_close", ctypes.CFUNCTYPE(gf_status, gf_splashscreen)),
]
gf_logical_point._fields_ = [
    ("x", ctypes.c_double),
    ("y", ctypes.c_double),
]
gf_logical_size._fields_ = [
    ("width", ctypes.c_double),
    ("height", ctypes.c_double),
]
gf_logical_rect._fields_ = [
    ("x", ctypes.c_double),
    ("y", ctypes.c_double),
    ("width", ctypes.c_double),
    ("height", ctypes.c_double),
]
gf_logical_insets._fields_ = [
    ("left", ctypes.c_double),
    ("top", ctypes.c_double),
    ("right", ctypes.c_double),
    ("bottom", ctypes.c_double),
]
gf_font._fields_ = [
    ("role", gf_font_role),
    ("weight", ctypes.c_uint32),
    ("italic", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("size", ctypes.c_double),
    ("letter_spacing", ctypes.c_double),
]
gf_value._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_value_kind),
    ("boolean", ctypes.c_uint32),
    ("color", ctypes.c_uint32),
    ("signed_integer", ctypes.c_int64),
    ("unsigned_integer", ctypes.c_uint64),
    ("number", ctypes.c_double),
    ("text", gf_utf8_view),
    ("point", gf_logical_point),
    ("size", gf_logical_size),
    ("rectangle", gf_logical_rect),
    ("insets", gf_logical_insets),
    ("font", gf_font),
    ("elements", ctypes.POINTER(gf_value)),
    ("element_count", ctypes.c_uint64),
]
gf_event_field._fields_ = [
    ("name", gf_utf8_view),
    ("kind", gf_value_kind),
    ("flags", gf_event_field_flags),
    ("value", ctypes.POINTER(gf_value)),
]
gf_event._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("cancel", ctypes.c_uint32),
    ("sender", gf_object),
    ("name", gf_utf8_view),
    ("payload", ctypes.POINTER(gf_value)),
    ("field_count", ctypes.c_uint64),
    ("fields", ctypes.POINTER(gf_event_field)),
]
gf_callback._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("invoke", ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(gf_event))),
    ("release", ctypes.CFUNCTYPE(None, ctypes.c_void_p)),
    ("context", ctypes.c_void_p),
]
gf_create_choice._fields_ = [
    ("name", gf_utf8_view),
    ("value", ctypes.c_int64),
]
gf_create_arguments._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_create_flags),
    ("owner", gf_object),
    ("enumeration", gf_utf8_view),
    ("choices", ctypes.POINTER(gf_create_choice)),
    ("choice_count", ctypes.c_uint64),
    ("value", ctypes.c_int64),
]
gf_objects_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("create", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, gf_utf8_view, ctypes.POINTER(gf_object))),
    ("retain", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("release", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("dispose", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("state", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_object_state))),
    ("type_id", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("stable_id", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("insert_child", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object, ctypes.c_uint64)),
    ("remove_child", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object)),
    ("child_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("child_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_object))),
    ("parent", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_object))),
    ("create_with", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, gf_utf8_view, ctypes.POINTER(gf_create_arguments), ctypes.POINTER(gf_object))),
]
gf_properties_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("get", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_value))),
    ("reset", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view)),
    ("element_at", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.c_uint64, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("read_elements", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("get_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_value))),
]
gf_events_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("subscribe", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_callback), ctypes.POINTER(gf_subscription))),
    ("subscribe_property", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_callback), ctypes.POINTER(gf_subscription))),
    ("disconnect", ctypes.CFUNCTYPE(gf_status, gf_subscription)),
    ("write_field", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_event), ctypes.c_uint64, ctypes.POINTER(gf_value))),
    ("field_element", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_event), ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_value))),
]
gf_dispatch_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("begin_invoke", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_callback))),
    ("run_pending", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint64))),
]
gf_schema_interaction._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("mutable_payload", ctypes.c_uint32),
    ("name", gf_utf8_view),
    ("payload", gf_utf8_view),
]
gf_run_options._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_run_flags),
    ("title", gf_utf8_view),
    ("width", ctypes.c_double),
    ("height", ctypes.c_double),
    ("ready", ctypes.POINTER(gf_callback)),
    ("closing", ctypes.POINTER(gf_callback)),
    ("closed", ctypes.POINTER(gf_callback)),
    ("minimum_width", ctypes.c_double),
    ("minimum_height", ctypes.c_double),
]
gf_owned_window_options._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_owned_window_flags),
    ("title", gf_utf8_view),
    ("width", ctypes.c_double),
    ("height", ctypes.c_double),
    ("owner", gf_object),
    ("ready", ctypes.POINTER(gf_callback)),
    ("closing", ctypes.POINTER(gf_callback)),
    ("closed", ctypes.POINTER(gf_callback)),
]
gf_window_band_options._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_window_band_flags),
    ("full_screen", gf_window_band_full_screen),
    ("reserved", ctypes.c_uint32),
    ("width", ctypes.c_double),
    ("edges", gf_logical_insets),
]
gf_window_band_appearance._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("state", gf_window_band_state),
    ("flags", gf_window_band_appearance_flags),
    ("lit_role", gf_window_band_role),
    ("rest_colour", ctypes.c_uint32),
    ("lit_colour", ctypes.c_uint32),
    ("frequency", ctypes.c_double),
    ("texture", gf_window_band_texture),
    ("texture_kind", ctypes.c_uint32),
    ("texture_seed", ctypes.c_uint32),
    ("texture_primary", ctypes.c_uint32),
    ("texture_secondary", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("texture_tile", ctypes.c_double),
    ("texture_strength", ctypes.c_double),
    ("texture_opacity", ctypes.c_double),
]
gf_window_band_report._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("status", gf_window_band_status),
    ("edges", gf_logical_insets),
    ("drawn_colour", ctypes.c_uint32),
    ("full_screen", gf_window_band_full_screen),
    ("frequency", ctypes.c_double),
    ("flash_changes", ctypes.c_uint64),
    ("cycle_frames", ctypes.c_uint64),
]
gf_window_shaping._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_window_shaping_flags),
    ("preference", gf_window_corner_preference),
    ("corner_shapes", ctypes.c_uint32),
    ("corner_shape", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("corner_radius", ctypes.c_double),
]
gf_windows_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("run", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_run_options))),
    ("request_close", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("create", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_object))),
    ("interaction_count", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint64))),
    ("interaction_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(gf_schema_interaction))),
    ("request_help", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("key_state", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32))),
    ("show_modal", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_owned_window_options), ctypes.POINTER(gf_dialog_result_code))),
    ("show_owned", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_owned_window_options))),
    ("window_properties", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_window_property_flags), ctypes.POINTER(gf_window_property_flags))),
    ("focused_control", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_object))),
    ("declare_band", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_window_band_options))),
    ("undeclare_band", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("set_band_appearance", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_window_band_appearance))),
    ("band_report", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_window_band_report))),
    ("set_corner_preference", ctypes.CFUNCTYPE(gf_status, gf_object, gf_window_corner_preference)),
    ("content_rect", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_logical_rect))),
    ("shaping", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_window_shaping))),
    ("pointer_location", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_logical_point), ctypes.POINTER(gf_logical_point), ctypes.POINTER(ctypes.c_uint32))),
    ("show_business_card", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("set_mdi_container", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("mdi_container", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("mdi_child_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("mdi_child_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("active_mdi_child", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("activate_mdi_child", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("layout_mdi", ctypes.CFUNCTYPE(gf_status, gf_object, gf_mdi_layout, ctypes.POINTER(ctypes.c_uint32))),
    ("set_mdi_children_minimized_anchor_bottom", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("mdi_children_minimized_anchor_bottom", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("set_main_menu_strip", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object)),
    ("main_menu_strip", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_object))),
]
gf_schema_type._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_schema_kind),
    ("id", gf_utf8_view),
    ("type_name", gf_utf8_view),
    ("part_count", ctypes.c_uint64),
    ("state_count", ctypes.c_uint64),
    ("custom_state_count", ctypes.c_uint64),
    ("item_system_count", ctypes.c_uint64),
    ("property_count", ctypes.c_uint64),
    ("interaction_count", ctypes.c_uint64),
]
gf_schema_item_system._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("name", gf_utf8_view),
    ("part_count", ctypes.c_uint64),
    ("state_count", ctypes.c_uint64),
    ("custom_state_count", ctypes.c_uint64),
]
gf_schema_part._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("name", gf_utf8_view),
    ("role", gf_utf8_view),
    ("composed_from", gf_utf8_view),
    ("state_count", ctypes.c_uint64),
]
gf_schema_property._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_value_kind),
    ("name", gf_utf8_view),
    ("category", gf_utf8_view),
    ("enumeration", gf_utf8_view),
    ("choice_count", ctypes.c_uint64),
    ("flags", gf_schema_property_flags),
    ("serialization", gf_schema_serialization),
]
gf_schema_choice._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("name", gf_utf8_view),
    ("value", ctypes.c_int64),
]
gf_schema_engine._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("version_major", ctypes.c_uint32),
    ("version_minor", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("operations_per_device_pixel", ctypes.c_uint64),
    ("animated_operations_per_frame", ctypes.c_uint64),
    ("expression_maximum_operations", ctypes.c_uint64),
    ("expression_maximum_stack", ctypes.c_uint64),
    ("published_values_maximum", ctypes.c_uint64),
    ("transition_maximum_states", ctypes.c_uint64),
    ("transition_maximum_per_part", ctypes.c_uint64),
    ("ambient_maximum_frames_per_second", ctypes.c_double),
    ("ambient_maximum_window_fraction", ctypes.c_double),
    ("primitive_count", ctypes.c_uint64),
]
gf_schema_primitive._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("introduced_major", ctypes.c_uint32),
    ("introduced_minor", ctypes.c_uint32),
    ("cost_per_device_pixel", ctypes.c_uint32),
    ("cost_fixed", ctypes.c_uint32),
    ("cost_preparation_per_device_pixel", ctypes.c_uint32),
    ("name", gf_utf8_view),
    ("outsets", gf_logical_insets),
    ("role_count", ctypes.c_uint64),
    ("state_read_count", ctypes.c_uint64),
    ("input_read_count", ctypes.c_uint64),
    ("parameter_count", ctypes.c_uint64),
]
gf_schema_parameter._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_schema_parameter_kind),
    ("name", gf_utf8_view),
    ("minimum", ctypes.c_double),
    ("maximum", ctypes.c_double),
    ("default_number", ctypes.c_double),
    ("default_color", ctypes.c_uint32),
    ("animated", ctypes.c_uint32),
    ("choice_count", ctypes.c_uint64),
]
gf_schema_effect._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("time_model", gf_schema_effect_time_model),
    ("name", gf_utf8_view),
    ("parent", gf_utf8_view),
    ("engine_version", ctypes.c_uint32),
    ("input", gf_schema_effect_input),
    ("cost_fixed", ctypes.c_uint32),
    ("cost_per_device_pixel", ctypes.c_uint32),
    ("setup_cost", ctypes.c_uint32),
    ("flags", gf_schema_effect_flags),
    ("state_budget", ctypes.c_uint64),
    ("frames_per_second", ctypes.c_double),
    ("outsets", gf_logical_insets),
]
gf_schema_composite._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("composite", ctypes.c_uint64),
    ("id", gf_utf8_view),
    ("name", gf_utf8_view),
    ("version", gf_utf8_view),
    ("slot", gf_utf8_view),
    ("part_count", ctypes.c_uint64),
    ("state_count", ctypes.c_uint64),
    ("custom_state_count", ctypes.c_uint64),
    ("property_count", ctypes.c_uint64),
    ("event_count", ctypes.c_uint64),
    ("command_count", ctypes.c_uint64),
]
gf_schema_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("vocabulary_count", ctypes.CFUNCTYPE(gf_status, gf_schema_vocabulary, ctypes.POINTER(ctypes.c_uint64))),
    ("vocabulary_at", ctypes.CFUNCTYPE(gf_status, gf_schema_vocabulary, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
    ("type_count", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint64))),
    ("find_type", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, ctypes.POINTER(ctypes.c_uint64))),
    ("type_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(gf_schema_type))),
    ("item_system_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_item_system))),
    ("part_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_part))),
    ("state_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
    ("custom_state_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
    ("property_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_property))),
    ("choice_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_choice))),
    ("interaction_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_interaction))),
    ("engine", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_schema_engine))),
    ("primitive_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(gf_schema_primitive))),
    ("primitive_name_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, gf_schema_primitive_list, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
    ("parameter_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_parameter))),
    ("parameter_choice_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
    ("effect_count", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint64))),
    ("effect_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(gf_schema_effect))),
    ("child_property_count", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("child_property_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_property))),
    ("child_choice_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_choice))),
    ("composite_count", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint64))),
    ("composite_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(gf_schema_composite))),
    ("composite_part_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_part))),
    ("composite_state_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
    ("composite_custom_state_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
    ("composite_property_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_property))),
    ("composite_choice_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_choice))),
    ("composite_event_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_schema_interaction))),
    ("composite_command_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
]
gf_bytes_view._fields_ = [
    ("data", ctypes.POINTER(ctypes.c_uint8)),
    ("size", ctypes.c_uint64),
]
gf_theme_file._fields_ = [
    ("path", gf_utf8_view),
    ("bytes", gf_bytes_view),
]
gf_theme_package._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("manifest", gf_bytes_view),
    ("files", ctypes.POINTER(gf_theme_file)),
    ("file_count", ctypes.c_uint64),
]
gf_theme_report._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("outcome", gf_theme_outcome),
    ("diagnostic_count", ctypes.c_uint64),
]
gf_theme_diagnostic._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("severity", gf_theme_severity),
    ("line", ctypes.c_uint32),
    ("column", ctypes.c_uint32),
]
gf_themes_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("load", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_theme_package), ctypes.POINTER(gf_theme_report))),
    ("reset", ctypes.CFUNCTYPE(gf_status)),
    ("install", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_theme_package), ctypes.POINTER(gf_theme_report))),
    ("remove", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("diagnostic_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(gf_theme_diagnostic))),
    ("diagnostic_text", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, gf_theme_diagnostic_text, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("theme_id", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("publish_value", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, ctypes.c_double)),
    ("withdraw_value", ctypes.CFUNCTYPE(gf_status, gf_utf8_view)),
    ("published_value", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_uint32))),
    ("load_image", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("remove_image", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64)),
    ("load_pixels", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("load_sheet", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, gf_utf8_view, ctypes.POINTER(gf_theme_report))),
    ("set_user_theme_policy", ctypes.CFUNCTYPE(gf_status, gf_user_theme_policy)),
    ("theme_request", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_theme_request_outcome))),
]
gf_host_capabilities._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("protocol_version", ctypes.c_uint32),
    ("available", gf_host_capability),
    ("transient_surfaces", gf_transient_surface_kind),
    ("reserved", ctypes.c_uint32),
    ("window_corner_shapes", gf_window_corner_shape),
    ("window_band_maximum_width", ctypes.c_uint32),
]
gf_file_filter._fields_ = [
    ("label", gf_utf8_view),
    ("extensions", ctypes.POINTER(gf_utf8_view)),
    ("extension_count", ctypes.c_uint64),
]
gf_dialog_request._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_dialog_kind),
    ("title", gf_utf8_view),
    ("message", gf_utf8_view),
    ("initial_directory", gf_utf8_view),
    ("suggested_name", gf_utf8_view),
    ("default_extension", gf_utf8_view),
    ("filters", ctypes.POINTER(gf_file_filter)),
    ("filter_count", ctypes.c_uint64),
    ("initial_filter", ctypes.c_uint64),
    ("buttons", gf_message_buttons),
    ("icon", gf_message_icon),
    ("default_choice", gf_dialog_choice),
    ("flags", gf_dialog_flags),
    ("initial_rgba", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("owner", gf_object),
]
gf_dialog_result._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("outcome", gf_dialog_outcome),
    ("choice", gf_dialog_choice),
    ("rgba", ctypes.c_uint32),
    ("path_count", ctypes.c_uint64),
    ("chosen_filter", ctypes.c_uint64),
]
gf_host_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("capabilities", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_host_capabilities))),
    ("platform_name", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_cursor", ctypes.CFUNCTYPE(gf_status, gf_pointer_cursor)),
    ("read_clipboard_text", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("write_clipboard_text", ctypes.CFUNCTYPE(gf_status, gf_utf8_view)),
    ("show_dialog", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_dialog_request), ctypes.POINTER(gf_dialog_result))),
    ("dialog_path_at", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
]
gf_shadow_frame._fields_ = [
    ("kind", gf_shadow_frame_kind),
    ("flags", gf_shadow_frame_flags),
    ("table_id", gf_table_id),
    ("slot_index", ctypes.c_uint32),
    ("sequence", ctypes.c_uint64),
    ("subject_size", ctypes.c_uint32),
    ("name_size", ctypes.c_uint32),
    ("subject", (ctypes.c_uint8 * 48)),
    ("name", (ctypes.c_uint8 * 32)),
]
gf_shadow_stack_info._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("depth", ctypes.c_uint32),
    ("pushed", ctypes.c_uint64),
    ("dropped", ctypes.c_uint64),
]
gf_failure_snapshot._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("status", gf_status),
    ("table_id", gf_table_id),
    ("slot_index", ctypes.c_uint32),
    ("sequence", ctypes.c_uint64),
    ("frame_count", ctypes.c_uint32),
    ("depth", ctypes.c_uint32),
    ("site_size", ctypes.c_uint32),
    ("message_size", ctypes.c_uint32),
    ("site", (ctypes.c_uint8 * 64)),
]
gf_failure_detail._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("status", gf_status),
    ("sequence", ctypes.c_uint64),
    ("type_size", ctypes.c_uint32),
    ("trace_count", ctypes.c_uint32),
    ("type", (ctypes.c_uint8 * 256)),
    ("trace", (ctypes.c_uint64 * 32)),
    ("flags", gf_failure_detail_flags),
    ("reserved", ctypes.c_uint32),
]
gf_diagnostics_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("shadow_frames", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_shadow_frame), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(gf_shadow_stack_info))),
    ("set_invalidation_overlay", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint32)),
    ("invalidation_overlay", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint32))),
    ("failure_snapshot", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_failure_snapshot), ctypes.POINTER(gf_shadow_frame), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("clear_failure_snapshot", ctypes.CFUNCTYPE(gf_status)),
    ("set_exception_reflection", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint32)),
    ("exception_reflection", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint32))),
    ("raise_native_exception", ctypes.CFUNCTYPE(gf_status, gf_utf8_view)),
    ("failure_detail", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_failure_detail))),
    ("set_diagnostic_overlay", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint32)),
    ("toggle_diagnostic_overlay", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint32))),
]
gf_layout_transaction._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("suspend_depth", ctypes.c_uint32),
    ("deferred", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("requested_revision", ctypes.c_uint64),
    ("committed_revision", ctypes.c_uint64),
]
gf_scroll_axis._fields_ = [
    ("enabled", ctypes.c_uint32),
    ("visible", ctypes.c_uint32),
    ("minimum", ctypes.c_double),
    ("maximum", ctypes.c_double),
    ("large_change", ctypes.c_double),
    ("small_change", ctypes.c_double),
    ("value", ctypes.c_double),
]
gf_scroll_snapshot._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("auto_scroll", ctypes.c_uint32),
    ("position", gf_logical_point),
    ("margin", gf_logical_size),
    ("minimum_content_size", gf_logical_size),
    ("display_rectangle", gf_logical_rect),
    ("viewport_rectangle", gf_logical_rect),
    ("horizontal", gf_scroll_axis),
    ("vertical", gf_scroll_axis),
    ("event_revision", ctypes.c_uint64),
    ("event_type", ctypes.c_uint32),
    ("event_orientation", gf_scroll_orientation),
    ("event_old_value", ctypes.c_double),
    ("event_new_value", ctypes.c_double),
]
gf_relative_pointer_request._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("mode", gf_relative_pointer_mode),
    ("hide_cursor", ctypes.c_uint32),
    ("raw_motion", ctypes.c_uint32),
    ("until_release", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
]
gf_relative_pointer_grant._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("result", gf_relative_pointer_result),
    ("mode", gf_relative_pointer_mode),
    ("raw", ctypes.c_uint32),
    ("cursor_hidden", ctypes.c_uint32),
    ("host_relative", ctypes.c_uint32),
]
gf_relative_pointer_state._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("owned", ctypes.c_uint32),
    ("active", ctypes.c_uint32),
    ("suspended", ctypes.c_uint32),
    ("mode", gf_relative_pointer_mode),
    ("raw", ctypes.c_uint32),
    ("host_relative", ctypes.c_uint32),
    ("last_end", gf_relative_pointer_end),
    ("grants", ctypes.c_uint64),
    ("samples", ctypes.c_uint64),
    ("suspensions", ctypes.c_uint64),
    ("resumptions", ctypes.c_uint64),
    ("ends", ctypes.c_uint64),
    ("support_relative_motion", ctypes.c_uint32),
    ("support_raw_motion", ctypes.c_uint32),
    ("support_lock", ctypes.c_uint32),
    ("support_confine", ctypes.c_uint32),
    ("support_warp", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
]
gf_effect_mask_layer._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("mode", gf_effect_mask_mode),
    ("composite", gf_effect_mask_composite),
    ("start_rgba", ctypes.c_uint32),
    ("end_rgba", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("start", gf_logical_point),
    ("end", gf_logical_point),
]
gf_content_effect._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("has_colour_matrix", ctypes.c_uint32),
    ("has_colour_table", ctypes.c_uint32),
    ("mask_count", ctypes.c_uint32),
    ("colour_matrix", (ctypes.c_double * 20)),
    ("colour_table", (ctypes.c_uint8 * 1024)),
    ("blur", ctypes.c_double),
    ("masks", ctypes.POINTER(gf_effect_mask_layer)),
]
gf_controls_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("suspend_layout", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("resume_layout", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("perform_layout", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("layout_state", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_layout_transaction))),
    ("window_bounds", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_logical_rect))),
    ("set_pointer_capture", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("pointer_capture", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("scroll_state", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_scroll_snapshot))),
    ("set_scroll_axis", ctypes.CFUNCTYPE(gf_status, gf_object, gf_scroll_orientation, ctypes.POINTER(gf_scroll_axis))),
    ("scroll_into_view", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object)),
    ("invalidate", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_logical_rect))),
    ("focus", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("focus_state", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32))),
    ("request_relative_pointer", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_relative_pointer_request), ctypes.POINTER(gf_relative_pointer_grant))),
    ("release_relative_pointer", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("relative_pointer_state", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_relative_pointer_state))),
    ("warp_pointer", ctypes.CFUNCTYPE(gf_status, gf_object, gf_logical_point, ctypes.POINTER(ctypes.c_uint32))),
    ("set_pointer_release_regions", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_logical_rect), ctypes.c_uint32)),
    ("set_content_effect", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_effect))),
]
gf_text_decoration._fields_ = [
    ("start", ctypes.c_uint64),
    ("end", ctypes.c_uint64),
    ("fields", gf_text_decoration_fields),
    ("ink", gf_text_ink_role),
    ("foreground", ctypes.c_uint32),
    ("weight", ctypes.c_uint32),
    ("italic", ctypes.c_uint32),
    ("underline", gf_text_underline),
    ("underline_color", ctypes.c_uint32),
    ("background", ctypes.c_uint32),
    ("tag", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
]
gf_text_editing_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("select", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint64)),
    ("selection", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint64))),
    ("grapheme_boundary", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_int32, ctypes.POINTER(ctypes.c_uint64))),
    ("replace_range", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint64, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("undo", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("redo", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("clear_undo_history", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("set_decorations", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.POINTER(gf_text_decoration), ctypes.c_uint64)),
    ("replace_decorations", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_text_decoration), ctypes.c_uint64)),
    ("clear_decorations", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("decoration_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint64))),
    ("decoration_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.c_uint64, ctypes.POINTER(gf_text_decoration))),
    ("utf8_to_utf16_offset", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("utf16_to_utf8_offset", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
]
gf_anchored_overlay_options._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_anchored_overlay_flags),
    ("width", ctypes.c_double),
    ("height", ctypes.c_double),
    ("gap", ctypes.c_double),
    ("events", ctypes.POINTER(gf_callback)),
]
gf_overlays_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("open_overlay", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object)),
    ("close_overlay", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("set_tool_tip", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object, gf_utf8_view)),
    ("show_tool_tip", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object, ctypes.c_uint64)),
    ("hide_tool_tip", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("open_anchored", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object, ctypes.POINTER(gf_anchored_overlay_options))),
    ("close_anchored", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("set_tool_tips_shown", ctypes.CFUNCTYPE(gf_status, gf_object, gf_tool_tips_setting)),
    ("tool_tips_shown", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(gf_tool_tips_setting))),
]
gf_property_grid_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("select_objects", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_object), ctypes.c_uint64)),
    ("refresh", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("try_set_text", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("reset_property", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("activate_editor", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
]
gf_custom_property._fields_ = [
    ("name", gf_utf8_view),
    ("category", gf_utf8_view),
    ("description", gf_utf8_view),
    ("kind", gf_value_kind),
    ("flags", gf_custom_property_flags),
    ("default_value", ctypes.POINTER(gf_value)),
    ("enumeration", gf_utf8_view),
    ("choices", ctypes.POINTER(gf_create_choice)),
    ("choice_count", ctypes.c_uint64),
]
gf_paint_target._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("width", ctypes.c_uint32),
    ("height", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("row_bytes", ctypes.c_uint64),
    ("pixels", ctypes.POINTER(ctypes.c_uint8)),
    ("scale", ctypes.c_double),
    ("damage", gf_logical_rect),
]
gf_custom_semantics._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("role", ctypes.c_uint32),
    ("name", gf_utf8_view),
    ("value", gf_utf8_view),
    ("description", gf_utf8_view),
]
gf_custom_control_callbacks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("context", ctypes.c_void_p),
    ("paint", ctypes.CFUNCTYPE(None, ctypes.c_void_p, gf_object, ctypes.POINTER(gf_paint_target))),
    ("get_property", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_value))),
    ("set_property", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_value))),
    ("release", ctypes.CFUNCTYPE(None, ctypes.c_void_p)),
]
gf_custom_layout_callbacks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("measure", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, gf_object, gf_logical_size, ctypes.POINTER(gf_logical_size))),
    ("hit_test", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, gf_object, gf_logical_point, ctypes.POINTER(ctypes.c_uint32))),
    ("semantics", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, gf_object, ctypes.POINTER(gf_custom_semantics))),
]
gf_custom_control_spec._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("base", gf_custom_base),
    ("flags", gf_custom_control_flags),
    ("property_size", ctypes.c_uint32),
    ("properties", ctypes.POINTER(gf_custom_property)),
    ("property_count", ctypes.c_uint64),
    ("callbacks", gf_custom_control_callbacks),
    ("layout", ctypes.POINTER(gf_custom_layout_callbacks)),
]
gf_composite_spec._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("file", gf_utf8_view),
    ("document", gf_utf8_view),
    ("child_types", ctypes.POINTER(gf_utf8_view)),
    ("child_type_count", ctypes.c_uint64),
]
gf_custom_controls_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("create", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_custom_control_spec), gf_utf8_view, ctypes.POINTER(gf_object))),
    ("notify_changed", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64)),
    ("load_composite", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_composite_spec), ctypes.POINTER(gf_object))),
    ("create_composite", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_object))),
    ("perform_composite", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("composite_child", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_object))),
]
gf_binding_arguments._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("source_update_mode", gf_source_update_mode),
    ("control_update_mode", gf_control_update_mode),
    ("formatting_enabled", ctypes.c_uint32),
    ("target", gf_object),
    ("source", gf_object),
    ("property", gf_utf8_view),
    ("data_member", gf_utf8_view),
    ("format_string", gf_utf8_view),
    ("null_value", ctypes.POINTER(gf_value)),
    ("source_null_value", ctypes.POINTER(gf_value)),
]
gf_binding_field._fields_ = [
    ("name", gf_utf8_view),
    ("value", ctypes.POINTER(gf_value)),
]
gf_binding_record._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("editable", ctypes.c_uint32),
    ("stable_id", gf_utf8_view),
    ("fields", ctypes.POINTER(gf_binding_field)),
    ("field_count", ctypes.c_uint64),
]
gf_binding_column._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_value_kind),
    ("name", gf_utf8_view),
    ("read_only", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
]
gf_binding_sort_key._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("direction", gf_binding_sort_direction),
    ("column", gf_utf8_view),
]
gf_binding_predicate._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("op", gf_binding_predicate_operator),
    ("column", gf_utf8_view),
    ("operand", ctypes.POINTER(gf_value)),
]
gf_binding_provider_callbacks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_binding_provider_flags),
    ("context", ctypes.c_void_p),
    ("row_count", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint64))),
    ("read_value", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_value))),
    ("read_stable_id", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.c_uint64, ctypes.POINTER(gf_utf8_view))),
    ("write_value", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(gf_utf8_view))),
    ("read_cell_state", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(gf_utf8_view))),
    ("apply_sort", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.POINTER(gf_binding_sort_key), ctypes.c_uint64)),
    ("apply_filter", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.POINTER(gf_binding_predicate), ctypes.c_uint64)),
    ("insert_row", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.c_uint64, gf_utf8_view, ctypes.POINTER(gf_value), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))),
    ("remove_rows", ctypes.CFUNCTYPE(gf_status, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))),
    ("release", ctypes.CFUNCTYPE(None, ctypes.c_void_p)),
]
gf_bindings_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("bind", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_binding_arguments), ctypes.POINTER(gf_object))),
    ("unbind", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("read_value", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("write_value", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("add_record", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_binding_record), ctypes.POINTER(ctypes.c_uint64))),
    ("insert_record", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_binding_record))),
    ("remove_record", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))),
    ("clear_records", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("set_position", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_int64, ctypes.POINTER(ctypes.c_uint32))),
    ("position", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(ctypes.c_uint64))),
    ("current_field", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_current_field", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_uint32))),
    ("add_records", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_binding_record), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_provider", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_binding_column), ctypes.c_uint64, ctypes.POINTER(gf_binding_provider_callbacks), ctypes.POINTER(ctypes.c_uint64))),
    ("notify", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, gf_binding_notification_kind, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)),
    ("set_sort", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_binding_sort_key), ctypes.c_uint64)),
    ("set_filter", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_binding_predicate), ctypes.c_uint64)),
    ("generation", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint64))),
    ("read_cell", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
]
gf_subsurface_content._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("opaque", ctypes.c_uint32),
    ("build", gf_callback),
]
gf_subsurfaces_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("set_content", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_subsurface_content))),
    ("set_root", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("state", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_subsurface_state))),
    ("content_epoch", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("failure", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
]
gf_application_config._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("theme_base", gf_theme_base),
    ("packages", ctypes.POINTER(gf_theme_package)),
    ("package_count", ctypes.c_uint64),
    ("presentation_source", gf_presentation_source),
    ("reserved", ctypes.c_uint32),
]
gf_program_identity._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("product", gf_utf8_view),
    ("version", gf_utf8_view),
    ("vendor", gf_utf8_view),
    ("website", gf_utf8_view),
    ("copyright", gf_utf8_view),
    ("credits", gf_utf8_view),
]
gf_application_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("create", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_application_config), ctypes.POINTER(gf_theme_report))),
    ("close", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(ctypes.c_uint64))),
    ("state", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_application_state))),
    ("set_program_identity", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_program_identity))),
]
gf_rule_condition._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_rule_condition_kind),
    ("object", gf_object),
    ("physical_key", ctypes.c_uint32),
    ("modifiers", ctypes.c_uint32),
    ("negated", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
]
gf_rule_action._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_rule_action_kind),
    ("target", gf_object),
    ("property", gf_utf8_view),
    ("value", ctypes.POINTER(gf_value)),
    ("callback", ctypes.POINTER(gf_callback)),
]
gf_rule._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_rule_flags),
    ("trigger", gf_rule_trigger_kind),
    ("physical_key", ctypes.c_uint32),
    ("source", gf_object),
    ("interaction", gf_utf8_view),
    ("condition_count", ctypes.c_uint64),
    ("conditions", ctypes.POINTER(gf_rule_condition)),
    ("action_count", ctypes.c_uint64),
    ("actions", ctypes.POINTER(gf_rule_action)),
]
gf_rules_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("add", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_rule), ctypes.POINTER(gf_rule_token))),
    ("remove", ctypes.CFUNCTYPE(gf_status, gf_rule_token)),
    ("state", ctypes.CFUNCTYPE(gf_status, gf_rule_token, ctypes.POINTER(gf_rule_state))),
]
gf_data_grid_column._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_data_grid_column_kind),
    ("value_kind", gf_value_kind),
    ("read_only", ctypes.c_uint32),
    ("hidden", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("width", ctypes.c_double),
    ("minimum_width", ctypes.c_double),
    ("name", gf_utf8_view),
    ("header_text", gf_utf8_view),
    ("data_property_name", gf_utf8_view),
    ("items", ctypes.POINTER(gf_utf8_view)),
    ("item_count", ctypes.c_uint64),
]
gf_data_grid_row._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("read_only", ctypes.c_uint32),
    ("stable_id", gf_utf8_view),
    ("header_text", gf_utf8_view),
    ("cells", ctypes.POINTER(gf_value)),
    ("cell_count", ctypes.c_uint64),
]
gf_data_grid_cell._fields_ = [
    ("row", ctypes.c_uint64),
    ("column", ctypes.c_uint64),
]
gf_data_grid_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("column_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("column_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_data_grid_column), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("column_item", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("insert_column", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_data_grid_column))),
    ("remove_column", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64)),
    ("column_index", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint64))),
    ("set_column_header_text", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, gf_utf8_view)),
    ("set_column_width", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_double)),
    ("set_column_read_only", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint32)),
    ("set_column_hidden", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint32)),
    ("row_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_int64))),
    ("insert_rows", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_data_grid_row), ctypes.c_uint64)),
    ("append_rows", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_data_grid_row), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("erase_rows", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint64)),
    ("replace_row", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_data_grid_row))),
    ("clear_rows", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("row_id", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("row_position", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint64))),
    ("cell_value", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.c_uint64, gf_value_kind, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_cell_value", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.c_uint64, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_uint32))),
    ("cell_text", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.c_uint64, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("read_cells", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_value), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("current_cell", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint64))),
    ("set_current_cell", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))),
    ("selected_rows", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("selected_cells", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_data_grid_cell), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_row_selected", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.c_uint32)),
    ("set_cell_selected", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.c_uint64, ctypes.c_uint32)),
    ("clear_selection", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("select_all", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("begin_edit", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32))),
    ("end_edit", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("cancel_edit", ctypes.CFUNCTYPE(gf_status, gf_object)),
]
gf_dock_panel._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_dock_panel_kind),
    ("allowed", gf_dock_allowed),
    ("dock_as_document", ctypes.c_uint32),
    ("default_placement", gf_dock_placement),
    ("default_side", gf_dock_side),
    ("default_ratio", ctypes.c_double),
    ("default_extent", ctypes.c_double),
    ("default_frame", gf_logical_rect),
    ("minimum_size", gf_logical_size),
    ("id", gf_utf8_view),
    ("title", gf_utf8_view),
    ("content", gf_object),
    ("reserved", ctypes.c_uint64),
]
gf_dock_edit._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("kind", gf_dock_edit_kind),
    ("subject_is_stack", ctypes.c_uint32),
    ("subject_stack", ctypes.c_uint32),
    ("target_node", ctypes.c_uint32),
    ("site", ctypes.c_uint32),
    ("side", gf_dock_side),
    ("index", ctypes.c_uint32),
    ("ratio", ctypes.c_double),
    ("extent", ctypes.c_double),
    ("frame", gf_logical_rect),
    ("panel", gf_utf8_view),
    ("reserved", ctypes.c_uint64),
    ("presentation", gf_dock_document_presentation),
    ("frame_state", gf_dock_frame_state),
]
gf_dock_location._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("placement", gf_dock_placement),
    ("stack", ctypes.c_uint32),
    ("index", ctypes.c_uint32),
    ("site", ctypes.c_uint32),
    ("stack_kind", gf_dock_node_kind),
    ("side", gf_dock_side),
    ("selected", ctypes.c_uint32),
    ("stack_panel_count", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
]
gf_dock_options._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("flags", gf_dock_option_flags),
    ("area_background", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
]
gf_dock_frame_memory._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("present", ctypes.c_uint32),
    ("bounds", gf_logical_rect),
    ("state", gf_dock_frame_state),
    ("icon_slot", ctypes.c_uint32),
    ("order", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
]
gf_docking_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("register_panel", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_dock_panel))),
    ("set_panel_content", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, gf_object)),
    ("set_panel_title", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, gf_utf8_view)),
    ("apply_edit", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_dock_edit), ctypes.POINTER(gf_dock_refusal))),
    ("locate", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_dock_location))),
    ("save_layout", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("load_layout", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint64))),
    ("activate_panel", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view)),
    ("attach_windows", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("document_area", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("panel_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.c_uint64, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("floating_sites", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("floating_site", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.POINTER(gf_logical_rect), ctypes.POINTER(ctypes.c_uint32))),
    ("update_panel", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_dock_panel))),
    ("set_options", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_dock_options))),
    ("set_floating_window_visibility", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, gf_dock_window_visibility)),
    ("document_presentation", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_dock_document_presentation))),
    ("arrange_frames", ctypes.CFUNCTYPE(gf_status, gf_object, gf_dock_frame_arrangement, ctypes.POINTER(gf_dock_refusal))),
    ("frame_memory", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(gf_dock_frame_memory))),
    ("set_frame_icons_at_bottom", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("area_document_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("area_document_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("area_active_document", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_panel_menu_strip", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, gf_object)),
    ("merged_document", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
]
gf_app_font_face._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("weight", ctypes.c_uint32),
    ("italic", ctypes.c_uint32),
    ("bytes", gf_bytes_view),
]
gf_fonts_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("family_id", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("family_name", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint32, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("load_family", ctypes.CFUNCTYPE(gf_status, gf_utf8_view, ctypes.POINTER(gf_app_font_face), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))),
    ("unload_family", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32))),
]
gf_help_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("attach", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object)),
    ("detach", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object)),
    ("load_built_in", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view)),
    ("show", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("show_navigator", ctypes.CFUNCTYPE(gf_status, gf_object, gf_help_navigator, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("show_popup", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("resolve", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint32))),
    ("enter_help_mode", ctypes.CFUNCTYPE(gf_status, gf_object, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("cancel_help_mode", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("load_translation", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view)),
    ("load_user_overrides", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view)),
    ("clear_user_overrides", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("use_built_in_language", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("export_template", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("read_field", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, gf_locale_field, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(gf_locale_origin))),
]
gf_content_pixel_rect._fields_ = [
    ("x", ctypes.c_uint32),
    ("y", ctypes.c_uint32),
    ("width", ctypes.c_uint32),
    ("height", ctypes.c_uint32),
]
gf_content_frame._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("pixel_format", gf_content_pixel_format),
    ("width", ctypes.c_uint32),
    ("height", ctypes.c_uint32),
    ("row_bytes", ctypes.c_uint64),
    ("opaque", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("damage", gf_content_pixel_rect),
    ("pixels", gf_bytes_view),
]
gf_content_request._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("width", ctypes.c_uint32),
    ("height", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("scale", ctypes.c_double),
    ("generation", ctypes.c_uint64),
]
gf_content_semantics._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("name", gf_utf8_view),
    ("text", gf_utf8_view),
    ("description", gf_utf8_view),
]
gf_content_statistics._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("last_refusal", gf_content_publish_result),
    ("frames_published", ctypes.c_uint64),
    ("frames_refused", ctypes.c_uint64),
    ("frames_dropped", ctypes.c_uint64),
    ("heartbeats", ctypes.c_uint64),
    ("stale_transitions", ctypes.c_uint64),
    ("recoveries", ctypes.c_uint64),
    ("semantics_published", ctypes.c_uint64),
    ("semantics_refused", ctypes.c_uint64),
    ("after_revocation", ctypes.c_uint64),
]
gf_content_program._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("opaque", ctypes.c_uint32),
    ("run", gf_callback),
]
gf_hosted_options._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("opaque", ctypes.c_uint32),
    ("executable", gf_utf8_view),
    ("arguments", ctypes.POINTER(gf_utf8_view)),
    ("argument_count", ctypes.c_uint64),
    ("slot_bytes", ctypes.c_uint64),
    ("start_timeout_ms", ctypes.c_uint64),
    ("stop_grace_ms", ctypes.c_uint64),
]
gf_hosted_input_report._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("connected", ctypes.c_uint32),
    ("dropped", ctypes.c_uint64),
]
gf_content_text_line._fields_ = [
    ("start", ctypes.c_uint64),
    ("end", ctypes.c_uint64),
    ("bounds", gf_logical_rect),
]
gf_content_text_cluster._fields_ = [
    ("start", ctypes.c_uint64),
    ("end", ctypes.c_uint64),
    ("line", ctypes.c_uint32),
    ("right_to_left", ctypes.c_uint32),
    ("bounds", gf_logical_rect),
]
gf_content_caret_stop._fields_ = [
    ("offset", ctypes.c_uint64),
    ("caret", gf_logical_rect),
]
gf_content_layout_transform._fields_ = [
    ("xx", ctypes.c_double),
    ("xy", ctypes.c_double),
    ("yx", ctypes.c_double),
    ("yy", ctypes.c_double),
    ("dx", ctypes.c_double),
    ("dy", ctypes.c_double),
]
gf_content_quad._fields_ = [
    ("top_left", gf_logical_point),
    ("top_right", gf_logical_point),
    ("bottom_right", gf_logical_point),
    ("bottom_left", gf_logical_point),
]
gf_content_text_layout._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("text_revision", ctypes.c_uint64),
    ("lines", ctypes.POINTER(gf_content_text_line)),
    ("line_count", ctypes.c_uint64),
    ("clusters", ctypes.POINTER(gf_content_text_cluster)),
    ("cluster_count", ctypes.c_uint64),
    ("carets", ctypes.POINTER(gf_content_caret_stop)),
    ("caret_count", ctypes.c_uint64),
    ("transformed", ctypes.c_uint32),
    ("transform_reserved", ctypes.c_uint32),
    ("transform", gf_content_layout_transform),
]
gf_content_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("open_content", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.POINTER(gf_content_sink))),
    ("close_content", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("start_program", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_program))),
    ("start_hosted", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_hosted_options))),
    ("terminate", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("set_termination_grace", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64)),
    ("set_stale_interval", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64)),
    ("status", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_status))),
    ("failure", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("statistics", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_statistics))),
    ("request", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_request))),
    ("set_status_caption", ctypes.CFUNCTYPE(gf_status, gf_object, gf_content_status, gf_utf8_view)),
    ("set_semantics", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_semantics))),
    ("program_running", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("hosted_input", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_hosted_input_report))),
    ("hosted_support", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_hosted_support))),
    ("sink_publish", ctypes.CFUNCTYPE(gf_status, gf_content_sink, ctypes.POINTER(gf_content_frame), ctypes.POINTER(gf_content_publish_result))),
    ("sink_heartbeat", ctypes.CFUNCTYPE(gf_status, gf_content_sink)),
    ("sink_publish_semantics", ctypes.CFUNCTYPE(gf_status, gf_content_sink, ctypes.POINTER(gf_content_semantics), ctypes.POINTER(gf_content_semantics_result))),
    ("sink_request", ctypes.CFUNCTYPE(gf_status, gf_content_sink, ctypes.POINTER(gf_content_request))),
    ("sink_wait_for_request", ctypes.CFUNCTYPE(gf_status, gf_content_sink, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(gf_content_request))),
    ("sink_state", ctypes.CFUNCTYPE(gf_status, gf_content_sink, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32))),
    ("sink_statistics", ctypes.CFUNCTYPE(gf_status, gf_content_sink, ctypes.POINTER(gf_content_statistics))),
    ("sink_release", ctypes.CFUNCTYPE(gf_status, gf_content_sink)),
    ("program_sink", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_content_sink))),
    ("program_fail", ctypes.CFUNCTYPE(gf_status, gf_utf8_view)),
    ("editor_text_revision", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("editor_text", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("editor_set_text", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view)),
    ("editor_submit_layout", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_text_layout), ctypes.POINTER(gf_content_layout_result))),
    ("editor_layout_current", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("editor_open_frames", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.POINTER(gf_content_sink))),
    ("editor_caret_rectangle", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(gf_logical_rect))),
    ("editor_selection_rectangles", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_logical_rect), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("editor_position_at", ctypes.CFUNCTYPE(gf_status, gf_object, gf_logical_point, ctypes.POINTER(ctypes.c_uint64))),
    ("editor_set_draws_selection", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("editor_set_multiline", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("editor_set_read_only", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("editor_set_accepts_tab", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32)),
    ("editor_replace_selection", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint32))),
    ("editor_delete_selection", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32))),
    ("editor_composition_range", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint64))),
    ("editor_caret_quad", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(gf_content_quad))),
    ("editor_selection_quads", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_quad), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("editor_composition_quads", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_content_quad), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
]
gf_list_view_column._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("alignment", gf_list_view_alignment),
    ("width", ctypes.c_double),
    ("stable_id", gf_utf8_view),
    ("text", gf_utf8_view),
]
gf_list_view_item._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("checked", ctypes.c_uint32),
    ("stable_id", gf_utf8_view),
    ("text", gf_utf8_view),
    ("image_key", gf_utf8_view),
    ("group", gf_utf8_view),
    ("sub_items", ctypes.POINTER(gf_utf8_view)),
    ("sub_item_count", ctypes.c_uint64),
]
gf_list_view_group._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("header_alignment", gf_list_view_alignment),
    ("stable_id", gf_utf8_view),
    ("header", gf_utf8_view),
]
gf_list_view_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("column_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("column_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_list_view_column), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_columns", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_list_view_column), ctypes.c_uint64)),
    ("set_column_width", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_double)),
    ("item_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("item_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_list_view_item), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("item_sub_item", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_items", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_list_view_item), ctypes.c_uint64)),
    ("index_of", ctypes.CFUNCTYPE(gf_status, gf_object, gf_utf8_view, ctypes.POINTER(ctypes.c_uint64))),
    ("set_item_checked", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint32)),
    ("group_count", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64))),
    ("group_at", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.POINTER(gf_list_view_group), ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_groups", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(gf_list_view_group), ctypes.c_uint64)),
    ("selected_items", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("set_selected", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, ctypes.c_uint32)),
    ("select_all", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("clear_selection", ctypes.CFUNCTYPE(gf_status, gf_object)),
    ("focused_item", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.POINTER(ctypes.c_int64))),
    ("set_focused_item", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_int64)),
    ("ensure_visible", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64)),
    ("set_sort_indicator", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_int64, gf_list_view_sort_order)),
    ("sort_items", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint64, gf_list_view_sort_order)),
]
gf_windows_paint_endpoint_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("acquire", ctypes.CFUNCTYPE(gf_status, gf_object, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(gf_paint_endpoint), ctypes.POINTER(ctypes.c_uint64))),
    ("configure", ctypes.CFUNCTYPE(gf_status, gf_paint_endpoint, ctypes.c_uint32, ctypes.c_uint32)),
    ("touch", ctypes.CFUNCTYPE(gf_status, gf_paint_endpoint, ctypes.c_uint32)),
    ("drain", ctypes.CFUNCTYPE(gf_status, gf_paint_endpoint)),
    ("snapshot", ctypes.CFUNCTYPE(gf_status, gf_paint_endpoint, ctypes.POINTER(ctypes.c_char), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("submit_bgra", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint8))),
    ("release", ctypes.CFUNCTYPE(gf_status, gf_paint_endpoint)),
    ("get_dc", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64))),
    ("release_dc", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.c_uint64)),
    ("publish_dc", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64)),
    ("begin_write", ctypes.CFUNCTYPE(gf_status, ctypes.c_uint64, ctypes.POINTER(gf_paint_write_lease))),
    ("end_write", ctypes.CFUNCTYPE(gf_status, gf_paint_write_lease, ctypes.c_uint32)),
]
gf_segment_header._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
]
gf_class_header._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("segment_count", ctypes.c_uint32),
    ("release", ctypes.CFUNCTYPE(None, ctypes.c_void_p)),
]
gf_control_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_auto_size_changed", gf_hook_entry),
    ("on_back_color_changed", gf_hook_entry),
    ("on_causes_validation_changed", gf_hook_entry),
    ("on_cursor_changed", gf_hook_entry),
    ("on_dock_changed", gf_hook_entry),
    ("on_enabled_changed", gf_hook_entry),
    ("on_fore_color_changed", gf_hook_entry),
    ("on_margin_changed", gf_hook_entry),
    ("on_padding_changed", gf_hook_entry),
    ("on_right_to_left_changed", gf_hook_entry),
    ("on_tab_index_changed", gf_hook_entry),
    ("on_tab_stop_changed", gf_hook_entry),
    ("on_visible_changed", gf_hook_entry),
    ("on_change_ui_cues", gf_hook_entry),
    ("on_click", gf_hook_entry),
    ("on_double_click", gf_hook_entry),
    ("on_drag_drop", gf_hook_entry),
    ("on_drag_enter", gf_hook_entry),
    ("on_drag_leave", gf_hook_entry),
    ("on_drag_over", gf_hook_entry),
    ("on_enter", gf_hook_entry),
    ("on_got_focus", gf_hook_entry),
    ("on_help_requested", gf_hook_entry),
    ("on_key_down", gf_hook_entry),
    ("on_key_press", gf_hook_entry),
    ("on_key_up", gf_hook_entry),
    ("on_layout", gf_hook_entry),
    ("on_leave", gf_hook_entry),
    ("on_lost_focus", gf_hook_entry),
    ("on_mouse_capture_changed", gf_hook_entry),
    ("on_mouse_click", gf_hook_entry),
    ("on_mouse_double_click", gf_hook_entry),
    ("on_mouse_down", gf_hook_entry),
    ("on_mouse_enter", gf_hook_entry),
    ("on_mouse_hover", gf_hook_entry),
    ("on_mouse_leave", gf_hook_entry),
    ("on_mouse_move", gf_hook_entry),
    ("on_mouse_up", gf_hook_entry),
    ("on_mouse_wheel", gf_hook_entry),
    ("on_paint_background", gf_hook_entry),
    ("on_preview_key_down", gf_hook_entry),
    ("on_validated", gf_hook_entry),
    ("on_validating", gf_hook_entry),
]
gf_masked_text_box_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_mask_changed", gf_hook_entry),
]
gf_picture_box_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_size_mode_changed", gf_hook_entry),
]
gf_combo_box_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_drop_down_style_changed", gf_hook_entry),
]
gf_data_grid_view_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_allow_user_to_delete_rows_changed", gf_hook_entry),
    ("on_allow_user_to_order_columns_changed", gf_hook_entry),
    ("on_allow_user_to_resize_columns_changed", gf_hook_entry),
    ("on_allow_user_to_resize_rows_changed", gf_hook_entry),
    ("on_alternating_rows_default_cell_style_changed", gf_hook_entry),
    ("on_auto_size_columns_mode_changed", gf_hook_entry),
    ("on_auto_size_rows_mode_changed", gf_hook_entry),
    ("on_background_color_changed", gf_hook_entry),
    ("on_border_style_changed", gf_hook_entry),
    ("on_cell_border_style_changed", gf_hook_entry),
    ("on_column_headers_border_style_changed", gf_hook_entry),
    ("on_column_headers_default_cell_style_changed", gf_hook_entry),
    ("on_column_headers_height_changed", gf_hook_entry),
    ("on_default_cell_style_changed", gf_hook_entry),
    ("on_edit_mode_changed", gf_hook_entry),
    ("on_grid_color_changed", gf_hook_entry),
    ("on_multi_select_changed", gf_hook_entry),
    ("on_read_only_changed", gf_hook_entry),
    ("on_row_headers_border_style_changed", gf_hook_entry),
    ("on_row_headers_default_cell_style_changed", gf_hook_entry),
    ("on_row_headers_width_changed", gf_hook_entry),
    ("on_rows_default_cell_style_changed", gf_hook_entry),
]
gf_check_box_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_appearance_changed", gf_hook_entry),
    ("on_checked_changed", gf_hook_entry),
    ("on_check_state_changed", gf_hook_entry),
]
gf_radio_button_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_checked_changed", gf_hook_entry),
]
gf_range_control_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_value_changed", gf_hook_entry),
]
gf_numeric_up_down_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_value_changed", gf_hook_entry),
]
gf_date_time_picker_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_format_changed", gf_hook_entry),
    ("on_value_changed", gf_hook_entry),
]
gf_node_canvas_hooks._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("class_id", gf_class_id),
    ("on_edit_ended", gf_hook_entry),
    ("on_graph_edited", gf_hook_entry),
    ("on_link_connected", gf_hook_entry),
    ("on_palette_requested", gf_hook_entry),
    ("on_selection_changed", gf_hook_entry),
    ("on_view_changed", gf_hook_entry),
]
gf_button_base_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_button_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_link_label_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_label_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_picture_box_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("picture_box", ctypes.POINTER(gf_picture_box_hooks)),
]
gf_progress_bar_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("range_control", ctypes.POINTER(gf_range_control_hooks)),
]
gf_sweep_scope_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("range_control", ctypes.POINTER(gf_range_control_hooks)),
]
gf_list_box_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_check_box_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("check_box", ctypes.POINTER(gf_check_box_hooks)),
]
gf_radio_button_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("radio_button", ctypes.POINTER(gf_radio_button_hooks)),
]
gf_range_control_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("range_control", ctypes.POINTER(gf_range_control_hooks)),
]
gf_track_bar_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("range_control", ctypes.POINTER(gf_range_control_hooks)),
]
gf_panel_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_group_box_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_material_panel_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_card_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_container_control_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_user_control_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_page_strip_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_page_view_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_navigation_pane_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_dock_site_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_dock_navigator_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_scaled_panel_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_scrollable_control_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_scroll_bar_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("range_control", ctypes.POINTER(gf_range_control_hooks)),
]
gf_tool_strip_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_gauge_base_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("range_control", ctypes.POINTER(gf_range_control_hooks)),
]
gf_dial_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("range_control", ctypes.POINTER(gf_range_control_hooks)),
]
gf_raster_canvas_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_text_box_base_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_list_control_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_up_down_base_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
]
gf_node_canvas_class._fields_ = [
    ("header", gf_class_header),
    ("control", ctypes.POINTER(gf_control_hooks)),
    ("node_canvas", ctypes.POINTER(gf_node_canvas_hooks)),
]
gf_classes_table._fields_ = [
    ("struct_size", ctypes.c_uint32),
    ("abi_minor", ctypes.c_uint32),
    ("create", ctypes.CFUNCTYPE(gf_status, ctypes.POINTER(gf_class_header), gf_utf8_view, ctypes.c_void_p, ctypes.POINTER(gf_object))),
    ("base_raiser", ctypes.CFUNCTYPE(gf_status, gf_class_id, ctypes.c_uint32, ctypes.POINTER(gf_base_raiser))),
]

# The one export, bound to a loaded library by bind_exports.


def bind_gf_abi_get_table(library):
    function = library.gf_abi_get_table
    function.restype = gf_status
    function.argtypes = [gf_table_id, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint64]
    return function


# Each function table's id for gf_abi_get_table.
TABLE_IDS = {
    "gf_runtime_table": GF_TABLE_RUNTIME,
    "gf_objects_table": GF_TABLE_OBJECTS,
    "gf_properties_table": GF_TABLE_PROPERTIES,
    "gf_events_table": GF_TABLE_EVENTS,
    "gf_dispatch_table": GF_TABLE_DISPATCH,
    "gf_windows_table": GF_TABLE_WINDOWS,
    "gf_schema_table": GF_TABLE_SCHEMA,
    "gf_themes_table": GF_TABLE_THEMES,
    "gf_host_table": GF_TABLE_HOST,
    "gf_diagnostics_table": GF_TABLE_DIAGNOSTICS,
    "gf_controls_table": GF_TABLE_CONTROLS,
    "gf_text_editing_table": GF_TABLE_TEXT_EDITING,
    "gf_overlays_table": GF_TABLE_OVERLAYS,
    "gf_property_grid_table": GF_TABLE_PROPERTY_GRID,
    "gf_custom_controls_table": GF_TABLE_CUSTOM_CONTROLS,
    "gf_bindings_table": GF_TABLE_BINDINGS,
    "gf_subsurfaces_table": GF_TABLE_SUBSURFACES,
    "gf_application_table": GF_TABLE_APPLICATION,
    "gf_rules_table": GF_TABLE_RULES,
    "gf_data_grid_table": GF_TABLE_DATA_GRID,
    "gf_docking_table": GF_TABLE_DOCKING,
    "gf_fonts_table": GF_TABLE_FONTS,
    "gf_help_table": GF_TABLE_HELP,
    "gf_content_table": GF_TABLE_CONTENT,
    "gf_list_view_table": GF_TABLE_LIST_VIEW,
    "gf_windows_paint_endpoint_table": GF_TABLE_WINDOWS_PAINT_ENDPOINT,
    "gf_classes_table": GF_TABLE_CLASSES,
}

# The manifest's size and field offsets of every record, for check_layout.
LAYOUT = {
    "gf_utf8_view": (16, (("data", 0), ("size", 8),)),
    "gf_abi_version_info": (24, (("struct_size", 0), ("abi_major", 4), ("abi_minor", 8), ("library_major", 12), ("library_minor", 16), ("library_patch", 20),)),
    "gf_error_detail": (24, (("struct_size", 0), ("status", 4), ("table_id", 8), ("slot_index", 12), ("message_size", 16),)),
    "gf_splashscreen_options": (48, (("struct_size", 0), ("show_progress", 4), ("artwork", 8), ("artwork_size", 16), ("status", 24), ("progress", 40),)),
    "gf_runtime_table": (64, (("struct_size", 0), ("abi_minor", 4), ("version", 8), ("error_detail", 16), ("clear_error", 24), ("splashscreen_show", 32), ("splashscreen_set_status", 40), ("splashscreen_set_progress", 48), ("splashscreen_close", 56),)),
    "gf_logical_point": (16, (("x", 0), ("y", 8),)),
    "gf_logical_size": (16, (("width", 0), ("height", 8),)),
    "gf_logical_rect": (32, (("x", 0), ("y", 8), ("width", 16), ("height", 24),)),
    "gf_logical_insets": (32, (("left", 0), ("top", 8), ("right", 16), ("bottom", 24),)),
    "gf_font": (32, (("role", 0), ("weight", 4), ("italic", 8), ("reserved", 12), ("size", 16), ("letter_spacing", 24),)),
    "gf_value": (200, (("struct_size", 0), ("kind", 4), ("boolean", 8), ("color", 12), ("signed_integer", 16), ("unsigned_integer", 24), ("number", 32), ("text", 40), ("point", 56), ("size", 72), ("rectangle", 88), ("insets", 120), ("font", 152), ("elements", 184), ("element_count", 192),)),
    "gf_event_field": (32, (("name", 0), ("kind", 16), ("flags", 20), ("value", 24),)),
    "gf_event": (56, (("struct_size", 0), ("cancel", 4), ("sender", 8), ("name", 16), ("payload", 32), ("field_count", 40), ("fields", 48),)),
    "gf_callback": (32, (("struct_size", 0), ("reserved", 4), ("invoke", 8), ("release", 16), ("context", 24),)),
    "gf_create_choice": (24, (("name", 0), ("value", 16),)),
    "gf_create_arguments": (56, (("struct_size", 0), ("flags", 4), ("owner", 8), ("enumeration", 16), ("choices", 32), ("choice_count", 40), ("value", 48),)),
    "gf_objects_table": (112, (("struct_size", 0), ("abi_minor", 4), ("create", 8), ("retain", 16), ("release", 24), ("dispose", 32), ("state", 40), ("type_id", 48), ("stable_id", 56), ("insert_child", 64), ("remove_child", 72), ("child_count", 80), ("child_at", 88), ("parent", 96), ("create_with", 104),)),
    "gf_properties_table": (64, (("struct_size", 0), ("abi_minor", 4), ("get", 8), ("set", 16), ("reset", 24), ("element_at", 32), ("read_elements", 40), ("get_at", 48), ("set_at", 56),)),
    "gf_events_table": (48, (("struct_size", 0), ("abi_minor", 4), ("subscribe", 8), ("subscribe_property", 16), ("disconnect", 24), ("write_field", 32), ("field_element", 40),)),
    "gf_dispatch_table": (24, (("struct_size", 0), ("abi_minor", 4), ("begin_invoke", 8), ("run_pending", 16),)),
    "gf_schema_interaction": (40, (("struct_size", 0), ("mutable_payload", 4), ("name", 8), ("payload", 24),)),
    "gf_run_options": (80, (("struct_size", 0), ("flags", 4), ("title", 8), ("width", 24), ("height", 32), ("ready", 40), ("closing", 48), ("closed", 56), ("minimum_width", 64), ("minimum_height", 72),)),
    "gf_owned_window_options": (72, (("struct_size", 0), ("flags", 4), ("title", 8), ("width", 24), ("height", 32), ("owner", 40), ("ready", 48), ("closing", 56), ("closed", 64),)),
    "gf_window_band_options": (56, (("struct_size", 0), ("flags", 4), ("full_screen", 8), ("reserved", 12), ("width", 16), ("edges", 24),)),
    "gf_window_band_appearance": (80, (("struct_size", 0), ("state", 4), ("flags", 8), ("lit_role", 12), ("rest_colour", 16), ("lit_colour", 20), ("frequency", 24), ("texture", 32), ("texture_kind", 36), ("texture_seed", 40), ("texture_primary", 44), ("texture_secondary", 48), ("reserved", 52), ("texture_tile", 56), ("texture_strength", 64), ("texture_opacity", 72),)),
    "gf_window_band_report": (72, (("struct_size", 0), ("status", 4), ("edges", 8), ("drawn_colour", 40), ("full_screen", 44), ("frequency", 48), ("flash_changes", 56), ("cycle_frames", 64),)),
    "gf_window_shaping": (32, (("struct_size", 0), ("flags", 4), ("preference", 8), ("corner_shapes", 12), ("corner_shape", 16), ("reserved", 20), ("corner_radius", 24),)),
    "gf_windows_table": (256, (("struct_size", 0), ("abi_minor", 4), ("run", 8), ("request_close", 16), ("create", 24), ("interaction_count", 32), ("interaction_at", 40), ("request_help", 48), ("key_state", 56), ("show_modal", 64), ("show_owned", 72), ("window_properties", 80), ("focused_control", 88), ("declare_band", 96), ("undeclare_band", 104), ("set_band_appearance", 112), ("band_report", 120), ("set_corner_preference", 128), ("content_rect", 136), ("shaping", 144), ("pointer_location", 152), ("show_business_card", 160), ("set_mdi_container", 168), ("mdi_container", 176), ("mdi_child_count", 184), ("mdi_child_at", 192), ("active_mdi_child", 200), ("activate_mdi_child", 208), ("layout_mdi", 216), ("set_mdi_children_minimized_anchor_bottom", 224), ("mdi_children_minimized_anchor_bottom", 232), ("set_main_menu_strip", 240), ("main_menu_strip", 248),)),
    "gf_schema_type": (88, (("struct_size", 0), ("kind", 4), ("id", 8), ("type_name", 24), ("part_count", 40), ("state_count", 48), ("custom_state_count", 56), ("item_system_count", 64), ("property_count", 72), ("interaction_count", 80),)),
    "gf_schema_item_system": (48, (("struct_size", 0), ("reserved", 4), ("name", 8), ("part_count", 24), ("state_count", 32), ("custom_state_count", 40),)),
    "gf_schema_part": (64, (("struct_size", 0), ("reserved", 4), ("name", 8), ("role", 24), ("composed_from", 40), ("state_count", 56),)),
    "gf_schema_property": (72, (("struct_size", 0), ("kind", 4), ("name", 8), ("category", 24), ("enumeration", 40), ("choice_count", 56), ("flags", 64), ("serialization", 68),)),
    "gf_schema_choice": (32, (("struct_size", 0), ("reserved", 4), ("name", 8), ("value", 24),)),
    "gf_schema_engine": (96, (("struct_size", 0), ("version_major", 4), ("version_minor", 8), ("reserved", 12), ("operations_per_device_pixel", 16), ("animated_operations_per_frame", 24), ("expression_maximum_operations", 32), ("expression_maximum_stack", 40), ("published_values_maximum", 48), ("transition_maximum_states", 56), ("transition_maximum_per_part", 64), ("ambient_maximum_frames_per_second", 72), ("ambient_maximum_window_fraction", 80), ("primitive_count", 88),)),
    "gf_schema_primitive": (104, (("struct_size", 0), ("introduced_major", 4), ("introduced_minor", 8), ("cost_per_device_pixel", 12), ("cost_fixed", 16), ("cost_preparation_per_device_pixel", 20), ("name", 24), ("outsets", 40), ("role_count", 72), ("state_read_count", 80), ("input_read_count", 88), ("parameter_count", 96),)),
    "gf_schema_parameter": (64, (("struct_size", 0), ("kind", 4), ("name", 8), ("minimum", 24), ("maximum", 32), ("default_number", 40), ("default_color", 48), ("animated", 52), ("choice_count", 56),)),
    "gf_schema_effect": (112, (("struct_size", 0), ("time_model", 4), ("name", 8), ("parent", 24), ("engine_version", 40), ("input", 44), ("cost_fixed", 48), ("cost_per_device_pixel", 52), ("setup_cost", 56), ("flags", 60), ("state_budget", 64), ("frames_per_second", 72), ("outsets", 80),)),
    "gf_schema_composite": (128, (("struct_size", 0), ("reserved", 4), ("composite", 8), ("id", 16), ("name", 32), ("version", 48), ("slot", 64), ("part_count", 80), ("state_count", 88), ("custom_state_count", 96), ("property_count", 104), ("event_count", 112), ("command_count", 120),)),
    "gf_schema_table": (256, (("struct_size", 0), ("abi_minor", 4), ("vocabulary_count", 8), ("vocabulary_at", 16), ("type_count", 24), ("find_type", 32), ("type_at", 40), ("item_system_at", 48), ("part_at", 56), ("state_at", 64), ("custom_state_at", 72), ("property_at", 80), ("choice_at", 88), ("interaction_at", 96), ("engine", 104), ("primitive_at", 112), ("primitive_name_at", 120), ("parameter_at", 128), ("parameter_choice_at", 136), ("effect_count", 144), ("effect_at", 152), ("child_property_count", 160), ("child_property_at", 168), ("child_choice_at", 176), ("composite_count", 184), ("composite_at", 192), ("composite_part_at", 200), ("composite_state_at", 208), ("composite_custom_state_at", 216), ("composite_property_at", 224), ("composite_choice_at", 232), ("composite_event_at", 240), ("composite_command_at", 248),)),
    "gf_bytes_view": (16, (("data", 0), ("size", 8),)),
    "gf_theme_file": (32, (("path", 0), ("bytes", 16),)),
    "gf_theme_package": (40, (("struct_size", 0), ("reserved", 4), ("manifest", 8), ("files", 24), ("file_count", 32),)),
    "gf_theme_report": (16, (("struct_size", 0), ("outcome", 4), ("diagnostic_count", 8),)),
    "gf_theme_diagnostic": (16, (("struct_size", 0), ("severity", 4), ("line", 8), ("column", 12),)),
    "gf_themes_table": (136, (("struct_size", 0), ("abi_minor", 4), ("load", 8), ("reset", 16), ("install", 24), ("remove", 32), ("diagnostic_at", 40), ("diagnostic_text", 48), ("theme_id", 56), ("publish_value", 64), ("withdraw_value", 72), ("published_value", 80), ("load_image", 88), ("remove_image", 96), ("load_pixels", 104), ("load_sheet", 112), ("set_user_theme_policy", 120), ("theme_request", 128),)),
    "gf_host_capabilities": (32, (("struct_size", 0), ("protocol_version", 4), ("available", 8), ("transient_surfaces", 16), ("reserved", 20), ("window_corner_shapes", 24), ("window_band_maximum_width", 28),)),
    "gf_file_filter": (32, (("label", 0), ("extensions", 16), ("extension_count", 24),)),
    "gf_dialog_request": (144, (("struct_size", 0), ("kind", 4), ("title", 8), ("message", 24), ("initial_directory", 40), ("suggested_name", 56), ("default_extension", 72), ("filters", 88), ("filter_count", 96), ("initial_filter", 104), ("buttons", 112), ("icon", 116), ("default_choice", 120), ("flags", 124), ("initial_rgba", 128), ("reserved", 132), ("owner", 136),)),
    "gf_dialog_result": (32, (("struct_size", 0), ("outcome", 4), ("choice", 8), ("rgba", 12), ("path_count", 16), ("chosen_filter", 24),)),
    "gf_host_table": (64, (("struct_size", 0), ("abi_minor", 4), ("capabilities", 8), ("platform_name", 16), ("set_cursor", 24), ("read_clipboard_text", 32), ("write_clipboard_text", 40), ("show_dialog", 48), ("dialog_path_at", 56),)),
    "gf_shadow_frame": (112, (("kind", 0), ("flags", 4), ("table_id", 8), ("slot_index", 12), ("sequence", 16), ("subject_size", 24), ("name_size", 28), ("subject", 32), ("name", 80),)),
    "gf_shadow_stack_info": (24, (("struct_size", 0), ("depth", 4), ("pushed", 8), ("dropped", 16),)),
    "gf_failure_snapshot": (104, (("struct_size", 0), ("status", 4), ("table_id", 8), ("slot_index", 12), ("sequence", 16), ("frame_count", 24), ("depth", 28), ("site_size", 32), ("message_size", 36), ("site", 40),)),
    "gf_failure_detail": (544, (("struct_size", 0), ("status", 4), ("sequence", 8), ("type_size", 16), ("trace_count", 20), ("type", 24), ("trace", 280), ("flags", 536), ("reserved", 540),)),
    "gf_diagnostics_table": (96, (("struct_size", 0), ("abi_minor", 4), ("shadow_frames", 8), ("set_invalidation_overlay", 16), ("invalidation_overlay", 24), ("failure_snapshot", 32), ("clear_failure_snapshot", 40), ("set_exception_reflection", 48), ("exception_reflection", 56), ("raise_native_exception", 64), ("failure_detail", 72), ("set_diagnostic_overlay", 80), ("toggle_diagnostic_overlay", 88),)),
    "gf_layout_transaction": (32, (("struct_size", 0), ("suspend_depth", 4), ("deferred", 8), ("reserved", 12), ("requested_revision", 16), ("committed_revision", 24),)),
    "gf_scroll_axis": (48, (("enabled", 0), ("visible", 4), ("minimum", 8), ("maximum", 16), ("large_change", 24), ("small_change", 32), ("value", 40),)),
    "gf_scroll_snapshot": (248, (("struct_size", 0), ("auto_scroll", 4), ("position", 8), ("margin", 24), ("minimum_content_size", 40), ("display_rectangle", 56), ("viewport_rectangle", 88), ("horizontal", 120), ("vertical", 168), ("event_revision", 216), ("event_type", 224), ("event_orientation", 228), ("event_old_value", 232), ("event_new_value", 240),)),
    "gf_relative_pointer_request": (24, (("struct_size", 0), ("mode", 4), ("hide_cursor", 8), ("raw_motion", 12), ("until_release", 16), ("reserved", 20),)),
    "gf_relative_pointer_grant": (24, (("struct_size", 0), ("result", 4), ("mode", 8), ("raw", 12), ("cursor_hidden", 16), ("host_relative", 20),)),
    "gf_relative_pointer_state": (96, (("struct_size", 0), ("owned", 4), ("active", 8), ("suspended", 12), ("mode", 16), ("raw", 20), ("host_relative", 24), ("last_end", 28), ("grants", 32), ("samples", 40), ("suspensions", 48), ("resumptions", 56), ("ends", 64), ("support_relative_motion", 72), ("support_raw_motion", 76), ("support_lock", 80), ("support_confine", 84), ("support_warp", 88), ("reserved", 92),)),
    "gf_effect_mask_layer": (56, (("struct_size", 0), ("mode", 4), ("composite", 8), ("start_rgba", 12), ("end_rgba", 16), ("reserved", 20), ("start", 24), ("end", 40),)),
    "gf_content_effect": (1216, (("struct_size", 0), ("has_colour_matrix", 4), ("has_colour_table", 8), ("mask_count", 12), ("colour_matrix", 16), ("colour_table", 176), ("blur", 1200), ("masks", 1208),)),
    "gf_controls_table": (160, (("struct_size", 0), ("abi_minor", 4), ("suspend_layout", 8), ("resume_layout", 16), ("perform_layout", 24), ("layout_state", 32), ("window_bounds", 40), ("set_pointer_capture", 48), ("pointer_capture", 56), ("scroll_state", 64), ("set_scroll_axis", 72), ("scroll_into_view", 80), ("invalidate", 88), ("focus", 96), ("focus_state", 104), ("request_relative_pointer", 112), ("release_relative_pointer", 120), ("relative_pointer_state", 128), ("warp_pointer", 136), ("set_pointer_release_regions", 144), ("set_content_effect", 152),)),
    "gf_text_decoration": (56, (("start", 0), ("end", 8), ("fields", 16), ("ink", 20), ("foreground", 24), ("weight", 28), ("italic", 32), ("underline", 36), ("underline_color", 40), ("background", 44), ("tag", 48), ("reserved", 52),)),
    "gf_text_editing_table": (120, (("struct_size", 0), ("abi_minor", 4), ("select", 8), ("selection", 16), ("grapheme_boundary", 24), ("replace_range", 32), ("undo", 40), ("redo", 48), ("clear_undo_history", 56), ("set_decorations", 64), ("replace_decorations", 72), ("clear_decorations", 80), ("decoration_count", 88), ("decoration_at", 96), ("utf8_to_utf16_offset", 104), ("utf16_to_utf8_offset", 112),)),
    "gf_anchored_overlay_options": (40, (("struct_size", 0), ("flags", 4), ("width", 8), ("height", 16), ("gap", 24), ("events", 32),)),
    "gf_overlays_table": (80, (("struct_size", 0), ("abi_minor", 4), ("open_overlay", 8), ("close_overlay", 16), ("set_tool_tip", 24), ("show_tool_tip", 32), ("hide_tool_tip", 40), ("open_anchored", 48), ("close_anchored", 56), ("set_tool_tips_shown", 64), ("tool_tips_shown", 72),)),
    "gf_property_grid_table": (48, (("struct_size", 0), ("abi_minor", 4), ("select_objects", 8), ("refresh", 16), ("try_set_text", 24), ("reset_property", 32), ("activate_editor", 40),)),
    "gf_custom_property": (96, (("name", 0), ("category", 16), ("description", 32), ("kind", 48), ("flags", 52), ("default_value", 56), ("enumeration", 64), ("choices", 80), ("choice_count", 88),)),
    "gf_paint_target": (72, (("struct_size", 0), ("width", 4), ("height", 8), ("reserved", 12), ("row_bytes", 16), ("pixels", 24), ("scale", 32), ("damage", 40),)),
    "gf_custom_semantics": (56, (("struct_size", 0), ("role", 4), ("name", 8), ("value", 24), ("description", 40),)),
    "gf_custom_control_callbacks": (48, (("struct_size", 0), ("reserved", 4), ("context", 8), ("paint", 16), ("get_property", 24), ("set_property", 32), ("release", 40),)),
    "gf_custom_layout_callbacks": (32, (("struct_size", 0), ("reserved", 4), ("measure", 8), ("hit_test", 16), ("semantics", 24),)),
    "gf_custom_control_spec": (88, (("struct_size", 0), ("base", 4), ("flags", 8), ("property_size", 12), ("properties", 16), ("property_count", 24), ("callbacks", 32), ("layout", 80),)),
    "gf_composite_spec": (56, (("struct_size", 0), ("reserved", 4), ("file", 8), ("document", 24), ("child_types", 40), ("child_type_count", 48),)),
    "gf_custom_controls_table": (56, (("struct_size", 0), ("abi_minor", 4), ("create", 8), ("notify_changed", 16), ("load_composite", 24), ("create_composite", 32), ("perform_composite", 40), ("composite_child", 48),)),
    "gf_binding_arguments": (96, (("struct_size", 0), ("source_update_mode", 4), ("control_update_mode", 8), ("formatting_enabled", 12), ("target", 16), ("source", 24), ("property", 32), ("data_member", 48), ("format_string", 64), ("null_value", 80), ("source_null_value", 88),)),
    "gf_binding_field": (24, (("name", 0), ("value", 16),)),
    "gf_binding_record": (40, (("struct_size", 0), ("editable", 4), ("stable_id", 8), ("fields", 24), ("field_count", 32),)),
    "gf_binding_column": (32, (("struct_size", 0), ("kind", 4), ("name", 8), ("read_only", 24), ("reserved", 28),)),
    "gf_binding_sort_key": (24, (("struct_size", 0), ("direction", 4), ("column", 8),)),
    "gf_binding_predicate": (32, (("struct_size", 0), ("op", 4), ("column", 8), ("operand", 24),)),
    "gf_binding_provider_callbacks": (96, (("struct_size", 0), ("flags", 4), ("context", 8), ("row_count", 16), ("read_value", 24), ("read_stable_id", 32), ("write_value", 40), ("read_cell_state", 48), ("apply_sort", 56), ("apply_filter", 64), ("insert_row", 72), ("remove_rows", 80), ("release", 88),)),
    "gf_bindings_table": (160, (("struct_size", 0), ("abi_minor", 4), ("bind", 8), ("unbind", 16), ("read_value", 24), ("write_value", 32), ("add_record", 40), ("insert_record", 48), ("remove_record", 56), ("clear_records", 64), ("set_position", 72), ("position", 80), ("current_field", 88), ("set_current_field", 96), ("add_records", 104), ("set_provider", 112), ("notify", 120), ("set_sort", 128), ("set_filter", 136), ("generation", 144), ("read_cell", 152),)),
    "gf_subsurface_content": (40, (("struct_size", 0), ("opaque", 4), ("build", 8),)),
    "gf_subsurfaces_table": (48, (("struct_size", 0), ("abi_minor", 4), ("set_content", 8), ("set_root", 16), ("state", 24), ("content_epoch", 32), ("failure", 40),)),
    "gf_application_config": (32, (("struct_size", 0), ("theme_base", 4), ("packages", 8), ("package_count", 16), ("presentation_source", 24), ("reserved", 28),)),
    "gf_program_identity": (104, (("struct_size", 0), ("reserved", 4), ("product", 8), ("version", 24), ("vendor", 40), ("website", 56), ("copyright", 72), ("credits", 88),)),
    "gf_application_table": (40, (("struct_size", 0), ("abi_minor", 4), ("create", 8), ("close", 16), ("state", 24), ("set_program_identity", 32),)),
    "gf_rule_condition": (32, (("struct_size", 0), ("kind", 4), ("object", 8), ("physical_key", 16), ("modifiers", 20), ("negated", 24), ("reserved", 28),)),
    "gf_rule_action": (48, (("struct_size", 0), ("kind", 4), ("target", 8), ("property", 16), ("value", 32), ("callback", 40),)),
    "gf_rule": (72, (("struct_size", 0), ("flags", 4), ("trigger", 8), ("physical_key", 12), ("source", 16), ("interaction", 24), ("condition_count", 40), ("conditions", 48), ("action_count", 56), ("actions", 64),)),
    "gf_rules_table": (32, (("struct_size", 0), ("abi_minor", 4), ("add", 8), ("remove", 16), ("state", 24),)),
    "gf_data_grid_column": (104, (("struct_size", 0), ("kind", 4), ("value_kind", 8), ("read_only", 12), ("hidden", 16), ("reserved", 20), ("width", 24), ("minimum_width", 32), ("name", 40), ("header_text", 56), ("data_property_name", 72), ("items", 88), ("item_count", 96),)),
    "gf_data_grid_row": (56, (("struct_size", 0), ("read_only", 4), ("stable_id", 8), ("header_text", 24), ("cells", 40), ("cell_count", 48),)),
    "gf_data_grid_cell": (16, (("row", 0), ("column", 8),)),
    "gf_data_grid_table": (272, (("struct_size", 0), ("abi_minor", 4), ("column_count", 8), ("column_at", 16), ("column_item", 24), ("insert_column", 32), ("remove_column", 40), ("column_index", 48), ("set_column_header_text", 56), ("set_column_width", 64), ("set_column_read_only", 72), ("set_column_hidden", 80), ("row_count", 88), ("insert_rows", 96), ("append_rows", 104), ("erase_rows", 112), ("replace_row", 120), ("clear_rows", 128), ("row_id", 136), ("row_position", 144), ("cell_value", 152), ("set_cell_value", 160), ("cell_text", 168), ("read_cells", 176), ("current_cell", 184), ("set_current_cell", 192), ("selected_rows", 200), ("selected_cells", 208), ("set_row_selected", 216), ("set_cell_selected", 224), ("clear_selection", 232), ("select_all", 240), ("begin_edit", 248), ("end_edit", 256), ("cancel_edit", 264),)),
    "gf_dock_panel": (136, (("struct_size", 0), ("kind", 4), ("allowed", 8), ("dock_as_document", 12), ("default_placement", 16), ("default_side", 20), ("default_ratio", 24), ("default_extent", 32), ("default_frame", 40), ("minimum_size", 72), ("id", 88), ("title", 104), ("content", 120), ("reserved", 128),)),
    "gf_dock_edit": (112, (("struct_size", 0), ("kind", 4), ("subject_is_stack", 8), ("subject_stack", 12), ("target_node", 16), ("site", 20), ("side", 24), ("index", 28), ("ratio", 32), ("extent", 40), ("frame", 48), ("panel", 80), ("reserved", 96), ("presentation", 104), ("frame_state", 108),)),
    "gf_dock_location": (40, (("struct_size", 0), ("placement", 4), ("stack", 8), ("index", 12), ("site", 16), ("stack_kind", 20), ("side", 24), ("selected", 28), ("stack_panel_count", 32), ("reserved", 36),)),
    "gf_dock_options": (16, (("struct_size", 0), ("flags", 4), ("area_background", 8), ("reserved", 12),)),
    "gf_dock_frame_memory": (56, (("struct_size", 0), ("present", 4), ("bounds", 8), ("state", 40), ("icon_slot", 44), ("order", 48), ("reserved", 52),)),
    "gf_docking_table": (208, (("struct_size", 0), ("abi_minor", 4), ("register_panel", 8), ("set_panel_content", 16), ("set_panel_title", 24), ("apply_edit", 32), ("locate", 40), ("save_layout", 48), ("load_layout", 56), ("activate_panel", 64), ("attach_windows", 72), ("document_area", 80), ("panel_at", 88), ("floating_sites", 96), ("floating_site", 104), ("update_panel", 112), ("set_options", 120), ("set_floating_window_visibility", 128), ("document_presentation", 136), ("arrange_frames", 144), ("frame_memory", 152), ("set_frame_icons_at_bottom", 160), ("area_document_count", 168), ("area_document_at", 176), ("area_active_document", 184), ("set_panel_menu_strip", 192), ("merged_document", 200),)),
    "gf_app_font_face": (32, (("struct_size", 0), ("reserved", 4), ("weight", 8), ("italic", 12), ("bytes", 16),)),
    "gf_fonts_table": (40, (("struct_size", 0), ("abi_minor", 4), ("family_id", 8), ("family_name", 16), ("load_family", 24), ("unload_family", 32),)),
    "gf_help_table": (128, (("struct_size", 0), ("abi_minor", 4), ("attach", 8), ("detach", 16), ("load_built_in", 24), ("show", 32), ("show_navigator", 40), ("show_popup", 48), ("resolve", 56), ("enter_help_mode", 64), ("cancel_help_mode", 72), ("load_translation", 80), ("load_user_overrides", 88), ("clear_user_overrides", 96), ("use_built_in_language", 104), ("export_template", 112), ("read_field", 120),)),
    "gf_content_pixel_rect": (16, (("x", 0), ("y", 4), ("width", 8), ("height", 12),)),
    "gf_content_frame": (64, (("struct_size", 0), ("pixel_format", 4), ("width", 8), ("height", 12), ("row_bytes", 16), ("opaque", 24), ("reserved", 28), ("damage", 32), ("pixels", 48),)),
    "gf_content_request": (32, (("struct_size", 0), ("width", 4), ("height", 8), ("reserved", 12), ("scale", 16), ("generation", 24),)),
    "gf_content_semantics": (56, (("struct_size", 0), ("reserved", 4), ("name", 8), ("text", 24), ("description", 40),)),
    "gf_content_statistics": (80, (("struct_size", 0), ("last_refusal", 4), ("frames_published", 8), ("frames_refused", 16), ("frames_dropped", 24), ("heartbeats", 32), ("stale_transitions", 40), ("recoveries", 48), ("semantics_published", 56), ("semantics_refused", 64), ("after_revocation", 72),)),
    "gf_content_program": (40, (("struct_size", 0), ("opaque", 4), ("run", 8),)),
    "gf_hosted_options": (64, (("struct_size", 0), ("opaque", 4), ("executable", 8), ("arguments", 24), ("argument_count", 32), ("slot_bytes", 40), ("start_timeout_ms", 48), ("stop_grace_ms", 56),)),
    "gf_hosted_input_report": (16, (("struct_size", 0), ("connected", 4), ("dropped", 8),)),
    "gf_content_text_line": (48, (("start", 0), ("end", 8), ("bounds", 16),)),
    "gf_content_text_cluster": (56, (("start", 0), ("end", 8), ("line", 16), ("right_to_left", 20), ("bounds", 24),)),
    "gf_content_caret_stop": (40, (("offset", 0), ("caret", 8),)),
    "gf_content_layout_transform": (48, (("xx", 0), ("xy", 8), ("yx", 16), ("yy", 24), ("dx", 32), ("dy", 40),)),
    "gf_content_quad": (64, (("top_left", 0), ("top_right", 16), ("bottom_right", 32), ("bottom_left", 48),)),
    "gf_content_text_layout": (120, (("struct_size", 0), ("reserved", 4), ("text_revision", 8), ("lines", 16), ("line_count", 24), ("clusters", 32), ("cluster_count", 40), ("carets", 48), ("caret_count", 56), ("transformed", 64), ("transform_reserved", 68), ("transform", 72),)),
    "gf_content_table": (368, (("struct_size", 0), ("abi_minor", 4), ("open_content", 8), ("close_content", 16), ("start_program", 24), ("start_hosted", 32), ("terminate", 40), ("set_termination_grace", 48), ("set_stale_interval", 56), ("status", 64), ("failure", 72), ("statistics", 80), ("request", 88), ("set_status_caption", 96), ("set_semantics", 104), ("program_running", 112), ("hosted_input", 120), ("hosted_support", 128), ("sink_publish", 136), ("sink_heartbeat", 144), ("sink_publish_semantics", 152), ("sink_request", 160), ("sink_wait_for_request", 168), ("sink_state", 176), ("sink_statistics", 184), ("sink_release", 192), ("program_sink", 200), ("program_fail", 208), ("editor_text_revision", 216), ("editor_text", 224), ("editor_set_text", 232), ("editor_submit_layout", 240), ("editor_layout_current", 248), ("editor_open_frames", 256), ("editor_caret_rectangle", 264), ("editor_selection_rectangles", 272), ("editor_position_at", 280), ("editor_set_draws_selection", 288), ("editor_set_multiline", 296), ("editor_set_read_only", 304), ("editor_set_accepts_tab", 312), ("editor_replace_selection", 320), ("editor_delete_selection", 328), ("editor_composition_range", 336), ("editor_caret_quad", 344), ("editor_selection_quads", 352), ("editor_composition_quads", 360),)),
    "gf_list_view_column": (48, (("struct_size", 0), ("alignment", 4), ("width", 8), ("stable_id", 16), ("text", 32),)),
    "gf_list_view_item": (88, (("struct_size", 0), ("checked", 4), ("stable_id", 8), ("text", 24), ("image_key", 40), ("group", 56), ("sub_items", 72), ("sub_item_count", 80),)),
    "gf_list_view_group": (40, (("struct_size", 0), ("header_alignment", 4), ("stable_id", 8), ("header", 24),)),
    "gf_list_view_table": (184, (("struct_size", 0), ("abi_minor", 4), ("column_count", 8), ("column_at", 16), ("set_columns", 24), ("set_column_width", 32), ("item_count", 40), ("item_at", 48), ("item_sub_item", 56), ("set_items", 64), ("index_of", 72), ("set_item_checked", 80), ("group_count", 88), ("group_at", 96), ("set_groups", 104), ("selected_items", 112), ("set_selected", 120), ("select_all", 128), ("clear_selection", 136), ("focused_item", 144), ("set_focused_item", 152), ("ensure_visible", 160), ("set_sort_indicator", 168), ("sort_items", 176),)),
    "gf_windows_paint_endpoint_table": (104, (("struct_size", 0), ("abi_minor", 4), ("acquire", 8), ("configure", 16), ("touch", 24), ("drain", 32), ("snapshot", 40), ("submit_bgra", 48), ("release", 56), ("get_dc", 64), ("release_dc", 72), ("publish_dc", 80), ("begin_write", 88), ("end_write", 96),)),
    "gf_segment_header": (8, (("struct_size", 0), ("class_id", 4),)),
    "gf_class_header": (24, (("struct_size", 0), ("abi_minor", 4), ("class_id", 8), ("segment_count", 12), ("release", 16),)),
    "gf_control_hooks": (352, (("struct_size", 0), ("class_id", 4), ("on_auto_size_changed", 8), ("on_back_color_changed", 16), ("on_causes_validation_changed", 24), ("on_cursor_changed", 32), ("on_dock_changed", 40), ("on_enabled_changed", 48), ("on_fore_color_changed", 56), ("on_margin_changed", 64), ("on_padding_changed", 72), ("on_right_to_left_changed", 80), ("on_tab_index_changed", 88), ("on_tab_stop_changed", 96), ("on_visible_changed", 104), ("on_change_ui_cues", 112), ("on_click", 120), ("on_double_click", 128), ("on_drag_drop", 136), ("on_drag_enter", 144), ("on_drag_leave", 152), ("on_drag_over", 160), ("on_enter", 168), ("on_got_focus", 176), ("on_help_requested", 184), ("on_key_down", 192), ("on_key_press", 200), ("on_key_up", 208), ("on_layout", 216), ("on_leave", 224), ("on_lost_focus", 232), ("on_mouse_capture_changed", 240), ("on_mouse_click", 248), ("on_mouse_double_click", 256), ("on_mouse_down", 264), ("on_mouse_enter", 272), ("on_mouse_hover", 280), ("on_mouse_leave", 288), ("on_mouse_move", 296), ("on_mouse_up", 304), ("on_mouse_wheel", 312), ("on_paint_background", 320), ("on_preview_key_down", 328), ("on_validated", 336), ("on_validating", 344),)),
    "gf_masked_text_box_hooks": (16, (("struct_size", 0), ("class_id", 4), ("on_mask_changed", 8),)),
    "gf_picture_box_hooks": (16, (("struct_size", 0), ("class_id", 4), ("on_size_mode_changed", 8),)),
    "gf_combo_box_hooks": (16, (("struct_size", 0), ("class_id", 4), ("on_drop_down_style_changed", 8),)),
    "gf_data_grid_view_hooks": (184, (("struct_size", 0), ("class_id", 4), ("on_allow_user_to_delete_rows_changed", 8), ("on_allow_user_to_order_columns_changed", 16), ("on_allow_user_to_resize_columns_changed", 24), ("on_allow_user_to_resize_rows_changed", 32), ("on_alternating_rows_default_cell_style_changed", 40), ("on_auto_size_columns_mode_changed", 48), ("on_auto_size_rows_mode_changed", 56), ("on_background_color_changed", 64), ("on_border_style_changed", 72), ("on_cell_border_style_changed", 80), ("on_column_headers_border_style_changed", 88), ("on_column_headers_default_cell_style_changed", 96), ("on_column_headers_height_changed", 104), ("on_default_cell_style_changed", 112), ("on_edit_mode_changed", 120), ("on_grid_color_changed", 128), ("on_multi_select_changed", 136), ("on_read_only_changed", 144), ("on_row_headers_border_style_changed", 152), ("on_row_headers_default_cell_style_changed", 160), ("on_row_headers_width_changed", 168), ("on_rows_default_cell_style_changed", 176),)),
    "gf_check_box_hooks": (32, (("struct_size", 0), ("class_id", 4), ("on_appearance_changed", 8), ("on_checked_changed", 16), ("on_check_state_changed", 24),)),
    "gf_radio_button_hooks": (16, (("struct_size", 0), ("class_id", 4), ("on_checked_changed", 8),)),
    "gf_range_control_hooks": (16, (("struct_size", 0), ("class_id", 4), ("on_value_changed", 8),)),
    "gf_numeric_up_down_hooks": (16, (("struct_size", 0), ("class_id", 4), ("on_value_changed", 8),)),
    "gf_date_time_picker_hooks": (24, (("struct_size", 0), ("class_id", 4), ("on_format_changed", 8), ("on_value_changed", 16),)),
    "gf_node_canvas_hooks": (56, (("struct_size", 0), ("class_id", 4), ("on_edit_ended", 8), ("on_graph_edited", 16), ("on_link_connected", 24), ("on_palette_requested", 32), ("on_selection_changed", 40), ("on_view_changed", 48),)),
    "gf_button_base_class": (32, (("header", 0), ("control", 24),)),
    "gf_button_class": (32, (("header", 0), ("control", 24),)),
    "gf_link_label_class": (32, (("header", 0), ("control", 24),)),
    "gf_label_class": (32, (("header", 0), ("control", 24),)),
    "gf_picture_box_class": (40, (("header", 0), ("control", 24), ("picture_box", 32),)),
    "gf_progress_bar_class": (40, (("header", 0), ("control", 24), ("range_control", 32),)),
    "gf_sweep_scope_class": (40, (("header", 0), ("control", 24), ("range_control", 32),)),
    "gf_list_box_class": (32, (("header", 0), ("control", 24),)),
    "gf_check_box_class": (40, (("header", 0), ("control", 24), ("check_box", 32),)),
    "gf_radio_button_class": (40, (("header", 0), ("control", 24), ("radio_button", 32),)),
    "gf_range_control_class": (40, (("header", 0), ("control", 24), ("range_control", 32),)),
    "gf_track_bar_class": (40, (("header", 0), ("control", 24), ("range_control", 32),)),
    "gf_panel_class": (32, (("header", 0), ("control", 24),)),
    "gf_group_box_class": (32, (("header", 0), ("control", 24),)),
    "gf_material_panel_class": (32, (("header", 0), ("control", 24),)),
    "gf_card_class": (32, (("header", 0), ("control", 24),)),
    "gf_container_control_class": (32, (("header", 0), ("control", 24),)),
    "gf_user_control_class": (32, (("header", 0), ("control", 24),)),
    "gf_page_strip_class": (32, (("header", 0), ("control", 24),)),
    "gf_page_view_class": (32, (("header", 0), ("control", 24),)),
    "gf_navigation_pane_class": (32, (("header", 0), ("control", 24),)),
    "gf_dock_site_class": (32, (("header", 0), ("control", 24),)),
    "gf_dock_navigator_class": (32, (("header", 0), ("control", 24),)),
    "gf_scaled_panel_class": (32, (("header", 0), ("control", 24),)),
    "gf_scrollable_control_class": (32, (("header", 0), ("control", 24),)),
    "gf_scroll_bar_class": (40, (("header", 0), ("control", 24), ("range_control", 32),)),
    "gf_tool_strip_class": (32, (("header", 0), ("control", 24),)),
    "gf_gauge_base_class": (40, (("header", 0), ("control", 24), ("range_control", 32),)),
    "gf_dial_class": (40, (("header", 0), ("control", 24), ("range_control", 32),)),
    "gf_raster_canvas_class": (32, (("header", 0), ("control", 24),)),
    "gf_text_box_base_class": (32, (("header", 0), ("control", 24),)),
    "gf_list_control_class": (32, (("header", 0), ("control", 24),)),
    "gf_up_down_base_class": (32, (("header", 0), ("control", 24),)),
    "gf_node_canvas_class": (40, (("header", 0), ("control", 24), ("node_canvas", 32),)),
    "gf_classes_table": (24, (("struct_size", 0), ("abi_minor", 4), ("create", 8), ("base_raiser", 16),)),
}


def check_layout():
    """The records whose ctypes size or field offsets differ from the manifest's, as messages."""
    mismatches = []
    module = globals()
    for name in LAYOUT:
        size, offsets = LAYOUT[name]
        record = module[name]
        if ctypes.sizeof(record) != size:
            mismatches.append(name + ": size " + str(ctypes.sizeof(record)) + ", manifest " + str(size))
        for field_name, offset in offsets:
            laid_out = getattr(record, field_name).offset
            if laid_out != offset:
                mismatches.append(name + "." + field_name + ": offset " + str(laid_out) + ", manifest " + str(offset))
    return mismatches
