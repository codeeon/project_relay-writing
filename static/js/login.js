// DOM 찾기
const $id = document.getElementById('id_user');
const $idMsg = document.getElementById('idMsg');
const $pw = document.getElementById('pw');
const $pwMsg = document.getElementById('pwMsg');
const $submit = document.getElementById('submit');
const $login_form = document.getElementById('login_form');

const $alertContainer = document.getElementById('alertContainer');
const $alertCloseBtn = document.getElementById('alertCloseBtn');

// ID input 자동 포커스
window.addEventListener('load', () => $id.focus());

// 에레메세지 객체 생성
const ERROR_MSG = '필수 정보입니다.';

const checkRegex = (target) => {
  const { value, id } = target;
  return value.length === 0 ? 'required' : true;
};

const checkValidation = (target, msgTarget) => {
  const isValid = checkRegex(target);
  if (isValid === 'required') {
    target.classList.add('border-red');
    msgTarget.innerText = ERROR_MSG;
  } else {
    target.classList.remove('border-red');
    msgTarget.innerText = '';
  }
};

// 로직 실행
$id.addEventListener('focusout', () => checkValidation($id, $idMsg));
$pw.addEventListener('focusout', () => checkValidation($pw, $pwMsg));

// 제출 버튼 누를 경우 유효성 검사
$submit.addEventListener('click', (event) => {
  event.preventDefault();
  checkValidation($id, $idMsg);
  checkValidation($pw, $pwMsg);
  const isValidForm = checkRegex($id, $idMsg) === true && checkRegex($pw, $pwMsg) === true;
  if (isValidForm) {
  }
});

$alertCloseBtn.addEventListener('click', () => {
  document.getElementById('alertContainer').style.display = 'none';
});
