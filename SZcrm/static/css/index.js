window.onload = function () {
    var oDiv = document.getElementById('div1');
    console.log(oDiv);
    oDiv.onmouseover = function () {

        startMove(10, 0);
    };
    oDiv.onmouseout = function () {
        startMove(-10, -200);
    };
};
var t = 0;
function startMove(speen, iTarget) {
    var setmove = null;
    clearInterval(t);
    var oDiv = document.getElementById('div1');
    t = setInterval(function () {

        if (oDiv.offsetLeft === iTarget) {
            clearInterval(t);
        } else {
            oDiv.style.left = oDiv.offsetLeft + speen + 'px';
        }
    }, 30)
}
