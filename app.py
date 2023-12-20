from flask import Flask, render_template, request, make_response
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import os

app = Flask(__name__)

# TestUnit 데이터 구조화
test_units_data = {
    "DiscoveryService": ["sTC001", "sTC002", "sTC003"],
    "SessionService": [
        "sTC004", "sTC005a", "sTC005b", "sTC006a", "sTC006b", "sTC007",
        "sTC008", "sTC009", "sTC010"
    ],
    "ViewService": [
        "sTC011", "sTC012", "sTC013", "sTC014", "sTC015", "sTC016", "sTC017",
        "sTC018", "sTC019", "sTC020"
    ],
    "AttributesService":
    ["sTC021", "sTC022", "sTC023", "sTC024", "sTC025", "sTC026", "sTC027"],
    "MethodService": ["sTC028a", "sTC028b"],
    "InformationModel": ["sTC029", "sTC030"],
    "SubscriptionService": [
        "sTC031", "sTC032", "sTC033", "sTC034", "sTC035", "sTC036", "sTC037",
        "sTC038"
    ],
    "Redundancy": ["sTC039"],
    "Event": ["sTC040", "sTC041", "sTC042", "sTC043"],
    "MonitoredItemService":
    ["sTC044a", "sTC044b", "sTC044c", "sTC045", "sTC046", "sTC047"],
    "AlarmCondition": [
        "sTC052", "sTC053", "sTC054", "sTC055", "sTC056", "sTC057", "sTC058",
        "sTC059"
    ],
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Device 정보와 Endpoint, Authentication 정보
        device_info = {
            'product_name': request.form.get('product_name', 'Unknown Product'),
            'product_version': request.form.get('product_version', 'Unknown Version'),
            'product_category': request.form.get('product_category', 'Unknown Category'),
            'company_name': request.form.get('company_name', 'Unknown Company'),
            'endpoint': request.form.get('endpoint', ''),
            'username': request.form.get('username', ''),
            'password': request.form.get('password', '')
        }

        selected_test_cases = {group: request.form.getlist(group) for group in test_units_data}

        # 추가 설정 데이터 수집
        additional_settings = {}
        for group in test_units_data:
            for case in test_units_data[group]:
                if case in selected_test_cases[group]:
                    settings = {}
                    for key in request.form:
                        if key.startswith(case + "_"):  # 예: sTC010_NsIdA
                            settings[key[len(case)+1:]] = request.form[key]
                    additional_settings[case] = settings

        xml_content = generate_xml(device_info, selected_test_cases, additional_settings)
        response = make_response(xml_content)
        response.headers["Content-Disposition"] = "attachment; filename=test_configuration.xml"
        return response

    # 각 테스트 케이스에 대한 설정 파일 존재 여부 확인
    settings_exists = {
        case: os.path.isfile(f'templates/settings/{case}.html')
        for group in test_units_data
        for case in test_units_data[group]
    }
    
    return render_template('index.html', test_units_data=test_units_data, settings_exists=settings_exists)



def collect_additional_settings(request_form):
    additional_settings = {}
    for key in request_form:
        if key.startswith("sTC"):
            parts = key.split('_')
            if len(parts) == 2:
                test_case, param = parts
                additional_settings.setdefault(test_case, {})[param] = request_form[key]
    return additional_settings

def generate_xml(device_info, selected_cases, additional_settings):
    root = Element('configuration')
    root.append(Comment('This file is a auto generated file from interoperability web portal'))

    # DeviceInformation 추가 (endpoint, username, password 제외)
    device_info_el = SubElement(root, 'DeviceInformation')
    for key in ['product_name', 'product_version', 'product_category', 'company_name']:
        SubElement(device_info_el, key).text = device_info.get(key, '')

    # DeviceConfiguration 추가 (endpoint, username, password 포함)
    device_config = SubElement(root, 'DeviceConfiguration')
    SubElement(device_config, 'Endpoint').text = device_info.get('endpoint', '')
    auth = SubElement(device_config, 'Authentication')
    SubElement(auth, 'Username').text = device_info.get('username', '')
    SubElement(auth, 'Password').text = device_info.get('password', '')

    # TestConfiguration 추가
    test_config = SubElement(root, 'TestConfiguration')
    for group, cases in test_units_data.items():
        test_unit = SubElement(test_config, 'TestUnit', {'group': group})
        for case in cases:
            if case in selected_cases.get(group, []):
                SubElement(test_unit, 'TestCase').text = case
            else:
                test_unit.append(Comment(f'<TestCase>{case}</TestCase>'))

    # 추가 설정이 있는 테스트 케이스만 XML에 추가
    for case, settings in additional_settings.items():
        if case in sum(selected_cases.values(), []) and settings:
            case_element = SubElement(test_config, case, {'name': settings.pop('name', case)})
            for key, value in settings.items():
                SubElement(case_element, key).text = value

    xml_str = minidom.parseString(tostring(root)).toprettyxml(indent="    ")
    return xml_str

if __name__ == '__main__':
    app.run(debug=True)