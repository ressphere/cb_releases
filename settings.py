
file_need_to_parse = [
    {
        'files': [
            '/cb_main.wsdl',
            '/fuel/application/config/MY_config.php',
            '/fuel/application/controllers/_unittest/CB_Info_unit_test.php',
            '/fuel/application/controllers/_unittest/GeneralFunc.php',
            '/fuel/application/controllers/_utils/GeneralFunc.php',
            '/properties/application/controllers/_utils/GeneralFunc.php',
            '/properties/application/controllers/_utils/properties_info.php',
            '/js/_ckeditor/ckeditor.min.js'
        ],
        'keys': {
            'http://localhost/cb_iloveproperty/trunk/circle_property':'http://www.ressphere.com'
        }
    },
    {
        'files': [
            '/fuel/application/controllers/_unittest/lm_properties_listing_unit_test.php',
            '/js/_ckeditor/ckeditor.min.js'
        ],
        'keys': {
            'http://localhost/cb_iloveproperty/trunk/client_views/properties_views':'http://www.ressphere.com/properties'
        }
    },
    {
        'files': [
            '/properties/js/property_new_listing.js',
            '/properties/js/property_edit_listing.js'
        ],
        'keys': {
            '/cb_iloveproperty/trunk/client_views/properties_views/index.php/_utils/properties_upload/images':'/properties/index.php/_utils/properties_upload/images'
        }
    },
    {
        'files': [
            '/properties/application/controllers/_utils/properties_upload.php'
        ],
        'keys': {
            'dirname(dirname(dirname(dirname(dirname(__DIR__)))))':'dirname(dirname(dirname(dirname(__DIR__))))'
        }
    },
    {
        'files': [
            '/js/cb_update_profile.js'
        ],
        'keys': {
            'http://localhost/cb_iloveproperty/trunk/client_views/properties_views/index.php/':'http://www.ressphere.com/properties/index.php/'
        }
    },
    {
        'files': [
            '/fuel/application/controllers/garbage_collector.php'
        ],
        'keys': {
            '"/client_views/properties_views/assets/images/properties"':'"/properties/assets/images/properties"',
            'dirname(dirname(dirname(dirname(__DIR__))))':'dirname(dirname(dirname(__DIR__)))'
        }
    },
    {
        'files': [
            '/properties/application/controllers/properties_base.php'
        ],
        'keys': {
            'dirname(dirname(dirname(dirname(__DIR__))))':'dirname(dirname(dirname(__DIR__)))'
        }
    },
	{
        'files': [
            '/db/cb_db/s8_cb_properties_trigger_function.sql'
        ],
        'keys': {
            'iloveproperties_db':'ressykir_iloveproperties_db'
        }
    }
]

replacement_files = "ressphere"
structure = [
    {"circle_property/*":"/"},
    {"client_views/properties_views/*":"/properties/"},
    {"client_views/aroundyou_views/*":"/aroundyou/"},
    {"fonts/*":"/fonts/"},
    {"fonts/*":"/properties/fonts/"},
    {"temp/*":"/temp/"}
]
excluded_files = []
js_paths = [
			'js',
			'js/_usercontrols',
            '/properties/js/',
            '/properties/js/_utils/'
            '/aroundyou_views/js/',
            '/aroundyou_views/js/_utils/'
           ]
css_paths = ['/css/',
            '/properties/css/',
            '/aroundyou_views/css/']



