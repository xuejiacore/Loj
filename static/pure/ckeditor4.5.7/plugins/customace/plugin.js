/**
 * Created by xuejia on 2016/2/21.
 */
(function () {
    CKEDITOR.plugins.add("customace", {
        requires: ["dialog"],
        init: function (editor) {
            editor.addCommand("customace", new CKEDITOR.dialogCommand("customace"));
            editor.ui.addButton("customace", {
                label: "插入代码",//调用dialog时显示的名称
                command: "customace",
                icon: this.path + "images/page_white_code_red.png"//在toolbar中的图标
            });
            CKEDITOR.dialog.add("customace", this.path + "dialogs/customace.js");
        }
    })

})();