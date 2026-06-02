function changeSource(ind) {
    let rate_inputs = document.getElementsByClassName("rates-cost-value");
    let rateInput = rate_inputs[ind];

    let sourceType = selectArray[ind].value;
    if (sourceType == "manual") {
        rateInput.readOnly = false
        rateInput.dataset.manual = "on"
        rateInput.value = rateInput.dataset.manual_rate;
        rateInput.title = "";
    } else {
        delete rateInput.dataset.manual
        rateInput.readOnly = true
        getRealTRates(rateInput, sourceType);
    }
}

function change_fee_policy(ind) {
    let percentArray = document.getElementsByClassName("percent-fee");
    let fixedArray = document.getElementsByClassName("fixed-fee");
    let policy = selectArray2[ind].value;
    switch (policy) {
        case "NO_FEE":
            percentArray[ind].style.display = "none";
            fixedArray[ind].style.display = "none";
            break;
        case "PERCENT_FEE":
            percentArray[ind].style.display = "block";
            fixedArray[ind].style.display = "none";
            break;
        case "FIXED_FEE":
            percentArray[ind].style.display = "none";
            fixedArray[ind].style.display = "block";
            break;
        case "PERCENT_OR_MINIMAL_FIXED_FEE":
            percentArray[ind].style.display = "block";
            fixedArray[ind].style.display = "block";
            break;
    }
}

function getRealTRates(currentRate, sourceType) {
    let currentCrypto = currentRate.dataset.crypto;
    if (!currentCrypto) {
        currentCrypto = currentRate.dataset.pairname.toLowerCase().replace("usdt", "").toUpperCase();
    }
    let app_conf = document.getElementById("app-config");
    let fiat = app_conf.dataset.fiat;
    if (fiat !== 'USD')
        { var url = "/" + currentCrypto + "/get-rate/" + fiat;} 
    else
        { var url = "/" + currentCrypto + "/get-rate";}

    if (sourceType) {
        url = url + "?source=" + encodeURIComponent(sourceType);
    }

    let http2 = new XMLHttpRequest();
    http2.onload = function(){
        let data = {};
        try {
            data = JSON.parse(this.responseText);
        } catch (error) {
            currentRate.title = "Failed to parse rate response";
            return;
        }
        if(http2.status == 200 && data[currentCrypto] !== false && data.status !== "error")
        {
            currentRate.value = data[currentCrypto];
            currentRate.title = "";
        } else {
            currentRate.value = "";
            currentRate.title = data.message || "Failed to get rate";
        }
    }
    http2.onerror = function() {
        currentRate.value = "";
        currentRate.title = "Failed to get rate";
    }

    http2.open("GET", url, true);
    http2.send();
}

let selectArray = document.getElementsByClassName("select-rate");
for (let i = 0; i < selectArray.length; i++) {
    selectArray[i].addEventListener("change", function () { changeSource(i); });
    changeSource(i);
}

let selectArray2 = document.getElementsByClassName("fee_policy_select");
for (let i = 0; i < selectArray2.length; i++) {
    selectArray2[i].addEventListener("change", function () { change_fee_policy(i); });
}

document.getElementById("all_fee_policy").addEventListener("change", function () {
    let per_fee = document.getElementById("percent-fee-for-all-container");
    let fix_fee = document.getElementById("fixed-fee-for-all-container");
    let all_pol_sel = document.getElementById('all_fee_policy')
    console.log(all_pol_sel.value);
    switch (all_pol_sel.value) {
        case "NO_FEE":
            per_fee.style.display = "none";
            fix_fee.style.display = "none";
            break;
        case "PERCENT_FEE":
            per_fee.style.display = "block";
            fix_fee.style.display = "none";
            break;
        case "FIXED_FEE":
            per_fee.style.display = "none";
            fix_fee.style.display = "block";
            break;
        case "PERCENT_OR_MINIMAL_FIXED_FEE":
            per_fee.style.display = "block";
            fix_fee.style.display = "block";
            break;
    }
});


document.getElementById("set-all").addEventListener("click", function (e) {
    e.preventDefault()
    let percent_fee_input_array = document.getElementsByClassName("percent-fee-value");
    let fixed_fee_input_array = document.getElementsByClassName("fixed-fee-value");
    let source_select_array = document.getElementsByClassName("rates-source-value");
    let policy_select_array = document.getElementsByClassName("fee_policy_select");

    let percent_fee_input = document.getElementById("percent-fee-value-for-all");
    let fixed_fee_input = document.getElementById("fixed-fee-value-for-all");
    let source_select = document.getElementById("select-all");
    let policy_select = document.getElementById("all_fee_policy");

    for (let i = 0; i < source_select_array.length; i++) {
        percent_fee_input_array[i].value = percent_fee_input.value;
        fixed_fee_input_array[i].value = fixed_fee_input.value;
        source_select_array[i].value = source_select.value;
        policy_select_array[i].value = policy_select.value;

        changeSource(i)
        change_fee_policy(i)
    }
});
