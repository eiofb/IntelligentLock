// 添加设备
function bindDeviceAddClick(){
    document.getElementById("add-device-btn").addEventListener("click", function(event){
        // 阻止默认的事件
        event.preventDefault();

        // 获取表单数据
        var device_id = $("input[name='add_device_id']").val();
        var device_name = $("input[name='add_device_name']").val();
        var formData = new FormData();
        formData.append("device_id", device_id);
        formData.append("device_name", device_name);
        $.ajax({
            url: "/device/addDevice",
            method: "POST",
            data: formData,
            processData: false, // 不要处理数据
            contentType: false, // 不要设置 Content-Type
            success: function(result){
                var code = result["code"];
                if (code == 200){
                    location.href="/device/devicelist";
                } else {
                    for (var key in result['data']){
                        $("#warning-message").text(result['data'][key]).show();
                        $("#warning-message").fadeOut(3000); // 300 毫秒的滑动效果
                    }
                }
            },
            error: function (error) {
              console.log(error);
            }
        });
    });
}

// 删除设备
function bindDeviceDeleteClick(){
    document.getElementById("confirm-delete-btn").addEventListener("click", function(event){
        // 阻止默认的事件
        event.preventDefault();

        // 获取设备ID
        var device_id = $("input[id='deviceIdInput']").val();
        $.ajax({
            url: "/device/delete_device?device_id=" + device_id,
            method: "GET",
            success: function(result){
                var code = result['code'];
                if (code == 200){
                    location.href="/device/devicelist";
                } else {
                    alert(result['message']);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    });
}

// 整个网页加载完成后再执行
$(function () {
    document.getElementById("inputName").addEventListener("keyup", function(event) {
        if (event.keyCode === 13) { // 按下回车键的键码是13
            event.preventDefault(); // 阻止回车键的默认行为
            document.getElementById("nameForm").submit(); // 提交表单
        }
    });

    bindDeviceAddClick();
    bindDeviceDeleteClick();
});

// 打开弹窗
function openAddModal() {
    document.getElementById("addDeviceModal").style.display = "block";
}
function openConfirmModal(event) {
    var clickedElement = event.target;
    var deviceId = clickedElement.getAttribute('data-device-id');
    document.getElementById('deviceIdInput').value = deviceId;
    document.getElementById("confirmModal").style.display = "block";
}

// 关闭弹窗
function closeAddModal() {
    document.getElementById("addDeviceModal").style.display = "none";
}
function closeConfirmModal() {
    document.getElementById("confirmModal").style.display = "none";
}