<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>新冠有效药物预测</title>
        <script type="text/javascript" src="data_info.js"></script>
        <style>
            .predictResult {color:blue;font-style:italic;}
        </style>
    </head>
    <body>
        <div id="BasicInfo">
            <h2>Basic Information Search:</h2>
            <div name="search">
                <form id="search" action="" method="post">
                    Input: 
                        <select name="inputType" onchange='onChange()'>
                            <option value="Virus">Virus</option>
                            <option value="HostProtein">HostProtein</option>
                            <option value="VirusProtein">VirusProtein</option>
                            <option value="Drug">Drug</option>
                        </select>
                        <select name="basicInput">
                        </select>
                    <input type="submit" value="Search">
                </form>
            </div>
        </div>
        <div id="Predict">
            <h2>Predict Now:</h2>
            <div name="search">
                <form name="predict" action="" method="get">
                    Input: 
                        <select name="inputType" onchange='onChange()'>
                            <option value="Virus">Virus</option>
                            <option value="HostProtein">HostProtein</option>
                            <option value="VirusProtein">VirusProtein</option>
                        </select>
                        <select name="predictInput">
                        </select>
                    <input type="submit" value="Predict">
                </form>
            </div>
            <div name="result">
                <h3>Query Result:</h3>
                <?php
                    if(array_key_exists("predictInput",$_GET)){
                        $host = "localhost";//"114.212.85.127";
                        $port = "8888";

                        $funcType = "";
                        $resultType = "";
                        switch($_GET['inputType']){
                            case "Virus":
                                $funcType = 'predictDrug';
                                $resultType = 'Drug';
                                break;
                            case "VirusProtein":
                                $funcType = 'predictBindingProtein';
                                $resultType = 'HostProtein';
                                break;
                            case "HostProtein":
                                $funcType = 'predictInteractionProtein';
                                $resultType = 'VirusProtein';
                                break;
                        }
                        $request = xmlrpc_encode_request($funcType, array(str_replace(" ","_",$_GET['predictInput'])));
                        $response = do_call($host,$port,$request);
                        
                        echo "(Your input is {$_GET['predictInput']}, and its prediction type must be $funcType)<br>";
                        for($idx = 0; $idx < count($response); $idx++){
                            echo "<u class='predictResult' name='$resultType' onclick='submit()'>".str_replace("_"," ",$response[$idx]['string'])."</u><br>";
                        } 
                    }
                ?>
            </div>
        </div>
        <div id="info">
            <?php
                if(array_key_exists("basicInput",$_POST)){
                    $_SESSION['basicInput'] = $_POST['basicInput'];

                    $basicInfo = getInfo($_POST['basicInput']);
                    $interactionRows = count($basicInfo['interaction']);
                    $allRows = $interactionRows+3;
                    echo "<h2>Object Info:</h2>";
                    echo "<table border=1>";
                    echo "<tr>";
                    echo "<th rowspan='$allRows'>{$_POST['basicInput']}</th>";
                    echo "<td>type_is</td>";
                    echo "<td>{$basicInfo['type_is']}</td>";
                    echo "</tr>";
                    echo "<tr>";
                    echo "<td>belong_to</td>";
                    echo "<td>{$basicInfo['belong_to']}</td>";
                    echo "</tr>";
                    echo "<tr>";
                    echo "<td>uniprotkb_entry_name</td>";
                    echo "<td>{$basicInfo['uniprotkb_entry_name']}</td>";
                    echo "</tr>";
                    echo "<tr>";
                    echo "<td rowspan='$interactionRows'>interation</th>";
                    if($interactionRows > 0){
                        echo "<td>{$basicInfo['interaction'][0]}</td>";
                    }
                    echo "</tr>";
                    for($idx = 1; $idx < $interactionRows; $idx++){
                        echo "<tr>";
                        echo "<td>{$basicInfo['interaction'][$idx]}</td>";
                        echo "</tr>";
                    }
                    echo "</table>";
                }
            ?>
        </div>
    </body>
</html>
<script>
    function setSelect(node,val){
        for(var i = 0; i < node.options.length; i++){
            if(node.options[i].value == val){
                node.options[i].selected = true;
                break;
            }
        }
    }

    function submit(){
        var form = document.getElementById("search");
        var type = event.target.getAttribute("name");
        setSelect(document.getElementsByName("inputType")[0], type);
        changeOptions(type,document.getElementsByName("basicInput")[0]);
        setSelect(document.getElementsByName("basicInput")[0], event.target.innerText);
        form.submit();
    }

    function changeOptions(inputType,targetNode){
        var childNodes = targetNode.childNodes;
        var len = childNodes.length;
        for(var i = 0; i < len; i++){
            targetNode.removeChild(childNodes[0]);
        }

        var data;
        switch (inputType) {
            case 'Virus':
                data = Virus;
                break;
            case 'HostProtein':
                data = HostProtein;
                break;
            case 'VirusProtein':
                data = VirusProtein;
                break;
            case 'Drug':
                data = Drug;
                break;
        }

        for(val in data){
            var option = document.createElement("option");
            option.value = data[val];
            option.innerHTML = data[val];
            targetNode.append(option);
        }
    }

    function onChange(){
        var targetNode = event.target.nextElementSibling;
        var type = event.target.value;
        changeOptions(type,targetNode);
    }

    var basicInputType = document.getElementsByName("inputType")[0].value;
    var predictInputType = document.getElementsByName("inputType")[1].value;
    var basicInput = document.getElementsByName("basicInput")[0];
    var predictInput = document.getElementsByName("predictInput")[0];
    changeOptions(basicInputType,basicInput);
    changeOptions(predictInputType,predictInput);
</script>
<?php 
function getInfo($head){
    $servername = "localhost";
    $usr = "root";
    $pwd = "963215njucshy!";
    $db = "hackthon";

    $conn = new mysqli($servername, $usr, $pwd, $db);
    if($conn->connect_error){
        die("connect error: ".$conn->connect_error);
    }

    $type_is = "";
    $belong_to = "";
    $uniprotkb_entry_name = "";
    $interaction = array();

    $sql = "SELECT tail FROM data_info WHERE head='$head' AND relation='type_is'";
    $result = $conn->query($sql);
    if($result->num_rows == 1){
        while($row = $result->fetch_assoc()){
            $type_is = $row['tail'];
        }
    }

    $sql = "SELECT tail FROM data_info WHERE head='$head' AND relation='belong_to'";
    $result = $conn->query($sql);
    if($result->num_rows == 1){
        while($row = $result->fetch_assoc()){
            $belong_to = $row['tail'];
        }
    }

    $sql = "SELECT tail FROM data_info WHERE head='$head' AND relation='uniprotkb_entry_name'";
    $result = $conn->query($sql);
    if($result->num_rows == 1){
        while($row = $result->fetch_assoc()){
            $uniprotkb_entry_name = $row['tail'];
        }
    }

    $sql = "SELECT tail FROM data_info WHERE head='$head' AND relation='interaction'";
    $result = $conn->query($sql);
    if($result->num_rows == 1){
        while($row = $result->fetch_assoc()){
            $interaction[] = $row['tail'];
        }
    }

    $result = Array('type_is'=>$type_is,'belong_to'=>$belong_to,'uniprotkb_entry_name'=>$uniprotkb_entry_name,'interaction'=>$interaction);
    return $result;
}
function do_call($host, $port, $request){
    $url = "http://$host:$port/";
    $header[] = "Content-type: text/xml";
    $header[] = "Content-length: ".strlen($request);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $request);

    $data = curl_exec($ch);

    while(curl_errno($ch)){
        $data = curl_exec($ch);
    }
    
    curl_close($ch);
    $xml_array = simplexml_load_string($data);
    $json_array = json_decode(json_encode($xml_array),true);
    $data = $json_array["params"]['param']['value']['array']['data']['value'];
    return $data;
}
?>