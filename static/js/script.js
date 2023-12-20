function toggleSettings(testCase) {
  console.log("toggleSettings called for:", testCase); // 이 부분 추가
  var settingsDiv = document.getElementById("settings_" + testCase);
  if (settingsDiv) {
    settingsDiv.style.display =
      settingsDiv.style.display === "none" ? "block" : "none";
  }
}
function selectAll() {
  var checkboxes = document.querySelectorAll('input[type="checkbox"]');
  var checkAllButton = document.getElementById("checkAllButton"); // 추가

  // 추가: 모든 체크박스 클리어
  clearAllChecks();

  // 추가: 모든 체크박스 체크
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = true;

    // 추가: 체크박스 상태에 따라 추가 설정 필드 토글
    toggleSettings(checkboxes[i].getAttribute("value"));
  }

  // 추가: 버튼 텍스트 변경
  checkAllButton.innerText = "Deselect All";
}

function selectKOLASTestCases() {
  var testCasesToSelect = [
    "sTC003",
    "sTC004",
    "sTC005a",
    "sTC005b",
    "sTC006a",
    "sTC006b",
    "sTC007",
    "sTC009",
    "sTC010",
    "sTC011",
    "sTC013",
    "sTC021",
    "sTC022",
    "sTC025",
    "sTC026",
    "sTC028a",
    "sTC028b",
    "sTC029",
    "sTC030",
    "sTC031",
    "sTC032",
    "sTC033",
    "sTC034",
    "sTC035",
    "sTC036",
    "sTC037",
    "sTC040",
    "sTC041",
    "sTC042",
    "sTC043",
    "sTC044a",
    "sTC044b",
    "sTC044c",
    "sTC045",
  ];

  var checkboxes = document.querySelectorAll('input[type="checkbox"]');
  var selectKOLASButton = document.getElementById("selectKOLASButton");

  // 추가: 모든 체크박스 클리어
  clearAllChecks();

  // KOLAS Test Case에 해당하는 체크박스만 체크
  for (var i = 0; i < checkboxes.length; i++) {
    var testCaseValue = checkboxes[i].getAttribute("value");
    if (testCasesToSelect.includes(testCaseValue)) {
      checkboxes[i].checked = true;

      // 체크박스 상태에 따라 추가 설정 필드 토글
      toggleSettings(testCaseValue);
    }
  }
}

function selectNecessaryTestCases() {
  var necessaryTestCases = [
    "sTC003",
    "sTC004",
    "sTC007",
    "sTC009",
    "sTC011",
    "sTC021",
    "sTC022",
    "sTC029",
    "sTC030",
    "sTC031",
    "sTC032",
    "sTC033",
    "sTC034",
    "sTC044a",
    "sTC044b",
    "sTC044c",
    "sTC045",
  ];

  var checkboxes = document.querySelectorAll('input[type="checkbox"]');
  var selectNecessaryButton = document.getElementById("selectNecessaryButton");

  // 추가: 모든 체크박스 클리어
  clearAllChecks();

  // 필수 Test Case에 해당하는 체크박스만 체크
  for (var i = 0; i < checkboxes.length; i++) {
    var testCaseValue = checkboxes[i].getAttribute("value");
    if (necessaryTestCases.includes(testCaseValue)) {
      checkboxes[i].checked = true;
      toggleSettings(testCaseValue);
    }
  }
}

function hideSettings(testCase) {
  var settingsDiv = document.getElementById("settings_" + testCase);
  if (settingsDiv) {
    settingsDiv.style.display = "none";
  }
}
function clearAllChecks() {
  var checkboxes = document.querySelectorAll('input[type="checkbox"]');

  // 모든 체크박스의 체크를 해제
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = false;

    // 추가 설정 필드 숨김
    var testCaseValue = checkboxes[i].getAttribute("value");
    hideSettings(testCaseValue); // 추가 설정 필드를 숨기는 함수 호출
  }
}
