// DOM 가져오기
const $id = document.getElementById('id_user');
const $idMsg = document.getElementById('idMsg');
const $name = document.getElementById('name');
const $nameMsg = document.getElementById('nameMsg');
const $pw = document.getElementById('pw');
const $pwMsg = document.getElementById('pwMsg');
const $pwConfirm = document.getElementById('pwConfirm');
const $pwConfirmMsg = document.getElementById('pwConfirmMsg');
const $submitBtn = document.getElementById('submit');

// ID input 자동 포커스
window.addEventListener('load', () => $id.focus());

// 정규식
// 아이디 : 5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.
var ID_REGEX = new RegExp('^[a-z0-9_-]{5,20}$');
// 비밀번호 : 8~16자 영문 대 소문자, 숫자를 사용하세요.
var PW_REGEX = new RegExp('^[a-zA-Z0-9]{8,16}$');

// 에레메세지 객체 생성
const ERROR_MSG = {
  required: '필수 정보입니다.',
  invalidId: '5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.',
  invalidPw: '8~16자 영문 대 소문자, 숫자를 사용하세요.',
  invalidPwCheck: '비밀번호가 일치하지 않습니다.',
};

// 유효성 검사 로직 생성
const checkRegex = (target) => {
  // destructuring 구조분해할당
  // destructuring = const value = target.value; const id = target.id
  const { value, id } = target;
  if (value.length === 0) {
    return 'required';
  } else {
    switch (id) {
      case 'id_user':
        return ID_REGEX.test(value) ? true : 'invalidId';
      case 'name':
        return true;
      case 'pw':
        return PW_REGEX.test(value) ? true : 'invalidPw';
      case 'pwConfirm':
        return value === $pw.value ? true : 'invalidPwCheck';
    }
  }
};

// 유효성 검사 로직 실행 및 css를 위한 class 추가
const checkValidation = (target, msgTarget) => {
  const isValid = checkRegex(target);
  if (isValid !== true) {
    target.classList.add('border-red');
    msgTarget.innerText = ERROR_MSG[isValid];
  } else {
    target.classList.remove('border-red');
    msgTarget.innerText = '';
  }
};

// 로직 실행
$id.addEventListener('focusout', () => checkValidation($id, $idMsg));
$name.addEventListener('focusout', () => checkValidation($name, $nameMsg));
$pw.addEventListener('focusout', () => checkValidation($pw, $pwMsg));
$pwConfirm.addEventListener('focusout', () => checkValidation($pwConfirm, $pwConfirmMsg));

// 제출 버튼 누를 경우 유효성 검사
// $submitBtn.addEventListener('click', (event) => {
//     event.preventDefault()
//     const isValidForm =
//     checkRegex($id, $idMsg) === true &&
//     checkRegex($name, $nameMsg) === true &&
//     checkRegex($pw, $pwMsg) === true &&
//     checkRegex($pwConfirm, $pwConfirmMsg) === true
//     if (isValidForm) {

//     }
// })
