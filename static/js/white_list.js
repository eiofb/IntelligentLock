// 添加访客
function bindGuestAddClick(){
    document.getElementById("add-guest-btn").addEventListener("click", function(event){
        // 阻止默认的事件
        event.preventDefault();

        // 获取表单数据
        var device_id = $("input[name='device_id']").val();
        var image_path = $("input[name='upload_image']").val();
        var name = $("input[name='add_guest_name']").val();
        var access = $("input[name='permission_type']").val();
        var formData = new FormData();
        formData.append("image_path", image_path);
        formData.append("name", name);
        formData.append("access", access);
        $.ajax({
            url: "/guest/add_guest",
            method: "POST",
            data: formData,
            processData: false, // 不要处理数据
            contentType: false, // 不要设置 Content-Type
            success: function(result){
                var code = result["code"];
                if (code == 200){
                    location.href= url_for('guest.white_list', device_id=device_id)
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

// 预览图片
function bindImageChange(){
    document.getElementById('uploadImage').addEventListener('change', function(event) {
        const file = event.target.files[0];
        console.log(file);
        const previewContainer = document.getElementById('imagePreview');
        previewContainer.innerHTML = '';
    
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('img-fluid');
                previewContainer.appendChild(img);
            }
            reader.readAsDataURL(file);
        } else {
            previewContainer.innerHTML = '<p>上传的图片将在这里预览。</p>';
        }
    });
}

// 整个网页加载完成后再执行
$(function () {
    // document.getElementById("inputName").addEventListener("keyup", function(event) {
    //     if (event.keyCode === 13) { // 按下回车键的键码是13
    //         event.preventDefault(); // 阻止回车键的默认行为
    //         document.getElementById("nameForm").submit(); // 提交表单
    //     }
    // });

    bindImageChange();
    bindGuestAddClick();
});

// 打开弹窗
function openAddModal() {
    document.getElementById("addModal").style.display = "block";
}
function openConfirmModal(event) {
    var clickedElement = event.target;
    var deviceId = clickedElement.getAttribute('data-device-id');
    document.getElementById('deviceIdInput').value = deviceId;
    document.getElementById("confirmModal").style.display = "block";
}

// 关闭弹窗
function closeAddModal() {
    document.getElementById("addModal").style.display = "none";
}
function closeConfirmModal() {
    document.getElementById("confirmModal").style.display = "none";
}