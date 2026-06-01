function refreshRates()
{
    let currentRates = document.getElementsByClassName("current-exchange-value");
    let totalMoney = document.getElementsByClassName("total-usd-value");
    let coinAmount = document.getElementsByClassName("coin-amount-value");
    for(let i = 0; i < currentRates.length; i++)
    {
        currentRates[i].id = currentRates[i].id.toLowerCase();
    }

    for(let i = 0; i < currentRates.length; i++)
    {

        updateCryptoRate(currentRates[i], totalMoney[i], coinAmount[i]);

    }
}

function updateCryptoRate(currentRate, totalMoney, coinAmount) 
{
    let currentCrypto = currentRate.id.replace("usdt", "").toUpperCase();
    let url = "/" + currentCrypto + "/get-rate";
    let http2 = new XMLHttpRequest();
    http2.onload = function(){
        let data = "";
        if(http2.status == 200)
            {
                data = JSON.parse(this.responseText);
            }
        if(data[currentCrypto] !== false)
            {
                currentRate.innerHTML = precise(parseFloat(data[currentCrypto]));
                 updateTotalMoney(currentRate, totalMoney, coinAmount);
            }
    }
    http2.open("GET", url, true );
    http2.send();
}


function updateTotalMoney(currentRate, totalMoney, coinAmount) 
{
    if (coinAmount.innerHTML !== "--") {
        totalMoney.innerHTML = precise(parseFloat(currentRate.innerHTML) * parseFloat(coinAmount.innerHTML));
    }
}

function precise(x)
{
    return x.toFixed(2);
}

function getShkeeperLocale()
{
    let match = document.cookie.match(/(?:^|;\s*)shkeeper_locale=([^;]+)/);
    if (!match) {
        return "en";
    }
    return decodeURIComponent(match[1]).replace("-", "_");
}

function localizeDynamicLabel(label)
{
    if (getShkeeperLocale().toLowerCase() !== "zh_cn") {
        return label;
    }

    const labels = {
        "Enabled": "\u5df2\u542f\u7528",
        "Disabled": "\u5df2\u7981\u7528",
        "Online": "\u5728\u7ebf",
        "Offline": "\u79bb\u7ebf",
        "Synced": "\u5df2\u540c\u6b65",
        "Sync In Progress": "\u540c\u6b65\u4e2d"
    };

    if (labels[label]) {
        return labels[label];
    }
    if (label.indexOf("Sync In Progress") === 0) {
        return label.replace("Sync In Progress", labels["Sync In Progress"]);
    }
    if (label.indexOf("Synced") === 0) {
        return label.replace("Synced", labels["Synced"]);
    }
    return label;
}

function getCryptoRate(crypto)
{
    let cryptoName = crypto.toUpperCase();
    let url = "/" + cryptoName + "/get-rate";
    let http2 = new XMLHttpRequest();
    let data = "";
    http2.open("GET", url, true ); // , false);
    http2.send();
    if(http2.status == 200)
    {
        data = JSON.parse(http2.responseText);
    }
    if(data[cryptoName] !== false)
    {
        return parseFloat(data[cryptoName]);
    }

}

function refreshWalletInfo()
{
    let serverStatus = document.getElementsByClassName("server-status");
    let walletStatus = document.getElementsByClassName("wallet-status");
    let coinAmount = document.getElementsByClassName("coin-amount-value");

    helperCycleWalletInfo(serverStatus,walletStatus,coinAmount);
    setInterval(function(){
        helperCycleWalletInfo(serverStatus,walletStatus,coinAmount);
    }, 10000);

    function helperCycleWalletInfo(serverStatus,walletStatus,coinAmount)
    {
        for(let i = 0; i < serverStatus.length; i++)
        {
            getWalletInfo(serverStatus[i], walletStatus[i],coinAmount[i]);
        }
    }


    function getWalletInfo(serverStatus,walletStatus,coinAmount)
    {
        let url = "/api/v1/"+coinAmount.id +"/status";
        let http = new XMLHttpRequest();
        http.onload = function(){
            let data = JSON.parse(this.responseText);
            if(data['amount'] !== false)
            {
                coinAmount.innerHTML = data['amount'];
            }
            setWallesStatus(serverStatus,walletStatus,data['server'])
        }
        http.open("GET", url, true);
        http.send();
    }

    function setWallesStatus(serverStatusF,walletStatus,serverStatus)
    {
        let splits = serverStatus.split(" ", 1);
        if(splits[0] == "Synced")
        {
            serverStatusF.innerHTML = localizeDynamicLabel(serverStatus);
            serverStatusF.style.color = "var(--success-color)";
            walletStatus.innerHTML = localizeDynamicLabel("Online");
            walletStatus.style.color = "var(--success-color)";
        }
        else if(splits[0] == "Sync")
        {
            serverStatusF.innerHTML = localizeDynamicLabel(serverStatus);
            serverStatusF.style.color = "var(--success-color)";
            walletStatus.innerHTML = localizeDynamicLabel("Offline");
            walletStatus.style.color = "var(--danger-color)";
        }
        else
        {
            serverStatusF.innerHTML = localizeDynamicLabel(serverStatus);
            serverStatusF.style.color = "var(--danger-color)";
            walletStatus.innerHTML = localizeDynamicLabel("Offline");
            walletStatus.style.color = "var(--danger-color)";
        }
    }
}
function setPolicyStatus()
{
    let policyStatus = document.querySelectorAll(".pstatus");
    policyStatus.forEach(item => {
        switch(item.innerHTML)
        {
        case "False":
        {
            item.innerHTML = localizeDynamicLabel("Disabled");
            item.style.color = "var(--danger-color)";
            break;
        }
        case "True":
        {
            item.innerHTML = localizeDynamicLabel("Enabled");
            item.style.color = "var(--success-color)";
            break;
        }
        }
    });

}
function APIStatus()
{
    const activeStatus = "Enabled";
    const unactiveStatus = "Disabled";
    const offlineStatus = "Offline"
    let APIswitchers = document.querySelectorAll(".apistatus");
    for(let i = 0;i<APIswitchers.length;i++)
    {
        let APIswitcher = APIswitchers[i];
        let crypto = APIswitcher.getAttribute('crypto');
        getStatus();
        function getStatus()
        {
            const http1 = new XMLHttpRequest()
            http1.open("GET","/api/v1/" + crypto + "/payment-gateway");
            http1.onload = function(){
                let data = checkAnswer(this);
                if(data != false)
                {
                    if(data["enabled"])
                    {
                        setStatus(activeStatus);
                    }
                    else
                    {
                        setStatus(unactiveStatus);
                    }
                }
                else{
                setStatus(offlineStatus);
                }
            }
            http1.send();
        }
        function setStatus(status)
        {
            if(status == activeStatus)
            {
                APIswitcher.innerText = localizeDynamicLabel(activeStatus);
                APIswitcher.style.color="var(--success-color)";
            }
            else if(status == unactiveStatus)
            {
                APIswitcher.innerText = localizeDynamicLabel(unactiveStatus);
                APIswitcher.style.color="var(--danger-color)";
            }
            else
            {
                APIswitcher.innerText = localizeDynamicLabel(offlineStatus);
                APIswitcher.style.color="var(--danger-color)";
            }
        }
        function checkAnswer(response)
        {
            if(response.status == 200)
            {
                let data = JSON.parse(response.responseText);
                if(data['status'] != "success")
                {
                    alert(data['message']);
                    return false;
                }
                else
                {
                    return data;
                }
            }
            return false;
        }
    }
}
window.addEventListener('DOMContentLoaded',function(){
    APIStatus();
    refreshRates();
    refreshWalletInfo();
    setPolicyStatus();

    setInterval(refreshRates, 10000);
});
