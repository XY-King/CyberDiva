function send_input() {
    var user_input = $("#user_input").val();
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/chat",
        contentType: "application/json",
        data: JSON.stringify({
            user_input: user_input,
        }),
        dataType: "json",
        success: function (data) {
            if (data.action_list) {
                action_index = 0; // reset action index
                var action_list = data.action_list; // grab the list of motions from the server response

                var model = new LAppModel();
                // start the first motion
                if (action_list[action_index].motion != "") {
                    model.startAppointMotion(
                        action_list[action_index].motion,
                        3,
                        0
                    );
                }
                if (action_list[action_index].text != "") {
                    showMessage(action_list[action_index].text, 2000);
                }
                action_index++;

                // schedule the rest of the motions
                var action_interval = setInterval(function () {
                    if (action_index >= action_list.length) {
                        clearInterval(action_interval); // stop the loop when run out of actions
                    } else {
                        // play motion if it’s not empty
                        if (action_list[action_index].motion != "") {
                            model.startAppointMotion(
                                action_list[action_index].motion,
                                3,
                                0
                            );
                        }
                        // show message if it’s not empty
                        if (action_list[action_index].text != "") {
                            showMessage(action_list[action_index].text);
                        }
                        action_index++;
                    }
                }, 2000); // trigger next action every 2 seconds
            } else {
                console.log("No action list received from server.");
            }
        },
    });
}

$("#user_input_form").on("submit", function (e) {
    e.preventDefault();
    send_input();
    $("#user_input").val(""); // clear the input field
});

function get_message_timeout(message) {
    // calculate how long the message should be displayed
    var timeout = 0;
    var a = 0.5;
    var b = 0.05;
    var x = message.length;
    console.log("message length", x);
    timeout = a * Math.log(x + 1) + b * x;
    return timeout;
}

function showMessage(text) {
    $(".message-text").stop();
    $(".message-text").html(text).fadeTo(200, 1);
    var fontSize = Math.min(24, 150 / Math.sqrt(text.length));
    $(".message-text").css("font-size", fontSize + "px");
    var timeout = get_message_timeout(text) * 1000;
    console.log("timeout", timeout);
    hideMessage(timeout);
}

function hideMessage(timeout) {
    $(".message-text").stop().css("opacity", 1);
    if (timeout === null) timeout = 5000;
    $(".message-text").delay(timeout).fadeTo(200, 0);
}
