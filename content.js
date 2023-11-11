let element = document.getElementById("login");
const question = element.innerText;
const start = question.indexOf("Please");
const end = question.indexOf("=");
let result = question.slice(start, end + 1).match(/\d+/g);
let ans;
if (question.includes('add')) {
    ans = parseInt(result[0]) + parseInt(result[1]);
} else if (question.includes('subtract')) {
    ans = result[0] - result[1];
} else if (question.includes('first')) {
    ans = result[0];
} else if (question.includes('second')) {
    ans = result[1];
} else {
    ans = "error";
    alert("error");
}
document.getElementById("valuepkg3").value = ans;