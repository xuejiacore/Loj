/**
 * Created by xuejia on 2016/2/23.
 */
CKEDITOR.editorConfig = function (config) {
    // 设置宽高
    config.height = 400;
    config.width = 785;
    config.resize_maxHeight = 1024;
    config.autosave = false;

    //  屏蔽换行符<br>
    config.enterMode = CKEDITOR.ENTER_BR;
    // 屏蔽段落<p>
    config.shiftEnterMode = CKEDITOR.ENTER_P;
    config.extraPlugins = 'customace';

    //config.pasteFromWordIgnoreFontFace = true; //默认为忽略格式
    config.pasteFromWordRemoveFontStyles = false;
    config.pasteFromWordRemoveStyles = false;
};
