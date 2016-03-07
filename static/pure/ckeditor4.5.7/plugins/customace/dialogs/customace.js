/**
 * Created by xuejia on 2016/2/21.
 */
/**
 * 获得代码编辑器实例
 */
function getACEEditor() {
    return document.getElementById("editor-iframe").contentWindow.editor;
}

function getAce() {
    return document.getElementById("editor-iframe").contentWindow.aceStatic;
}

//document.write("");


(function () {
    CKEDITOR.dialog.add("customace",
        function (api) {
            return {
                title: "代码编辑器",
                resizeable: CKEDITOR.DIALOG_RESIZE_WIDTH,
                minWidth: 800,
                minHeight: 300,
                contents: [{
                    id: "customace",
                    label: "",
                    title: "",
                    expand: true,
                    padding: 0,
                    elements: [{
                        type: "html",
                        html: '' +
                        '<div style="display: none"><textarea></textarea></div>' +
                        '<iframe id="editor-iframe" style="width:100%;height:' + calHeight() + 'px;padding:0;"  ' +
                        'width="100%" height="100%" frameborder="0" scrolling="no" src="data:text/html,' +
                        '<pre id=\'editor\' style=\'height:100%\'></pre>' +
                        '<script src=\'https://ajaxorg.github.io/ace-builds/src/ace.js\'></script>' +
                        '<script src=\'https://ajaxorg.github.io/ace-builds/src/ext-language_tools.js\'></script>' +
                        '<script src=\'https://ajaxorg.github.io/ace-builds/src/ext-emmet.js\'></script>' +
                        '<script src=\'https://ajaxorg.github.io/ace-builds/src/ext-static_highlight.js\'></script>' +
                        '<script src=\'https://cloud9ide.github.io/emmet-core/emmet.js\'></script>' +

                        '<script>' +
                        'var aceStatic = ace;' +
                        'ace.require(\'ace/ext/language_tools\');' +
                        'var editor = ace.edit(\'editor\');' +
                        'editor.setTheme(\'ace/theme/twilight\');' +
                        'editor.session.setMode(\'ace/mode/html\');' +

                        'editor.setOptions({' +
                        'enableBasicAutocompletion: true,' +
                        'enableSnippets: true,' +
                        'enableLiveAutocompletion: true,' +
                        'enableEmmet: true' +
                        '});' +

                        '</script>"' +
                        '</iframe>'
                    }]
                }],
                onOk: function () {
                    //点击确定按钮后的操作
                    try {
                        //document.querySelector('.cke_wysiwyg_frame').contentWindow.document.write("");
                        api.insertHtml("" +
                            "<div id='test' style='width: 50%;white-space: pre-wrap;border: solid lightgrey 1px'></div>");
                        api.insertText(getACEEditor().getValue());
                        var highlight = getAce().require("ace/ext/static_highlight");

                        highlight(document.querySelector('.cke_wysiwyg_frame').contentWindow.document.getElementById("test"), {
                            mode: "ace/mode/java",
                            theme: "ace/theme/twilight",
                            startLineNumber: 1,
                            trim: true
                        }, function (highlighted) {

                        });

                    } catch (e) {
                        alert(e.message);
                    }
                }
            }
        });

})();

function calHeight() {
    var clientHeight = document.documentElement.clientHeight;
    // Size adjustments.
    var size = CKEDITOR.document.getWindow().getViewPaneSize(),
    // Make it maximum 800px wide, but still fully visible in the viewport.
        _width = Math.min(size.width - 70, 800),
    // Make it use 2/3 of the viewport height.
        _height = size.height / 1.5;

    // Low resolution settings.
    if (clientHeight < 650) {
        _height = clientHeight - 220;
    }
    return _height;
}


